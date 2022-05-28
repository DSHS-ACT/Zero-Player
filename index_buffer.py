from OpenGL.GL import *

UNSIGNED_INT_SIZE = 4


class IndexBuffer:
    def __init__(self, data, count: int):
        self.id = glGenBuffers(1)
        self.count = count
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.id)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.count * UNSIGNED_INT_SIZE, data, GL_STATIC_DRAW)

    def __del__(self):
        glDeleteBuffers(1, self.id)

    def bind(self):
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.id)

    def unbind(self):
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
