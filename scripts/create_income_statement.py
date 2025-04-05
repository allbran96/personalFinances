### script that creates the payg_tax csv

import pandas as pd

from config.config import BRACKET_SOURCE_INFO, PROCESSED_DATA_DIR
from scripts.tax_bracket_calculator import calculate_tax_bracket_amount


def create_income_statement():

    # initialize empty row structure
    rows = []

    # for each item in BRACKET_SOURCE_INFO (sources of tax/rebates dependent on tax brackets), calculate the amount
    for source, (is_tax, is_cumulative) in BRACKET_SOURCE_INFO.items():
        row = {"name": source, "is_tax": is_tax, "amount": calculate_tax_bracket_amount(source, is_tax, is_cumulative)}
        rows.append(row)
    payg_tax_df = pd.DataFrame(rows).sort_values(by="is_tax", ascending=False)

    # save to repo
    output_path = f"{PROCESSED_DATA_DIR}/payg_tax.csv"
    payg_tax_df.to_csv(output_path, index=False, mode="w")

    return f"PAYG tax table saved to {output_path} with {len(payg_tax_df)} rows."
