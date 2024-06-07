"""
A very simple pygame, where only one image is placed on the screen.
"""
from pathlib import Path
import pygame

from not_rocketscience import GameBase


class VerySimple(GameBase):

    def __init__(self):
        super().__init__((500, 500), fps=20, caption="Very basic pygame")
        self.sprite = pygame.image.load(Path(__file__).parents[1] / "src" / "not_rocketscience" / "assets" / "ships" / "ship_cd_3.png")

    def render_scene(self):
        self.screen.fill((19, 20, 36))
        self.screen.blit(self.sprite, self.sprite.get_rect(center=(250, 250)))

    def process_inputs(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            pass
        elif keys[pygame.K_LEFT]:
            pass
        else:
            pass


if __name__ == "__main__":
    VerySimple().gameloop()
