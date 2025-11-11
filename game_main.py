import arcade # make sure to install arcade
import controls # type: ignore
import update # type: ignore
from texture_files import player_walk_textures # type: ignore
import environment # type: ignore
import map # type: ignore

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 360
WINDOW_NAME = "Dungeon Priest"


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        # === Background ===
        self.BG_TILE_SIZE = 294
        self.bg_scale_var = 1
        self.TILE_NUMBER_X = 10
        self.TILE_NUMBER_Y = 10

        # === Player ===
        self.player_list = arcade.SpriteList()

        # Stamina attributes ( update.py )
        self.stamina = True
        self.stamina_bar = 100

        # initialize player sprite
        self.player_sprite = arcade.Sprite( "C:/MyGames/pythonGame/assets/playerWalk/playerWalkDown/playerWalkDown1.png", scale=1.0 )
        self.player_list.append(self.player_sprite)
        
        # variables that help animation
        self.current_direction = "down"
        self.current_frame = 0
        self.animation_speed = 0.15  # smaller = faster animation
        self.time_since_last_frame = 0

        # Start position
        self.player_sprite.center_x = self.window.width / 2
        self.player_sprite.center_y = self.window.height / 2
        self.dx = 0
        self.dy = 0

        # Key Map
        self.key_map = {
                "W": arcade.key.W,
                "A": arcade.key.A,
                "S": arcade.key.S,
                "D": arcade.key.D,
                "SHIFT": arcade.key.LSHIFT,
                "ESC": arcade.key.ESCAPE
            }

        self.active_keys = {
                "W": False,
                "A": False,
                "S": False,
                "D": False,
                "SHIFT": False,
                "ESC": False
            }

        map.handle_load_map(self)

    def on_draw(self):
        self.clear((37, 19, 26))
        if self.scene:
            self.scene.draw()
        self.player_list.draw()
        self.camera.use()

    def on_key_press(self, key, modifiers):
        controls.handle_key_press(self, key)

    def on_key_release(self, key, modifiers):
        controls.handle_key_release(self, key)

    def center_camera_to_player(self):
        # Camera2D expects a 2D position tuple
        player_center = (self.player_sprite.center_x, self.player_sprite.center_y)
        self.camera.position = player_center

        # TODO : make it smooth follow



    def on_update(self, delta_time):
        if self.physics_engine:
            self.physics_engine.update()
        update.handle_update(self, delta_time)
        update.handle_animation(self, delta_time)

        self.center_camera_to_player()

    def setup(self):
        """Initialize game world and load map."""
        map.handle_load_map(self)
        self.camera = arcade.Camera2D()


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
        self.camera.use()


    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(GameView())


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_NAME, fullscreen=True, antialiasing=False, resizable=True)
    start_view = GameView()
    start_view.setup()
    window.show_view(start_view)
    arcade.run()

main()