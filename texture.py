import imageio.v3 as iio
from OpenGL.GL import *
import numpy as np

# ZPG 의 텍스처를 책임지는 클래스
# 새로운 텍스쳐를 추가하고 싶으면, QUESTION = None 과 같이
class Texture:
    # 현재 게임에서 사용하는 텍스쳐들
    EMPTY = None
    ARROW = None
    QUESTION = None
    SUICIDE = None
    LAVA = None
    WALL = None
    PUSHABLE = None
    DIRECTIONAL = None
    STAR = None
    MINE = None
    EXPLOSION = None
    KEY = None
    LOCK = None
    PORTAL_ORANGE = None
    PORTAL_BLUE = None

    # 현재 게임에서 사용하는 텍스쳐들이 들어있는 리스트, create_texture 정적 함수가 호출되면 초기화된다
    TEXTURE_LIST = None

    def __init__(self, path: str):
        img = np.flip(iio.imread(path), 0)
        self.id = glGenTextures(1)
        self.path = path
        self.slot = -1

        print("이미지 위치: " + self.path + " 크기: " + str(img.shape) + " 아이디: " + str(self.id))
        glBindTexture(GL_TEXTURE_2D, self.id)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, img.shape[0], img.shape[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, img)
        self.unbind()

    def delete(self):
        glDeleteTextures(1, self.id)

    def bind(self, slot: int = 0):
        assert slot < 32
        print("텍스쳐", self.path, "가", slot, "번 텍스쳐 슬롯에 바인드됨!")
        glActiveTexture(GL_TEXTURE0 + slot)
        glBindTexture(GL_TEXTURE_2D, self.id)
        self.slot = slot

    def unbind(self):
        glBindTexture(GL_TEXTURE_2D, 0)
        self.slot = -1

    def __deepcopy__(self, memodict={}):
        return self

    # 클래스를 등록하고 텍스처 리스트를 구성하는 함수
    @staticmethod
    def create_textures():
        Texture.EMPTY = Texture("empty.png")
        Texture.ARROW = Texture("1.png")
        Texture.QUESTION = Texture("2.png")
        Texture.SUICIDE = Texture("5.png")
        Texture.LAVA = Texture("6.png")
        Texture.WALL = Texture("7.png")
        Texture.PUSHABLE = Texture("pushable.png")
        Texture.DIRECTIONAL = Texture("directional.png")
        Texture.STAR = Texture("star.png")
        Texture.MINE = Texture("mine.png")
        Texture.EXPLOSION = Texture("explosion.png")
        Texture.KEY = Texture("key.png")
        Texture.LOCK = Texture("lock.png")
        Texture.PORTAL_ORANGE = Texture("portal_orange.png")
        Texture.PORTAL_BLUE = Texture("portal_blue.png")
        Texture.TEXTURE_LIST = [Texture.EMPTY, Texture.ARROW, Texture.QUESTION, Texture.SUICIDE, Texture.LAVA,
                                Texture.WALL, Texture.PUSHABLE, Texture.DIRECTIONAL, Texture.STAR, Texture.MINE,
                                Texture.EXPLOSION, Texture.KEY, Texture.LOCK, Texture.PORTAL_ORANGE,
                                Texture.PORTAL_BLUE]
