# script that creates the payg_tax csv


from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

from config.config import BRACKET_SOURCE_INFO, PROCESSED_DATA_DIR
from scripts.tax_bracket_calculator import calculate_tax_bracket_amount


def create_income_statement() -> str:

    # initialize empty row structure
    rows: List[Dict[str, Any]] = []

    # for each item in BRACKET_SOURCE_INFO (sources of tax/rebates dependent on tax brackets), calculate the amount
    for source, (is_tax, is_cumulative) in BRACKET_SOURCE_INFO.items():
        row: Dict[str, Any] = {"name": source, "is_tax": is_tax, "amount": calculate_tax_bracket_amount(source, is_tax, is_cumulative)}
        rows.append(row)
    income_df = pd.DataFrame(rows).sort_values(by="is_tax", ascending=False)

    # save to repo
    output_path: Path = PROCESSED_DATA_DIR / "income_statement.csv"
    income_df.to_csv(output_path, index=False, mode="w")

    return f"Income statement saved to {output_path} with {len(income_df)} rows."
