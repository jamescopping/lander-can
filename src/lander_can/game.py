import asyncio
import os
import platform
import sys

import pyray as rl

from .ending_screen import EndingScreen
from .gameplay_screen import GameplayScreen
from .logo_screen import LogoScreen
from .options_screen import OptionsScreen
from .screens import BaseScreen, GameScreen
from .title_screen import TitleScreen


class Game:
    def __init__(self, width: int = 800, height: int = 450, title: str = "Lander Can!"):
        self.screen_width = width
        self.screen_height = height
        self.title = title

        # Print Python version info
        python_impl = platform.python_implementation()
        python_version = sys.version.split()[0]
        print(f"Running on {python_impl} {python_version}")
        print(f"Full version: {sys.version}")

        # Screen management
        self.current_screen = GameScreen.GAMEPLAY

        self.music = None

        # Screen transition variables
        self.trans_alpha = 0.0
        self.on_transition = False
        self.trans_fade_out = False
        self.trans_from_screen = -1
        self.trans_to_screen = GameScreen.UNKNOWN

        # Screen instances
        self.screens = {}

        # Render texture for consistent rendering
        self.render_texture = None
        self.virtual_screen_width = width
        self.virtual_screen_height = height

    async def run(self):
        rl.init_window(self.screen_width, self.screen_height, self.title)
        rl.set_window_state(rl.ConfigFlags.FLAG_WINDOW_RESIZABLE)
        rl.init_audio_device()

        # Create render texture for consistent virtual screen rendering
        self.render_texture = rl.load_render_texture(
            self.virtual_screen_width, self.virtual_screen_height
        )

        # Set bilinear filtering for smooth scaling
        rl.set_texture_filter(
            self.render_texture.texture, rl.TextureFilter.TEXTURE_FILTER_POINT
        )

        # Load global data (assets that must be available in all screens)

        # Initialize screens
        self.screens[GameScreen.LOGO] = LogoScreen()
        self.screens[GameScreen.GAMEPLAY] = GameplayScreen(
            self.virtual_screen_width, self.virtual_screen_height - 100
        )
        self.screens[GameScreen.OPTIONS] = OptionsScreen()

        # Setup and init first screen
        self.current_screen = GameScreen.GAMEPLAY
        self.screens[self.current_screen].init()

        rl.set_target_fps(60)

        while not rl.window_should_close():
            self._update_draw_frame()
            await asyncio.sleep(0)

        # De-Initialization
        self._unload_current_screen()

        # Unload global data
        if self.music:
            rl.unload_music_stream(self.music)

        # Unload render texture
        if self.render_texture:
            rl.unload_render_texture(self.render_texture)

        rl.close_audio_device()
        rl.close_window()

    def _change_to_screen(self, screen):
        # Unload current screen
        self.screens[self.current_screen].unload()

        # Init next screen
        self.screens[screen].init()

        self.current_screen = screen

    def _transition_to_screen(self, screen):
        self.on_transition = True
        self.trans_fade_out = False
        self.trans_from_screen = self.current_screen
        self.trans_to_screen = screen
        self.trans_alpha = 0.0

    def _update_transition(self):
        if not self.trans_fade_out:
            self.trans_alpha += 0.05

            # NOTE: Due to float internal representation, condition jumps on 1.0f instead of 1.05f
            # For that reason we compare against 1.01f, to avoid last frame loading stop
            if self.trans_alpha > 1.01:
                self.trans_alpha = 1.0

                # Unload current screen
                self.screens[self.trans_from_screen].unload()

                # Load next screen
                self.screens[self.trans_to_screen].init()

                self.current_screen = self.trans_to_screen

                # Activate fade out effect to next loaded screen
                self.trans_fade_out = True
        else:  # Transition fade out logic
            self.trans_alpha -= 0.02

            if self.trans_alpha < -0.01:
                self.trans_alpha = 0.0
                self.trans_fade_out = False
                self.on_transition = False
                self.trans_from_screen = -1
                self.trans_to_screen = GameScreen.UNKNOWN

    def _draw_transition(self):
        rl.draw_rectangle(
            0,
            0,
            self.virtual_screen_width,
            self.virtual_screen_height,
            rl.fade(rl.BLACK, self.trans_alpha),
        )

    def _unload_current_screen(self):
        if self.current_screen in self.screens:
            self.screens[self.current_screen].unload()

    def _update_draw_frame(self):
        # Update
        if self.music:
            rl.update_music_stream(
                self.music
            )  # NOTE: Music keeps playing between screens

        if not self.on_transition:
            current_screen_obj: BaseScreen = self.screens[self.current_screen]
            current_screen_obj.update()

            if self.current_screen == GameScreen.LOGO:
                if current_screen_obj.should_finish():
                    self._transition_to_screen(GameScreen.TITLE)
            elif self.current_screen == GameScreen.TITLE:
                finish_result = current_screen_obj.should_finish()
                if finish_result == 1:
                    self._transition_to_screen(GameScreen.OPTIONS)
                elif finish_result == 2:
                    self._transition_to_screen(GameScreen.GAMEPLAY)
            elif self.current_screen == GameScreen.OPTIONS:
                if current_screen_obj.should_finish():
                    self._transition_to_screen(GameScreen.TITLE)
            elif self.current_screen == GameScreen.GAMEPLAY:
                finish_result = current_screen_obj.should_finish()
                if finish_result == 1:
                    self._transition_to_screen(GameScreen.ENDING)
            elif self.current_screen == GameScreen.ENDING:
                finish_result = current_screen_obj.should_finish()
                if finish_result == 1:
                    self._transition_to_screen(GameScreen.TITLE)
        else:
            self._update_transition()  # Update transition (fade-in, fade-out)

        # Draw to render texture (virtual screen)
        if self.render_texture:
            rl.begin_texture_mode(self.render_texture)
        rl.clear_background(rl.BLACK)

        # Draw current screen
        self.screens[self.current_screen].draw(
            self.virtual_screen_width, self.virtual_screen_height
        )

        # Draw full screen rectangle in front of everything
        if self.on_transition:
            self._draw_transition()

        # rl.draw_fps(10, 10)

        rl.end_texture_mode()

        # Draw render texture to actual screen (scaled to fit window)
        rl.begin_drawing()
        rl.clear_background(rl.BLACK)  # Letterbox areas will be black

        # Calculate scaling to fit the window while maintaining aspect ratio
        screen_width = rl.get_render_width()
        screen_height = rl.get_render_height()

        scale = min(
            screen_width / self.virtual_screen_width,
            screen_height / self.virtual_screen_height,
        )

        # Calculate position to center the scaled texture
        virtual_width = self.virtual_screen_width * scale
        virtual_height = self.virtual_screen_height * scale
        virtual_x = (screen_width - virtual_width) // 2
        virtual_y = (screen_height - virtual_height) // 2

        # Draw the render texture scaled and centered
        dest_rec = rl.Rectangle(virtual_x, virtual_y, virtual_width, virtual_height)
        if self.render_texture:
            source_rec = rl.Rectangle(
                0,
                0,
                self.render_texture.texture.width,
                -self.render_texture.texture.height,
            )
            rl.draw_texture_pro(
                self.render_texture.texture,
                source_rec,
                dest_rec,
                rl.Vector2(0, 0),
                0.0,
                rl.WHITE,
            )

        rl.end_drawing()
