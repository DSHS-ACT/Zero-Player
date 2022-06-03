import glfw
import numpy as np
from OpenGL.GL import *

import game
import global_variables
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
        registered_textures.append(Texture(image))
    for index, texture in enumerate(registered_textures):
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

    shader.set_uniform1iv("tiles", len(global_variables.registered_textures),
                          np.array(range(0, len(global_variables.registered_textures)), dtype=np.int32)
                          )

    vertex_array.unbind()
    vertex_buffer.unbind()
    index_buffer.unbind()
    shader.unbind()

    renderer = Renderer()

    print("최대 텍스쳐 갯수:", glGetIntegerv(GL_MAX_TEXTURE_IMAGE_UNITS))

    while not glfw.window_should_close(window):
        renderer.clear()

        shader.bind()
        shader.set_uniform1f("width", get_width())
        shader.set_uniform1iv("world", 16 * 9, game.get_gpu_world())

        renderer.draw(vertex_array, index_buffer, shader)

        glfw.swap_buffers(window)
        glfw.poll_events()
        set_frame_count(get_frame_count() + 1)
        if get_frame_count() % (60 / get_game_speed()) == 0:
            game.tick()

    glfw.terminate()
    for texture in registered_textures:
        texture.delete()
    return


def main():
    init_window()


if __name__ == '__main__':
    main()
