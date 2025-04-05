import yaml
from pathlib import Path

with open(Path("config/parameters.yml"), "r") as f:
    config = yaml.safe_load(f)

# file paths
TAX_BRACKETS_FILE = Path(config["paths"]["tax_brackets_file"])
RAW_DATA_DIR = Path(config["paths"]["raw_data"])
PROCESSED_DATA_DIR = Path(config["paths"]["processed_data"])

# numbers
LEVY_RATE = config["fixed_values"]["levy_rate"]
BASE_SALARY = config["fixed_values"]["base_salary"]
HEALTH_INSURANCE_COST = config["fixed_values"]["medibank_cost"]

# information on tax brackets, like name (income, hecs, medibank), whether its a tax or not and whether its cumulatively added
BRACKET_SOURCE_INFO = config["bracket_source_info"]

# debugging
DEBUG_MODE = config["other_settings"]["debug_mode"]
