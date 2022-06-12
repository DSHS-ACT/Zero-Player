import enums
from texture import Texture
import uuid
import game


# 0, 1, 2, 3 중 하나인 direction 을 속도로 바꿔주는 함수
def direction_to_velocity(direction: int):
    if direction == enums.UP:
        return 0, -1
    elif direction == enums.RIGHT:
        return 1, 0
    elif direction == enums.DOWN:
        return 0, 1
    elif direction == enums.LEFT:
        return -1, 0


# 타일의 기반을 정의하는 클래스
class Tile:
    # 해당 클래스를 초기화하는 함수, 타일의 텍스처를 인자로 받는다.
    def __init__(self, texture: Texture):
        self.velocity = (0, 0)
        self.direction = enums.UP
        self.texture = texture
        # UUID는 64비트 길이의 절때 겹칠 일이 없는 고유한 무작위로 생성되는 난수이다.
        # 이를 사용하여 생성된 타일들을 구분한다.
        self.uuid = uuid.uuid4()
        self.is_alive = True

    # 해당 타일의 위치를 받아오는 함수. 타일은 위치 데이터를 가지고 있지 않기에 UUID 를 비교하여야 한다.
    def get_position(self):
        for x in range(0, 32):
            for y in range(0, 18):
                if game.world_tiles[x][y] is None:
                    continue
                if game.world_tiles[x][y].uuid == self.uuid:
                    return x, y
        # 예외 발생시키지 말고 (-1, -1) 를 반환해야 할려나?
        raise Exception("월드상에 존재하지 않는 타일이 있습니다!")

    # 타일의 시간을 진행시키는 함수. game.py 에서 이 함수를 호출한다.
    def tick(self, x, y):
        pass

    # 다른 타일과 충돌했을 때, 이 타일이 다른 타일 안으로 밀고 들어가려고 할때 호출되는 함수
    def pushing(self, other):
        pass

    def when_pushed(self, other):
        pass

    # 이 타일의 정보를 GPU가 알아들을 수 있는 바이트로 변환하는 함수
    def to_int(self):
        if self is None:
            return Texture.EMPTY.slot
        else:
            element = self.texture.slot
            element += self.direction << 5
            return element

    def get_next(self):
        position = self.get_position()
        return position[0] + self.velocity[0], position[1] + self.velocity[1]

class Arrow(Tile):
    def tick(self, x, y):
        self.velocity = direction_to_velocity(self.direction)

        move_result = game.try_move(self, self.velocity)
        if move_result is not None:
            move_result.when_pushed(self)
            if isinstance(move_result, Pushable):
                game.try_move(self, self.velocity)
            else:
                self.pushing(move_result)


    def pushing(self, other):
        assert isinstance(other, Tile)
        self.direction += 2
        self.direction %= 4


class Suicide(Tile):
    def when_pushed(self, other):
        other.is_alive = False
        self.is_alive = False


class Lava(Tile):
    def when_pushed(self, other):
        other.is_alive = False


class Wall(Tile):
    pass


class Pushable(Tile):
    def __init__(self, texture: Texture):
        super().__init__(texture)
        self.pushed = False

    def tick(self, x, y):
        if not self.pushed:
            self.velocity = (0, 0)
        self.pushed = False

    def when_pushed(self, other):
        self.pushed = True
        self.velocity = other.velocity

        next_position = self.get_next()
        at_next = game.world_tiles[next_position[0]][next_position[1]]
        if at_next is not None:
            at_next.when_pushed(self)
        if game.world_tiles[next_position[0]][next_position[1]] is None:
            game.try_move(self, self.velocity)




