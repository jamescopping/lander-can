import pyray as rl
from pyray import (
    GOLD,
    Vector2,
    vector2_add,
    vector2_rotate,
    vector2_scale,
    vector2_subtract,
)
from raylib.defines import PI

vertices: list[Vector2] = [
    Vector2(0, 0),
    Vector2(1, 0),
    Vector2(1, 0.8),
    Vector2(0, 0.8),
    Vector2(-0.45, 1.25),
    Vector2(0, 0.3),
    Vector2(1.45, 1.25),
    Vector2(1, 0.3),
    Vector2(0.33, 0.8),
    Vector2(0.33, 0.99),
    Vector2(0.66, 0.99),
    Vector2(0.66, 0.8),
]
# idx list of tuples whick join together to make a like
edges: list[list[int]] = [
    [0, 1],
    [1, 2],
    [2, 3],
    [3, 0],
    [4, 5],
    [6, 7],
    [8, 9],
    [9, 10],
    [10, 11],
]


class Lander:
    def __init__(self, start_pos: Vector2, scale: float = 15.0) -> None:
        self.scale = scale
        self.pos = Vector2(start_pos.x, start_pos.y)
        self.vel = Vector2(15.0, 0.0)
        self.rot = 90 * (PI / 180.0)
        self.origin_vec = Vector2(0.5, 0.5)

    def draw(self):
        # rl.draw_rectangle_pro(self.lander_rect, self.origin, self.rot, GOLD)
        screen_space_vertices = [
            vector2_add(
                self.pos,
                vector2_scale(
                    vector2_rotate(vector2_subtract(vertex, self.origin_vec), self.rot),
                    self.scale,
                ),
            )
            for vertex in vertices
        ]
        for edge in edges:
            rl.draw_line_v(
                screen_space_vertices[edge[0]], screen_space_vertices[edge[1]], GOLD
            )

    def update(self, dt: float):
        self.rot += -4 * (PI / 180.0) * dt
        self.vel = vector2_add(self.vel, vector2_scale(Vector2(0, 1.625), dt))
        self.pos = vector2_add(self.pos, vector2_scale(self.vel, dt))
