import enums
import tiles
from tiles import *
from os.path import exists

def deserialize_to_world(world, file_path: str):
    if not exists(file_path):
        print("해당 파일을 찾을 수 없습니다!")
        return
    with open(file_path) as file:
        lines = [line.rstrip() for line in file]

    portals_to_resolve = []

    for line in lines:
        split = line.split(" ")
        x = int(split[0])
        y = int(split[1])
        if split[2] == "arrow":
            tile = Arrow(Texture.ARROW)
            direction = int(split[3])
            if split[4] == "FIXED":
                is_fixed = True
            else:
                is_fixed = False
            tile.direction = direction
            tile.is_fixed = is_fixed
        elif split[2] == "suicide":
            tile = Suicide(Texture.SUICIDE)
            if split[3] == "FIXED":
                is_fixed = True
            else:
                is_fixed = False
            tile.is_fixed = is_fixed
        elif split[2] == "lava":
            tile = Lava(Texture.LAVA)
            if split[3] == "FIXED":
                is_fixed = True
            else:
                is_fixed = False
            tile.is_fixed = is_fixed
        elif split[2] == "wall":
            tile = Wall(Texture.WALL)
            if split[3] == "FIXED":
                is_fixed = True
            else:
                is_fixed = False
            tile.is_fixed = is_fixed
        elif split[2] == "pushable":
            tile = Pushable(Texture.PUSHABLE)
            if split[3] == "FIXED":
                is_fixed = True
            else:
                is_fixed = False
            tile.is_fixed = is_fixed
        elif split[2] == "directional":
            tile = Directional(Texture.DIRECTIONAL)
            direction = int(split[3])
            if split[4] == "FIXED":
                is_fixed = True
            else:
                is_fixed = False
            tile.direction = direction
            tile.is_fixed = is_fixed
        elif split[2] == "star":
            tile = Star(Texture.STAR)
            if split[3] == "FIXED":
                is_fixed = True
            else:
                is_fixed = False
            tile.is_fixed = is_fixed
        elif split[2] == "mine":
            tile = Mine(Texture.MINE)
            if split[3] == "FIXED":
                is_fixed = True
            else:
                is_fixed = False
            tile.is_fixed = is_fixed
        elif split[2] == "key":
            tile = Key(Texture.KEY)
            if split[3] == "FIXED":
                is_fixed = True
            else:
                is_fixed = False
            tile.is_fixed = is_fixed
        elif split[2] == "lock":
            tile = Lock(Texture.LOCK)
            if split[3] == "FIXED":
                is_fixed = True
            else:
                is_fixed = False
            tile.is_fixed = is_fixed
        elif split[2] == "portal":
            if split[4] == "orange":
                tile = Portal(Texture.PORTAL_ORANGE)
            else:
                tile = Portal(Texture.PORTAL_BLUE)
            if split[3] == "FIXED":
                is_fixed = True
            else:
                is_fixed = False
            tile.is_fixed = is_fixed
            opposite_x = int(split[5])
            opposite_y = int(split[6])

            if world[opposite_x][opposite_y] is None:
                portals_to_resolve.append(tile)
            else:
                opposite = world[opposite_x][opposite_y]
                tile.opposite = opposite
                opposite.opposite = tile
                portals_to_resolve.remove(opposite)
        elif split[2] == "duplicate":
            tile = Duplicate(Texture.DUPLICATE)
            if split[3] == "FIXED":
                is_fixed = True
            else:
                is_fixed = False
            tile.is_fixed = is_fixed
        elif split[2] == "rotate":
            direction = int(split[3])
            if direction == enums.RIGHT:
                tile = Rotate(Texture.ROTATE_RIGHT)
                tile.direction = enums.RIGHT
            else:
                tile = Rotate(Texture.ROTATE_LEFT)
                tile.direction = enums.LEFT

            if split[4] == "FIXED":
                is_fixed = True
            else:
                is_fixed = False
            tile.is_fixed = is_fixed

        assert tile is not None
        world[x][y] = tile
    if len(portals_to_resolve) != 0:
        raise Exception("맵 파일에 끊어진 포탈이 있습니다!")

def serialize(world, save_to: str):
    with open(save_to, 'w+') as output:
        for x in range(0, 32):
            for y in range(0, 18):
                tile = world[x][y]
                if tile is not None and not isinstance(tile, tiles.Explosion):
                    if isinstance(tile, Portal) and tile.opposite is None:
                        continue
                    output.write(tile.serialize() + "\n")
