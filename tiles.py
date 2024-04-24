import numpy as np
import pygame

from powerup import PowerUp
from trap import Trap


class Tileset:
    def __init__(self, file, size=(32, 32), margin=0, spacing=0):
        self.file = file
        self.size = size
        self.margin = margin
        self.spacing = spacing
        self.image = pygame.image.load(file).convert_alpha()
        self.rect = self.image.get_rect()
        self.tiles = []
        self.load()

    def load(self):
        self.tiles = []
        x0 = y0 = self.margin
        w, h = self.rect.size
        dx = self.size[0] + self.spacing
        dy = self.size[1] + self.spacing

        for x in range(x0, w, dx):
            for y in range(y0, h, dy):
                tile = pygame.Surface(self.size, pygame.SRCALPHA)
                tile.blit(self.image, (0, 0), (x, y, *self.size))
                tile = pygame.transform.scale(tile, (32, 32))
                self.tiles.append(tile)


class Tilemap:
    def __init__(
        self,
        tileset1,
        tileset2,
        tileset3,
        base_layer,
        terrain_layer,
        top_layer,
        powerup_map,
        trap_map,
        maze_layer,
        sol_layer,
        wall_tile,
        sol_tile,
        powerup_tiles,
        trap_tile,
        size=(110, 110),
        game=(70 - 1, 70 - 1),
        rect=None,
    ):
        self.size = size
        self.tileset1 = tileset1
        self.tileset2 = tileset2
        self.tileset3 = tileset3
        self.layer1 = np.load(base_layer)
        self.layer2 = None
        self.layer3 = None
        self.powerup_map = powerup_map
        self.trap_map = trap_map
        if terrain_layer is not None:
            self.layer2 = np.load(terrain_layer)
        if top_layer is not None:
            self.layer3 = np.load(top_layer)
        self.maze = maze_layer
        self.sol = sol_layer
        self.wall_tile = wall_tile
        self.sol_tile = sol_tile
        self.trap_tile = trap_tile
        self.powerup_tiles = powerup_tiles
        self.gamestart = (size[0] - game[0]) // 2
        self.gameend = (size[0] + game[0]) // 2

        h, w = self.size
        self.image = pygame.Surface((32 * w, 32 * h))
        self.solimage = pygame.Surface((32 * w, 32 * h))
        if rect:
            self.rect = pygame.Rect(rect)
        else:
            self.rect = self.image.get_rect()

    def process_layers(self):
        m, n = self.size
        for i in range(m):
            for j in range(n):
                if self.layer1[i, j] != -1:
                    tile1 = self.tileset1.tiles[self.layer1[i, j]]
                    self.image.blit(tile1, (j * 32, i * 32))
                if self.layer2 is not None and self.layer2[i, j] != -1:
                    tile2 = self.tileset2.tiles[self.layer2[i, j]]
                    self.image.blit(tile2, (j * 32, i * 32))
                if self.layer3 is not None and self.layer3[i, j] != -1:
                    tile3 = self.tileset3.tiles[self.layer3[i, j]]
                    self.image.blit(tile3, (j * 32, i * 32))
                if (
                    self.gamestart <= i < self.gameend
                    and self.gamestart <= j < self.gameend
                    and self.maze[i - self.gamestart, j - self.gamestart]
                ):
                    if isinstance(self.wall_tile, int):
                        wall = self.tileset1.tiles[self.wall_tile]
                    else:
                        wall = self.tileset1.tiles[np.random.choice(self.wall_tile)]
                    self.image.blit(wall, (j * 32, i * 32))
                if (
                    self.powerup_map is not None
                    and self.gamestart <= i < self.gameend
                    and self.gamestart <= j < self.gameend
                    and self.powerup_map[i - self.gamestart, j - self.gamestart]
                    != PowerUp.EMPTY
                    and self.powerup_map[i - self.gamestart, j - self.gamestart] != 0
                ):
                    self.image.blit(
                        self.powerup_tiles[
                            self.powerup_map[i - self.gamestart, j - self.gamestart]
                        ],
                        (j * 32, i * 32),
                    )
                if (
                    self.trap_map is not None
                    and self.gamestart <= i < self.gameend
                    and self.gamestart <= j < self.gameend
                    and self.trap_map[i - self.gamestart, j - self.gamestart]
                    != Trap.EMPTY
                    and self.trap_map[i - self.gamestart, j - self.gamestart] != 0
                ):
                    self.image.blit(self.trap_tile, (j * 32, i * 32))
        self.solimage = self.image.copy()
        soltile = self.tileset1.tiles[self.sol_tile]
        for i in range(self.gamestart, self.gameend):
            for j in range(self.gamestart, self.gameend):
                if not self.sol[i - self.gamestart, j - self.gamestart]:
                    self.solimage.blit(soltile, (j * 32, i * 32))
        pygame.image.save(self.solimage, "path.png")
        self.solimage = None

    def remove_powerup(self, i, j):
        if self.layer1[i, j] != -1:
            tile1 = self.tileset1.tiles[self.layer1[i, j]]
            self.image.blit(tile1, (j * 32, i * 32))
        if self.layer2 is not None and self.layer2[i, j] != -1:
            tile2 = self.tileset2.tiles[self.layer2[i, j]]
            self.image.blit(tile2, (j * 32, i * 32))
        if self.layer3 is not None and self.layer3[i, j] != -1:
            tile3 = self.tileset3.tiles[self.layer3[i, j]]
            self.image.blit(tile3, (j * 32, i * 32))
        if (
            self.gamestart <= i < self.gameend
            and self.gamestart <= j < self.gameend
            and self.maze[i - self.gamestart, j - self.gamestart]
        ):
            wall = self.tileset1.tiles[self.wall_tile]
            self.image.blit(wall, (j * 32, i * 32))
