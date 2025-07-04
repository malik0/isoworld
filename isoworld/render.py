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
    for y in range(height):
        offset = ' ' * (height - y - 1)
        line_parts = [offset]
        for x in range(width):
            tile = world[height - y - 1][x]
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
    """Darken or lighten a hex color by a factor."""
    if not color.startswith("#") or len(color) != 7:
        return color
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)
    r = min(255, max(0, int(r * factor)))
    g = min(255, max(0, int(g * factor)))
    b = min(255, max(0, int(b * factor)))
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

    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True)

    h_scroll = tk.Scrollbar(frame, orient="horizontal")
    h_scroll.pack(side="bottom", fill="x")
    v_scroll = tk.Scrollbar(frame, orient="vertical")
    v_scroll.pack(side="right", fill="y")

    window_w = min(canvas_w, 800)
    window_h = min(canvas_h, 600)

    canvas = tk.Canvas(
        frame,
        width=window_w,
        height=window_h,
        bg="white",
        scrollregion=(0, 0, canvas_w, canvas_h),
        xscrollcommand=h_scroll.set,
        yscrollcommand=v_scroll.set,
    )
    canvas.pack(side="left", fill="both", expand=True)

    h_scroll.config(command=canvas.xview)
    v_scroll.config(command=canvas.yview)

    def iso(x: int, y: int, z: int) -> tuple[float, float]:
        sx = (x - y) * tile_w + x_offset
        sy = (x + y) * tile_h * 0.5 - z * tile_d + y_offset
        return sx, sy

    def draw_block(x: int, y: int) -> None:
        tile = world[y][x]
        h = tile.height
        color = TILE_COLORS.get(tile.terrain, "#808080")

        right_h = world[y][x + 1].height if x + 1 < width else 0
        left_h = world[y + 1][x].height if y + 1 < height else 0

        top = [iso(x, y, h), iso(x + 1, y, h), iso(x + 1, y + 1, h), iso(x, y + 1, h)]
        if h > right_h:
            right = [
                iso(x + 1, y, right_h),
                iso(x + 1, y + 1, right_h),
                iso(x + 1, y + 1, h),
                iso(x + 1, y, h),
            ]
            canvas.create_polygon(right, fill=_shade_color(color, 0.55), outline="black")
        if h > left_h:
            left = [
                iso(x, y + 1, left_h),
                iso(x, y, left_h),
                iso(x, y, h),
                iso(x, y + 1, h),
            ]
            canvas.create_polygon(left, fill=_shade_color(color, 0.75), outline="black")

        canvas.create_polygon(top, fill=_shade_color(color, 1.1), outline="black")

    coords = []
    for y in range(height):
        for x in range(width):
            world_y = height - y - 1
            coords.append((x, world_y, x + world_y))

    for x, y, _ in sorted(coords, key=lambda c: c[2]):
        tile = world[y][x]
        draw_block(x, y)

    root.mainloop()
