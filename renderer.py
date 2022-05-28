from index_buffer import IndexBuffer
from shader import Shader
from vertex_array import VertexArray
from OpenGL.GL import *


class Renderer:
    def clear(self):
        glClear(GL_COLOR_BUFFER_BIT)

    def draw(self, vertex_array: VertexArray, index_buffer: IndexBuffer, shader: Shader):
        shader.bind()
        vertex_array.bind()
        index_buffer.bind()
        glDrawElements(GL_TRIANGLES, index_buffer.count, GL_UNSIGNED_INT, None)
