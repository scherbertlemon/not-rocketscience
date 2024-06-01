"""
Demonstrate spaceship class
"""
import numpy as np
from not_rocketscience import GameBase, config, Ship


class TestSpaceship(GameBase):

    def __init__(self):
        super().__init__(config.screen_size, fps=20, vsync=0)

        self.ship = Ship(
            np.array((self.screen_width / 2, self.screen_height / 2)),
            np.array((self.screen_width / 2, self.screen_height / 2)),
            **config.pilots[0]
        )

    def render_scene(self):
        self.ship.draw(self.screen, self.frametime_s, np.array((0, 0)))

    def process_inputs(self):
        self.ship.controls()


if __name__ == "__main__":
    ship = TestSpaceship()
    ship.gameloop()
