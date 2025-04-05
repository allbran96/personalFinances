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

# numbers
LEVY_RATE = config["fixed_values"]["levy_rate"]
BASE_SALARY = config["fixed_values"]["base_salary"]
HEALTH_INSURANCE_COST = config["fixed_values"]["medibank_cost"]

# information on tax brackets, like name (income, hecs, medibank), whether its a tax or not and whether its cumulatively added
BRACKET_SOURCE_INFO = config["bracket_source_info"]

# debugging
DEBUG_MODE = config["other_settings"]["debug_mode"]
