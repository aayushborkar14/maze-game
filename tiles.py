import numpy as np
import pygame


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
                self.tiles.append(tile)


class Tilemap:
    def __init__(
        self, tileset, base_layer, terrain_layer, top_layer, size=(110, 110), rect=None
    ):
        self.size = size
        self.tileset = tileset
        self.map = np.zeros(size, dtype=int)
        self.layer1 = np.load(base_layer)
        self.layer2 = np.load(terrain_layer)
        self.layer3 = np.load(top_layer)

        h, w = self.size
        self.image = pygame.Surface((32 * w, 32 * h))
        if rect:
            self.rect = pygame.Rect(rect)
        else:
            self.rect = self.image.get_rect()

    def render(self):
        m, n = self.map.shape
        for i in range(m):
            for j in range(n):
                tile = self.tileset.tiles[self.map[i, j]]
                self.image.blit(tile, (j * 32, i * 32))

    def process_layers(self):
        m, n = self.map.shape
        for i in range(m):
            for j in range(n):
                tile1 = self.tileset.tiles[self.layer1[i, j]]
                self.image.blit(tile1, (j * 32, i * 32))
                if self.layer2[i, j] != 6124:
                    tile2 = self.tileset.tiles[self.layer2[i, j]]
                    self.image.blit(tile2, (j * 32, i * 32))
                if self.layer3[i, j] != 6124:
                    tile3 = self.tileset.tiles[self.layer3[i, j]]
                    self.image.blit(tile3, (j * 32, i * 32))
