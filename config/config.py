import yaml
from pathlib import Path

with open(Path("config/parameters.yml"), "r") as f:
    config = yaml.safe_load(f)

# file paths
LANDING_DATA_DIR = Path(config["paths"]["landing_data"])
PROCESSED_DATA_DIR = Path(config["paths"]["processed_data"])
ARCHIVED_DATA_DIR = Path(config["paths"]["archived_data"])

# file names inputs
TAX_BRACKETS_FILE = Path(config["file_names_inputs"]["tax_brackets"])
COMMSEC_TRANSACTIONS_FILE_NAME = Path(config["file_names_inputs"]["commsec_transactions_in"])

# file names outputs
CURRENT_PORTFOLIO_FILE_NAME = Path(config["file_names_outputs"]["current_portfolio"])
CAPITAL_GAINS_FILE_NAME = Path(config["file_names_outputs"]["capital_gains"])
TAX_STATEMENT_FILE_NAME = Path(config["file_names_outputs"]["tax_statement"])
INFLOWS_FILE_NAME = Path(config["file_names_outputs"]["inflows"])

# information on inflow/outflow sources
BRACKET_SOURCE_INFO = {
    "income": {"is_tax": True, "is_cumulative": True, "base_amount": config["fixed_values"]["base_salary"]},
    "hecs": {"is_tax": True, "is_cumulative": False, "base_amount": config["fixed_values"]["base_salary"]},
    "medicare": {"is_tax": True, "is_cumulative": False, "base_amount": config["fixed_values"]["base_salary"]},
    "medibank": {"is_tax": False, "is_cumulative": False, "base_amount": config["fixed_values"]["medibank_cost"]},
}

# fixed values
FINANCIAL_YEAR = config["fixed_values"]["financial_year"]


# debugging
DEBUG_MODE = config["other_settings"]["debug_mode"]
