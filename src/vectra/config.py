"""Layer 0: configuration loading."""
from pathlib import Path
import yaml


def load_config(path):
    with open(Path(path), "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)
