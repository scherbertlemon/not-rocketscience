from not_rocketscience import GameBase, config
from not_rocketscience.planets import PlanetTexture
import numpy as np


class PlanetTest(GameBase):

    def __init__(self):
        super().__init__((400, 400), fps=60)
        self.planet = PlanetTexture((200, 200), diameter=200, rotation_speed=20, atmosphere_thickness=10, atmosphere_layers=5)

    def render_scene(self):
        self.screen.fill(config.hex_to_rgb(config.space_color))
        self.planet.update_position_and_draw(self.screen, 0, np.zeros(2))
        # self.logger.debug(f"fps: {self.clock.get_fps():3.0f}")



    def process_inputs(self):
        pass


if __name__ == "__main__":
    pt = PlanetTest()
    pt.gameloop()