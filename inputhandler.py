from math import floor

import glfw

import enums
import game
import tiles
from global_variables import global_infos
import data
from tiles import Portal
from texture import Texture

"""
ZPG의 키보드 핸들러
key: 눌러진 키의 번호, glfw.KEY_<키> 와 동일한지 비교하여 무슨 키가 눌러졌는지 확인할 수 있음.
action: 키보드 행동 번호, 키보드가 "내려갔"는지, "올라갔"는지, 내려간 상태로 "유지되었"는지 확인할 수 있음
"""


def on_key(window, key: int, scancode: int, action: int, mods: int):
    is_press = action == glfw.PRESS
    if not is_press:
        return

    allowed_speeds = [0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 10.0, 12.0, 15.0, 20.0, 30.0, 60.0]
    is_ctrl_pressed = glfw.get_key(window, glfw.KEY_LEFT_CONTROL)
    is_alt_pressed = glfw.get_key(window, glfw.KEY_LEFT_ALT)
    if key == glfw.KEY_ESCAPE:
        if global_infos.show_help:
            global_infos.show_help = False
            return
        if global_infos.show_placer:
            global_infos.show_placer = False
            return
        if global_infos.show_debug_ui:
            global_infos.show_debug_ui = False
            return
        if global_infos.show_stage_picker:
            global_infos.show_stage_picker = False
            return
        if global_infos.stage_tracker is not None and global_infos.stage_tracker.cleared:
            return
        glfw.set_window_should_close(window, True)

    if key == glfw.KEY_L:
        index = 0
        for speed in allowed_speeds:
            if speed == global_infos.game_speed:
                break
            index += 1
            assert speed != allowed_speeds[-1]

        if index < len(allowed_speeds) - 1:
            index += 1
        global_infos.game_speed = allowed_speeds[index]

    if key == glfw.KEY_K:
        index = 0
        for speed in allowed_speeds:
            if speed == global_infos.game_speed:
                break
            index += 1
            assert speed != allowed_speeds[-1]

        if index > 0:
            index -= 1
        global_infos.game_speed = allowed_speeds[index]

    if key == glfw.KEY_SPACE:
        if game.holding is None:
            if game.unresolved_portal is not None:
                position = game.unresolved_portal.get_position()
                game.world_tiles[position[0]][position[1]] = None
                game.unresolved_portal = None

            if global_infos.stage_tracker is None:
                global_infos.ticking = not global_infos.ticking
            else:
                global_infos.ticking = True
                global_infos.stage_tracker.about_to_start(game.world_tiles)
            global_infos.show_placer = False

    if key == glfw.KEY_U:
        global_infos.is_wrapping = not global_infos.is_wrapping

    if key == glfw.KEY_SLASH:
        global_infos.show_help = not global_infos.show_help

    if key == glfw.KEY_S:
        global_infos.show_stage_picker = not global_infos.show_stage_picker

    # 개발자 모드 전용 키바인드들
    if global_infos.stage_tracker is None:
        if key == glfw.KEY_MINUS:
            global_infos.show_debug_ui = not global_infos.show_debug_ui

        if key == glfw.KEY_P:
            game.play_wav("menu.wav")
            if not global_infos.ticking:
                global_infos.show_placer = not global_infos.show_placer

        if key == glfw.KEY_1:
            if is_ctrl_pressed:
                data.serialize(game.world_tiles, "1.map")
            elif is_alt_pressed:
                game.clear_level()
                data.deserialize_to_world(game.world_tiles, "1.map")

        if key == glfw.KEY_2:
            if is_ctrl_pressed:
                data.serialize(game.world_tiles, "2.map")
            elif is_alt_pressed:
                game.clear_level()
                data.deserialize_to_world(game.world_tiles, "2.map")

        if key == glfw.KEY_3:
            if is_ctrl_pressed:
                data.serialize(game.world_tiles, "3.map")
            elif is_alt_pressed:
                game.clear_level()
                data.deserialize_to_world(game.world_tiles, "3.map")

        if key == glfw.KEY_4:
            if is_ctrl_pressed:
                data.serialize(game.world_tiles, "4.map")
            elif is_alt_pressed:
                game.clear_level()
                data.deserialize_to_world(game.world_tiles, "4.map")

        if key == glfw.KEY_5:
            if is_ctrl_pressed:
                data.serialize(game.world_tiles, "5.map")
            elif is_alt_pressed:
                game.clear_level()
                data.deserialize_to_world(game.world_tiles, "5.map")

        if key == glfw.KEY_6:
            if is_ctrl_pressed:
                data.serialize(game.world_tiles, "6.map")
            elif is_alt_pressed:
                game.clear_level()
                data.deserialize_to_world(game.world_tiles, "6.map")

        if key == glfw.KEY_7:
            if is_ctrl_pressed:
                data.serialize(game.world_tiles, "7.map")
            elif is_alt_pressed:
                game.clear_level()
                data.deserialize_to_world(game.world_tiles, "7.map")

        if key == glfw.KEY_8:
            if is_ctrl_pressed:
                data.serialize(game.world_tiles, "8.map")
            elif is_alt_pressed:
                game.clear_level()
                data.deserialize_to_world(game.world_tiles, "8.map")

        if key == glfw.KEY_9:
            if is_ctrl_pressed:
                data.serialize(game.world_tiles, "9.map")
            elif is_alt_pressed:
                game.clear_level()
                data.deserialize_to_world(game.world_tiles, "9.map")

        if key == glfw.KEY_0:
            if is_ctrl_pressed:
                data.serialize(game.world_tiles, "0.map")
            elif is_alt_pressed:
                game.clear_level()
                data.deserialize_to_world(game.world_tiles, "0.map")

        if key == glfw.KEY_UP:
            if game.holding is not None and not isinstance(game.holding, tiles.Rotate):
                game.holding.direction = enums.UP

        if key == glfw.KEY_RIGHT:
            if game.holding is not None:
                if isinstance(game.holding, tiles.Rotate):
                    game.holding.texture = Texture.ROTATE_RIGHT
                game.holding.direction = enums.RIGHT

        if key == glfw.KEY_DOWN:
            if game.holding is not None and not isinstance(game.holding, tiles.Rotate):
                game.holding.direction = enums.DOWN

        if key == glfw.KEY_LEFT:
            if game.holding is not None:
                if isinstance(game.holding, tiles.Rotate):
                    game.holding.texture = Texture.ROTATE_LEFT
                game.holding.direction = enums.LEFT


"""
ZPG 의 마우스 핸들러
button: 클릭된 마우스 키의 번호, glfw_MOUSE_BUTTON_LEFT 와 같은 값들과 비교하여 눌러진 마우스가 무엇인지 알아낼 수 있다
action: 마우스 행동 번호, 마우스가 "내려갔"는지, "올라갔"는지, 내려간 상태로 "유지되었"는지 확인할 수 있음
"""


def on_mouse(window, button: int, action: int, mods: int):
    # 게임 실행중에는 마우스 입력 무시
    if global_infos.ticking:
        return

    # GUI 표시중에는 마우스 입력 무시
    if global_infos.imgui_io.want_capture_mouse:
        return

    # 왼쪽 버튼인가?
    is_left = button == glfw.MOUSE_BUTTON_LEFT
    # 그 버튼이 눌러졌는가?
    is_press = action == glfw.PRESS

    # 모니터는 좌표의 범위가 x는 0~1919, y는 0~1079 임
    monitor_x, monitor_y = glfw.get_cursor_pos(window)

    world_x = int(floor(monitor_x / 60))
    world_y = int(floor(monitor_y / 60))
    print("위치: (" + str(monitor_x) + ", " + str(monitor_y) + ")")
    print("타일: (" + str(world_x) + ", " + str(world_y) + ")")
    if is_press:
        clicked_tile = game.world_tiles[world_x][world_y]
        if is_left:
            if clicked_tile is None:
                if game.holding is not None:
                    game.world_tiles[world_x][world_y] = game.holding
                    if isinstance(game.holding, Portal):
                        if game.unresolved_portal is None:
                            game.unresolved_portal = game.holding
                        else:
                            if game.holding != game.unresolved_portal:
                                game.unresolved_portal.opposite = game.holding
                                game.holding.opposite = game.unresolved_portal
                                game.unresolved_portal = None
                    game.holding = None
            else:
                if game.holding is None:
                    if global_infos.stage_tracker is None or not clicked_tile.is_fixed:
                        game.holding = clicked_tile
                        if isinstance(clicked_tile, Portal):
                            if clicked_tile.opposite is not None:
                                clicked_tile.opposite.opposite = None
                                game.unresolved_portal = clicked_tile.opposite

                        game.holding.is_fixed = global_infos.is_holding_fixed
                        game.world_tiles[world_x][world_y] = None
        else:
            if game.holding is None:
                to_delete = game.world_tiles[world_x][world_y]
                if to_delete is not None:
                    if isinstance(to_delete, Portal):
                        if to_delete.opposite is not None:
                            to_delete.opposite.opposite = None
                            game.unresolved_portal = to_delete.opposite
                        else:
                            assert to_delete.uuid == game.unresolved_portal.uuid
                            game.unresolved_portal = None
                game.world_tiles[world_x][world_y] = None


"""
마우스 휠 핸들러
마우스 휠을 위로 회전시킬 시, y 는 1이 됨
마우스 휠을 아래로 회전시킬 시 y 는 -1이 됨

(x는 노트북 터치패드나 타블렛에만 존재함, 그렇기에 ZPG 에선 사용하지 않음)
마우스 휠을 오른쪽으로 회전시킬 시, x 는 1 이 됨
마우스 휠을 왼쪽으로 회전시킬 시, x 는 -1 이 됨
"""


def on_mouse_wheel(window, x: float, y: float):
    if y > 0:
        global_infos.width += 0.5
    elif y < 0:
        if global_infos.width >= 1:
            global_infos.width -= 0.5
