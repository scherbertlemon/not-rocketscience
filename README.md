![logo](src/not_rocketscience/assets/logo.png)

# This game is Not Rocketscience!

This started out as a [pygame](https://github.com/pygame/pygame) playground and turns into a 2D spaceship-flying game.

## Setup

The standard setup relies on [conda](https://docs.anaconda.com/free/miniconda/index.html) being present. Simply run ``setup.sh``: 

* creates a named conda environment ``not-rocketscience``
* installs dependencies from ``requirements.txt`` into it
* does a editable install of the package ``src/not_rocketscience``, so it can be imported in the ``not-rocketscience`` environment

You can also do those steps manually:

```bash
conda create -n not-rocketscience --file requirements.txt -c conda-forge -y
conda run -n not-rocketscience pip install -e .
```

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

* Apply constant thrust by pressing and holding the ``X`` key
* Change orientation of spaceship with the left and right arrow keys

That's about all you can do :-D
