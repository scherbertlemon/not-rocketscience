from not_rocketscience import PlanetTexture, GameBase, config
from not_rocketscience.math import newton_gravity_force, canonical_newton_parameterset
import numpy as np


class GravityDemo(GameBase):
    def __init__(self):
        super().__init__(config.screen_size, vsync=1, caption="gravity demo")
        self.p1 = PlanetTexture(np.array((250, 250)), 75, rotation_speed=20, atmosphere_layers=3, atmosphere_thickness=10)
        self.s1 = np.array((-400, 400))
        self.m1 = 0.5
        self.p2 = PlanetTexture(np.array((500, 500)), 200, rotation_speed=20, atmosphere_layers=3, atmosphere_thickness=10)
        self.s2 = np.array((50, -50))
        self.m2 = 2

    def render_scene(self):
        self.screen.fill(config.colors.space)
        d2 = self.p2.screen_coordinates - self.p1.screen_coordinates
        
        force_on_p2 = self.m1 * self.p1.calc_gravity(d2, np.sqrt(np.sum(d2**2)))
        self.s2 = self.s2 - self.frametime_s * force_on_p2

        d1 = self.p1.screen_coordinates - self.p2.screen_coordinates
        force_on_p1 = self.m2 * self.p2.calc_gravity(d1, np.sqrt(np.sum(d1**2)))

        self.s1 = self.s1 - self.frametime_s * force_on_p1

        self.p1.update_position_and_draw(self.screen, self.frametime_s, self.s1)
        self.p2.update_position_and_draw(self.screen, self.frametime_s, self.s2)

        self.mid = (self.m1 * self.p1.screen_coordinates + self.m2 * self.p2.screen_coordinates) / (self.m1 + self.m2)
        self.p1.screen_coordinates = self.p1.screen_coordinates - self.mid + 0.5 * np.array(self.screen_size)
        self.p2.screen_coordinates = self.p2.screen_coordinates - self.mid + 0.5 * np.array(self.screen_size)

    def process_inputs(self):
        pass


if __name__ == "__main__":
    GravityDemo().gameloop()

