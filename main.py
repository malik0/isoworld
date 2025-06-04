import argparse
from isoworld.world import generate_world
from isoworld.render import render_isometric, render_3d_plot, render_3d_window

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate and render an isometric world")
    parser.add_argument("--width", type=int, default=10, help="world width")
    parser.add_argument("--height", type=int, default=10, help="world height")
    parser.add_argument("--smoothing", type=int, default=2, help="smoothing rounds")
    parser.add_argument(
        "--algorithm",
        choices=["simple", "fractal"],
        default="simple",
        help="height generation algorithm",
    )
    parser.add_argument("--seed", type=int, default=None, help="random seed")
    parser.add_argument(
        "--moisture-seed", type=int, default=None, help="seed for moisture map"
    )
    parser.add_argument(
        "--temperature-seed", type=int, default=None, help="seed for temperature map"
    )
    parser.add_argument("--color", action="store_true", help="use ANSI colors")
    parser.add_argument("--plot", action="store_true", help="save a 3D plot to world.png")
    parser.add_argument("--window", action="store_true", help="display a 3D window")
    args = parser.parse_args()

    world = generate_world(
        args.width,
        args.height,
        smoothing=args.smoothing,
        algorithm=args.algorithm,
        seed=args.seed,
        moisture_seed=args.moisture_seed,
        temperature_seed=args.temperature_seed,
    )
    print(render_isometric(world, color=args.color))
    if args.window:
        try:
            render_3d_window(world)
        except RuntimeError as exc:
            print(exc)
    if args.plot:
        try:
            path = render_3d_plot(world)
            print(f"Saved 3D plot to {path}")
        except RuntimeError as exc:
            print(exc)
