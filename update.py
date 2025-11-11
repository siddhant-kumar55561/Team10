import arcade
from controls import stopped # type: ignore
import texture_files # type: ignore


stamina_bar = 100

def handle_update(game, delta_time):
    dx = game.dx
    dy = game.dy

    dx = dy = 0
    speed = 5

    # Sprint/Stamina Movement
    stamina_constant = 20
    recovery_constant = 7


    if game.stamina_bar <= 0:
        game.stamina = False
        game.stamina_bar = 0

    if game.stamina_bar < 100 and not game.active_keys["SHIFT"]:
        game.stamina_bar += delta_time * recovery_constant
        game.stamina = True

    if game.active_keys["SHIFT"] and game.stamina:
        speed = 20
        game.stamina_bar -= delta_time * stamina_constant


    # Regular Movement
    if game.active_keys["W"]:
        dy += speed
        game.current_direction = "up"
    if game.active_keys["S"]:
        dy -= speed
        game.current_direction = "down"
    if game.active_keys["A"]:
        dx -= speed
        game.current_direction = "left"
    if game.active_keys["D"]:
        dx += speed
        game.current_direction = "right"


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
            game.textures = texture_files.player_walk_textures["walk_right_textures"]
        elif game.current_direction == "left":
            game.textures = texture_files.player_walk_textures["walk_left_textures"]
        elif game.current_direction == "right":
            game.textures = texture_files.player_walk_textures["walk_right_textures"]
        elif game.current_direction == "up":
            game.textures = texture_files.player_walk_textures["walk_right_textures"]

        # Loop back to start if past last frame
        if game.current_frame >= len(game.textures):
            game.current_frame = 0

        game.player_sprite.texture = game.textures[game.current_frame]