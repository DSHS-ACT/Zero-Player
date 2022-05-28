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
from global_variables import *

window = None

def prepare_textuers(images):
    for image in images:
        created.append(Texture(image))
    for index, texture in enumerate(created):
        print("index:" + str(index))
        texture.bind(index)

def init_window():
    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    global window
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

    prepare_textuers(game.texture_list)

    shader.set_uniform1iv("tiles", 5, np.array([0, 1, 2, 3, 4], dtype=np.int32))

    vertex_array.unbind()
    vertex_buffer.unbind()
    index_buffer.unbind()
    shader.unbind()

    renderer = Renderer()

    while not glfw.window_should_close(window):
        renderer.clear()

        shader.bind()
        shader.set_uniform1f("width", get_width())
        shader.set_uniform1iv("world", 16 * 9, game.get_gpu_world())

        renderer.draw(vertex_array, index_buffer, shader)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()
    return


def main():
    init_window()


if __name__ == '__main__':
    main()
