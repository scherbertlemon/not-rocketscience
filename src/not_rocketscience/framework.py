import pygame
import numpy as np
import logging
from .config import config


class GameBase:
    
    def __init__(self, screen_size, fps=60, vsync=0):
        config.init_logging()
        pygame.init()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.screen_size = screen_size
        if vsync:
            self.screen = pygame.display.set_mode(screen_size, pygame.SCALED, vsync=1)
            self.fps = 0
        else:
            self.screen = pygame.display.set_mode(screen_size, pygame.SCALED, vsync=1)
            self.fps = fps
        self.clock = pygame.time.Clock()
        self.running = False
        
        self.frametime_s = 0

    @property
    def screen_width(self):
        return self.screen_size[0]

    @property
    def screen_height(self):
        return self.screen_size[1]

    def render_scene(self):
        raise NotImplementedError("needs to be implemented in subclass")

    def process_inputs(self):
        raise NotImplementedError("needs to be implemented in subclass")
    
    def gameloop(self):
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
            self.logger.info(f"Exiting. Last frametime was {self.frametime_s}s")
            pygame.quit()

        




    
        