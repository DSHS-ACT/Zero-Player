import glfw
import numpy as np
from OpenGL.GL import *

import game
import inputhandler
from index_buffer import IndexBuffer
from renderer import Renderer
from shader import Shader
from texture import Texture
from vertex_array import VertexArray
from vertex_buffer import VertexBuffer
from vertex_buffer_layout import VertexBufferLayout

window = None
width = 3.0

def init_window():
    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    global window
    global width
    window = glfw.create_window(1920, 1080, "Zero Player Game", glfw.get_primary_monitor(), None)
    if window is None:
        print("창 생성에 실패했습니다!")
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, inputhandler.on_key)
    glfw.set_mouse_button_callback(window, inputhandler.on_mouse)

    positions = np.array([
        -1.0, -1.0, 0.0, 0.0,
        1.0, -1.0, 1.0, 0.0,
        1.0, 1.0, 1.0, 1.0,
        -1.0, 1.0, 0.0, 1.0
    ], dtype=np.float32)

    indices = np.array([
        0, 1, 2,
        2, 3, 0
    ], dtype=np.uint32)

    vertex_array = VertexArray()
    vertex_buffer = VertexBuffer(positions, positions.nbytes)
    vertex_buffer_layout = VertexBufferLayout()
    vertex_buffer_layout.push(GL_FLOAT, 2)
    vertex_buffer_layout.push(GL_FLOAT, 2)
    vertex_array.add_buffer(vertex_buffer, vertex_buffer_layout)

    index_buffer = IndexBuffer(indices, 6)

    shader = Shader("vertex.vert", "fragment.frag")
    shader.bind()

    texture0 = Texture("0.png")
    texture1 = Texture("1.png")
    texture2 = Texture("2.png")
    texture3 = Texture("3.png")
    texture4 = Texture("4.png")

    texture0.bind(0)
    texture1.bind(1)
    texture2.bind(2)
    texture3.bind(3)
    texture4.bind(4)

    shader.set_uniform1iv("tiles", 5, np.array([0, 1, 2, 3, 4], dtype=np.int32))

    vertex_array.unbind()
    vertex_buffer.unbind()
    index_buffer.unbind()
    shader.unbind()

    renderer = Renderer()

    while not glfw.window_should_close(window):
        renderer.clear()

        shader.bind()
        shader.set_uniform1f("width", width)
        shader.set_uniform1iv("world", 16 * 9, game.get_gpu_world())

        renderer.draw(vertex_array, index_buffer, shader)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()
    return


def main():
    init_window()

def set_width(w):
    global width
    width = w

def get_width():
    return width


if __name__ == '__main__':
    main()
