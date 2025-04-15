# script that creates inflows.csv

from pathlib import Path
import pandas as pd

from config.config import LANDING_DATA_DIR, BASE_SALARY, BONUSES, PROCESSED_DATA_DIR, FINANCIAL_YEAR, SUPERANNUATION_RATE
from utils.utils import capital_gains_amount, save_df_to_csv
from utils.dates import in_current_financial_year


def create_inflows(cg_amount: float) -> pd.DataFrame:
    
    inflows = [
        {"name": "base_salary", "amount": BASE_SALARY},
        {"name": "bonuses", "amount": BONUSES},
        {"name": "capital_gains", "amount": cg_amount},
        {"name": "superannuation_work", "amount": round(BASE_SALARY*SUPERANNUATION_RATE,2)},
        {"name": "dividends", "amount": 0}
    ]

    return pd.DataFrame(inflows)


def main():

    # defining paths
    # input path for after processing commsec transactions
    commsec_transactions_path = Path(PROCESSED_DATA_DIR / "commsec" / "capital_gains.csv")
    # output path for inflows.csv
    inflows_path = Path(PROCESSED_DATA_DIR / f"inflows_{FINANCIAL_YEAR}.csv")


    # calculate capital gains
    cg_amount = capital_gains_amount(commsec_transactions_path)

    # create the inflows dataframe
    inflows_df = create_inflows(cg_amount)

    # save df to csv 
    save_status = save_df_to_csv(inflows_df, inflows_path)
    print(save_status)
        

    return 

main()