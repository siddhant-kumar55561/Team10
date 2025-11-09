import arcade

def handle_key_press(game, key):
    if key == arcade.key.W: game.active_keys["W"] = True
    elif key == arcade.key.S: game.active_keys["S"] = True
    elif key == arcade.key.A: game.active_keys["A"] = True
    elif key == arcade.key.D: game.active_keys["D"] = True

def handle_key_release(game, key):
    if key == arcade.key.W: game.active_keys["W"] = False
    elif key == arcade.key.S: game.active_keys["S"] = False
    elif key == arcade.key.A: game.active_keys["A"] = False
    elif key == arcade.key.D: game.active_keys["D"] = False