"""
Base class for main game loop
"""
import logging
import pygame

from .config import config


class GameBase:
    """
    Base class defining the structure for a pygame game loop: There are some tasks for window setup
    in the constructor, and two abstract methods

    * :py:meth:`GameBase.process_inputs`:
        Runs before rendering the current frame and can hold
        everything that needs to happen whenever buttons are pressed
    * :py:meth:`GameBase.render_scene`:
        Supposed to run all the game logic that has to run for
        every frame generation, after processing the inputs

    Both of those methods need to be implemented in a class inheriting from :py:class:`GameBase`.
    The most important method is :py:meth:`GameBase.gameloop`, which runs the ``pygame`` gameloop,
    until the pygame window is closed. Whenever that happens or if a breaking error happens,
    everything gets properly tidied up.
    
    Example
    -------

    .. code-block:: python

        class MyGame(GameBase):
        
            def __init__(self, screen_size):
                super().__init__(screen_size, vsync=1, caption="my super duper game")
                # whatever you ened to set up
                self.player = pygame.Surface((50, 50))

            def process_inputs(self):
                # key bindings for your game
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    # do something...

            def render_scene(self):
                # calculate everything necessary for the next frame:
                # update positions, blit sprites, etc.

                # GameBase provides the latest frametime in self.frametime_s, which can be used as
                # a timestep
                self.position += self.frametime_s * self.speed
                
                # screen surface is in self.screen
                self.screen.blit(self.player, self.player.get_rect())

                
        if __name__ == "__main__":
            game = MyGame((800, 600))
            game.gameloop()
    
    :param screen_size: tuple of screen size in pixels (width, height)
    :param fps: target frames per second, only looked at if ``vsync`` is 0
    :param vsync: turn vertical synchronisation on or off (synchronizes frame rate with screen
        refresh rate)
    :param caption: name of the game window
    """
    def __init__(self, screen_size, fps=60, vsync=0, caption="Not Rocketscience"):
        config.init_logging()
        pygame.init()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.screen_size = screen_size

        pygame.display.set_icon(pygame.image.load(config.asset_path / "ship_icon.png"))

        if vsync:
            self.screen = pygame.display.set_mode(screen_size, pygame.SCALED, vsync=1)
            self.fps = 0
        else:
            self.screen = pygame.display.set_mode(screen_size, pygame.SCALED, vsync=1)
            self.fps = fps

        pygame.display.set_caption(caption)

        self.clock = pygame.time.Clock()
        self.running = False

        self.frametime_s = 0

    @property
    def screen_width(self):
        """convenience property returning screen width"""
        return self.screen_size[0]

    @property
    def screen_height(self):
        """convenience property returning screen height"""
        return self.screen_size[1]

    def render_scene(self):
        """
        calculate everything necessary for the next frame: update positions, blit sprites, etc.
        """
        raise NotImplementedError("needs to be implemented in subclass")

    def process_inputs(self):
        """
        key bindings for your game, what should happen when which key is pressed.
        """
        raise NotImplementedError("needs to be implemented in subclass")

    def gameloop(self):
        """
        Method running a while loop until an error happens or the pygame window is closed. In every iteration, the screen is cleared, inputs are processed, the new frame is generated and then displayed.
        """
        self.logger.info("Commencing game loop")
        self.running = True
        try:
            while self.running:
                self.screen.fill((0, 0, 0))
                self.process_inputs()
                self.render_scene()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False

                pygame.display.flip()
                self.frametime_s = self.clock.tick(self.fps) / 1000
        finally:
            self.logger.info("Exiting. Last frametime was %s s", self.frametime_s)
            pygame.quit()





    
        