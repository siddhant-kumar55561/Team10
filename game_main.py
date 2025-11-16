import arcade
import texture_files
import math
import random

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

        maps = []
    
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

class VitalitySystem:
    def __init__(self, health):
        self.is_alive = True
        self.max_health = health
        self.health = self.max_health

    def hurt(self, damage):
        if self.health >= 0:
            self.health -= damage

    def heal(self, heals):
        if self.health <=100:
            self.health += heals

    def update(self):
        if self.health > self.max_health:
            self.health = self.max_health
        if self.health < 0:
            self.health = 0
        if self.health == 0:
            self.is_alive = False

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

class StateMachine:
    def __init__(self, state_list : list, start_state : str):
        self.state_list = state_list
        self.state = start_state

    def switch(self, new_state):
        if new_state in self.state_list:
            self.state = new_state
    """        self.state_call()
    
    def state_call(self):
        match self.state:
            case "idle":
                self.animation_speed = 0"""

class Player(arcade.Sprite):

    def __init__(self, position, scale = 1):
        """Initialize player sprite"""
        super().__init__()
        self.center_x, self.center_y = position
        self.scale = scale
        self.speed_constant = 4
        self.speed = self.speed_constant

        # Vitality
        self.vitality_system = VitalitySystem(100)
        self.damage_timer = 0

        # Animation
        self.textures = texture_files.player_textures      
        self.time_since_last_frame = 0
        self.anim_speed_constant = 0.1
        self.direction_x = "right"
        self.direction_y = "down"
        self.current_texture = 0
        self.texture = self.textures["idle_right_down"][self.current_texture]

        # Movement
        self.change_x = 0
        self.change_y = 0

        move_state_list = ["idle", "walk", "dead"]
        self.state_machine = StateMachine(move_state_list, "idle")
        self.stamina_system = StaminaSystem()
        
    def update_animation(self, delta_time = float(1 / 60)):
        """Update which animation is shown depending on the movement direction"""
        #self.move_states = enumerate("idle", "walk")

        # Switch to relevant state
        if self.change_x == 0 and self.change_y == 0:
            if self.vitality_system.health > 0 and self.state_machine.state != "idle":
                self.state_machine.switch("idle")
            elif self.vitality_system.health <= 0 and self.state_machine.state != "dead":
                self.state_machine.switch("dead")
        elif self.state_machine.state != "walk":
            self.state_machine.switch("walk")

        # Moving
        if self.state_machine.state == "walk":
            if self.change_x > 0:
                self.direction_x = "right"
            elif self.change_x < 0:
                self.direction_x = "left"

            if self.change_y > 0:
                self.direction_y = "up"
            elif self.change_y < 0:
                self.direction_y = "down"

        # Cycle through animation
        try:
            self.sync_hit_box_to_texture()
            self.texture = self.textures[f"{self.state_machine.state}_{self.direction_x}_{self.direction_y}"][self.current_texture]
        except (IndexError, KeyError):
            pass

        self.time_since_last_frame += delta_time

        if self.time_since_last_frame >= self.animation_speed:
            self.current_texture = (self.current_texture + 1) % len(self.textures[f"{self.state_machine.state}_{self.direction_x}_{self.direction_y}"])
            self.time_since_last_frame = 0
     
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

    def update_stamina(self, input_manager, delta_time):
        if self.stamina_system.can_sprint:
            if input_manager.is_sprinting():
                self.speed = 3 * self.speed_constant
                self.stamina_system.drain(delta_time)
                self.animation_speed = self.anim_speed_constant / 2
            else:
                self.speed = self.speed_constant
                self.stamina_system.recover(delta_time)
                self.animation_speed = self.anim_speed_constant
        else:
            self.speed = 0.25 * self.speed_constant
            self.animation_speed = 4 * self.anim_speed_constant
            self.stamina_system.recover(delta_time)

    def update_vitality(self, delta_time, target_list):
        self.vitality_system.update()
        
        self.damage_timer += delta_time

        if self.vitality_system.is_alive == False:
            #self.remove_from_sprite_lists() # Death
            self.speed_constant = 0

    def update(self, input_manager, delta_time, target):
        self.update_movement(input_manager, delta_time)
        self.update_stamina(input_manager, delta_time)
        self.update_animation(delta_time)
        self.update_vitality(delta_time, target)

class Enemy(arcade.Sprite):
    def __init__(self, position, textures, scale = 1):
        super().__init__()
        self.center_x, self.center_y = position
        self.scale = scale
        self.speed_constant = 2
        self.speed = self.speed_constant


        self.vitality_system = VitalitySystem(100)

        # Animation
        self.textures = textures   
        self.time_since_last_frame = 0
        self.anim_speed_constant = 0.1
        self.animation_speed = self.anim_speed_constant
        self.direction_x = "right"
        self.direction_y = "down"
        self.current_texture = 0
        self.texture = self.textures["idle_right"][self.current_texture]
        self.enum_direction = {
            "left" : -1,
            "right" : 1,
            "up" : 1,
            "right" : -1 
            }

        # Combat
        self.never_found = False
        state_list = ("idle", "chasing", "combat")
        self.state_machine = StateMachine(state_list, "idle")

    def update_state(self, target, delta_time):
        if self.state_machine.state != "idle" and distanceFrom(target, self) > lenConvert(8):
            self.state_machine.switch("idle")
        elif self.state_machine.state != "chasing" and distanceFrom(target, self) > lenConvert(3) and distanceFrom(target, self) < lenConvert(8):
            self.state_machine.switch("chasing")
        elif self.state_machine.state != "combat" and distanceFrom(target, self) < lenConvert(3):
            self.state_machine.switch("combat")

    def update_action(self, delta_time, target):
        try:
            self.sync_hit_box_to_texture()
            self.texture = self.textures[f"idle_{self.direction_x}"][self.current_texture]
        except (IndexError, KeyError):
            pass

        self.time_since_last_frame += delta_time

        if self.time_since_last_frame >= self.animation_speed:
            self.current_texture = (self.current_texture + 1) % len(self.textures[f"idle_{self.direction_x}"])
            self.time_since_last_frame = 0

        match self.state_machine.state:
            case "idle":
                (self.change_x, self.change_y) = (0, 0)
            case "chasing":
                (self.change_x, self.change_y) = findVelocity(target, self)
            case "combat":
                (self.change_x, self.change_y) = findVelocity(target, self)

        if target.center_x > self.center_x:
            self.direction_x = "right"
        elif target.center_x < self.center_x:
            self.direction_x = "left"

    def deal_damage(self, target, damage):
        if target.damage_timer >= 0.5 and target.vitality_system.health > 0:
            if self.collides_with_sprite(target):
                target.vitality_system.hurt(damage)
                target.damage_timer = 0

    def update(self, delta_time, target):
        self.update_state(target, delta_time)
        self.update_action(delta_time, target)

class Skeleton(Enemy):
    def __init__(self, position, textures, scale=1):
        super().__init__(position, textures, scale)

        self.speed_constant = 3

    def update_state(self, target, delta_time):
        if self.state_machine.state != "idle" and distanceFrom(target, self) > lenConvert(8): #
            self.state_machine.switch("idle")
        elif self.state_machine.state != "chasing" and distanceFrom(target, self) > lenConvert(3) and distanceFrom(target, self) < lenConvert(8): #
            self.state_machine.switch("chasing")
        elif self.state_machine.state != "combat" and distanceFrom(target, self) < lenConvert(3): #
            self.state_machine.switch("combat")

    def update_action(self, delta_time, target):
        try:
            self.sync_hit_box_to_texture()
            self.texture = self.textures[f"idle_{self.direction_x}"][self.current_texture]
        except (IndexError, KeyError):
            pass

        self.time_since_last_frame += delta_time

        if self.time_since_last_frame >= self.animation_speed:
            self.current_texture = (self.current_texture + 1) % len(self.textures[f"idle_{self.direction_x}"])
            self.time_since_last_frame = 0

        match self.state_machine.state:
            case "idle":
                (self.change_x, self.change_y) = (0, 0)
                if self.never_found == True:
                    if target.center_x < self.center_x:
                        self.direction_x = "right"
                    elif target.center_x > self.center_x:
                        self.direction_x = "left"

            case "chasing":
                self.never_found = False
                (self.change_x, self.change_y) = findVelocity(target, self)
                if target.center_x > self.center_x:
                    self.direction_x = "right"
                elif target.center_x < self.center_x:
                    self.direction_x = "left"

            case "combat":
                self.never_found = False
                (self.change_x, self.change_y) = findVelocity(target, self)
                if target.center_x > self.center_x:
                    self.direction_x = "right"
                elif target.center_x < self.center_x:
                    self.direction_x = "left"
        
        self.deal_damage(target, 8)

class DashingSkeleton(Skeleton):
    """ DREAM - A skeleton that telegraphs its dash, dashes while dropping some bones, and if player escapes for enough time then skeleton runs out of bones and dies """
    def __init__(self, position, textures, scale=1):
        super().__init__(position, textures, scale)

        self.dash_timer = 0
    
    def update_action(self, delta_time, target):
        try:
            self.sync_hit_box_to_texture()
            self.texture = self.textures[f"idle_{self.direction_x}"][self.current_texture]
        except (IndexError, KeyError):
            pass

        self.time_since_last_frame += delta_time

        if self.time_since_last_frame >= self.animation_speed:
            self.current_texture = (self.current_texture + 1) % len(self.textures[f"idle_{self.direction_x}"])
            self.time_since_last_frame = 0

        match self.state_machine.state:
            case "idle":
                self.deal_damage(target, 10)
                (self.change_x, self.change_y) = (0, 0)
                if self.never_found == True:
                    if target.center_x < self.center_x:
                        self.direction_x = "right"
                    elif target.center_x > self.center_x:
                        self.direction_x = "left"

                self.animation_speed = self.anim_speed_constant
                self.dash_timer = 0
                self.dashing = False
                self.speed = self.speed_constant
                
            case "chasing":
                self.deal_damage(target, 10)
                self.never_found = False
                (self.change_x, self.change_y) = findVelocity(target, self)
                if target.center_x > self.center_x:
                    self.direction_x = "right"
                elif target.center_x < self.center_x:
                    self.direction_x = "left"

                self.animation_speed = self.anim_speed_constant
                self.dash_timer = 0
                self.dashing = False
                self.speed = self.speed_constant

            case "combat":
                self.never_found = False
                (self.change_x, self.change_y) = findVelocity(target, self)
                if target.center_x > self.center_x:
                    self.direction_x = "right"
                elif target.center_x < self.center_x:
                    self.direction_x = "left"

                self.animation_speed = self.anim_speed_constant / 4
                self.dash_timer += delta_time

                if self.dash_timer > 3:
                    self.speed = self.speed_constant * 3.2
                    self.dash_timer = 0
                    self.dashing = True

                if self.dashing == True:
                    self.animation_speed = self.anim_speed_constant * 100

        if self.dashing == True:
            self.deal_damage(target, 85)
        else:
            self.deal_damage(target, 10)

class Weapon(arcade.Sprite): # TODO
    def __init__(self, texture_files, damage, range, speed, rarity):
        super().__init__()
        self.textures = texture_files
        self.damage = damage
        self.range = range
        self.speed = speed
        self.rarity = rarity
        
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
        self.hp_width = (target.vitality_system.health/target.vitality_system.max_health) * self.hp_bar_const
        self.hp_bar_bg = arcade.draw_lbwh_rectangle_filled(self.hp_bg_x, self.hp_bg_y, self.hp_bar_const + 4, 20, (55, 55, 55))
        self.hp_bar_bg = arcade.draw_lbwh_rectangle_filled(self.hp_x, self.hp_y, self.hp_bar_const, 16, arcade.color.BLACK)
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


# ----------- HELPER FUNCTIONS ------------

def tileConvert(tile_ix, tile_iy, tile_size = 64):
    return (tile_ix * tile_size, tile_iy * tile_size)
    
def lenConvert(len, tile_size = 64):
    return len * tile_size


    return textures

def distanceFrom(player, enemy):
    distance = math.sqrt((player.center_x - enemy.center_x)**2 + (player.center_y - enemy.center_y)**2)
    return distance

def findVelocity(player, enemy):
    vx = enemy.speed * ((enemy.center_x - player.center_x))/distanceFrom(player, enemy)
    vy = enemy.speed * ((enemy.center_y - player.center_y))/distanceFrom(player, enemy)
    return (-vx, -vy)

def printDrawOrder(scene):
        # Gives draw order
        # scene = self.scene
        # scene_sprite_lists = (self.scene._sprite_lists)
        for spritelist in scene._sprite_lists:
            for name, stored_list in scene._name_mapping.items():
                if spritelist is stored_list:
                    print(name)

def printTileIndex(self):
    # Print Tile Index
    si_x = int(self.player.center_x)//(64)
    si_y = int(self.player.center_y)//(64)
    self.standing_index = (si_x, si_y)
    if self.old_print != self.standing_index:
        print(self.standing_index)
        self.old_print = self.standing_index


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
        self.player.update(self.input_manager, delta_time, self.enemy_list)
        self.enemy_list.update(delta_time, self.player)
        for engine in self.enemy_engines:
            engine.update()
        self.map_handler.update()
        self.camera.update()
        self.hud_manager.update(self.player)

        printTileIndex(self)

    def on_draw(self):
        self.clear((37, 19, 26))
        self.map_handler.draw()
        self.camera.apply()
        self.hud_manager.draw(self.player)
        #self.player.draw_hit_box(arcade.color.RED)
        #self.enemy.draw_hit_box(arcade.color.RED)

    def setup(self):
        # Player
        #self.map_current = self.map_handler.maps[random.randint[0,3]]
        self.map_current = r"C:\MyGames\pythonGame\assets\myAssetPack\tileset\map2.tmx"
        self.player = Player((tileConvert(7, 9)))
        self.player_list = arcade.SpriteList(use_spatial_hash = True)
        self.textures = self.player.textures[f"idle_{self.player.direction_x}_{self.player.direction_y}"]
        
        # Enemy(s)
        self.enemy_list = arcade.SpriteList(use_spatial_hash = True)
        N = 1
        for i in range(N):
            spawn_pos = tileConvert(60 + i, 10)  # different tile each enemy
            enemy = DashingSkeleton(spawn_pos, texture_files.skeleton_textures)
            self.enemy_list.append(enemy)
        
        # Map/Scene init
        self.map_handler = MapHandler(self.player)
        self.map_handler.load(self.map_current)
        self.scene = self.map_handler.scene
        
        # Append sprites late
        self.player_list.append(self.player)
        self.enemy_engines = []
        for enemy in self.enemy_list:
            self.enemy_engines.append(arcade.PhysicsEngineSimple(enemy, self.map_handler.scene["Walls"]))

        # Add to scene
        self.scene.add_sprite_list_after("Player", "Walls", sprite_list = self.player_list)
        self.scene.add_sprite_list_after("Enemy1", "Player", sprite_list = self.enemy_list)
        
        # Camera
        self.camera = CameraManager()
        self.camera.set_target(self.player)
        
        # UI / other systems
        self.input_manager = InputManager()
        self.hud_manager = HUDManager()
        
        printDrawOrder(self.scene)

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_NAME, fullscreen=True, antialiasing=False, resizable=False)
    start_view = GameView()
    start_view.setup()
    window.show_view(start_view)
    arcade.run()

main()