import arcade

def handle_load_map(self):
    # for some reason it cant handle if imported file already has the collision object inside it 
    map_name = r"C:\MyGames\pythonGame\assets\background\tilesets_success\map1_map.tmx"
    tile_map = arcade.load_tilemap(map_name, scaling=1.0)
    self.scene = None
    self.physics_engine = None
    self.wall_list = None
    self.scene = arcade.Scene.from_tilemap(tile_map)

    try:
        self.wall_list = self.scene["Walls"]
        self.wall_list.use_spatial_hash = True # optimize collision loop
    except KeyError:
        print("[!] No layer named 'Walls' found in map!")

    if self.wall_list:
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)