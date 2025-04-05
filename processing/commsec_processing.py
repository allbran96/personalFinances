# transforms the raw confirmation_details.csv from Commsec into a table

from datetime import datetime
from pathlib import Path
from shutil import copy, move

import pandas as pd

from config.config import ARCHIVE_DATA_DIR, CAPITAL_GAINS_FILE_NAME, COMMSEC_TRANSACTIONS_FILE_NAME, CURRENT_PORTFOLIO_FILE_NAME, DEBUG_MODE, PROCESSED_DATA_DIR, RAW_DATA_DIR
from utils.dates import in_current_financial_year


def clean_transactions_df(transactions_df: pd.DataFrame) -> pd.DataFrame:

    # transform date column to datetime type
    transactions_df["Trade Date"] = pd.to_datetime(transactions_df["Trade Date"], dayfirst=True)

    # normalize column names and values
    transactions_df = transactions_df.rename(
        columns={"Trade Date": "date", "Buy/ Sell": "type", "Security": "security", "Units": "units", "Average Price ($)": "price", "Net Proceeds ($)": "proceeds"}
    )

    # transoform types and clean up
    transactions_df["type"] = transactions_df["type"].str.strip().str.upper().map({"B": "buy", "S": "sell"})
    transactions_df["units"] = transactions_df["units"].astype(float)
    transactions_df["price"] = transactions_df["price"].astype(float)

    return transactions_df


def current_portfolio(transactions_df: pd.DataFrame) -> pd.DataFrame:

    # add new column for units, negative for sales and positive for buys
    transactions_df["signed_units"] = transactions_df.apply(lambda row: row["units"] if row["type"].lower() == "buy" else -row["units"], axis=1)

    # sum up buys and sales per unit
    current_portfolio_df = transactions_df.groupby("security")["signed_units"].sum().reset_index()

    return current_portfolio_df


def capital_gains(transactions_df: pd.DataFrame) -> pd.DataFrame:

    # make copy of original df and then sort by date
    df = transactions_df.copy()
    df.sort_values(by="date", inplace=True)

    # split copy into buys and sells
    buys = df[df["type"] == "buy"].copy()
    sells = df[(df["type"] == "sell") & df["date"].apply(in_current_financial_year)].copy()

    # initialize empty list for cgt
    gains = []

    # loop through sales to calculate cgt
    for _, sell in sells.iterrows():

        # grab columns
        security = sell["security"]
        units_to_match = sell["units"]
        sell_date = sell["date"]

        # grab matching buys of same security, for FIFO
        matching_buys = buys[(buys["security"] == security) & (buys["units"] > 0)]

        # loop through the matching buys for each sell
        for i, buy in matching_buys.iterrows():

            # if no matching units (no sales) then no CGT
            if units_to_match == 0:
                break

            # any sale that has a buy order will get matched
            available_units = buy["units"]
            match_units = min(available_units, units_to_match)

            # for buy transactions
            buy_total_cost = match_units * buy["price"]
            buy_brokerage = buy["proceeds"] * (match_units / buy["units"])  # proportional
            total_cost_basis = buy_total_cost + buy_brokerage

            # for sell transactions
            proceeds = match_units * sell["price"]
            sell_brokerage = sell["proceeds"] * (match_units / sell["units"])
            net_proceeds = proceeds - sell_brokerage

            # total
            gain = net_proceeds - total_cost_basis

            gains.append(
                {
                    "security": security,
                    "sell_date": sell_date,
                    "units": match_units,
                    "cost_basis": round(total_cost_basis, 2),
                    "proceeds": round(proceeds, 2),
                    "gain": round(gain, 2),
                }
            )

            buys.at[i, "units"] -= match_units
            units_to_match -= match_units

    return pd.DataFrame(gains)


def archive_transactions_file() -> str:

    # archives the raw csv with timestamp
    source_path = RAW_DATA_DIR / COMMSEC_TRANSACTIONS_FILE_NAME
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_path = ARCHIVE_DATA_DIR / f"{timestamp}_commsec_transactions.csv"

    if DEBUG_MODE:
        copy(str(source_path), str(archive_path))
        print(f"[DEBUG] Copied file to archive: {archive_path}")
    else:
        move(str(source_path), str(archive_path))
        print(f"Moved file to archive: {archive_path}")

    return f"Commsec transactions statement archived to {archive_path}."


def process_commsec_transactions_file() -> str:

    # read in transactions csv from commsec
    transactions_df = pd.read_csv(RAW_DATA_DIR / COMMSEC_TRANSACTIONS_FILE_NAME)

    # clean and normalize df
    transactions_df = clean_transactions_df(transactions_df)

    # run to create current_portfolio
    current_portfolio_df = current_portfolio(transactions_df)

    # run to create capital_gains
    capital_gains_df = capital_gains(transactions_df)

    # run to archive the input file
    archive_transactions_file()

    # save portfolio to data/processed
    output_path_portfolio: Path = PROCESSED_DATA_DIR / CURRENT_PORTFOLIO_FILE_NAME
    current_portfolio_df.to_csv(output_path_portfolio, index=False, mode="w")
    print(f"Current portfolio saved to {output_path_portfolio} with {len(current_portfolio_df)} rows.")

    # save portfolio to data/processed
    output_path_cg: Path = PROCESSED_DATA_DIR / CAPITAL_GAINS_FILE_NAME
    capital_gains_df.to_csv(output_path_cg, index=False, mode="w")
    print(f"Capital gains saved to {output_path_cg} with {len(capital_gains_df)} rows.")

    return "Commsec transactions file converted to current_portfolio, capital_gains and archived."
