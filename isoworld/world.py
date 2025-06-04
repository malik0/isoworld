import random
from typing import List

class Tile:
    """Represents a tile in the world."""
    def __init__(self, height: int):
        self.height = height

    def __repr__(self) -> str:
        return f"Tile(height={self.height})"


def generate_height_map(width: int, height: int) -> List[List[int]]:
    """Generate a height map using simple random values."""
    return [[random.randint(0, 2) for _ in range(width)] for _ in range(height)]


def generate_world(width: int, height: int) -> List[List[Tile]]:
    """Generate the world as a 2D grid of tiles."""
    height_map = generate_height_map(width, height)
    return [[Tile(h) for h in row] for row in height_map]
