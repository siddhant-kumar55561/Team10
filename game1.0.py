import arcade # make sure to install arcade

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
WINDOW_NAME = "Legend of the Legendary Hero"

BG_TILE_SIZE = 294
TILE_NUMBER_X = 10
TILE_NUMBER_Y = 10

class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        # Background
        self.grass_list = arcade.SpriteList()
        TILE_X = TILE_NUMBER_X * BG_TILE_SIZE
        TILE_Y = TILE_NUMBER_Y * BG_TILE_SIZE
        for x in range(-TILE_X, TILE_X, BG_TILE_SIZE):
            for y in range(-TILE_Y, TILE_Y, BG_TILE_SIZE):
                grass = arcade.Sprite("C:/MyGames/pythonGame/assets/grass2.png", scale=1.0) # grass tile sprite goes here
                grass.center_x = x
                grass.center_y = y
                self.grass_list.append(grass)

        # Player
        self.player_list = arcade.SpriteList()
        self.player_sprite = arcade.Sprite("C:/MyGames/pythonGame/assets/characterSpritePh.png", scale=1.0) # player sprite goes here
        self.player_sprite.center_x = 960
        self.player_sprite.center_y = 540
        self.player_list.append(self.player_sprite)

    def on_draw(self):
        self.clear()
        self.grass_list.draw()
        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(PauseView())

        elif key == arcade.key.W:
            self.player_sprite.change_y = 5
        elif key == arcade.key.S:
            self.player_sprite.change_y = -5
        elif key == arcade.key.A:
            self.player_sprite.change_x = -5
        elif key == arcade.key.D:
            self.player_sprite.change_x = 5

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.W, arcade.key.S):
            self.player_sprite.change_y = 0
        elif key in (arcade.key.A, arcade.key.D):
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        self.player_list.update()


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
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_NAME, fullscreen=True)
    start_view = GameView()
    window.show_view(start_view)
    arcade.run()

main()
