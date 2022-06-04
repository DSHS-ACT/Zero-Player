import imageio.v3 as iio
from OpenGL.GL import *
import numpy as np


class Texture:
    EMPTY = None
    ARROW = None
    QUESTION = None

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

    @staticmethod
    def create_textures():
        Texture.EMPTY = Texture("empty.png")
        Texture.ARROW = Texture("1.png")
        Texture.QUESTION = Texture("2.png")

    @staticmethod
    def texture_list():
        return [Texture.EMPTY, Texture.ARROW, Texture.QUESTION]
