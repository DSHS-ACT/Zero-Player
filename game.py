import numpy as np

from main import configuration
import tiles
from texture import Texture

world_tiles = np.empty((16, 9), dtype=Texture)


# TODO 화살표 방향으로 이동하는 타일, 키보드 방향키를 눌러 방향을 고른다
# TODO 무작위로 움직이는 타일
# TODO 배속시키는 키보드 키

def clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)


def get_gpu_world():
    # GPU 에 보낼 숫자 버퍼 미리 마련
    processor = np.vectorize(tiles.Tile.to_int)
    to_send = processor(world_tiles)

    return to_send.flatten(order="F")


def tick():
    if not configuration.ticking:
        return
    ticked = []
    for x in range(0, 16):
        for y in range(0, 9):
            tile = world_tiles[x][y]
            if tile is None:
                continue
            if tile in ticked:
                continue

            tile.tick()
            ticked.append(tile)
            print("방향:", tile.direction)
            if configuration.is_wrapping:
                next_position = (x + tile.velocity[0]) % 16, (y + tile.velocity[1]) % 9
            else:
                next_position = (clamp(x + tile.velocity[0], 0, 15), clamp(y + tile.velocity[1], 0, 8))

            is_different = (x, y) != next_position
            if world_tiles[next_position[0]][next_position[1]] is None:
                world_tiles[next_position[0]][next_position[1]] = tile
                world_tiles[x][y] = None
            else:
                if is_different:
                    collided = world_tiles[next_position[0]][next_position[1]]
                    tile.pushing(collided)
