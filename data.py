from tiles import *
from os.path import exists

def deserialize_to_world(world, file_path: str):
    if not exists(file_path):
        print("해당 파일을 찾을 수 없습니다!")
        return
    with open(file_path) as file:
        lines = [line.rstrip() for line in file]

    for line in lines:
        split = line.split(" ")
        x = int(split[0])
        y = int(split[1])
        if split[2] == "arrow":
            tile = Arrow(Texture.ARROW)
            direction = int(split[3])
            tile.direction = direction
        elif split[2] == "suicide":
            tile = Suicide(Texture.SUICIDE)
        elif split[2] == "lava":
            tile = Lava(Texture.LAVA)
        elif split[2] == "wall":
            tile = Wall(Texture.WALL)
        elif split[2] == "pushable":
            tile = Pushable(Texture.PUSHABLE)
        elif split[2] == "directional":
            tile = Directional(Texture.DIRECTIONAL)
            direction = int(split[3])
            tile.direction = direction

        assert tile is not None
        world[x][y] = tile

def serialize(world, save_to: str):
    with open(save_to, 'w+') as output:
        for x in range(0, 32):
            for y in range(0, 18):
                tile = world[x][y]
                if tile is not None:
                    output.write(tile.serialize() + "\n")
