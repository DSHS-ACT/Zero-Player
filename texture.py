import imageio.v3 as iio
from OpenGL.GL import *
import numpy as np


class Texture:
    def __init__(self, path: str):
        img = np.flip(iio.imread(path), 0)

        print("이미지 위치: " + path + " 크기: " + str(img.shape))

        self.id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.id)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, img.shape[0], img.shape[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, img)
        self.unbind()

    def __del__(self):
        glDeleteTextures(1, self.id)

    def bind(self, slot: int = 0):
        assert slot < 32
        glActiveTexture(GL_TEXTURE0 + slot)
        glBindTexture(GL_TEXTURE_2D, self.id)

    def unbind(self):
        glBindTexture(GL_TEXTURE_2D, 0)
