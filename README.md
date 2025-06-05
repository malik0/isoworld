# isoworld

This repository contains a small isometric world generator written in Python. It
generates a grid of tiles with smoothed height, moisture and temperature values
and renders them in a basic ASCII isometric projection. Terrain is derived from
all three properties so worlds feature water, sand, desert, grass, forest,
mountain, snow and additional biomes such as tundra, taiga, savanna and
rainforest.

## Usage

Run the main script:

```bash
python main.py [--width N] [--height N] [--smoothing N]
               [--algorithm {simple,fractal}] [--seed SEED]
               [--moisture-seed SEED] [--temperature-seed SEED]
               [--color] [--plot] [--window]
```

The `--algorithm` option selects the height-map generator: the default "simple"
algorithm averages random values, while `fractal` uses a diamond-square
implementation for more natural terrain. `--seed`, `--moisture-seed` and
`--temperature-seed` allow deterministic height, moisture and temperature maps
respectively. Pass `--color` to render
ANSI-colored tiles. Use `--plot` to also save a 3D height map to `world.png`
(requires `matplotlib`). Use `--window` to open a simple interactive 3D view
powered by `tkinter`.


