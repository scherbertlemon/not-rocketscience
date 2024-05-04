import logging
import pygame
import numpy as np
from pprint import pformat


class ScrollingStarBackground:

    def __init__(self,
                 tile_size: tuple,
                 initial_position: np.array,
                 spacecolor=(10, 10, 30, 255),
                 starcolor=(255, 255, 200, 255),
                 fill_background=True,
                 star_size=2,
                 n_stars=10):
        self.logger = logging.getLogger("ScrollingStarBackground")
        self.tile_size = tile_size
        self.delete_radius = sum(2 * dim for dim in self.tile_size)
        self.positions = {(0, 0): initial_position.copy()}
        self.spacecolor = spacecolor
        self.starcolor = starcolor
        self.fill_background = fill_background
        self.n_stars = n_stars
        self.star_size = star_size
        self._tiles = {}
    
    @property
    def tiles(self):
        # add new tiles that are not here
        for tile_id in self.positions:
            if tile_id not in self._tiles:
                self.logger.debug(f"Generating tile {tile_id}")
                tile = pygame.Surface(self.tile_size).convert_alpha()

                if self.fill_background:
                    tile.fill(self.spacecolor)
                
                self._tiles[tile_id] = self.add_stars(tile)
        
        # remove tiles that are no longer needed
        delete_tile_ids = [tile_id for tile_id in self._tiles if tile_id not in self.positions]
        for delete_id in delete_tile_ids:
            self.logger.debug(f"Removing tile {delete_id}")
            self._tiles.pop(delete_id)
        
        return self._tiles

    def add_stars(self, tile):
        star_coordinates = np.vstack(
            (
                np.random.randint(0, self.tile_size[0], (1, self.n_stars)),
                np.random.randint(0, self.tile_size[1], (1, self.n_stars))
            )
        )
        for index in range(0, star_coordinates.shape[1]):
            pygame.draw.rect(
                tile,
                self.starcolor,
                (star_coordinates[0, index], star_coordinates[1, index], self.star_size, self.star_size)
            )
        return tile
    
    def block_distance_to_tiles(self, pos):
        coords, positions = zip(*self.positions.items())
        # broadcasting n x 2 with 1 x 2
        return {coord: dist for coord, dist in zip(coords, np.abs(np.vstack(positions) - pos).sum(axis=1))}
    
    def manage_tile_positions(self, pos, speed):
        tiles_distance = self.block_distance_to_tiles(pos)

        # determine new tile coordinates, 3 of them
        closest_tile = min(tiles_distance.items(), key=lambda td: td[1])
        closest_tile_id = closest_tile[0]
        
        dx, dy = np.sign(speed)
        for increment in [(dx, 0), (0, dy), (dx, dy)]:
            tile_coord = (closest_tile_id[0] + increment[0], closest_tile_id[1] + increment[1])
            if tile_coord not in self.positions:
                self.positions[tile_coord] = self.positions[closest_tile_id] + np.array(increment) * np.array(self.tile_size)
                self.logger.debug(f"Added coordinates {[int(c) for c in self.positions[tile_coord]]} for tile {tile_coord}, ctid {closest_tile_id}, speed {speed}")
                # self.logger.debug(f"pos: {[int(p) for p in pos]}, closest tpos: {[int(p) for p in self.positions[closest_tile_id]]}, dist {tiles_distance[closest_tile_id]}, id {closest_tile_id}")
                # self.logger.debug(pformat(self.positions))
        
        # remove tiles that are far away
        delete_ids = [tile_id for tile_id, distance in tiles_distance.items() if distance > self.delete_radius]
        for delete_id in delete_ids:
            coord = self.positions.pop(delete_id)
            self.logger.debug(f"Removed tile coordinates {coord} for tile id {delete_id}")

    def draw_tiles(self, screen, ship_position, dt, speed):
        self.manage_tile_positions(ship_position, speed.astype(int))
        for tile_id, tile in self.tiles.items():
            self.positions[tile_id] -= dt * speed
            screen.blit(tile, tile.get_rect(center=self.positions[tile_id]))



class ScrollingStars:

    def __init__(self,
                 size: tuple,
                 screen_size: tuple,
                 initial_position: np.array,
                 spacecolor=(10, 10, 30, 255),
                 starcolor=(255, 255, 200, 255),
                 n_layers=3,
                 n_stars=20,
                 star_size=2):
        
        self.logger = logging.getLogger("ScrollingStars")
        self.size = size
        self.screen_size = screen_size
        self.space_color = spacecolor
        self.star_color = starcolor
        self.n_layers = n_layers
        self.n_stars = n_stars
        self.star_size = star_size
        self.layer_positions = [initial_position.copy() for _ in range(0, n_layers)]
        self._surfaces = None 

    @property
    def surfaces(self):
        if self._surfaces is None:
            self._surfaces = []
            for i in range(0, self.n_layers):
                self.logger.debug(f"Generating surface {i}")
                surf = pygame.Surface(self.size).convert_alpha()
                if i == 0:
                    surf.fill(self.space_color)
                else:
                    surf.fill(self.space_color[:3] + (0,))
                self.add_stars(surf, self.n_stars)
                scale_factor = 1 + i * .75
                self._surfaces.append(
                    pygame.transform.scale(
                        surf, 
                        (int(scale_factor * self.size[0]), int(scale_factor * self.size[1]))
                    )
                )
        return self._surfaces
        
    def add_stars(self, surf, n_stars):
        star_coordinates = np.vstack(
            (
                np.random.randint(0, self.size[0], (1, n_stars)),
                np.random.randint(0, self.size[1], (1, n_stars))
            )
        )
        for index in range(0, star_coordinates.shape[1]):
            pygame.draw.rect(
                surf,
                self.star_color,
                (star_coordinates[0, index], star_coordinates[1, index], self.star_size, self.star_size)
            )

    def blit(self, screen, dt=0, speed=np.zeros((1,2))):
        for i, surf in enumerate(self.surfaces):
            self.layer_positions[i] -= dt * (i + 1) / (self.n_layers + 1) * speed
            rect = surf.get_rect(center=tuple(self.layer_positions[i]))
            pos = self.layer_positions[i] - 0.5 * np.array((rect.width, rect.height))
            screen.blit(surf, rect)
