import pyray as rl

from .screens import BaseScreen


class EndingScreen(BaseScreen):
    def __init__(self, font, fx_coin):
        super().__init__()
        self.font = font
        self.fx_coin = fx_coin

    def update(self):
        # Press enter or tap to return to TITLE screen
        if rl.is_key_pressed(rl.KeyboardKey.KEY_ENTER) or rl.is_gesture_detected(
            rl.Gesture.GESTURE_TAP
        ):
            rl.toggle_borderless_windowed()
            self.finish_screen = 1
            rl.play_sound(self.fx_coin)

    def draw(self, width: int, height: int):
        rl.draw_rectangle(0, 0, width, height, rl.BLUE)

        pos = rl.Vector2(20, 10)
        rl.draw_text_ex(
            self.font, "ENDING SCREEN", pos, self.font.baseSize * 3.0, 4, rl.DARKBLUE
        )
        rl.draw_text(
            "PRESS ENTER or TAP to RETURN to TITLE SCREEN", 120, 220, 20, rl.DARKBLUE
        )
