import arcade

# --- Load player walk textures ---
# (organize animation frames in lists for easy cycling)
player_walk_textures = {
    "walk_up_textures" : [
        arcade.load_texture("C:/MyGames/pythonGame/assets/playerWalk/playerWalkUp/playerWalkUp1.png"),
        arcade.load_texture("C:/MyGames/pythonGame/assets/playerWalk/playerWalkUp/playerWalkUp2.png"),
        arcade.load_texture("C:/MyGames/pythonGame/assets/playerWalk/playerWalkUp/playerWalkUp3.png"),
        arcade.load_texture("C:/MyGames/pythonGame/assets/playerWalk/playerWalkUp/playerWalkUp4.png"),
    ],

    "walk_down_textures" : [
        arcade.load_texture("C:/MyGames/pythonGame/assets/playerWalk/playerWalkDown/playerWalkDown1.png"),
        arcade.load_texture("C:/MyGames/pythonGame/assets/playerWalk/playerWalkDown/playerWalkDown2.png"),
        arcade.load_texture("C:/MyGames/pythonGame/assets/playerWalk/playerWalkDown/playerWalkDown3.png"),
        arcade.load_texture("C:/MyGames/pythonGame/assets/playerWalk/playerWalkDown/playerWalkDown4.png"),
    ],

    "walk_left_textures" : [
        arcade.load_texture("C:/MyGames/pythonGame/assets/playerWalk/playerWalkLeft/playerWalkLeft1.png"),
        arcade.load_texture("C:/MyGames/pythonGame/assets/playerWalk/playerWalkLeft/playerWalkLeft2.png"),
        arcade.load_texture("C:/MyGames/pythonGame/assets/playerWalk/playerWalkLeft/playerWalkLeft3.png"),
        arcade.load_texture("C:/MyGames/pythonGame/assets/playerWalk/playerWalkLeft/playerWalkLeft4.png"),
    ],

    "walk_right_textures" : [
        arcade.load_texture("C:/MyGames/pythonGame/assets/playerWalk/playerWalkRight/playerWalkRight1.png"),
        arcade.load_texture("C:/MyGames/pythonGame/assets/playerWalk/playerWalkRight/playerWalkRight2.png"),
        arcade.load_texture("C:/MyGames/pythonGame/assets/playerWalk/playerWalkRight/playerWalkRight3.png"),
        arcade.load_texture("C:/MyGames/pythonGame/assets/playerWalk/playerWalkRight/playerWalkRight4.png"),
]

}


# ---------------------

# background (grass)

background_textures = {
    "grass" : "C:/MyGames/pythonGame/assets/background/grass2.png"
}