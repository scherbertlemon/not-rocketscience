# This game is Not Rocketscience!

This started out as a [pygame](https://github.com/pygame/pygame) playground and turns into a 2D spaceship-flying game.

## Setup

The standard setup relies on [conda](https://docs.anaconda.com/free/miniconda/index.html) being present. Simply run ``setup.sh``: 

* creates a named conda environment ``not-rocketscience``
* installs dependencies from ``requirements.txt`` into it
* does a editable install of the package ``src/not_rocketscience``, so it can be imported in the ``_venv``environment

## Running the game

```bash
conda run -n not-rocketscience not-rocketscience
```

or 

```bash
conda activate not-rocketscience
not-rocketscience
```

## Controls

* Apply constant thrust by pressing and holding space
* Change orientation of spaceship with the left and right arrow keys

That's about all you can do :-D
