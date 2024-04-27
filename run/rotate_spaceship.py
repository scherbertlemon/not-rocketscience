from not_rocketscience import GameBase, config
import pygame
import numpy as np


class Spaceship(GameBase):

    def __init__(self):
        super().__init__(config.convert_tuple(config.screen_size), fps=15)
        self.ship_layer = pygame.Surface((100, 100)).convert_alpha()
        self.ship_layer.fill((0, 0, 0, 0))
        self.ship = pygame.draw.rect(self.ship_layer, (255, 0, 0, 255), (40, 25, 20, 50))
        self.screen.fill(config.hex_to_rgb(config.background["space_color"]))
        self.rotation = 0
        self.angle = 0
        self.thrust = False

    def fire_color(self):
        return 255, 200, 100, 200 if self.thrust else 0

    def render_scene(self):

        self.angle += self.rotation
        self.logger.debug(f"angle: {self.angle}")
        fire = pygame.draw.rect(self.ship_layer, self.fire_color(), (45, 75, 10, 15))
        rotated_ship = pygame.transform.rotate(self.ship_layer, self.angle)
        pos = rotated_ship.get_rect(center=tuple(0.5 * np.array(self.screen_size)))
        self.screen.blit(rotated_ship, pos)

    def process_inputs(self):
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rotation = 10
        elif keys[pygame.K_RIGHT]:
            self.rotation = -10
        else:
            self.rotation = 0

        if keys[pygame.K_w]:
            self.thrust = True
        else:
            self.thrust = False


if __name__ == "__main__":
    ship = Spaceship()
    ship.gameloop()