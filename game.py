import numpy as np

from global_variables import configuration
from texture import Texture
import simpleaudio as sa

world_tiles = np.empty((32, 18), dtype=np.object)

# 현재 마우스에 잡고 있는 타일
holding = None

"""
값을 min_value <= num <= max_value 사이로 만드는 함수
"""
def clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)

def correct_position(position):
    if configuration.is_wrapping:
        next_position = position[0] % 32, position[1] % 18
    else:
        next_position = (clamp(position[0], 0, 31), clamp(position[1], 0, 17))
    return next_position

"""
world 배열을 GPU에 알맞은 형태로 가공하는 함수
"""
def get_gpu_world():
    # GPU 에 보낼 숫자 버퍼 미리 마련
    flattened = world_tiles.flatten(order="F")
    return list(map(lambda tile: tile.to_int() if (tile is not None) else Texture.EMPTY.slot, flattened))

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

    for dead in filter(lambda tile: tile is not None and not tile.is_alive, world_tiles.flatten()):
        position = dead.get_position()
        world_tiles[position[0]][position[1]] = None


def try_move(tile):
    position = tile.get_position()
    next_position = correct_position(tile.get_next())

    if world_tiles[next_position[0]][next_position[1]] is not None:
        return world_tiles[next_position[0]][next_position[1]]
    world_tiles[position[0]][position[1]] = None
    world_tiles[next_position[0]][next_position[1]] = tile
    return None


def play_wav(path: str):
    player = sa.WaveObject.from_wave_file(path)
    player.play()

def clear_level():
    for x in range(0, 32):
        for y in range(0, 18):
            world_tiles[x][y] = None
