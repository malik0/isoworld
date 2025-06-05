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

## Example worlds

A few example commands demonstrate how the generator can produce different terrain
styles. The choice of seeds influences the result so feel free to experiment.

- **Mountainous world** using the fractal algorithm
  ```bash
  python main.py --width 20 --height 20 --algorithm fractal --seed 42 --color
  ```
- **Desert world** with hot and dry conditions
  ```bash
  python main.py --width 20 --height 20 --seed 1 --moisture-seed 1 --temperature-seed 999 --color
  ```
- **Snowy tundra**
  ```bash
  python main.py --width 20 --height 20 --moisture-seed 5 --temperature-seed 0 --color
  ```
- **Dense rainforest**
  ```bash
  python main.py --width 20 --height 20 --seed 8 --moisture-seed 999 --temperature-seed 999 --color
  ```

