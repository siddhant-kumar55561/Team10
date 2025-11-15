import arcade

# ---------------- CONSTANTS ----------------

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 360
WINDOW_NAME = "Dungeon Priest"

# ----------------- CLASSES -----------------

class MapHandler:
    def __init__(self, player_sprite):
        self.player_sprite = player_sprite
        self.scene = None
        self.physics_engine = None
    
    def load(self, map_path):
        tile_map = arcade.load_tilemap(map_path, scaling=1.0)
        self.scene = arcade.Scene.from_tilemap(tile_map)
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
    def __init__(self, width, height):
        self.camera = arcade.Camera2D()
        self.width = width
        self.height = height
        self.target = None
        self.smooth_speed = 0.1

    def set_target(self, target):
        """Set which sprite the camera should follow."""
        self.target = target

    def update(self):
        """Update camera position each frame."""
        if not self.target:
            return
        
        target_x = self.target.center_x - self.width / 2
        target_y = self.target.center_y - self.height /2

        self.camera.move_to((target_x, target_y))

    def apply(self):
        """Activate this camera for drawing."""
        self.camera.use()

class Player(arcade.Sprite):

    time_since_last_frame = 0

    def __init__(self, x, y, scale):
        """Initialize player sprite"""
        super().__init__()

        self.speed_constant = 5
        self.center_x = x
        self.center_y = y
        self.scale = scale
        self.speed = self.speed_constant

        self.animations = {
            "idle_left" : [
        arcade.load_texture("C:/MyGames/pythonGame/assets/assetPack/Character_animation/priest_anim/walkLeft/priest2_v1_1L.png"),
        arcade.load_texture("C:/MyGames/pythonGame/assets/assetPack/Character_animation/priest_anim/walkLeft/priest2_v1_2L.png"),
        arcade.load_texture("C:/MyGames/pythonGame/assets/assetPack/Character_animation/priest_anim/walkLeft/priest2_v1_3L.png"),
        arcade.load_texture("C:/MyGames/pythonGame/assets/assetPack/Character_animation/priest_anim/walkLeft/priest2_v1_4L.png"),
        ],
            "idle_right" : [
        arcade.load_texture("C:/MyGames/pythonGame/assets/assetPack/Character_animation/priest_anim/walkRIght/priest2_v1_1R.png"),
        arcade.load_texture("C:/MyGames/pythonGame/assets/assetPack/Character_animation/priest_anim/walkRIght/priest2_v1_2R.png"),
        arcade.load_texture("C:/MyGames/pythonGame/assets/assetPack/Character_animation/priest_anim/walkRIght/priest2_v1_3R.png"),
        arcade.load_texture("C:/MyGames/pythonGame/assets/assetPack/Character_animation/priest_anim/walkRIght/priest2_v1_4R.png"),
        ]

        }
        
        self.player_list = arcade.SpriteList()

        self.direction = "left"
        self.current_texture = 0
        self.texture = self.animations["idle_right"][self.current_texture]

        # Movement
        self.change_x = 0
        self.change_y = 0
        self.stamina_system = StaminaSystem()

    def update_animation(self, delta_time = float(1 / 60)):
        """Update which animation is shown depending on the movement direction"""
        # Idle
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.animations[f"idle_{self.direction}"][self.current_texture]
        
        # Moving
        if self.change_x > 0:
            self.direction = "right"
        elif self.change_x < 0:
            self.direction = "left"

        # Cycle through animation
        self.animation_speed = 0.15
        Player.time_since_last_frame += delta_time

        if Player.time_since_last_frame >= self.animation_speed:
            self.current_texture = (self.current_texture + 1) % len(self.animations[f"idle_{self.direction}"])
            Player.time_since_last_frame = 0

        self.texture = self.animations[f"idle_{self.direction}"][self.current_texture]
    
    def update_movement(self, input_manager, delta_time):
        # Horizontal movement
        if input_manager.is_moving_left():
            self.change_x = -self.speed
            self.direction = "left"
        elif input_manager.is_moving_right():
            self.change_x = self.speed
            self.direction = "right"
        else:
            self.change_x = 0

        # Vertical movement
        if input_manager.is_moving_up():
            self.change_y = self.speed
        elif input_manager.is_moving_down():
            self.change_y = -self.speed
        else:
            self.change_y = 0

        # Normalize diagonal movement
        if self.change_x != 0 and self.change_y != 0:
            diagonal = (2 ** 0.5)
            self.change_x /= diagonal
            self.change_y /= diagonal

        # Sprint
        if input_manager.is_sprinting() and self.stamina_system.can_sprint:
            self.speed = 3 * self.speed_constant
            self.stamina_system.drain(delta_time)
        else:
            self.speed = self.speed_constant
            self.stamina_system.recover(delta_time)

    





# --------------- MAIN CODE ----------------
        

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.scene = None

        self.player = Player(self.window.width / 2, self.window.height / 2, 1)

        self.player_list = arcade.SpriteList()
        self.textures = self.player.animations[f"idle_{self.player.direction}"]
        self.player_list.append(self.player)

        self.input_manager = InputManager()
        self.stamina_system = StaminaSystem()

    def on_key_press(self, key, modifiers):
        self.input_manager.on_key_press(key)

    def on_key_release(self, key, modifiers):
        self.input_manager.on_key_release(key)

    def on_update(self, delta_time):
        self.player.update_animation(delta_time)
        self.player_list.update()
        self.player.update_movement(self.input_manager, delta_time)
        #print(self.player.center_x, self.player.center_y)
        si_x = int(self.player.center_x)//(self.tile_map.tile_width)
        si_y = int(self.player.center_y)//(self.tile_map.tile_height)
        standing_index = (si_x, si_y)
        print(standing_index)

    def on_draw(self):
        self.clear((37, 19, 26))
        if self.scene:
            self.scene.draw()
        self.player_list.draw()

    def setup(self):
        map_walls = "C:/team10pvt/Team10/assets/background/tilesets_success/map1_map.tmx"
        self.tile_map = arcade.load_tilemap(map_walls, scaling=1.0)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.scene.add_sprite_list("Player", sprite_list = self.player_list)
        
        # Gives draw order (temp)
        for spritelist in self.scene._sprite_lists:
            for name, stored_list in self.scene._name_mapping.items():
                if spritelist is stored_list:
                    print(name)

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_NAME, fullscreen=False, antialiasing=False, resizable=True)
    start_view = GameView()
    start_view.setup()
    window.show_view(start_view)
    arcade.run()

main()