import arcade
from controls import stopped # type: ignore
import texture_files # type: ignore

def handle_update(game):
    dx = game.dx
    dy = game.dy

    dx = dy = 0
    speed = 4

    if game.active_keys["W"]:
        dy += speed
        game.current_direction = "up"
        game.textures = texture_files.player_walk_textures["walk_up_textures"]
    if game.active_keys["S"]:
        dy -= speed
        game.current_direction = "down"
        game.textures = texture_files.player_walk_textures["walk_down_textures"]
    if game.active_keys["A"]:
        dx -= speed
        game.current_direction = "left"
        game.textures = texture_files.player_walk_textures["walk_left_textures"]
    if game.active_keys["D"]:
        dx += speed
        game.current_direction = "right"
        game.textures = texture_files.player_walk_textures["walk_right_textures"]


    # Normalize diagonal speed
    if dx != 0 and dy != 0:
        dx /= 2**0.5
        dy /= 2**0.5

    game.player_sprite.center_x += dx
    game.player_sprite.center_y += dy


def handle_animation(game, delta_time):
    # every delta_time second, timer should update
    game.time_since_last_frame += delta_time

    if game.time_since_last_frame > game.animation_speed:
        # Advance frame
        game.current_frame += 1
        game.time_since_last_frame = 0

        # Get current animation list
        if game.current_direction == "down":
            game.textures = texture_files.player_walk_textures["walk_down_textures"]
        elif game.current_direction == "left":
            game.textures = texture_files.player_walk_textures["walk_left_textures"]
        elif game.current_direction == "right":
            game.textures = texture_files.player_walk_textures["walk_right_textures"]
        elif game.current_direction == "up":
            game.textures = texture_files.player_walk_textures["walk_up_textures"]

        # Loop back to start if past last frame
        if game.current_frame >= len(game.textures):
            game.current_frame = 0

        game.player_sprite.texture = game.textures[game.current_frame]
        if stopped(game):
            game.player_sprite.texture = game.textures[0]