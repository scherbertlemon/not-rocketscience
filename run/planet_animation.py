"""
Demonstrate planets
"""
import numpy as np
from not_rocketscience import GameBase, config, PlanetTexture


class PlanetAnimation(GameBase):

    def __init__(self):
        super().__init__((600, 600), vsync=True)
        self.planet = PlanetTexture(
            (300, 300),
            diameter=300,
            rotation_speed=20,
            atmosphere_thickness=10,
            atmosphere_layers=5
        )

    def render_scene(self):
        self.screen.fill(config.colors.space)
        self.planet.update_position_and_draw(self.screen, 0, np.array((100, -100)))

    def process_inputs(self):
        pass


if __name__ == "__main__":
    PlanetAnimation().gameloop()
