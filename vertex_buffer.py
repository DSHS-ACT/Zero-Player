from OpenGL.GL import *


class VertexBuffer:
    def __init__(self, data, size: int):
        self.id = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.id)
        glBufferData(GL_ARRAY_BUFFER, size, data, GL_STATIC_DRAW)

    def __del__(self):
        glDeleteBuffers(1, self.id)

    def bind(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.id)

    def unbind(self):
        glBindBuffer(GL_ARRAY_BUFFER, 0)
