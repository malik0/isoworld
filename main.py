from isoworld.world import generate_world
from isoworld.render import render_isometric

if __name__ == "__main__":
    width = 10
    height = 10
    world = generate_world(width, height)
    print(render_isometric(world))
