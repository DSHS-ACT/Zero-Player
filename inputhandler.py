from math import floor

import glfw

import enums
import game
from global_variables import configuration

"""
ZPG의 키보드 핸들러
key: 눌러진 키의 번호, glfw.KEY_<키> 와 동일한지 비교하여 무슨 키가 눌러졌는지 확인할 수 있음.
action: 키보드 행동 번호, 키보드가 "내려갔"는지, "올라갔"는지, 내려간 상태로 "유지되었"는지 확인할 수 있음
"""
def on_key(window, key: int, scancode: int, action: int, mods: int):
    is_press = action == glfw.PRESS
    if not is_press:
        return

    allowed_speeds = [0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 10.0, 12.0, 15.0, 20.0, 30.0]
    if key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

    if key == glfw.KEY_L:
        index = 0
        for speed in allowed_speeds:
            if speed == configuration.game_speed:
                break
            index += 1
            assert speed != allowed_speeds[-1]

        if index < len(allowed_speeds) - 1:
            index += 1
        configuration.game_speed = allowed_speeds[index]

    if key == glfw.KEY_K:
        index = 0
        for speed in allowed_speeds:
            if speed == configuration.game_speed:
                break
            index += 1
            assert speed != allowed_speeds[-1]

        if index > 0:
            index -= 1
        configuration.game_speed = allowed_speeds[index]

    if key == glfw.KEY_SPACE:
        if game.holding is None:
            configuration.ticking = not configuration.ticking

    if key == glfw.KEY_U:
        configuration.is_wrapping = not configuration.is_wrapping

    if key == glfw.KEY_MINUS:
        configuration.show_debug_ui = not configuration.show_debug_ui

    if key == glfw.KEY_SLASH:
        configuration.show_help = not configuration.show_help

    if key == glfw.KEY_P:
        configuration.show_placer = not configuration.show_placer

"""
ZPG 의 마우스 핸들러
button: 클릭된 마우스 키의 번호, glfw_MOUSE_BUTTON_LEFT 와 같은 값들과 비교하여 눌러진 마우스가 무엇인지 알아낼 수 있다
action: 마우스 행동 번호, 마우스가 "내려갔"는지, "올라갔"는지, 내려간 상태로 "유지되었"는지 확인할 수 있음
"""
def on_mouse(window, button: int, action: int, mods: int):
    # 게임 실행중에는 마우스 입력 무시
    if configuration.ticking:
        return

    # GUI 표시중에는 마우스 입력 무시
    if configuration.show_help or configuration.show_debug_ui or configuration.show_placer:
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
        if is_left:

            # 현재 누루고 있는 키보드 방향키의 방향 파악
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

            clicked_tile = game.world_tiles[world_x][world_y]
            if clicked_tile is None:
                if game.holding is not None:
                    game.world_tiles[world_x][world_y] = game.holding
                    game.holding = None
            else:
                if game.holding is None:
                    game.holding = clicked_tile
                    game.world_tiles[world_x][world_y] = None
        else:
            if game.holding is None:
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
        configuration.width += 0.5
    elif y < 0:
        if configuration.width >= 1:
            configuration.width -= 0.5

