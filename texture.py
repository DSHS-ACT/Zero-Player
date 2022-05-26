import imageio as iio
from OpenGL.GL import *

class Texture:
    def __init__(self, path: str):
        img = iio.v2.imread(path)
        self.id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.id)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, img.shape[0], img.shape[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, img)
        glBindTexture(GL_TEXTURE_2D, 0)

    def __del__(self):
        glDeleteTextures(1, self.id)

    def bind(self, slot: int):
        assert slot < 32
        glActiveTexture(GL_TEXTURE0 + slot)
        glBindTexture(GL_TEXTURE_2D, self.id)

    def unbind(self):
        glBindTexture(GL_TEXTURE_2D, 0)
