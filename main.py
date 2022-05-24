import glfw
import imageio
import numpy as np
from OpenGL.GL import *

import game
import keyhandler

window = None
width = 3

texture_count = 0


def register_images():
    global texture_count
    if texture_count >= 32:
        raise OverflowError("최대 텍스쳐 갯수에 도달했습니다! (atlas 안써...)")
    img = imageio.v2.imread("1.png")
    texture_id = glGenTextures(1)
    glActiveTexture(GL_TEXTURE0 + texture_count)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 120, 120, 0, GL_RGB, GL_UNSIGNED_BYTE, img)
    texture_count += 1


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

    vertex_file = open("vertex.vert")
    vertex_src = vertex_file.read()
    vertex_file.close()

    fragment_file = open("fragment.frag")
    fragment_src = fragment_file.read()
    fragment_file.close()

    vertex_shader = glCreateShader(GL_VERTEX_SHADER)
    fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)

    glShaderSource(vertex_shader, vertex_src)
    glShaderSource(fragment_shader, fragment_src)
    glCompileShader(vertex_shader)
    glCompileShader(fragment_shader)

    vertex_log = glGetShaderInfoLog(vertex_shader)
    if vertex_log:
        print("Vertex 쉐이더 컴파일 오류")
        raise Exception(vertex_log)
    fragment_log = glGetShaderInfoLog(fragment_shader)
    if fragment_log:
        print("Fragment 쉐이더 컴파일 오류")
        raise Exception(fragment_log)

    shader_program = glCreateProgram()
    glAttachShader(shader_program, vertex_shader)
    glAttachShader(shader_program, fragment_shader)
    glLinkProgram(shader_program)

    program_log = glGetProgramInfoLog(shader_program)

    if program_log:
        print("쉐이더 프로그램 링크 오류")
        raise Exception(program_log)

    register_images()

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)
    vertices = np.array([
        -1, -1, 0.0,
        1, -1, 0.0,
        -1, 1, 0.0,
        1, -1, 0,
        -1, 1, 0,
        1, 1, 0
    ], dtype=np.float32)

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(vertices), vertices, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * 4, None)
    glEnableVertexAttribArray(0)
    glUseProgram(shader_program)
    map_uniform_location = glGetUniformLocation(shader_program, "map")
    width_uniform_location = glGetUniformLocation(shader_program, "width")

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)

        glUniform1fv(map_uniform_location, 16 * 9, game.world)
        glUniform1f(width_uniform_location, width)

        glDrawArrays(GL_TRIANGLES, 0, 6)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()
    return


def main():
    init_window()


if __name__ == '__main__':
    main()
