from typing import List
from .world import Tile

TILE_SYMBOLS = {
    0: '. ',
    1: 'o ',
    2: '^ ',
}

def render_isometric(world: List[List[Tile]]) -> str:
    """Render the world in a simple isometric ASCII representation."""
    height = len(world)
    width = len(world[0]) if world else 0
    lines = []
    for y in range(height - 1, -1, -1):
        offset = ' ' * (y)
        line_parts = [offset]
        for x in range(width):
            tile = world[y][x]
            symbol = TILE_SYMBOLS.get(tile.height, '? ')
            line_parts.append(symbol)
        lines.append(''.join(line_parts))
    return '\n'.join(lines)
