from logging.config import dictConfig
from pathlib import Path
import re
import yaml


class Configuration:

    def __init__(self):
        self._dict_from_yaml = None
        self.logging_initialized = False
    
    @property
    def asset_path(self):
        return Path(__file__).parent / "assets"
    
    @property
    def dict_from_yaml(self):
        if self._dict_from_yaml is None:
            self._dict_from_yaml = self.get_config_file()
        return self._dict_from_yaml
    
    def get_config_file(self):
        with open(Path(__file__).parent / "config.yaml", "r") as fid:
            cfg = yaml.safe_load(fid)
        return cfg
    
    def __getattr__(self, key):
        if key in self.dict_from_yaml:
            return self.dict_from_yaml[key]
        else:
            raise KeyError(f"Configuration field '{key}' does not exist")
    
    @staticmethod
    def convert_tuple(value: list):
        return tuple(value)

    @staticmethod
    def hex_to_rgb(value: str):
        v = value.strip("#")
        if not re.match("[0-9a-f]{6}", v):
            raise ValueError(f"not a color code: {v}")
        return tuple(int(v[2 * i:2 * i + 2], 16) for i in range(0, 3))
    
    @staticmethod
    def rgb_to_hex(rgb: tuple):
        return "#" + "".join(f"{c:x}" for c in rgb)

    def init_logging(self):
        if not self.logging_initialized:
            dictConfig(self.logging)


config = Configuration()

    