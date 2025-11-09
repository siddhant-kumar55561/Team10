import arcade

def handle_update(game):
    dx = dy = 0
    speed = 5

    if game.active_keys["W"]:
        dy += speed
    if game.active_keys["S"]:
        dy -= speed
    if game.active_keys["A"]:
        dx -= speed
    if game.active_keys["D"]:
        dx += speed

    # Normalize diagonal speed
    if dx != 0 and dy != 0:
        dx /= 2**0.5
        dy /= 2**0.5

    game.player_sprite.center_x += dx
    game.player_sprite.center_y += dy