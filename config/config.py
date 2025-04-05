import yaml
from pathlib import Path

with open(Path("config/parameters.yml"), "r") as f:
    config = yaml.safe_load(f)

# file paths
RAW_DATA_DIR = Path(config["paths"]["raw_data"])
PROCESSED_DATA_DIR = Path(config["paths"]["processed_data"])
ARCHIVE_DATA_DIR = Path(config["paths"]["archived_data"])

# file names
TAX_BRACKETS_FILE = Path(config["paths"]["tax_brackets_file"])
COMMSEC_TRANSACTIONS_FILE_NAME = Path(config["paths"]["commsec_transactions_file_name"])
CURRENT_PORTFOLIO_FILE_NAME = Path(config["paths"]["current_portfolio_file_name"])
CAPITAL_GAINS_FILE_NAME = Path(config["paths"]["capital_gains_file_name"])

# information on inflow/outflow sources
BRACKET_SOURCE_INFO = {
    "income": {
        "is_tax": True,
        "is_cumulative": True,
        "base_amount": config["fixed_values"]["base_salary"],
    },
    "hecs": {
        "is_tax": True,
        "is_cumulative": False,
        "base_amount": config["fixed_values"]["base_salary"],
    },
    "medicare": {
        "is_tax": True,
        "is_cumulative": False,
        "base_amount": config["fixed_values"]["base_salary"],
    },
    "medibank": {"is_tax": False, "is_cumulative": False, "base_amount": config["fixed_values"]["medibank_cost"]},
}

# debugging
DEBUG_MODE = config["other_settings"]["debug_mode"]
