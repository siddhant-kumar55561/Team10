import arcade # make sure to install arcade
import controls # type: ignore
import update # type: ignore
from texture_files import player_walk_textures # type: ignore
import background # type: ignore

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
WINDOW_NAME = "Legend of the Legendary Hero"


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        # === Background ===
        self.BG_TILE_SIZE = 294
        self.bg_scale_var = 0.5
        self.TILE_NUMBER_X = 10
        self.TILE_NUMBER_Y = 10

        background.handle_background(self)


        # === Player ===
        self.player_list = arcade.SpriteList()

        # placeholder single sprite, SHOULD NOT MATTER IF ANIMATION WORKS AS IT SHOULD
        self.player_sprite = arcade.Sprite(
            "C:/MyGames/pythonGame/assets/playerWalk/playerWalkDown/playerWalkDown1.png", scale=1.0
        )
        

        self.current_direction = "down"
        self.current_frame = 0
        self.animation_speed = 0.15  # smaller = faster animation
        self.time_since_last_frame = 0

        
        # Start position
        self.player_sprite.center_x = 960
        self.dx = 0
        self.player_sprite.center_y = 540
        self.dy = 0
        self.player_list.append(self.player_sprite)

        self.key_map = {
                "W": arcade.key.W,
                "A": arcade.key.A,
                "S": arcade.key.S,
                "D": arcade.key.D,
                "ESC": arcade.key.ESCAPE
            }

        self.active_keys = {
                "W": False,
                "A": False,
                "S": False,
                "D": False
            }
        
        self.misc_active_keys = {
                "ESC": False
        }


        # Optional: state tracking for animation
        self.current_direction = "down"
        self.current_frame = 0


    def on_draw(self):
        self.clear()
        self.grass_list.draw()
        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        controls.handle_key_press(self, key)

    def on_key_release(self, key, modifiers):
        controls.handle_key_release(self, key)

    def on_update(self, delta_time):
        update.handle_update(self)
        update.handle_animation(self, delta_time)


class PauseView(arcade.View):
    def __init__(self):
        super().__init__()
        self.paused_text = arcade.Text(
            "Paused", self.window.width / 2, self.window.height / 2,
            arcade.color.BLACK, 50, anchor_x="center", anchor_y="center"
        )

    def on_draw(self):
        self.clear(arcade.color.RED)
        self.paused_text.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(GameView())


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_NAME, fullscreen=True, antialiasing=False)
    start_view = GameView()
    window.show_view(start_view)
    arcade.run()

main()
