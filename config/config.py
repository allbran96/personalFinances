import yaml
from pathlib import Path

with open(Path('config/parameters.yml'), 'r') as f:
    config = yaml.safe_load(f)

TAX_BRACKETS_DIR = Path(config["paths"]["tax_brackets"])