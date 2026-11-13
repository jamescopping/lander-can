
import pyray as rl
from pyray import Vector2
from raylib import KEY_R

from lander_can.lander import Lander

from .screens import BaseScreen
from .terrain import Terrain


class GameplayScreen(BaseScreen):
    def __init__(self, width: int, height: int):
        super().__init__()
        self.terrain = Terrain(width, height)
        self.terrain.generate()
        self.lander = Lander(Vector2(10.0, 10.0))

    def update(self):
        dt = rl.get_frame_time()
        self.lander.update(dt)

        if rl.is_key_pressed(KEY_R):
            self.lander = Lander(Vector2(10.0, 10.0))

    def draw(self, width: int, height: int):

        # draw lander can
        self.lander.draw()
        # draw terrian
        self.terrain.draw()
