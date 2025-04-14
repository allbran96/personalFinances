# script that creates the payg_tax csv


import pandas as pd


def inflow_outflow() -> str:

    # initialize empty row structure
    tax_statement_df = pd.read_csv("data/processed/tax_statement.csv")

    return f"Read tax_statement_df {tax_statement_df}"
