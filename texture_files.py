import arcade

player_textures = {
            "dead_left_down" : [
        arcade.make_soft_square_texture(64, (255, 0, 0, 255), 255)
        ],
            "dead_right_down" : [
        arcade.make_soft_square_texture(64, (255, 0, 0, 255), 255)
        ],
            "dead_left_up" : [
        arcade.make_soft_square_texture(64, (255, 0, 0, 255), 255)
        ],
            "dead_right_up" : [
        arcade.make_soft_square_texture(64, (255, 0, 0, 255), 255)
        ],
            "idle_left_down" : [
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\idle\LeftDown\priestILD1.png"),
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\idle\LeftDown\priestILD2.png"),
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\idle\LeftDown\priestILD3.png"),
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\idle\LeftDown\priestILD4.png"),
        ],
            "idle_right_down" : [
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\idle\RightDown\priestIRD1.png"),
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\idle\RightDown\priestIRD2.png"),
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\idle\RightDown\priestIRD3.png"),
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\idle\RightDown\priestIRD4.png"),
        ],
            "idle_left_up" : [
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\idle\LeftUp\priestILU1.png"),
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\idle\LeftUp\priestILU2.png"),
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\idle\LeftUp\priestILU3.png"),
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\idle\LeftUp\priestILU4.png"),
        ],
            "idle_right_up" : [
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\idle\RightUp\priestIRU1.png"),
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\idle\RightUp\priestIRU2.png"),
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\idle\RightUp\priestIRU3.png"),
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\idle\RightUp\priestIRU4.png"),
        ],
            "walk_left_down" : [
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\walk\LeftDown\priestWLD1.png"),
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\walk\LeftDown\priestWLD2.png"),
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\walk\LeftDown\priestWLD3.png"),
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\walk\LeftDown\priestWLD4.png"),
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\walk\LeftDown\priestWLD5.png"),
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\walk\LeftDown\priestWLD6.png"),
        ],
            "walk_left_up" : [
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\walk\LeftDown\priestWLD1.png"),
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\walk\LeftDown\priestWLD2.png"),
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\walk\LeftDown\priestWLD3.png"),
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\walk\LeftDown\priestWLD5.png"),
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\walk\LeftDown\priestWLD6.png"),
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\walk\LeftDown\priestWLD4.png"),
        ],
            "walk_right_down" : [
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\walk\RightDown\priestWRD1.png"),
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\walk\RightDown\priestWRD2.png"),
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\walk\RightDown\priestWRD3.png"),
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\walk\RightDown\priestWRD4.png"),
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\walk\RightDown\priestWRD5.png"),
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\walk\RightDown\priestWRD6.png"),
        ],
            "walk_right_up" : [
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\walk\RightDown\priestWRD1.png"),
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\walk\RightDown\priestWRD2.png"),
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\walk\RightDown\priestWRD3.png"),
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\walk\RightDown\priestWRD4.png"),
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\walk\RightDown\priestWRD5.png"),
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\priest\walk\RightDown\priestWRD6.png"),
        ]
        }

skeleton_textures = {
            "idle_right" :[
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\skeleton\right\skeleton2_v1_1.png"),
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\skeleton\right\skeleton2_v1_2.png"),
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\skeleton\right\skeleton2_v1_3.png"),
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\skeleton\right\skeleton2_v1_4.png")
    ],
            "idle_left" :[
        
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\skeleton\left\skeleton2_v1_1.png"),
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\skeleton\left\skeleton2_v1_2.png"),
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\skeleton\left\skeleton2_v1_3.png"),
        arcade.load_texture(r"C:\MyGames\pythonGame\assets\myAssetPack\skeleton\left\skeleton2_v1_4.png")
    ]
}