# script that creates the payg_tax csv


from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

from config.config import BRACKET_SOURCE_INFO, PROCESSED_DATA_DIR
from scripts.tax_bracket_calculator import calculate_tax_bracket_amount
from utils.utils import capital_gains_amount


def create_tax_statement() -> str:

    base_salary = BRACKET_SOURCE_INFO["income"]["base_amount"]
    capital_gains = capital_gains_amount("gain")
    gross_salary = base_salary + capital_gains
    total_payg_tax = 0.0
    total_gross_tax = 0.0

    # initialize empty row structure
    rows: List[Dict[str, Any]] = []

    # for each item in BRACKET_SOURCE_INFO (sources of tax/rebates dependent on tax brackets), calculate the amount
    for category, config in BRACKET_SOURCE_INFO.items():

        is_tax = config["is_tax"]
        is_cumulative = config["is_cumulative"]
        base_amount = config["base_amount"]

        if not is_tax:
            continue

        payg_tax = -calculate_tax_bracket_amount(category, is_tax, is_cumulative, base_amount, base_salary)
        total_payg_tax += payg_tax

        rows.append({"category": f"{category}_tax", "payg": True, "amount": round(payg_tax, 2)})

        gross_tax = -calculate_tax_bracket_amount(category, is_tax, is_cumulative, gross_salary, gross_salary)
        total_gross_tax += gross_tax

        if category == "income":
            cgt_tax = gross_tax - payg_tax

    rows.append({"category": "capital_gains_tax", "payg": False, "amount": round(cgt_tax, 2)})

    payment_delta = total_gross_tax - total_payg_tax

    rows.append({"category": "extra_tax", "payg": False, "amount": round(payment_delta + cgt_tax, 2)})

    tax_df = pd.DataFrame(rows)

    # save to data/processed
    output_path: Path = PROCESSED_DATA_DIR / "tax_statement.csv"
    tax_df.to_csv(output_path, index=False, mode="w")

    return f"Tax statement saved to {output_path} with {len(tax_df)} rows."
