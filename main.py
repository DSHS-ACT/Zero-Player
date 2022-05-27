import glfw
import imageio
import numpy as np
from OpenGL.GL import *

import game
import keyhandler
from index_buffer import IndexBuffer
from texture import Texture
from vertex_buffer import VertexBuffer

window = None
width = 3

FLOAT_SIZE = 4

def __read_file__(path: str):
    file = open(path)
    contents = file.read()
    file.close()
    return contents

def __compile_shader__(shader_type, source: str):
    shader_id = glCreateShader(shader_type)
    glShaderSource(shader_id, source)
    glCompileShader(shader_id)

    result = glGetShaderiv(shader_id, GL_COMPILE_STATUS)
    if result == GL_FALSE:
        log = glGetShaderInfoLog(shader_id)
        if log:
            print("쉐이더 컴파일 오류!")
            if shader_type == GL_VERTEX_SHADER:
                print("Vertex shader")
            elif shader_type == GL_FRAGMENT_SHADER:
                print("Fragment shader")
            glDeleteShader(shader_id)
            raise Exception(log)

    return shader_id


def __create_shader__(vertex_src: str, fragment_src: str):
    shader_program = glCreateProgram()
    vertex_shader = __compile_shader__(GL_VERTEX_SHADER, vertex_src)
    fragment_shader = __compile_shader__(GL_FRAGMENT_SHADER, fragment_src)

    glAttachShader(shader_program, vertex_shader)
    glAttachShader(shader_program, fragment_shader)
    glLinkProgram(shader_program)
    glValidateProgram(shader_program)

    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    program_log = glGetProgramInfoLog(shader_program)

    if program_log:
        print("쉐이더 프로그램 링크 오류")
        raise Exception(program_log)
    return shader_program


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
    glfw.set_key_callback(window, keyhandler.on_key)

    shader_program = __create_shader__(__read_file__("vertex.vert"), __read_file__("fragment.frag"))

    positions = np.array([
        -0.5, -0.5,
        0.5, -0.5,
        0.5, 0.5,
        -0.5, 0.5
    ], dtype=np.float32)

    indices = np.array([
        0, 1, 2,
        2, 3, 0
    ], dtype=np.uint32)

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vertex_buffer = VertexBuffer(positions, FLOAT_SIZE * 8)
    vertex_buffer.bind()

    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 2 * FLOAT_SIZE, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    #glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4 * FLOAT_SIZE, ctypes.c_void_p(2 * FLOAT_SIZE))
    #glEnableVertexAttribArray(1)

    index_buffer = IndexBuffer(indices, 6)


    glUseProgram(shader_program)
    map_uniform_location = glGetUniformLocation(shader_program, "map")
    width_uniform_location = glGetUniformLocation(shader_program, "width")
    texture_uniform_location = glGetUniformLocation(shader_program, "input_texture")

    texture = Texture("1.png")
    texture.bind(0)
    glUniform1i(texture_uniform_location, 0)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        glUseProgram(shader_program)

        glUniform1fv(map_uniform_location, 16 * 9, game.world)
        glUniform1f(width_uniform_location, width)

        glBindVertexArray(vao)
        index_buffer.bind()

        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glDeleteProgram(shader_program)
    glfw.terminate()
    return


def main():
    init_window()


if __name__ == '__main__':
    main()
