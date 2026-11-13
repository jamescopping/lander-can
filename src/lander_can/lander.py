from readline import redisplay
from string import whitespace

import pyray as rl
from pyray import (
    GOLD,
    RED,
    WHITE,
    Vector2,
    vector2_add,
    vector2_length,
    vector2_length_sqr,
    vector2_one,
    vector2_rotate,
    vector2_scale,
    vector2_subtract,
)
from raylib import KEY_A, KEY_D, KEY_SPACE, Vector2Length
from raylib.defines import DEG2RAD, PI

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
        self.angle = -90  # inital angle
        self.origin_vec = Vector2(0.5, 0.5)
        self.rotation_speed = 0  # scalar should be clamped to small +- value like +-5
        self.thrust_mag = 15

    def draw(self):
        # rl.draw_rectangle_pro(self.lander_rect, self.origin, self.rot, GOLD)
        pointA = self.pos
        pointB = vector2_add(pointA, self.vel)
        rl.draw_line_ex(
            pointA,
            pointB,
            vector2_length(vector2_subtract(pointB, pointA)) / 10.0,
            RED,
        )
        rl.draw_pixel_v(self.pos, WHITE)
        screen_space_vertices = [
            vector2_add(
                self.pos,
                vector2_scale(
                    vector2_rotate(
                        vector2_subtract(vertex, self.origin_vec), self.angle * DEG2RAD
                    ),
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
        self.rotation_speed = 0
        if rl.is_key_down(KEY_A):
            self.rotation_speed = 65.0
        elif rl.is_key_down(KEY_D):
            self.rotation_speed = -65.0
        if rl.is_key_down(KEY_A) and rl.is_key_down(KEY_D):
            self.rotation_speed = 0.0
        self.angle += self.rotation_speed * dt

        if rl.is_key_down(KEY_SPACE):
            thrust = self.thrust_vector(dt)
            print(f"{thrust.x} {thrust.y}")
            self.vel = vector2_add(self.vel, thrust)
        self.vel = vector2_add(self.vel, vector2_scale(Vector2(0, 1.625), dt))  # 9.8
        self.pos = vector2_add(self.pos, vector2_scale(self.vel, dt))

    def thrust_vector(self, dt):
        return vector2_scale(
            vector2_rotate(Vector2(0, -1), self.angle * DEG2RAD),
            self.thrust_mag * dt,
        )
