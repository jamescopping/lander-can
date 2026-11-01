import pyray as rl

from .screens import BaseScreen


class TitleScreen(BaseScreen):
    def __init__(self, font, fx_coin):
        super().__init__()
        self.font = font
        self.fx_coin = fx_coin

    def update(self):
        # Press enter or tap to change to GAMEPLAY screen
        if rl.is_key_pressed(rl.KeyboardKey.KEY_ENTER) or rl.is_gesture_detected(
            rl.Gesture.GESTURE_TAP
        ):
            rl.toggle_borderless_windowed()
            # finishScreen = 1   # OPTIONS
            self.finish_screen = 2  # GAMEPLAY
            rl.play_sound(self.fx_coin)

    def draw(self, width: int, height: int):
        rl.draw_rectangle(0, 0, width, height, rl.GREEN)
        pos = rl.Vector2(20, 10)
        rl.draw_text_ex(
            self.font, "TITLE SCREEN", pos, self.font.baseSize * 3.0, 4, rl.DARKGREEN
        )
        rl.draw_text(
            "PRESS ENTER or TAP to JUMP to GAMEPLAY SCREEN", 120, 220, 20, rl.DARKGREEN
        )
