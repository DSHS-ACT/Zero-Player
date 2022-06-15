import os

import glfw
import imgui
import numpy as np
from OpenGL.GL import *
from imgui.integrations.glfw import GlfwRenderer

import data
import inputhandler
from global_variables import global_infos
from index_buffer import IndexBuffer
from renderer import Renderer
from shader import Shader
from stage_tracker import Stage1
from tiles import *
from vertex_array import VertexArray
from vertex_buffer import VertexBuffer
from vertex_buffer_layout import VertexBufferLayout

window = None

# afasdfsdfsadfsdf
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

    global_infos.window = window
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

    imgui.create_context()

    global_infos.imgui_io = imgui.get_io()

    global_infos.imgui_io.display_size = 100, 100
    nanum_font = global_infos.imgui_io.fonts.add_font_from_file_ttf("NanumSquareRoundR.ttf", 17,
                                                       global_infos.imgui_io.fonts.get_glyph_ranges_korean())
    global_infos.imgui_io.fonts.get_tex_data_as_rgba32()

    impl = GlfwRenderer(window, False)

    Texture.create_textures()
    bind_textures(Texture.TEXTURE_LIST)

    shader = Shader("vertex.vert", "fragment.frag")
    shader.bind()

    # GPU 에 보내지는 유니폼은 슬롯 번호들의 배열
    shader.set_uniform1iv(
        "tiles", len(Texture.TEXTURE_LIST) + 8,
        list(range(0, len(Texture.TEXTURE_LIST) + 8))
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
        shader.set_uniform1f("width", global_infos.width)
        shader.set_uniform1iv("world", 32 * 18, game.get_gpu_world())
        if game.holding is not None:
            shader.set_uniform1i("holding", game.holding.to_int())
        else:
            shader.set_uniform1i("holding", -1)

        mouse_x, mouse_y = glfw.get_cursor_pos(window)
        shader.set_uniform2f("mouse_pos", mouse_x, mouse_y)

        renderer.draw(vertex_array, index_buffer, shader)

        global_infos.frame_count += 1
        if global_infos.frame_count % (60 / global_infos.game_speed) == 0:
            game.tick()

        if global_infos.show_debug_ui:
            debug_screen()
        if global_infos.show_help:
            show_help()
        if global_infos.show_placer:
            show_placer()
        if global_infos.show_stage_picker:
            show_stage_picker()
        if global_infos.stage_tracker is not None:
            if global_infos.stage_tracker.cleared:
                global_infos.stage_tracker.display_cleared_gui(imgui)

        imgui.render()
        impl.render(imgui.get_draw_data())

        glfw.swap_buffers(window)
        glfw.poll_events()

    impl.shutdown()
    glfw.terminate()

    for texture in Texture.TEXTURE_LIST:
        texture.delete()
    return


def show_help():
    imgui.begin("제로 플레이어 게임 조작키")
    imgui.text("월드 테두리 이어 붙이기: U")
    imgui.text("디버그 GUI: -")
    imgui.text("이 창 띄우기/닫기: ?")
    imgui.text("격자 선 굵기 조절: 마우스 휠")
    imgui.text("게임 종료: ESC")
    imgui.text("게임 속도 감속: K")
    imgui.text("게임 속도 가속: L")
    imgui.text("엔티티 배치 메뉴: P")
    imgui.text("시뮬레이션 시작: SPACE")
    imgui.text("스테이지 불러오기 메뉴: S")
    imgui.end()


def debug_screen():
    imgui.begin("제로 플레이어 게임 디버그 UI")
    imgui.text("게임 속도: " + str(global_infos.game_speed) + " x")
    if global_infos.is_wrapping:
        imgui.text("월드 테두리 이어 붙임")
    else:
        imgui.text("월드 테두리 이어 붙이지 않음")

    if global_infos.play_sound:
        sound_text = "소리 활성화됨"
    else:
        sound_text = "소리 비활성화됨"

    if imgui.button(sound_text):
        global_infos.play_sound = not global_infos.play_sound

    imgui.image(1, 60, 60, (0, 1), (1, 0))
    for texture in Texture.TEXTURE_LIST:
        imgui.image(texture.id, 60, 60, (0, 1), (1, 0))


    imgui.end()


def show_placer():
    imgui.begin("타일 배치 메뉴")
    imgui.text("화살표 타일은, 방향키를 누루면서 클릭하여 화살표의 방향을 지정할 수 있습니다")
    if global_infos.is_holding_fixed:
        text = "타일 이동 가능: OFF"
    else:
        text = "타일 이동 가능: ON"
    if imgui.button(text):
        global_infos.is_holding_fixed = not global_infos.is_holding_fixed
    if imgui.image_button(Texture.ARROW.id, 120, 120, (0, 1), (1, 0)):
        arrow = Arrow(Texture.ARROW)

        if glfw.PRESS == glfw.get_key(window, glfw.KEY_UP):
            direction = enums.UP
        elif glfw.PRESS == glfw.get_key(window, glfw.KEY_RIGHT):
            direction = enums.RIGHT
        elif glfw.PRESS == glfw.get_key(window, glfw.KEY_DOWN):
            direction = enums.DOWN
        elif glfw.PRESS == glfw.get_key(window, glfw.KEY_LEFT):
            direction = enums.LEFT
        else:
            # 방향키를 누루고 있지 않을시, 위로 함
            direction = enums.UP
        arrow.direction = direction
        game.holding = arrow
        arrow.is_fixed = global_infos.is_holding_fixed
    imgui.same_line()
    placer_entry(Texture.SUICIDE, Suicide)
    imgui.same_line()
    placer_entry(Texture.LAVA, Lava)
    placer_entry(Texture.WALL, Wall)
    imgui.same_line()
    placer_entry(Texture.PUSHABLE, Pushable)
    imgui.same_line()
    placer_entry(Texture.DIRECTIONAL, Directional)
    placer_entry(Texture.STAR, Star)
    imgui.same_line()
    placer_entry(Texture.MINE, Mine)
    imgui.same_line()
    placer_entry(Texture.KEY, Key)
    placer_entry(Texture.LOCK, Lock)
    imgui.same_line()
    placer_entry(Texture.PORTAL_ORANGE, Portal)
    imgui.same_line()
    placer_entry(Texture.PORTAL_BLUE, Portal)
    placer_entry(Texture.DUPLICATE, Duplicate)
    imgui.same_line()
    if imgui.image_button(Texture.ROTATE_RIGHT.id, 120, 120, (0, 1), (1, 0)):
        rotate = Rotate(Texture.ROTATE_RIGHT)

        direction = enums.RIGHT
        if glfw.PRESS == glfw.get_key(window, glfw.KEY_RIGHT):
            direction = enums.RIGHT
        elif glfw.PRESS == glfw.get_key(window, glfw.KEY_LEFT):
            direction = enums.LEFT

        rotate.direction = direction
        game.holding = rotate
        rotate.is_fixed = global_infos.is_holding_fixed
    imgui.end()

def show_stage_picker():
    if global_infos.stage_tracker is None:
        dev_mode_text = "개발 모드 활성화됨"
    else:
        dev_mode_text = "개발 모드 비활성화됨"
    if imgui.button(dev_mode_text):
        global_infos.stage_tracker = None

    if imgui.button("스테이지 1"):
        close_all()
        game.clear_level()
        data.deserialize_to_world(game.world_tiles, "1.map")
        global_infos.stage_tracker = Stage1(game.world_tiles)

    imgui.same_line()

def close_all():
    global_infos.show_placer = False
    game.holding = None
    global_infos.show_help = False
    global_infos.show_stage_picker = False
    global_infos.show_debug_ui = False

def placer_entry(texture, tile_class):
    if imgui.image_button(texture.id, 120, 120, (0, 1), (1, 0)):
        tile = tile_class(texture)
        game.holding = tile
        tile.is_fixed = global_infos.is_holding_fixed

def main():
    print("PID:", os.getpid())
    init_window()


if __name__ == '__main__':
    main()
