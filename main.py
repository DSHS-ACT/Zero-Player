import glfw
import imgui
import game
import inputhandler
import numpy as np
import os

from index_buffer import IndexBuffer
from renderer import Renderer
from shader import Shader
from texture import Texture
from vertex_array import VertexArray
from vertex_buffer import VertexBuffer
from vertex_buffer_layout import VertexBufferLayout
from global_variables import configuration
from OpenGL.GL import *
from imgui.integrations.glfw import GlfwRenderer

window = None


def bind_textures(to_load):
    for index, texture in enumerate(to_load):
        texture.bind(index + 1)


def init_window():
    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)

    global window
    window = glfw.create_window(1920, 1080, "Zero Player Game", glfw.get_primary_monitor(), None)
    if window is None:
        print("창 생성에 실패했습니다!")
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, inputhandler.on_key)
    glfw.set_mouse_button_callback(window, inputhandler.on_mouse)
    glfw.set_scroll_callback(window, inputhandler.on_mouse_wheel)

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

    imgui.create_context()
    io = imgui.get_io()

    io.display_size = 100, 100
    nanum_font = io.fonts.add_font_from_file_ttf("NanumSquareRoundR.ttf", 17, io.fonts.get_glyph_ranges_korean())
    io.fonts.get_tex_data_as_rgba32()

    impl = GlfwRenderer(window, False)

    Texture.create_textures()
    bind_textures(Texture.texture_list())

    # GPU 에 보내지는 유니폼은 슬롯 번호들의 배열
    shader.set_uniform1iv(
        "tiles", len(Texture.texture_list()) + 8,
        list(range(0, len(Texture.texture_list()) + 8))
    )

    vertex_array.unbind()
    vertex_buffer.unbind()
    index_buffer.unbind()
    shader.unbind()

    renderer = Renderer()

    print("최대 텍스쳐 갯수:", glGetIntegerv(GL_MAX_TEXTURE_IMAGE_UNITS))
    while not glfw.window_should_close(window):
        renderer.clear()

        impl.process_inputs()
        imgui.new_frame()

        shader.bind()
        shader.set_uniform1f("width", configuration.width)
        shader.set_uniform1iv("world", 16 * 9, game.get_gpu_world())

        renderer.draw(vertex_array, index_buffer, shader)

        configuration.frame_count += 1
        if configuration.frame_count % (60 / configuration.game_speed) == 0:
            game.tick()

        if configuration.show_debug_ui:
            debug_screen()
        if configuration.show_help:
            show_help()

        imgui.render()
        impl.render(imgui.get_draw_data())

        glfw.swap_buffers(window)
        glfw.poll_events()

    impl.shutdown()
    glfw.terminate()

    for texture in Texture.texture_list():
        texture.delete()
    return

def show_help():
    imgui.begin("제로 플레이어 게임 조작키")
    imgui.text("월드 테두리 이어 붙이기: U")
    imgui.text("디버그 GUI: -")
    imgui.text("이 창 띄우기/닫기: ?")
    imgui.text("격자 선 굵기 조절: 마우스 휠")
    imgui.text("게임 종료: ESC")
    imgui.text("게임 속도 가속: K")
    imgui.text("게임 속도 감속: L")
    imgui.text("시뮬레이션 시작: SPACE")
    imgui.end()

def debug_screen():
    imgui.begin("제로 플레이어 게임 디버그 UI")
    imgui.text("게임 속도: " + str(configuration.game_speed) + " x")
    if configuration.is_wrapping:
        imgui.text("월드 테두리 이어 붙임")
    else:
        imgui.text("월드 테두리 이어 붙이지 않음")

    imgui.image(1, 120, 120, (0, 1), (1, 0))
    for texture in Texture.texture_list():
        imgui.image(texture.id, 120, 120, (0, 1), (1, 0))

    imgui.end()

def main():
    print("PID:", os.getpid())
    init_window()


if __name__ == '__main__':
    main()
