"""
Contains everything to run the spaceship flying game Not Rocketscience!
"""
from .framework import GameBase
from .config import config
from .background import ScrollingStarBackground, LayeredScrollingStarBackground
from .main import NotRocketScience
from .ship import Ship
from .planets import PlanetGroup, PlanetTexture, PlanetSimple
