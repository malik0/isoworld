import random
from typing import List

class Tile:
    """Represents a tile in the world."""

    def __init__(self, height: int, moisture: int, temperature: int):
        self.height = height
        self.moisture = moisture
        self.temperature = temperature

    def __repr__(self) -> str:
        return (
            f"Tile(height={self.height}, moisture={self.moisture}, "
            f"temperature={self.temperature})"
        )

    @property
    def terrain(self) -> str:
        """Return a terrain type based on height, moisture and temperature."""
        if self.height <= 0:
            return "water"

        if self.height >= 4:
            return "snow" if self.temperature <= 1 else "mountain"

        if self.moisture <= 1:
            return "desert" if self.temperature >= 2 else "tundra"

        if self.moisture >= 3:
            return "rainforest" if self.temperature >= 3 else "forest"

        # Moderate moisture
        if self.temperature >= 3:
            return "savanna"
        if self.temperature <= 1:
            return "taiga"
        return "grass"


def generate_height_map(width: int, height: int, smoothing: int = 1, seed: int | None = None) -> List[List[int]]:
    """Generate a height map using a basic smoothing algorithm."""
    rng = random.Random(seed)
    height_map = [[rng.randint(0, 4) for _ in range(width)] for _ in range(height)]

    for _ in range(smoothing):
        new_map = [[0 for _ in range(width)] for _ in range(height)]
        for y in range(height):
            for x in range(width):
                neighbors = []
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < height and 0 <= nx < width:
                            neighbors.append(height_map[ny][nx])
                new_map[y][x] = round(sum(neighbors) / len(neighbors))
        height_map = new_map

    return height_map


def generate_moisture_map(width: int, height: int, smoothing: int = 1, seed: int | None = None) -> List[List[int]]:
    """Generate a moisture map using the same algorithm as heights."""
    return generate_height_map(width, height, smoothing=smoothing, seed=seed)


def generate_temperature_map(
    width: int, height: int, smoothing: int = 1, seed: int | None = None
) -> List[List[int]]:
    """Generate a temperature map using the same algorithm as heights."""
    return generate_height_map(width, height, smoothing=smoothing, seed=seed)


def _next_power_of_two(n: int) -> int:
    """Return the next power of two greater than or equal to n."""
    return 1 << (n - 1).bit_length()


def generate_height_map_fractal(width: int, height: int, roughness: float = 1.0, seed: int | None = None) -> List[List[int]]:
    """Generate a height map using the diamond-square algorithm."""
    rng = random.Random(seed)

    size = _next_power_of_two(max(width, height)) + 1
    grid = [[0.0 for _ in range(size)] for _ in range(size)]

    grid[0][0] = grid[0][-1] = grid[-1][0] = grid[-1][-1] = rng.random()

    step = size - 1
    scale = roughness
    while step > 1:
        half = step // 2
        # Diamond step
        for y in range(half, size - 1, step):
            for x in range(half, size - 1, step):
                avg = (
                    grid[y - half][x - half]
                    + grid[y - half][x + half]
                    + grid[y + half][x - half]
                    + grid[y + half][x + half]
                ) / 4.0
                grid[y][x] = avg + (rng.random() - 0.5) * scale

        # Square step
        for y in range(0, size, half):
            for x in range((y + half) % step, size, step):
                vals = []
                if y - half >= 0:
                    vals.append(grid[y - half][x])
                if y + half < size:
                    vals.append(grid[y + half][x])
                if x - half >= 0:
                    vals.append(grid[y][x - half])
                if x + half < size:
                    vals.append(grid[y][x + half])
                grid[y][x] = sum(vals) / len(vals) + (rng.random() - 0.5) * scale

        step = half
        scale /= 2.0

    # Normalize 0..1
    min_v = min(min(row) for row in grid)
    max_v = max(max(row) for row in grid)
    for y in range(size):
        for x in range(size):
            grid[y][x] = (grid[y][x] - min_v) / (max_v - min_v)

    height_map = [
        [int(round(grid[y][x] * 4)) for x in range(width)]
        for y in range(height)
    ]
    return height_map


def generate_moisture_map_fractal(width: int, height: int, roughness: float = 1.0, seed: int | None = None) -> List[List[int]]:
    """Generate a moisture map using the diamond-square algorithm."""
    return generate_height_map_fractal(width, height, roughness=roughness, seed=seed)


def generate_temperature_map_fractal(
    width: int, height: int, roughness: float = 1.0, seed: int | None = None
) -> List[List[int]]:
    """Generate a temperature map using the diamond-square algorithm."""
    return generate_height_map_fractal(width, height, roughness=roughness, seed=seed)


def generate_world(
    width: int,
    height: int,
    smoothing: int = 2,
    algorithm: str = "simple",
    seed: int | None = None,
    moisture_seed: int | None = None,
    temperature_seed: int | None = None,
) -> List[List[Tile]]:
    """Generate the world as a 2D grid of tiles."""
    if algorithm == "fractal":
        height_map = generate_height_map_fractal(width, height, seed=seed)
        moisture_map = generate_moisture_map_fractal(width, height, seed=moisture_seed)
        temperature_map = generate_temperature_map_fractal(
            width, height, seed=temperature_seed
        )
    else:
        height_map = generate_height_map(width, height, smoothing=smoothing, seed=seed)
        moisture_map = generate_moisture_map(width, height, smoothing=smoothing, seed=moisture_seed)
        temperature_map = generate_temperature_map(
            width, height, smoothing=smoothing, seed=temperature_seed
        )

    world = []
    for h_row, m_row, t_row in zip(height_map, moisture_map, temperature_map):
        world.append([Tile(h, m, t) for h, m, t in zip(h_row, m_row, t_row)])
    return world
