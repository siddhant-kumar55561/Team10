import arcade
import os

# ---------------- CONSTANTS ----------------

SCREEN_WIDTH = 12 * 64
SCREEN_HEIGHT = 7 * 64
WINDOW_NAME = "Dungeon Priest"
RESOLUTION = 1536, 896

# ----------------- CLASSES -----------------

class MapHandler:
    def __init__(self, player_sprite):
        self.player_sprite = player_sprite
        self.scene = None
        self.physics_engine = None
    
    def load(self, map_path):
        self.tile_map = arcade.load_tilemap(
                map_path,
                scaling=1.0,
                layer_options={
                    "Walls": {"use_spatial_hash": True}
                }
            )

        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.scene["Walls"])

    def draw(self):
        if self.scene:
            self.scene.draw()
    
    def update(self):
        if self.physics_engine:
            self.physics_engine.update()

class InputManager:
    def __init__(self):
        self.keys_pressed = set()
    
    def on_key_press(self, key):
        self.keys_pressed.add(key)

    def on_key_release(self, key):
        self.keys_pressed.discard(key)
    
    def is_moving_left(self):
        return arcade.key.A in self.keys_pressed
    
    def is_moving_right(self):
        return arcade.key.D in self.keys_pressed
    
    def is_moving_up(self):
        return arcade.key.W in self.keys_pressed
    
    def is_moving_down(self):
        return arcade.key.S in self.keys_pressed
    
    def is_sprinting(self):
        return arcade.key.LSHIFT in self.keys_pressed
       
class StaminaSystem:
    def __init__(self, max_stamina = 100, drain_rate = 20, recovery_rate = 7):
        self.max_stamina = max_stamina
        self.current = max_stamina # current = current stamina value
        self.drain_rate = drain_rate
        self.recovery_rate = recovery_rate
        self.can_sprint = True
    
    def drain(self, delta_time):
        """drain stamina while sprinting"""
        if self.current > 0:
            self.current -= self.drain_rate * delta_time
        if self.current <= 0:
            self.current = 0
            self.can_sprint = False

    def recover(self, delta_time):
        """recover stamina while not sprinting"""
        if self.current < self.max_stamina:
            self.current += self.recovery_rate * delta_time
        if self.current >= 20:
            self.can_sprint = True
        if self.current > self.max_stamina:
            self.current = self.max_stamina

class CameraManager:
    def __init__(self):
        self.camera = arcade.Camera2D()
        self.target = None
        self.smooth_speed = 0.1

    def set_target(self, target):
        """Set which sprite the camera should follow."""
        self.target = target

    def update(self):
        """Update camera position each frame."""
        if not self.target:
            return
        
        target_x = self.target.center_x
        target_y = self.target.center_y

        self.camera.position = (target_x, target_y)

    def apply(self):
        """Activate this camera for drawing."""
        self.camera.use()

class Player(arcade.Sprite):

    def __init__(self, position, scale = 1):
        """Initialize player sprite"""
        super().__init__()
        self.time_since_last_frame = 0
        self.speed_constant = 5
        self.center_x, self.center_y = position
        self.scale = scale
        self.speed = self.speed_constant

        self.is_alive = True # TODO
        self.health = 100 # TODO

        self.animation_folders = []
        self.animations = {
            "idle_left_down" : [
        arcade.load_texture("C:/MyGames/pythonGame/assets/assetPack/Character_animation/priest_anim/walkLeftDown/priest2_v1_1LD.png"),
        arcade.load_texture("C:/MyGames/pythonGame/assets/assetPack/Character_animation/priest_anim/walkLeftDown/priest2_v1_2LD.png"),
        arcade.load_texture("C:/MyGames/pythonGame/assets/assetPack/Character_animation/priest_anim/walkLeftDown/priest2_v1_3LD.png"),
        arcade.load_texture("C:/MyGames/pythonGame/assets/assetPack/Character_animation/priest_anim/walkLeftDown/priest2_v1_4LD.png"),
        ],
            "idle_right_down" : [
        arcade.load_texture("C:/MyGames/pythonGame/assets/assetPack/Character_animation/priest_anim/walkRightDown/priest2_v1_1RD.png"),
        arcade.load_texture("C:/MyGames/pythonGame/assets/assetPack/Character_animation/priest_anim/walkRightDown/priest2_v1_2RD.png"),
        arcade.load_texture("C:/MyGames/pythonGame/assets/assetPack/Character_animation/priest_anim/walkRightDown/priest2_v1_3RD.png"),
        arcade.load_texture("C:/MyGames/pythonGame/assets/assetPack/Character_animation/priest_anim/walkRightDown/priest2_v1_4RD.png"),
        ],
            "idle_left_up" : [
        arcade.load_texture("C:/MyGames/pythonGame/assets/assetPack/Character_animation/priest_anim/walkLeftUp/priest2_v1_1LU.png"),
        arcade.load_texture("C:/MyGames/pythonGame/assets/assetPack/Character_animation/priest_anim/walkLeftUp/priest2_v1_2LU.png"),
        arcade.load_texture("C:/MyGames/pythonGame/assets/assetPack/Character_animation/priest_anim/walkLeftUp/priest2_v1_3LU.png"),
        arcade.load_texture("C:/MyGames/pythonGame/assets/assetPack/Character_animation/priest_anim/walkLeftUp/priest2_v1_4LU.png"),
        ],
            "idle_right_up" : [
        arcade.load_texture("C:/MyGames/pythonGame/assets/assetPack/Character_animation/priest_anim/walkRightUp/priest2_v1_1RU.png"),
        arcade.load_texture("C:/MyGames/pythonGame/assets/assetPack/Character_animation/priest_anim/walkRightUp/priest2_v1_2RU.png"),
        arcade.load_texture("C:/MyGames/pythonGame/assets/assetPack/Character_animation/priest_anim/walkRightUp/priest2_v1_3RU.png"),
        arcade.load_texture("C:/MyGames/pythonGame/assets/assetPack/Character_animation/priest_anim/walkRightUp/priest2_v1_4RU.png"),
        ]

        }
        
        self.player_list = arcade.SpriteList()

        self.direction_x = "right"
        self.direction_y = "down"
        self.current_texture = 0
        self.texture = self.animations["idle_right_down"][self.current_texture]

        # Movement
        self.change_x = 0
        self.change_y = 0
        self.stamina_system = StaminaSystem()

    def update_animation(self, delta_time = float(1 / 60)):
        """Update which animation is shown depending on the movement direction"""
        # Idle
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.animations[f"idle_{self.direction_x}_{self.direction_y}"][self.current_texture]
        
        # Moving
        if self.change_x > 0:
            self.direction_x = "right"
        elif self.change_x < 0:
            self.direction_x = "left"

        if self.change_y > 0:
            self.direction_y = "up"
        elif self.change_y < 0:
            self.direction_y = "down"

        # Cycle through animation
        self.animation_speed = 0.15
        self.time_since_last_frame += delta_time

        if self.time_since_last_frame >= self.animation_speed:
            self.current_texture = (self.current_texture + 1) % len(self.animations[f"idle_{self.direction_x}_{self.direction_y}"])
            self.time_since_last_frame = 0

        self.texture = self.animations[f"idle_{self.direction_x}_{self.direction_y}"][self.current_texture]
    
    def update_movement(self, input_manager, delta_time):
        # Horizontal movement
        if input_manager.is_moving_left():
            self.change_x = -self.speed
            self.direction_x = "left"
        elif input_manager.is_moving_right():
            self.change_x = self.speed
            self.direction_x = "right"
        else:
            self.change_x = 0

        # Vertical movement
        if input_manager.is_moving_up():
            self.change_y = self.speed
            self.direction_y = "up"
        elif input_manager.is_moving_down():
            self.change_y = -self.speed
            self.direction_y = "down"
        else:
            self.change_y = 0

        if self.direction_y == "up":
            if input_manager.is_moving_left() or input_manager.is_moving_right():
                self.direction_y = "down"

        # Normalize diagonal movement
        if self.change_x != 0 and self.change_y != 0:
            diagonal = (2 ** 0.5)
            self.change_x /= diagonal
            self.change_y /= diagonal

        # Sprint
        if self.stamina_system.can_sprint:
            if input_manager.is_sprinting():
                self.speed = 3 * self.speed_constant
                self.stamina_system.drain(delta_time)
            else:
                self.speed = self.speed_constant
                self.stamina_system.recover(delta_time)
        else:
            self.speed = 0.5 * self.speed_constant
            self.stamina_system.recover(delta_time)
        


    """def get_hurt(self, input_manager):
        if input_manager.is_hurt():
            self.health -= 5
        if self.health <= 0 :
            self.health = 0
            self.is_alive = False"""

class HUDManager:

    def __init__(self):
        # Health
        self.hp_bg_x = 0
        self.hp_bg_y = 0
        self.hp_x = 0
        self.hp_y = 0
        # Stamina
        self.stmn_bg_x = 0
        self.stmn_bg_y = 0
        self.stmn_x = 0
        self.stmn_y = 0

    def draw_hp_bar(self, target):
        self.hp_bar_const = 296
        self.hp_width = (target.health/100) * self.hp_bar_const
        self.hp_bar_bg = arcade.draw_lbwh_rectangle_filled(self.hp_bg_x, self.hp_bg_y, self.hp_bar_const + 4, 20, (55, 55, 55))
        self.hp_bar =  arcade.draw_lbwh_rectangle_filled(self.hp_x, self.hp_y, self.hp_width , 16, (207, 104, 109))
    
    def draw_stmn_bar(self, target):
        self.stmn_color = arcade.color.BLUE
        self.stmn_bg_color = arcade.color.BLUE_GRAY
        if target.stamina_system.can_sprint:    
            self.stmn_color = arcade.color.BLUE
            self.stmn_bg_color = arcade.color.BLUE_GRAY
        else:
            self.stmn_color = arcade.color.RED_BROWN
            self.stmn_bg_color = arcade.color.RED

        self.stmn_bar_const = 146
        self.stmn_width = (target.stamina_system.current/100) * self.stmn_bar_const
        self.stmn_bar_bg = arcade.draw_lbwh_rectangle_filled(self.stmn_bg_x, self.stmn_bg_y, self.stmn_bar_const + 4, 20, self.stmn_bg_color)
        self.stmn_bar =  arcade.draw_lbwh_rectangle_filled(self.stmn_x, self.stmn_y, self.stmn_width , 16, self.stmn_color)
    
    def update(self, target):
        # Health
        self.hp_bg_x, self.hp_bg_y = target.center_x - lenConvert(11), target.center_y - lenConvert(5.5)
        self.hp_x = self.hp_bg_x + 2
        self.hp_y = self.hp_bg_y + 2
        # Stamina
        self.stmn_bg_x, self.stmn_bg_y = target.center_x - lenConvert(11), target.center_y - lenConvert(6)
        self.stmn_x = self.stmn_bg_x + 2
        self.stmn_y = self.stmn_bg_y + 2

    def draw(self, target):
        self.draw_hp_bar(target)
        self.draw_stmn_bar(target)

        


def tileConvert(tile_ix, tile_iy, tile_size = 64):
    return (tile_ix * tile_size, tile_iy * tile_size)
    
def lenConvert(len, tile_size = 64):
    return len * tile_size


    return textures



# --------------- MAIN CODE ----------------
        

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.screen_width = 1596
        self.screen_height = 896
        self.old_print = None
        
    def on_key_press(self, key, modifiers):
        self.input_manager.on_key_press(key)

    def on_key_release(self, key, modifiers):
        self.input_manager.on_key_release(key)

    def on_update(self, delta_time):
        self.player.update_movement(self.input_manager, delta_time)
        self.player.update_animation(delta_time)
        self.map_handler.update()
        self.camera.update()
        self.hud_manager.update(self.player)

        # Print Tile Index (Temp)
        # --------------
        si_x = int(self.player.center_x)//(64)
        si_y = int(self.player.center_y)//(64)
        self.standing_index = (si_x, si_y)
        if self.old_print != self.standing_index:
            print(self.standing_index)
            self.old_print = self.standing_index
        # --------------

    def on_draw(self):
        self.clear((37, 19, 26))
        self.map_handler.draw()
        self.camera.apply()
        self.hud_manager.draw(self.player)


    def setup(self):
        # Player
        self.map_current = r"C:\MyGames\pythonGame\assets\background\tilesets\map1\map1_map - Copy2.tmx"
        self.player = Player((tileConvert(36, 12)))
        self.player_list = arcade.SpriteList()
        self.textures = self.player.animations[f"idle_{self.player.direction_x}_{self.player.direction_y}"]
        # Map/Scene init
        self.map_handler = MapHandler(self.player)
        self.map_handler.load(self.map_current)
        self.scene = self.map_handler.scene
        # Player append late
        self.player_list.append(self.player) 
        self.scene.add_sprite_list_after("Player", "Walls", sprite_list = self.player_list)
        # Camera
        self.camera = CameraManager()
        self.camera.set_target(self.player)
        # UI / other systems
        self.input_manager = InputManager()
        self.stamina_system = StaminaSystem()
        self.hud_manager = HUDManager()
        

        # Gives draw order (temp)
        for spritelist in self.scene._sprite_lists:
            for name, stored_list in self.scene._name_mapping.items():
                if spritelist is stored_list:
                    print(name)

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_NAME, fullscreen=True, antialiasing=False, resizable=True)
    start_view = GameView()
    start_view.setup()
    window.show_view(start_view)
    arcade.run()

main()