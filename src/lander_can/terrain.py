# Terrain generates a list of points [(x, y)] that go from x = 0 to x = width

from datetime import datetime

import pyray as rl
from pyray import WHITE, Vector2


class Terrain:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.points: list[Vector2] = []
        rl.set_random_seed((int)(datetime.now().timestamp()))

    def generate(self):
        self.points.clear()
        scale_factor = 50
        delta_x = 30
        current_height = rl.get_random_value(self.height, self.height + 100)

        for x in range(0, self.width + delta_x, delta_x):
            self.points.append(Vector2(x, (int)(current_height)))
            delta_y = (rl.get_random_value(0, 1000) / 1000.0 * 2) - 1
            delta_y *= scale_factor
            current_height += delta_y

    def draw(self):
        for p in range(len(self.points)):
            # rl.draw_pixel((int)(self.points[p].x), (int)(self.points[p].y), WHITE)
            if p == 0:
                continue
            rl.draw_line_v(self.points[p - 1], self.points[p], WHITE)
