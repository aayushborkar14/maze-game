from maze import Maze
from powerup import PowerUp, PowerUpMap
from tiles import Tilemap, Tileset
from trap import Trap, TrapMap


class LevelConfig:
    """
    Class that holds the configuration for each level.
    Contains the tilesets, tilemaps, powerups, traps, and time limits for each level.
    """

    def __init__(self):
        """
        Initializes the tilesets, tilemaps, powerups, traps, and time limits for each level.
        """
        self.ts2 = Tileset("assets/gen5.png")
        self.ts11 = Tileset("assets/underwater1.png", size=(16, 16))
        self.ts12 = Tileset("assets/underwater2.png", size=(16, 16))
        self.ts3 = Tileset("assets/swampy.png")
        self.tsc = Tileset("assets/cavetiles.png")
        self.box = Tileset("assets/itembox.png", size=(252, 252))
        self.vent = Tileset("assets/vent.png")
        self.trap_tile = Tileset("assets/beartrap.png").tiles[0]
        self.powerup_weights = {
            PowerUp.EMPTY: 0.95,
            PowerUp.SCORE_GAIN: 0.02,
            PowerUp.TIME_GAIN: 0.02,
            PowerUp.CAVE_VENT: 0.01,
        }
        self.powerup_tiles = {
            PowerUp.EMPTY: self.box.tiles[0],
            PowerUp.SCORE_GAIN: self.box.tiles[0],
            PowerUp.TIME_GAIN: self.box.tiles[0],
            PowerUp.CAVE_VENT: self.vent.tiles[0],
        }
        self.trap_weights = {
            Trap.EMPTY: 0.25,
            Trap.SPRITE_FREEZE: 0.25,
            Trap.REDUCED_VISION: 0.5,
        }

    def get_level_config(self, level):
        """
        Returns the configuration for the given level.
        Args:
            level: int, the level number.
        Returns:
            map: Tilemap, the tilemap for the level.
            maze: Maze, the maze for the level.
            powerup_map: PowerUpMap, the powerup map for the level.
            trap_map: TrapMap, the trap map for the level.
            time: int, the time limit for the level.
        """
        map = None
        powerup_map = PowerUpMap(70, self.powerup_weights)
        maze = Maze(level, 70)
        trap_map = TrapMap(maze.cells, self.trap_weights)
        time = None
        if level == 1:
            self.trap_weights = {
                Trap.EMPTY: 0.5,
                Trap.SPRITE_FREEZE: 0.25,
                Trap.REDUCED_VISION: 0.25,
            }
            map = Tilemap(
                self.ts11,
                self.ts11,
                self.ts12,
                "assets/BaseLayer1.npy",
                "assets/TerrainLayer1.npy",
                "assets/TopLayer1.npy",
                powerup_map.map,
                trap_map.map,
                maze.cells,
                maze.sol_cells,
                434,
                90,
                self.powerup_tiles,
                self.trap_tile,
                size=(110, 110),
            )
            time = 180
        elif level == 2:
            map = Tilemap(
                self.ts2,
                self.ts2,
                self.ts2,
                "assets/BaseLayer2.npy",
                "assets/TerrainLayer2.npy",
                "assets/TopLayer2.npy",
                powerup_map.map,
                trap_map.map,
                maze.cells,
                maze.sol_cells,
                4109,
                4378,
                self.powerup_tiles,
                self.trap_tile,
                size=(110, 110),
            )
            time = 180
        elif level == 3:
            self.trap_weights = {
                Trap.EMPTY: 0.25,
                Trap.SPRITE_FREEZE: 0.375,
                Trap.REDUCED_VISION: 0.375,
            }
            map = Tilemap(
                self.ts3,
                self.ts3,
                self.ts3,
                "assets/BaseLayer3.npy",
                "assets/TerrainLayer3.npy",
                None,
                powerup_map.map,
                trap_map.map,
                maze.cells,
                maze.sol_cells,
                0,
                3,
                self.powerup_tiles,
                self.trap_tile,
                size=(110, 110),
            )
            time = 180
        elif level == "cave":
            maze = Maze("cave", 30)
            powerup_map = None
            trap_map = None
            map = Tilemap(
                self.tsc,
                self.tsc,
                self.tsc,
                "assets/BaseLayerCave.npy",
                None,
                None,
                None,
                None,
                maze.cells,
                maze.sol_cells,
                1,
                3,
                None,
                None,
                size=(70, 70),
                game=(30 - 1, 30 - 1),
                image_path="cave_path.png",
            )
        return map, maze, powerup_map, trap_map, time
