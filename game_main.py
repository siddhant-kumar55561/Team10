import arcade # make sure to install arcade
import controls # type: ignore
import update # type: ignore

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
WINDOW_NAME = "Legend of the Legendary Hero"

BG_TILE_SIZE = 294
bg_scale_var = 0.5
TILE_NUMBER_X = 10
TILE_NUMBER_Y = 10

class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        # === Background ===
        self.grass_list = arcade.SpriteList()
        local_tile_size = BG_TILE_SIZE
        local_tile_size *= bg_scale_var
        local_tile_size = int(local_tile_size)
        TILE_X = TILE_NUMBER_X * BG_TILE_SIZE
        TILE_Y = TILE_NUMBER_Y * BG_TILE_SIZE

        for x in range(-TILE_X, TILE_X, local_tile_size):
            for y in range(-TILE_Y, TILE_Y, local_tile_size):
                grass = arcade.Sprite(
                    "C:/MyGames/pythonGame/assets/background/grass2.png", scale=bg_scale_var
                )
                grass.center_x = x
                grass.center_y = y
                self.grass_list.append(grass)

        # === Player ===
        self.player_list = arcade.SpriteList()
        # placeholder single sprite
        self.player_sprite = arcade.Sprite(
            "C:/MyGames/pythonGame/assets/playerWalk/playerWalkDown/playerWalkDown1.png", scale=1.0
        )

        self.current_direction = "right"
        self.current_frame = 0
        self.animation_speed = 0.15  # smaller = faster animation
        self.time_since_last_frame = 0

        # --- Load player walk textures ---
        # (organize animation frames in lists for easy cycling)
        self.walk_up_textures = [
            arcade.load_texture("C:/MyGames/pythonGame/assets/playerWalk/playerWalkUp/playerWalkUp1.png"),
            arcade.load_texture("C:/MyGames/pythonGame/assets/playerWalk/playerWalkUp/playerWalkUp2.png"),
            arcade.load_texture("C:/MyGames/pythonGame/assets/playerWalk/playerWalkUp/playerWalkUp3.png"),
            arcade.load_texture("C:/MyGames/pythonGame/assets/playerWalk/playerWalkUp/playerWalkUp4.png"),
        ]

        self.walk_down_textures = [
            arcade.load_texture("C:/MyGames/pythonGame/assets/playerWalk/playerWalkDown/playerWalkDown1.png"),
            arcade.load_texture("C:/MyGames/pythonGame/assets/playerWalk/playerWalkDown/playerWalkDown2.png"),
            arcade.load_texture("C:/MyGames/pythonGame/assets/playerWalk/playerWalkDown/playerWalkDown3.png"),
            arcade.load_texture("C:/MyGames/pythonGame/assets/playerWalk/playerWalkDown/playerWalkDown4.png"),
        ]

        self.walk_left_textures = [
            arcade.load_texture("C:/MyGames/pythonGame/assets/playerWalk/playerWalkLeft/playerWalkLeft1.png"),
            arcade.load_texture("C:/MyGames/pythonGame/assets/playerWalk/playerWalkLeft/playerWalkLeft2.png"),
            arcade.load_texture("C:/MyGames/pythonGame/assets/playerWalk/playerWalkLeft/playerWalkLeft3.png"),
            arcade.load_texture("C:/MyGames/pythonGame/assets/playerWalk/playerWalkLeft/playerWalkLeft4.png"),
        ]

        self.walk_right_textures = [
            arcade.load_texture("C:/MyGames/pythonGame/assets/playerWalk/playerWalkRight/playerWalkRight1.png"),
            arcade.load_texture("C:/MyGames/pythonGame/assets/playerWalk/playerWalkRight/playerWalkRight2.png"),
            arcade.load_texture("C:/MyGames/pythonGame/assets/playerWalk/playerWalkRight/playerWalkRight3.png"),
            arcade.load_texture("C:/MyGames/pythonGame/assets/playerWalk/playerWalkRight/playerWalkRight4.png"),
        ]

        # Start position
        self.player_sprite.center_x = 960
        self.player_sprite.center_y = 540
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
                "D": False,
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
