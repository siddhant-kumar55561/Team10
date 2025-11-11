import arcade

# --- Load player walk textures ---
# (organize animation frames in lists for easy cycling)
player_walk_textures = {

    "walk_left_textures": [
        arcade.load_texture("C:/MyGames/pythonGame/assets/assetPack/Character_animation/priest_anim/walkLeft/priest2_v1_1L.png"),
        arcade.load_texture("C:/MyGames/pythonGame/assets/assetPack/Character_animation/priest_anim/walkLeft/priest2_v1_2L.png"),
        arcade.load_texture("C:/MyGames/pythonGame/assets/assetPack/Character_animation/priest_anim/walkLeft/priest2_v1_3L.png"),
        arcade.load_texture("C:/MyGames/pythonGame/assets/assetPack/Character_animation/priest_anim/walkLeft/priest2_v1_4L.png"),
    ],

    "walk_right_textures": [
        arcade.load_texture("C:/MyGames/pythonGame/assets/assetPack/Character_animation/priest_anim/walkRIght/priest2_v1_1R.png"),
        arcade.load_texture("C:/MyGames/pythonGame/assets/assetPack/Character_animation/priest_anim/walkRIght/priest2_v1_2R.png"),
        arcade.load_texture("C:/MyGames/pythonGame/assets/assetPack/Character_animation/priest_anim/walkRIght/priest2_v1_3R.png"),
        arcade.load_texture("C:/MyGames/pythonGame/assets/assetPack/Character_animation/priest_anim/walkRIght/priest2_v1_4R.png"),
]


}


# ---------------------

# background (grass)

background_textures = {
    "grass" : "C:/MyGames/pythonGame/assets/background/grass2.png",
    "demo_stage" : "C:/MyGames/pythonGame/assets/background/demoStage2.png"

}