from typing import List
from .world import Tile

TILE_SYMBOLS = {
    "water": "~ ",
    "sand": ". ",
    "desert": "` ",
    "grass": ", ",
    "forest": "^ ",
    "mountain": "A ",
    "snow": "* ",
    "tundra": ": ",
    "taiga": "; ",
    "savanna": "' ",
    "rainforest": "! ",
}

TILE_SYMBOLS_COLOR = {
    "water": "\x1b[34m~ \x1b[0m",
    "sand": "\x1b[33m. \x1b[0m",
    "desert": "\x1b[33m` \x1b[0m",
    "grass": "\x1b[32m, \x1b[0m",
    "forest": "\x1b[32m^ \x1b[0m",
    "mountain": "\x1b[37mA \x1b[0m",
    "snow": "\x1b[37m* \x1b[0m",
    "tundra": "\x1b[37m: \x1b[0m",
    "taiga": "\x1b[32m; \x1b[0m",
    "savanna": "\x1b[33m' \x1b[0m",
    "rainforest": "\x1b[32m! \x1b[0m",
}

TILE_COLORS = {
    "water": "#3b6efb",
    "sand": "#d2b48c",
    "desert": "#edc9af",
    "grass": "#00aa00",
    "forest": "#228b22",
    "mountain": "#777777",
    "snow": "#ffffff",
    "tundra": "#cccccc",
    "taiga": "#006400",
    "savanna": "#bdb76b",
    "rainforest": "#005500",
}

def render_isometric(world: List[List[Tile]], color: bool = False) -> str:
    """Render the world in a simple isometric ASCII representation."""
    height = len(world)
    width = len(world[0]) if world else 0
    lines = []
    for y in range(height - 1, -1, -1):
        offset = ' ' * (y)
        line_parts = [offset]
        for x in range(width):
            tile = world[y][x]
            symbols = TILE_SYMBOLS_COLOR if color else TILE_SYMBOLS
            symbol = symbols.get(tile.terrain, '? ')
            line_parts.append(symbol)
        lines.append(''.join(line_parts))
    return '\n'.join(lines)


def render_3d_plot(world: List[List[Tile]], filename: str = "world.png") -> str:
    """Render the world as a 3D height map saved to an image file."""
    try:
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
        import numpy as np
    except ImportError as exc:  # pragma: no cover - optional dependency
        raise RuntimeError("matplotlib is required for 3D rendering") from exc

    height = len(world)
    width = len(world[0]) if world else 0
    z_values = [[tile.height for tile in row] for row in world]
    x_values, y_values = np.meshgrid(range(width), range(height))
    z_array = np.array(z_values)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(x_values, y_values, z_array, cmap="terrain", edgecolor="k")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("height")
    plt.savefig(filename)
    plt.close(fig)
    return filename


def _shade_color(color: str, factor: float) -> str:
    """Return a darker shade of the given hex color."""
    if not color.startswith("#") or len(color) != 7:
        return color
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)
    r = int(r * factor)
    g = int(g * factor)
    b = int(b * factor)
    return f"#{r:02x}{g:02x}{b:02x}"


def render_3d_window(world: List[List[Tile]]) -> None:
    """Display a simple 3D view of the world using tkinter."""
    try:
        import tkinter as tk
    except Exception as exc:  # pragma: no cover - optional dependency
        raise RuntimeError("tkinter is required for window rendering") from exc

    tile_w = 30
    tile_h = 15
    tile_d = 10
    width = len(world[0]) if world else 0
    height = len(world)
    x_offset = width * tile_w
    y_offset = 50
    max_h = max(tile.height for row in world for tile in row)
    canvas_w = (width + height) * tile_w + x_offset
    canvas_h = (width + height) * tile_h // 2 + max_h * tile_d + y_offset * 2

    try:
        root = tk.Tk()
    except tk.TclError as exc:  # pragma: no cover - headless environments
        raise RuntimeError("tkinter failed to initialize") from exc
    root.title("isoworld 3D")
    canvas = tk.Canvas(root, width=canvas_w, height=canvas_h, bg="white")
    canvas.pack()

    def iso(x: int, y: int, z: int) -> tuple[int, int]:
        sx = (x - y) * tile_w + x_offset
        sy = (x + y) * tile_h // 2 - z * tile_d + y_offset
        return sx, sy

    def draw_block(x: int, y: int, h: int, terrain: str) -> None:
        color = TILE_COLORS.get(terrain, "#808080")
        top = [iso(x, y, h), iso(x + 1, y, h), iso(x + 1, y + 1, h), iso(x, y + 1, h)]
        left = [iso(x, y + 1, 0), iso(x, y, 0), iso(x, y, h), iso(x, y + 1, h)]
        right = [iso(x + 1, y, 0), iso(x + 1, y + 1, 0), iso(x + 1, y + 1, h), iso(x + 1, y, h)]
        canvas.create_polygon(right, fill=_shade_color(color, 0.7), outline="black")
        canvas.create_polygon(left, fill=_shade_color(color, 0.85), outline="black")
        canvas.create_polygon(top, fill=color, outline="black")

    for y in range(height - 1, -1, -1):
        for x in range(width):
            tile = world[y][x]
            draw_block(x, y, tile.height, tile.terrain)

    root.mainloop()
