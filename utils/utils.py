from config.config import PROCESSED_DATA_DIR, CAPITAL_GAINS_FILE_NAME, TAX_STATEMENT_FILE_NAME, DEBUG_MODE
import pandas as pd
import shutil
from pathlib import Path
import os

def read_tax_statement() -> pd.DataFrame:
    tax_statement_df = pd.read_csv(PROCESSED_DATA_DIR / TAX_STATEMENT_FILE_NAME)
    return tax_statement_df


def capital_gains_amount(capital_gains_csv=Path(PROCESSED_DATA_DIR / "capital_gains.csv")) -> int:
    capital_gains_df = pd.read_csv(capital_gains_csv)
    return capital_gains_df["gain"].sum()

def archive_file(landing_path: Path, archive_path: Path) -> str:

    file_name = landing_path.name
    archive_path.mkdir(parents=True, exist_ok=True)

    if DEBUG_MODE:
        shutil.copy(str(landing_path), str(archive_path))
    else:
        shutil.move(str(landing_path), str(archive_path))

    return f"File {file_name} archived to {archive_path}."

def save_df_to_csv(df: pd.DataFrame, processed_path: Path, index_status=False) -> str:

    # dont rewrite old columns
    if os.path.exists(processed_path) :
        existing_data = pd.read_csv(processed_path)
        combined = pd.concat([existing_data, df])
        combined = combined.drop_duplicates()
    else:
        combined = df

    # save as csv    
    combined.to_csv(processed_path,index=index_status)
    return f"Dataframe saved to csv at {str(processed_path)}."