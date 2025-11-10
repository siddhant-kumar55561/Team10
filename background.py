import arcade
import texture_files # type: ignore

def handle_background(game):
    game.grass_list = arcade.SpriteList()
    local_tile_size = game.BG_TILE_SIZE
    local_tile_size *= game.bg_scale_var
    local_tile_size = int(local_tile_size)
    TILE_X = game.TILE_NUMBER_X * game.BG_TILE_SIZE
    TILE_Y = game.TILE_NUMBER_Y * game.BG_TILE_SIZE

    for x in range(-TILE_X, TILE_X, local_tile_size):
        for y in range(-TILE_Y, TILE_Y, local_tile_size):
            grass = arcade.Sprite(
                texture_files.background_textures["grass"], scale=game.bg_scale_var
            )
            grass.center_x = x
            grass.center_y = y
            game.grass_list.append(grass)
