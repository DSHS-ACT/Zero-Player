import numpy as np

from main import configuration
import tiles
from texture import Texture

world_tiles = np.empty((32, 18), dtype=Texture)

"""
값을 min_value <= num <= max_value 사이로 만드는 함수
"""
def clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)

"""
world 배열을 GPU에 알맞은 형태로 가공하는 함수
"""
def get_gpu_world():
    # GPU 에 보낼 숫자 버퍼 미리 마련
    processor = np.vectorize(tiles.Tile.to_int)
    to_send = processor(world_tiles)

    return to_send.flatten(order="F")

"""
월드의 시간을 진행시키는 함수
이 함수가 발동될 프레임 빈도는 L 또는 K 를 눌러 다음중 하나로 설정할 수 있다: [120, 60, 40, 30, 20, 15, 10, 5, 4, 3, 2]
기본적으론 60이다, 게임이 60프레임이니, 1초에 한번 발동된다.
"""
def tick():
    if not configuration.ticking:
        return

    ticked = []
    for x in range(0, 32):
        for y in range(0, 18):
            tile = world_tiles[x][y]

            if tile is None:
                continue
            if tile in ticked:
                continue

            tile.tick(x, y)
            ticked.append(tile)
            print("방향:", tile.direction)

            if configuration.is_wrapping:
                next_position = (x + tile.velocity[0]) % 32, (y + tile.velocity[1]) % 18
            else:
                next_position = (clamp(x + tile.velocity[0], 0, 31), clamp(y + tile.velocity[1], 0, 17))

            is_different = (x, y) != next_position
            if world_tiles[next_position[0]][next_position[1]] is None:
                world_tiles[next_position[0]][next_position[1]] = tile
                world_tiles[x][y] = None
            else:
                if is_different:
                    collided = world_tiles[next_position[0]][next_position[1]]
                    tile.pushing(collided)
