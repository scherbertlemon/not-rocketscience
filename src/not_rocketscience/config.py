from logging.config import dictConfig
import yaml
from pathlib import Path


def get_config_file():
    with open(Path(__file__).parents[2] / "config.yaml", "r") as fid:
        cfg = yaml.safe_load(fid)
    return cfg


config = get_config_file()


def init_log():
    dictConfig(config["logging"])
    