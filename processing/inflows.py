# script that creates inflows.csv


import pandas as pd

from config.config import BRACKET_SOURCE_INFO, INFLOWS_FILE_NAME, PROCESSED_DATA_DIR
from utils.utils import capital_gains_amount, read_tax_statement


def inflows() -> str:

    tax_df = read_tax_statement()

    base_salary_annl = BRACKET_SOURCE_INFO["income"]["base_amount"]
    net_salary_mthly = round((base_salary_annl - tax_df[tax_df["payg"]]["amount"].sum()) / 12, 2)
    cgt_amount = capital_gains_amount()
    bonuses = 5000
    inflows = [
        {"name": "base_salary_annl", "frequency": "Annually", "amount": base_salary_annl},
        {"name": "net_salary_mthly", "frequency": "Monthly", "amount": net_salary_mthly},
        {"name": "cgt_amount", "frequency": "Annually", "amount": cgt_amount},
        {"name": "bonuses", "frequency": "Annually", "amount": bonuses},
    ]

    inflows_df = pd.DataFrame(inflows)
    output_path = PROCESSED_DATA_DIR / INFLOWS_FILE_NAME
    inflows_df.to_csv(output_path, index=False)

    return f"Inflow statement saved to {output_path} with {len(inflows_df)} rows."
