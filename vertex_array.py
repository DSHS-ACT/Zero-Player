from vertex_buffer import VertexBuffer
from vertex_buffer_layout import VertexBufferLayout, VertexBufferElement
from OpenGL.GL import *


class VertexArray:
    def __init__(self):
        self.id = glGenVertexArrays(1)

    def __del__(self):
        glDeleteVertexArrays(1, self.id)

    def add_buffer(self, buffer: VertexBuffer, layout: VertexBufferLayout):
        self.bind()
        buffer.bind()
        elements = layout.elements
        offset = 0
        for idx, element in enumerate(elements):
            glEnableVertexAttribArray(idx)
            gl_normalized = GL_TRUE
            if not element.normalized:
                gl_normalized = GL_FALSE
            glVertexAttribPointer(idx, element.count, element.type_number, gl_normalized, layout.stride,
                                  ctypes.c_void_p(offset))
            offset += element.count * VertexBufferElement.get_size(element.type_number)

    def bind(self):
        glBindVertexArray(self.id)

    def unbind(self):
        glBindVertexArray(0)
