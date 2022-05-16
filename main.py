import glfw
from OpenGL.GL import *

import keyhandler

window = None


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
    glfw.set_key_callback(window, keyhandler.on_key)

    vertex_file = open("vertex.vert")
    vertex_src = vertex_file.read()
    vertex_file.close()

    fragment_file = open("fragment.frag")
    fragment_src = fragment_file.read()
    fragment_file.close()

    vertex_shader = glCreateShader(GL_VERTEX_SHADER)
    fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(vertex_shader, 1, vertex_src, None)
    glShaderSource(fragment_shader, 1, fragment_src, None)
    glCompileShader(vertex_shader)
    glCompileShader(fragment_shader)

    shader_program = glCreateProgram()
    glAttachShader(shader_program, vertex_shader)
    glAttachShader(shader_program, fragment_shader)
    glLinkProgram(shader_program)

    vertices = [
        -0.5, -0.5, 0,
        0.5, -0.5, 0,
        0, 0.5, 0
    ]
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertices) * 8, vertices, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_DOUBLE, 3 * 8, 0)
    glEnableVertexAttribArray(0)
    glUseProgram(shader_program)
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    while not glfw.window_should_close(window):
        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT)

        glDrawArrays(GL_TRIANGLES, 0, 3)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()
    return



def main():
    init_window()


if __name__ == '__main__':
    main()
