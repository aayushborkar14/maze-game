from maze import Maze
from powerup import PowerUp, PowerUpMap
from tiles import Tilemap, Tileset


class LevelConfig:
    def __init__(self):
        self.ts2 = Tileset("assets/gen5.png")
        self.ts11 = Tileset("assets/underwater1.png", size=(16, 16))
        self.ts12 = Tileset("assets/underwater2.png", size=(16, 16))
        self.ts3 = Tileset("assets/swampy.png")
        self.tsc = Tileset("assets/legacyadventure.png", size=(16, 16))
        self.box = Tileset("assets/itembox.png", size=(252, 252))
        self.powerup_weights = {
            PowerUp.EMPTY: 0.95,
            PowerUp.SCORE_GAIN: 0.01,
            PowerUp.TIME_GAIN: 0.01,
            PowerUp.SCORE_LOSS: 0.01,
            PowerUp.TIME_LOSS: 0.01,
            PowerUp.DUNGEON: 0.01,
        }

        self.powerup_tiles = {
            PowerUp.EMPTY: self.box.tiles[0],
            PowerUp.SCORE_GAIN: self.box.tiles[0],
            PowerUp.TIME_GAIN: self.box.tiles[0],
            PowerUp.SCORE_LOSS: self.box.tiles[0],
            PowerUp.TIME_LOSS: self.box.tiles[0],
            PowerUp.DUNGEON: self.box.tiles[0],
        }

    def load_tiles(self):
        self.ts2.load()
        self.ts11.load()
        self.ts12.load()
        self.ts3.load()
        self.box.load()

    def get_level_config(self, level):
        pmap = PowerUpMap(70, self.powerup_weights)
        maze = Maze(level, 70)
        if level == 1:
            return (
                Tilemap(
                    self.ts11,
                    self.ts11,
                    self.ts12,
                    "assets/BaseLayer1.npy",
                    "assets/TerrainLayer1.npy",
                    "assets/TopLayer1.npy",
                    pmap.map,
                    maze.cells,
                    maze.sol_cells,
                    434,
                    90,
                    self.powerup_tiles,
                    size=(110, 110),
                ),
                maze,
                pmap,
            )
        if level == 2:
            return (
                Tilemap(
                    self.ts2,
                    self.ts2,
                    self.ts2,
                    "assets/BaseLayer2.npy",
                    "assets/TerrainLayer2.npy",
                    "assets/TopLayer2.npy",
                    None,
                    maze.cells,
                    maze.sol_cells,
                    4109,
                    4378,
                    None,
                    size=(110, 110),
                ),
                maze,
                pmap,
            )
        if level == 3:
            return (
                Tilemap(
                    self.ts3,
                    self.ts3,
                    self.ts3,
                    "assets/BaseLayer3.npy",
                    "assets/TerrainLayer3.npy",
                    None,
                    None,
                    maze.cells,
                    maze.sol_cells,
                    0,
                    3,
                    None,
                    size=(110, 110),
                ),
                maze,
                pmap,
            )
        if level == "cave":
            maze = Maze(1, 30)
            return (
                Tilemap(
                    self.tsc,
                    self.tsc,
                    self.tsc,
                    "assets/BaseLayerCave.npy",
                    "assets/TerrainLayerCave.npy",
                    None,
                    None,
                    maze.cells,
                    maze.sol_cells,
                    30,
                    99,
                    None,
                    size=(70, 70),
                    game=(30 - 1, 30 - 1),
                ),
                maze,
                pmap,
            )
        return None, maze, pmap
