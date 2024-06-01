from setuptools import setup, find_packages
from pathlib import Path
import re


def parse_requirements():
    with open(Path(__file__).parent / "requirements.txt", "r") as req:
        reqs = [line for line in re.split("\r?\n", req.read())]
    return [r for r in reqs if not re.match("python[\=<>]", r)]


setup(
    name="not-rocketscience",
    version="0.2.1",
    description="A spaceship-flying game based on pygame",
    author="Andreas Roth",
    author_email="kommentare@s-lemon.de",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=parse_requirements(),
    package_data={"not_rocketscience": ["*.png", "*.yaml"]},
    entry_points={
        "console_scripts": ["not-rocketscience = not_rocketscience.main:cli"]
    }
        
)