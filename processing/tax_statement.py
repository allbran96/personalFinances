# script that creates the payg_tax csv


from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

from config.config import BRACKET_SOURCE_INFO, PROCESSED_DATA_DIR
from processing.tax_bracket_calculator import calculate_tax_bracket_amount


def create_tax_statement() -> str:

    base_salary = BRACKET_SOURCE_INFO["income"]["base_amount"]

    # initialize empty row structure
    rows: List[Dict[str, Any]] = []

    # for each item in BRACKET_SOURCE_INFO (sources of tax/rebates dependent on tax brackets), calculate the amount
    for category, config in BRACKET_SOURCE_INFO.items():

        is_tax = config["is_tax"]
        is_cumulative = config["is_cumulative"]
        base_amount = config["base_amount"]

        if is_tax:
            row: Dict[str, Any] = {"category": category, "is_tax": is_tax, "amount": calculate_tax_bracket_amount(category, is_tax, is_cumulative, base_amount, base_salary)}
            rows.append(row)
        else:
            continue

    tax_df = pd.DataFrame(rows).sort_values(by="is_tax", ascending=False)

    # save to data/processed
    output_path: Path = PROCESSED_DATA_DIR / "tax_statement.csv"
    tax_df.to_csv(output_path, index=False, mode="w")

    return f"Tax statement saved to {output_path} with {len(tax_df)} rows."
