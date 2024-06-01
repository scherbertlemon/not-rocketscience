"""
Everything related to the scrolling background for Not Rocketscience. Scrolling background effect
is achieved by initializing multiple layers of starry backgrounds
(:py:class:`ScrollingStarBackground`), which are then scrolled with different speeds. This
generates a fake 3D effect.
"""
import logging
import pygame
import numpy as np


class ScrollingStarBackground:
    """
    One layer of scrolling star backgrounds. The background color can be opaque or transparent to
    layer multiple star backgrounds on top of each other. One layer of background is tiled, i.e.
    if the center of attention (usually ship position) shifts into a certain direction, new tiles
    with random stars are generated in that direction. Tiles that have shifted away far enough
    are removed. Far enough means 3 times tile size in city block metric distance to center of
    attention.

    :param tile_size: Size in pixels of one tile of starry background
    :param initial_position: center position in screen coordinates of first tile
    :param space_color: background color. Only shows if `fill_background` is `True`
    :param star_color: color which stars are drawn in
    :param fill_background: fill background with ``space_color`` (``True`` default), if
        ``False`` transparent
    :param star_size: Size in pixels of 'square' stars
    :param n_stars: amount of stars in one tile.
    """
    def __init__(self,
                 tile_size: tuple,
                 initial_position: np.array,
                 space_color=(10, 10, 30),
                 star_color=(255, 255, 200),
                 fill_background=True,
                 star_size=2,
                 n_stars=10):
        self.logger = logging.getLogger("ScrollingStarBackground")
        self.tile_size = tile_size
        self.delete_radius = sum(3 * dim for dim in self.tile_size)
        self.positions = {(0, 0): initial_position.copy()}
        self.space_color = space_color + (255,)
        self.star_color = star_color + (255,)
        self.fill_background = fill_background
        self.n_stars = n_stars
        self.star_size = star_size
        self._tiles = {}

    @property
    def tiles(self):
        """
        Manages the tiles by id, based on coordinates in
        :py:attr:`ScrollingStarBackground.positions`. For tile ids in ``positions``, which are not
        yet in the ``_tiles`` dictionary, a new tile is added.
        Tile ids which are in ``_tiles`` but not in ``positions`` any more are deleted.
        """
        # add new tiles that are not here
        for tile_id in self.positions:
            if tile_id not in self._tiles:
                self.logger.info(
                    "Generating tile %s, amount of tiles: %s", tile_id, len(self.positions)
                )
                tile = pygame.Surface(self.tile_size).convert_alpha()

                if self.fill_background:
                    tile.fill(self.space_color)
                else:
                    tile.fill(self.space_color[:3] + (0,))

                self._tiles[tile_id] = self.add_stars(tile)

        # remove tiles that are no longer needed
        delete_tile_ids = [tile_id for tile_id in self._tiles if tile_id not in self.positions]
        for delete_id in delete_tile_ids:
            self.logger.info(
                "Removing tile %s, amount of tiles: %s", delete_id, len(self.positions)
            )
            self._tiles.pop(delete_id)

        return self._tiles

    def add_stars(self, tile):
        """
        Randomly distribute stars on a tile surface

        :param tile: :py:class:`pygame.Surface` object representing one tile of background.
        :return: same :py:class:`pygame.Surface` object that comes in, but with stars drawn on it
        """
        star_coordinates = np.vstack(
            (
                np.random.randint(0, self.tile_size[0], (1, self.n_stars)),
                np.random.randint(0, self.tile_size[1], (1, self.n_stars))
            )
        )
        for index in range(0, star_coordinates.shape[1]):
            pygame.draw.rect(
                tile,
                self.star_color,
                (
                    star_coordinates[0, index],  # x position
                    star_coordinates[1, index],  # y position
                    self.star_size,              # width pixels
                    self.star_size               # height pixels
                )
            )
        return tile

    def block_distance_to_tiles(self, pos):
        """
        Calculates city block distance of screen coordinate ``pos`` to all tile center positions
        
        :param pos: 1 x 2 :py:class:`numpy.array` representing a screen coordinate
        :return: dict of `tile_id -> distance to pos`
        """
        coords, positions = zip(*self.positions.items())
        # broadcasting n x 2 with 1 x 2
        return {
            coord: dist
            for coord, dist in zip(coords, np.abs(np.vstack(positions) - pos).sum(axis=1))
        }

    def manage_tile_positions(self, pos, speed):
        """
        Dynamically adds tiles as neighbors to tile closest to screen coordinate ``pos``, in the 
        direction pointed by ``speed``.

        :param pos: 1 x 2 :py:class:`numpy.array` representing a screen coordinate, to determine closest tile
        :param speed: 1 x 2 :py:class:`numpy.array` indicating the speed vector of movement to determine
            direction in which tiles need to be added
        """
        tiles_distance = self.block_distance_to_tiles(pos)

        # determine new tile coordinates, 3 of them
        closest_tile = min(tiles_distance.items(), key=lambda td: td[1])
        closest_tile_id = closest_tile[0]

        dx, dy = np.sign(speed)
        for increment in [(dx, 0), (0, dy), (dx, dy)]:
            tile_coord = (closest_tile_id[0] + increment[0], closest_tile_id[1] + increment[1])
            if tile_coord not in self.positions:
                self.positions[tile_coord] = self.positions[closest_tile_id] + \
                    np.array(increment) * np.array(self.tile_size)
                self.logger.debug(
                    "Added coordinates %s for tile %s, ctid %s, speed %s",
                    [int(c) for c in self.positions[tile_coord]],
                    tile_coord,
                    closest_tile_id,
                    speed
                )

        # remove tiles that are far away
        delete_ids = [
            tile_id
            for tile_id, distance in tiles_distance.items()
            if distance > self.delete_radius
        ]
        for delete_id in delete_ids:
            coord = self.positions.pop(delete_id)
            self.logger.debug("Removed tile coordinates %s for tile id %s", coord, delete_id)

    def draw_tiles(self, screen, ship_position, dt, speed):
        """
        After deciding which tiles need to be removed and which need to be added based on
        ``ship_position`` and ``speed``, shift all tiles by the distance travelled during time step
        ``dt`` with ``speed`` into the opposite direction, and then draw them on the screen.

        :param screen: Display surface of ``pygame``.
        :param ship_position: 1 x 2 :py:class:`numpy.array` position towards which tile positions will be
            evaluated.
        :param dt: time step size, usually the time passed during one frame.
        :param speed: 1 x 2 :py:class:`numpy.array` representing speed vector. tiles wil move in opposite
            direction to simulate movement.
        """
        self.manage_tile_positions(ship_position, speed.astype(int))
        for tile_id, tile in self.tiles.items():
            self.positions[tile_id] -= dt * speed
            screen.blit(tile, tile.get_rect(center=self.positions[tile_id]))


class LayeredScrollingStarBackground:
    """
    Container class to layer multiple instances of :py:class:`ScrollingStarBackground` on top of each other.
    Layers will be enlarged by factors defined in :py:attr:`LayeredScrollingStarBackground.scale_modifiers`
    and movement speeds will be changed by :py:attr:`LayeredScrollingStarBackground.speed_modifiers` to
    create a parallactic effect.

    :param tile_size: unmodified tile size of the back-most layer. This layer will also have opaque
        background.
    :param initial_position: Initial screen position of the initial tiles on all layers.
    :param space_color: RGB tuple for color drawn as background of the back-most layer
    :param star_color: RGB tuple for color of stars drawn on all layers
    :param n_stars: amount of stars on each layer
    :param n_layers: amount of layers
    """
    def __init__(self,
                 tile_size: tuple,
                 initial_position: np.array,
                 space_color=(10, 10, 30, 255),
                 star_color=(255, 255, 200, 255),
                 n_stars=10,
                 n_layers=3):
        self.logger = logging.getLogger("LayeredScrollingStarBackrgound")
        self.layers = []
        self.n_layers = n_layers

        for index, scale_mod in enumerate(self.scale_modifiers):
            self.logger.info(
                "Create background layer with factor %s increased tile size %s",
                scale_mod,
                tile_size
            )
            self.layers.append(
                ScrollingStarBackground(
                    tuple(dim * scale_mod for dim in tile_size),
                    initial_position,
                    space_color=space_color,
                    star_color=star_color,
                    n_stars=n_stars,
                    star_size=2 + index,
                    fill_background=(index == 0)
                )
            )

    @property
    def speed_modifiers(self):
        """
        layer movement speeds are reduced by a quadratically reducing factor for each layer index
        """
        return [((i + 1) / (self.n_layers + 1))**2  for i in range(0, self.n_layers)]

    @property
    def scale_modifiers(self):
        """
        Foreground layers appear bigger by the factor indicated in this list.
        """
        return [1.0 + i * .1 for i in range(0, self.n_layers)]

    def draw_tiles(self, screen, ship_position, dt, speed):
        """
        Draws the tiles for all layers, see :py:meth:`ScrollingStarBackground.draw_tiles`. The factors in
        :py:attr:`LayeredScrollingStarBackground.speed_modifiers` are applied to the speed vector on each
        layer.

        :param screen: Display surface of ``pygame``.
        :param ship_position: 1 x 2 :py:class:`numpy.array` position towards which tile positions will be
            evaluated.
        :param dt: time step size, usually the time passed during one frame.
        :param speed: 1 x 2 :py:class:`numpy.array` representing speed vector. tiles wil move in opposite
            direction to simulate movement.
        """
        for layer, speed_mod in zip(self.layers, self.speed_modifiers):
            layer.draw_tiles(screen, ship_position, dt, speed * speed_mod)
