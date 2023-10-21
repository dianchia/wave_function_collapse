from abc import ABC, abstractmethod
from itertools import product

import pygame
from omegaconf import DictConfig

from .world import World


class Visualizer(ABC):
    @abstractmethod
    def update(self) -> None:
        pass


class PyGameVisualizer(Visualizer):
    def __init__(self, world: World, config: DictConfig) -> None:
        print(__file__)
        self.spritesheet = pygame.image.load(config.SPRITE.PATH).convert_alpha()
        self.sprite_coord: dict[str, list[int]] = config.SPRITE.COORD

        self.world = world
        self.world_width = config.WORLD.WIDTH
        self.world_height = config.WORLD.HEIGHT

        self.tile_types = config.TILE.TYPES
        self.tile_size = config.TILE.SIZE
        self.tile_scale = config.TILE.SCALE
        surface_width = self.world_width * self.tile_size * self.tile_scale
        surface_height = self.world_height * self.tile_size * self.tile_scale
        self.world_surface = pygame.Surface((surface_width, surface_height))

        default_font = pygame.font.get_default_font()
        self.font_l = pygame.font.Font(default_font, 14)
        self.font_m = pygame.font.Font(default_font, 11)
        self.font_s = pygame.font.Font(default_font, 8)

    def _draw_tile(self, x: int, y: int, tile_type: str) -> None:
        pos = self.sprite_coord[tile_type]
        tile_image = self.spritesheet.subsurface(
            pygame.Rect(pos[0], pos[1], self.tile_size, self.tile_size)
        )
        tile_image = pygame.transform.scale_by(tile_image, (self.tile_scale, self.tile_scale))
        scaled_size = self.tile_size * self.tile_scale
        self.world_surface.blit(tile_image, (x * scaled_size, y * scaled_size))

    def update(self) -> None:
        lowest_entropy = self.world.get_lowest_entropy()
        for y, x in product(range(self.world_height), range(self.world_width)):
            tile_entropy = self.world.get_tile_entropy(x, y)

            if tile_entropy:
                tile_image = pygame.Surface((self.tile_size, self.tile_size))

                if tile_entropy >= 27:
                    text_surface = self.font_s.render(str(tile_entropy), True, "darkgrey")
                    pos = (3, 3)
                elif tile_entropy >= 10:
                    text_surface = self.font_m.render(str(tile_entropy), True, "grey")
                    pos = (2, 3)
                elif tile_entropy == lowest_entropy:
                    text_surface = self.font_l.render(str(tile_entropy), True, "green")
                    pos = (4, 1)
                else:
                    text_surface = self.font_l.render(str(tile_entropy), True, "white")
                    pos = (4, 1)

                tile_image.blit(text_surface, pos)
                continue

            tile_type = self.world.get_tile_type(x, y)
            if "FOREST" in tile_type and tile_type != "FOREST":
                self._draw_tile(x, y, "GRASS")
                self._draw_tile(x, y, tile_type)
            else:
                self._draw_tile(x, y, tile_type)

    def draw(self, draw_surface: pygame.Surface) -> None:
        draw_surface.blit(self.world_surface, (0, 0))

