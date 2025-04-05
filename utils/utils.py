from config.config import PROCESSED_DATA_DIR, CAPITAL_GAINS_FILE_NAME, TAX_STATEMENT_FILE_NAME
import pandas as pd


def read_tax_statement() -> pd.DataFrame:
    tax_statement_df = pd.read_csv(PROCESSED_DATA_DIR / TAX_STATEMENT_FILE_NAME)
    return tax_statement_df


def capital_gains_amount() -> int:
    capital_gains_df = pd.read_csv(PROCESSED_DATA_DIR / CAPITAL_GAINS_FILE_NAME)
    total_gains = capital_gains_df["gain"].sum()
    return total_gains
