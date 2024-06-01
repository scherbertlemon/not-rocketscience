"""
Module with helper classes to make yaml config available as python variables
"""
from logging.config import dictConfig
from pathlib import Path
import re
from pprint import pformat
import yaml


class Colors:
    """Provding hex colors as rgb tuples"""
    def __init__(self, colors: dict):
        self.colors = colors

    def __getattr__(self, color):
        if color in self.colors:
            return self.hex_to_rgb(self.colors[color])
        else:
            raise KeyError(f"{color} is not present in color dictionary, try one of "
                           f"{list(self.colors.keys())}")

    @staticmethod
    def hex_to_rgb(value: str):
        """
        Convert a hex string prefixed with # to an RGB tuple, e.g. '#ff0000' -> (255, 0, 0)

        :param value: hex string
        :return: RGB tuple
        """
        v = value.strip("#").lower()
        if not re.match("[0-9a-f]{6}", v):
            raise ValueError(f"not a color code: {v}")
        return tuple(int(v[2 * i:2 * i + 2], 16) for i in range(0, 3))

    @staticmethod
    def rgb_to_hex(rgb: tuple):
        """
        Convert RGB tuple to hex string representation, opposite of `Colors.hex_to_rgb`

        :param rgb: RGB tuple
        :return: hex string
        """
        return "#" + "".join(f"{c:x}" for c in rgb)

    def __repr__(self):
        return pformat(self.colors)


class Configuration:
    """
    Configuration class providing the contents of the config.yaml in the not rocketscience
    package folder as variables.
    """
    def __init__(self):
        self._dict_from_yaml = None
        self.logging_initialized = False
        self._colors = None

    @property
    def asset_path(self):
        """
        Predefined path to the asset folder with all the picture files, in the not-rocketscience
        package folder

        :return: path to assets folder
        :rtype: pathlib.Path
        """
        return Path(__file__).parent / "assets"

    @property
    def colors(self):
        """
        Special property for colors that returns all colors as RGB tuples

        :return: `Colors` object
        """
        if self._colors is None:
            self._colors = Colors(self.dict_from_yaml["colors"])
        return self._colors

    @property
    def dict_from_yaml(self):
        """
        dictionary parsed from config.yaml. Read on first call.

        :return: dictionary with all fields from config.yaml
        """
        if self._dict_from_yaml is None:
            self._dict_from_yaml = self.get_config_file()
        return self._dict_from_yaml

    @property
    def screen_size(self):
        """
        Special property returning screen size as tuple, because can only define a list in yaml

        :return: screen size for the game as tuple
        """
        return tuple(self.dict_from_yaml["screen_size"])

    @staticmethod
    def get_config_file():
        """
        Static method to read the contents of config.yaml

        :return: dictionary with all fields from config.yaml
        """
        with open(Path(__file__).parent / "config.yaml", "r", encoding="utf-8") as fid:
            cfg = yaml.safe_load(fid)
        return cfg

    def __getattr__(self, key):
        if key in self.dict_from_yaml:
            return self.dict_from_yaml[key]
        else:
            raise KeyError(f"Configuration field '{key}' does not exist")

    def init_logging(self):
        """
        Initializes the logger if not already done.
        """
        if not self.logging_initialized:
            dictConfig(self.logging)
            self.logging_initialized = True

    def __repr__(self):
        return pformat(self.dict_from_yaml)


config = Configuration()
