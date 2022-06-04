from OpenGL.GL import *


class VertexBufferElement:
    def __init__(self, type_number: int, count: int, normalized: bool):
        self.type_number = type_number
        self.count = count
        self.normalized = normalized

    @staticmethod
    def get_size(type_number: int):
        if type_number == GL_FLOAT:
            return 4
        elif type_number == GL_UNSIGNED_INT:
            return 4
        elif type_number == GL_UNSIGNED_BYTE:
            return 1
        else:
            assert False


class VertexBufferLayout:
    def __init__(self):
        self.elements = []
        self.stride = 0

    def push(self, type_number: int, count: int):
        self.elements.append(VertexBufferElement(type_number, count, False))
        self.stride += VertexBufferElement.get_size(type_number) * count
