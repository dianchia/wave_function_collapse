import random

from omegaconf import DictConfig

from .enums import Direction


class Tile:
    def __init__(self, x: int, y: int, tile_config: DictConfig) -> None:
        self.x = x
        self.y = y
        self.tile_rules: dict[str, list[str]] = tile_config.RULES
        self.tile_weights: dict[str, int] = tile_config.WEIGHTS

        self.possibilities = list(self.tile_rules.keys())
        self.entropy = len(self.possibilities)
        self.neighbours: dict[Direction, Tile] = {}
        self.tile_type: str | None = None

    def add_neighbour(self, direction: Direction, tile: "Tile") -> None:
        self.neighbours[direction] = tile

    def get_directions(self) -> list[Direction]:
        return list(self.neighbours.keys())

    def get_neighbour(self, direction: Direction) -> "Tile":
        return self.neighbours[direction]

    def get_posibilities(self) -> list[str]:
        return self.possibilities

    def collapse(self) -> None:
        weights = [self.tile_weights[p] for p in self.possibilities]
        self.possibilities = random.choices(self.possibilities, weights, k=1)
        self.tile_type = self.possibilities[0]
        self.entropy = 0

    def constrain(self, neighbour_possibilities: list[str], direction: Direction) -> bool:
        reduced = False

        if self.entropy > 0:
            connectors = [self.tile_rules[n][direction] for n in neighbour_possibilities]
            opposite = Direction.opposite(direction)

            for p in self.possibilities.copy():
                if self.tile_rules[p][opposite] not in connectors:
                    self.possibilities.remove(p)
                    reduced = True

            self.entropy = len(self.possibilities)
        return reduced

