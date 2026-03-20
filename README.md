![logo](src/not_rocketscience/assets/logo.png)

# This game is Not Rocketscience! 🚀

This started out as a [pygame-ce](https://github.com/pygame-community/pygame-ce) playground and turned into a 2D spaceship-flying game. There is really not much more you can do 😄

## ⚙️Setup

A python installation with Python 3.11 or higher is required, a virtual environment to run the game or to develop in can be created following the instructions below:

1. Create a virtual Python environment in the root folder of this repo
    ```shell
    python -m venv .venv
    ```
2. Activate the environment
    ```shell
    # Windows
    .venv/Scripts/activate.bat
    # Mac / Linux
    source .venv/bin/activate
3. install dependencies from ``pyproject.toml``:
    ```shell
    pip install -e .
    ````
4. Run any of the scripts in ``run`` or run the game itself with the command ``not-rocketscience`` from any terminal where the environment is activated.

## 🕹️Controls

* Apply constant thrust by pressing and holding the ``X`` key
* Change orientation of spaceship with the left and right arrow keys

## 📎Installing dev dependencies for creating documentation / running jupyter

Run from a terminal with activated environment

```shell
pip install -e ".[pres,docs]"
```

The presentation in ``run/presentation.ipynb`` is currently broken!

## 📜License

The code is released under the MIT License [(see LICENSE)](./LICENSE). All artwork distributed with the code is originally created by me and falls under the same conditions.

All artwork included in this repository originally by Andreas Roth.