import re
import shutil
from datetime import datetime
from pathlib import Path

import fitz  # PyMuPDF
import pandas as pd

from config.config import ARCHIVED_DATA_DIR, DEBUG_MODE, LANDING_DATA_DIR, PROCESSED_DATA_DIR


def extract_date(text: str, page=None) -> dict:

    data = {}

    # Parse dates from text
    match = re.search(r"(\d{2}/\d{2}/\d{4})\s*-\s*(\d{2}/\d{2}/\d{4})\s+(\d{2}/\d{2}/\d{4})", text)
    if match:
        data["start_date"], data["end_date"], data["issue_date"] = match.groups()
    else:
        data["start_date"] = data["end_date"] = data["issue_date"] = None

    return data


def block_matches_label(text: str, label: str) -> bool:
    lines = [line.strip().lower() for line in text.split("\n")]
    label = label.strip().lower()
    return label in lines or lines[-1] == label


def extract_labeled_row_blocks(page, target_labels, y_tolerance=1.0, super_block_start=280):
    blocks = page.get_text("blocks")
    parsed_blocks = []

    # Build structured block list
    for x0, y0, x1, y1, text, block_no, block_type in blocks:
        clean_text = text.strip()
        if clean_text:
            parsed_blocks.append({"bbox": (x0, y0, x1, y1), "text": clean_text, "x0": x0, "y": round(y0, 1)})

    result = {}
    for label in target_labels:
        # Find the block matching the label
        label_block = next((b for b in parsed_blocks if block_matches_label(b["text"], label)), None)
        if not label_block:
            continue

        label_y = label_block["y"]

        # Match blocks with same y and x0 >= label_x0 - x_tolerance
        matched_blocks = [b for b in parsed_blocks if abs(b["y"] - label_y) <= y_tolerance and b["x0"] < super_block_start]

        # Sort left to right
        matched_blocks = sorted(matched_blocks, key=lambda b: b["x0"])

        # Return just the text content
        result[label.lower().replace(" ", "_")] = [b["text"] for b in matched_blocks]

    return result


def extract_totals_from_block_map(block_map: dict) -> pd.DataFrame:
    results = {}

    for key, items in block_map.items():
        if not items:
            continue

        # First item is the label
        label = key

        # Next items may contain \n, so flatten them
        numeric_parts = []
        for part in items[0:]:
            parts = part.split("\n")
            for p in parts:
                p = p.strip()
                if re.match(r"^-?[\d,]+\.\d{2}$", p):  # match currency-style values
                    numeric_parts.append(p.replace(",", ""))
        if label == "gross":
            results[label] = numeric_parts[1]
            results[f"{label}_ytd"] = numeric_parts[2]
        else:
            results[label] = numeric_parts[0]
            results[f"{label}_ytd"] = numeric_parts[1]

    return pd.DataFrame([results])


def parse_all_payslips():
    landing_path = Path(LANDING_DATA_DIR / "payslips" / "2025")
    archive_base = Path(ARCHIVED_DATA_DIR / "payslips")
    processed_path = Path(PROCESSED_DATA_DIR)

    target_labels = [
        "Taxable Income",
        "Additions After Tax",
        "Gross",
        "Tax",
        "Deductions After Tax",
        "NET PAY",
    ]

    if not landing_path.exists():
        raise FileNotFoundError(f"Landing folder {landing_path} does not exist.")

    all_records = []

    for file in sorted(landing_path.glob("*.pdf")):
        with fitz.open(file) as doc:
            page = doc[-1]

            # Extract block rows and turn into DataFrame
            blocks = extract_labeled_row_blocks(page, target_labels)
            df_values = extract_totals_from_block_map(blocks)

            if df_values.empty:
                print(f"⚠️ Skipping {file.name} (no structured totals found)")
                continue

            data = df_values.iloc[0].to_dict()

            # Extract date from full text
            text = "".join(page.get_text() for page in doc)  # type: ignore
            match = re.search(r"(\d{2}/\d{2}/\d{4})\s*-\s*(\d{2}/\d{2}/\d{4})\s+(\d{2}/\d{2}/\d{4})", text)
            if match:
                data["start_date"], data["end_date"], data["issue_date"] = match.groups()
            else:
                print(f"⚠️ Skipping {file.name} (missing pay period dates)")
                continue

        issue_date = datetime.strptime(data["issue_date"], "%d/%m/%Y")
        fy = f"{issue_date.year + 1}" if issue_date.month > 6 else f"{issue_date.year}"

        data["filename"] = file.name
        all_records.append(data)

        # Archive
        archive_path = archive_base / fy
        archive_path.mkdir(parents=True, exist_ok=True)
        archive_pdf = archive_path / f"payslip_{issue_date.strftime('%Y')}-{issue_date.strftime('%m')}.pdf"
        if DEBUG_MODE:
            shutil.copy(str(file), archive_pdf)
        else:
            shutil.move(str(file), archive_pdf)

    if not all_records:
        print("No payslips parsed.")
        return

    # Write or append CSV
    output_csv = processed_path / f"payslips_{fy}.csv"
    df_new = pd.DataFrame(all_records)

    if output_csv.exists():
        df_existing = pd.read_csv(output_csv)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new

    # Reorder columns
    column_order = [
        "start_date",
        "end_date",
        "issue_date",
        "taxable_income",
        "taxable_income_ytd",
        "additions_after_tax",
        "additions_after_tax_ytd",
        "gross",
        "gross_ytd",
        "tax",
        "tax_ytd",
        "deductions_after_tax",
        "deductions_after_tax_ytd",
    ]
    df_combined = df_combined[[col for col in column_order if col in df_combined.columns]]
    # Compute net pay and net pay ytd safely
    if "gross" in df_combined.columns and "tax" in df_combined.columns:
        df_combined.loc[:, "net_pay"] = pd.to_numeric(df_combined["gross"], errors="coerce") + pd.to_numeric(df_combined["tax"], errors="coerce")

    if "gross_ytd" in df_combined.columns and "tax_ytd" in df_combined.columns:
        df_combined.loc[:, "net_pay_ytd"] = pd.to_numeric(df_combined["gross_ytd"], errors="coerce") + pd.to_numeric(df_combined["tax_ytd"], errors="coerce")

    df_combined.to_csv(output_csv, index=False)

    print(f"✅ Parsed {len(all_records)} payslips → {output_csv}")


parse_all_payslips()
