import random
from itertools import product

from omegaconf import DictConfig

from .enums import Direction
from .tile import Tile


class World:
    def __init__(self, config: DictConfig) -> None:
        self.is_collapsed = False
        self.cols = config.WORLD.WIDTH
        self.rows = config.WORLD.HEIGHT
        self.tile_rules = config.TILE.RULES

        self.tile_rows: list[list[Tile]] = []
        for y in range(self.rows):
            tiles = []
            for x in range(self.cols):
                tiles.append(Tile(x, y, config.TILE))
            self.tile_rows.append(tiles)

        for y, x in product(range(self.rows), range(self.cols)):
            tile = self.tile_rows[y][x]
            if y > 0:
                tile.add_neighbour(Direction.NORTH, self.tile_rows[y - 1][x])
            if x < self.cols - 1:
                tile.add_neighbour(Direction.EAST, self.tile_rows[y][x + 1])
            if y < self.rows - 1:
                tile.add_neighbour(Direction.SOUTH, self.tile_rows[y + 1][x])
            if x > 0:
                tile.add_neighbour(Direction.WEST, self.tile_rows[y][x - 1])

    def get_tile_entropy(self, x: int, y: int) -> int:
        return self.tile_rows[y][x].entropy

    def get_tile_type(self, x: int, y: int) -> str:
        return self.tile_rows[y][x].get_posibilities()[0]

    def get_lowest_entropy(self) -> int:
        lowest = len(list(self.tile_rules))
        for y, x in product(range(self.rows), range(self.cols)):
            tile_entropy = self.tile_rows[y][x].entropy
            if tile_entropy > 0 and tile_entropy < lowest:
                lowest = tile_entropy
        return lowest

    def get_lowest_entropy_tiles(self) -> list[Tile]:
        lowest = len(list(self.tile_rules))
        tiles = []

        for y, x in product(range(self.rows), range(self.cols)):
            tile_entropy = self.tile_rows[y][x].entropy
            if tile_entropy <= 0:
                continue

            if tile_entropy < lowest:
                tiles.clear()
                lowest = tile_entropy
            if tile_entropy == lowest:
                tiles.append(self.tile_rows[y][x])

        return tiles

    def wave_function_collapse(self) -> bool:
        lowest_entropy_tiles = self.get_lowest_entropy_tiles()

        # No more tiles to collapse
        if not lowest_entropy_tiles:
            print("World generation completed")
            self.is_collapsed = True
            return True

        tile_to_collapse = random.choice(lowest_entropy_tiles)
        tile_to_collapse.collapse()

        stack: list[Tile] = [tile_to_collapse]

        while len(stack) > 0:
            tile = stack.pop()
            poss = tile.get_posibilities()
            directions = tile.get_directions()

            for dir in directions:
                neighbour = tile.get_neighbour(dir)
                if neighbour.entropy != 0 and neighbour.constrain(poss, dir):
                    stack.append(neighbour)

        return False

