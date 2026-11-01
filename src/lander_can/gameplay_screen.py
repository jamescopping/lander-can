import random

import pyray as rl

from .screens import BaseScreen
from .terrain import Terrain


class GameplayScreen(BaseScreen):
    def __init__(self, width, height):
        super().__init__()
        self.terrain = Terrain(width, height)
        self.terrain.generate()

    def update(self):
        pass

    def draw(self, width: int, height: int):

        # draw lander can

        # draw terrian
        self.terrain.draw()
