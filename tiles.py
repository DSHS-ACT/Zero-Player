import random
import enums
from texture import Texture
import uuid
import game


def direction_to_velocity(direction: int):
    if direction == enums.UP:
        return 0, -1
    elif direction == enums.RIGHT:
        return 1, 0
    elif direction == enums.DOWN:
        return 0, 1
    elif direction == enums.LEFT:
        return -1, 0


class Tile:
    def __init__(self, texture: Texture):
        self.velocity = (0, 0)
        self.direction = enums.UP
        self.texture = texture
        self.uuid = uuid.uuid4()

    def get_position(self):
        for x in range(0, 16):
            for y in range(0, 9):
                if game.world_tiles[x][y].uuid == self.uuid:
                    return x, y
        # 예외 발생시키지 말고 (-1, -1) 를 반환해야 할려나?
        raise Exception("월드상에 존재하지 않는 타일이 있습니다!")

    def tick(self):
        pass

    def pushing(self, other):
        assert isinstance(other, Tile)
        self.direction += 2
        self.direction %= 4
        pass

    def to_int(self):
        if self is None:
            return Texture.EMPTY.slot
        else:
            element = self.texture.slot
            element += self.direction << 5
            return element


class Arrow(Tile):
    def tick(self):
        self.velocity = direction_to_velocity(self.direction)


class Question(Tile):
    def tick(self):
        current_direction = random.randint(0, 3)
        self.velocity = direction_to_velocity(current_direction)
