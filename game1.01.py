import arcade
import pyglet

# CONSTANTS
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 360
WINDOW_NAME = "Legend of the Legendary Hero"

BG_TILE_SIZE = 294
TILE_NUMBER_X = 10
TILE_NUMBER_Y = 10


def main():
    window = arcade.Window(
                            SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_NAME, 
                            resizable = False, 
                            fullscreen = True, 
                            center_window = False,
                            update_rate = 1/60, 
                            vsync = True
                            )

    start_view = GameView()
    window.show_view(start_view)
    arcade.run()


class GameView(arcade.View):
    # Main Game state

    # Recieve the opened window from main()
    def __init__(self):
        super().__init__()


        # Background
        self.grass_list = arcade.SpriteList()
        
        # Calculate how many tiles fit
        TILE_X = TILE_NUMBER_X * BG_TILE_SIZE
        TILE_Y = TILE_NUMBER_Y * BG_TILE_SIZE

        for x in range(-TILE_X, TILE_X, BG_TILE_SIZE):
            for y in range(-TILE_Y, TILE_Y, BG_TILE_SIZE):
                
                # Create a sprite from asset file
                grass = arcade.Sprite("C:/MyGames/pythonGame/assets/grass2.png", scale = 1.0)
                
                # Center the tile at the calculated position
                grass.center_x = x
                grass.center_y = y
                
                # Add the tile to the SpriteList along with coordinates
                self.grass_list.append(grass) 

        # Player
        player_sprite = self.player_list = arcade.SpriteList()
        self.player_sprite_attribute = arcade.Sprite("C:/MyGames/pythonGame/assets/characterSpritePh.png", scale = 1.0)
        player_sprite.center_x = 0

        self.player_list.append(player_sprite)
        
        # Have a list of sprites. change according to direction.
        # so i need to draw some var "spriteP" each frame, and change the value of "spriteP" depending on direction
            


    def on_draw(self):
        self.clear((98, 191, 41))
        self.grass_list.draw()
        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            pause_view = PauseView()
            self.window.show_view(pause_view)
    
    

    
class PauseView(arcade.View):
    # Pause screen state

    def __init__(self):
        super().__init__()

        self.paused_text = arcade.Text("Paused",
                                        self.window.width / 2, 
                                        self.window.height / 2,
                                        arcade.color.BLACK,
                                        font_size = 50,
                                        anchor_x = "center",
                                        anchor_y = "center"
                                        )

    
    def on_draw(self):
        self.clear(arcade.color.ALABAMA_CRIMSON)
        self.paused_text.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            game_view = GameView()
            self.window.show_view(game_view)

main()