from math import floor
import glfw
import game
from global_variables import configuration
import tiles
import enums
from texture import Texture


def on_key(window, key: int, scancode: int, action: int, mods: int):
    is_press = action == glfw.PRESS
    if is_press:
        if key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)
        if key == glfw.KEY_K:
            if configuration.game_speed < 2.5:
                configuration.game_speed += 0.5
        if key == glfw.KEY_L:
            if configuration.game_speed > 0.5:
                configuration.game_speed -= 0.5
        if key == glfw.KEY_SPACE:
            configuration.ticking = not configuration.ticking
        if key == glfw.KEY_U:
            configuration.is_wrapping = not configuration.is_wrapping
        if key == glfw.KEY_MINUS:
            configuration.show_debug_ui = not configuration.show_debug_ui


def on_mouse(window, button: int, action: int, mods: int):
    is_left = button == glfw.MOUSE_BUTTON_LEFT
    is_press = action == glfw.PRESS

    # 모니터는 좌표의 범위가 x는 0~1919, y는 0~1079 임
    monitor_x, monitor_y = glfw.get_cursor_pos(window)

    # 16x9 타일맵 기준으로 변경
    world_x = int(floor(monitor_x / 120))
    world_y = int(floor(monitor_y / 120))
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
                # 방향키를 누루고 있지 않을시, 방향을 없음으로 함
                direction = None

            clicked_tile = game.world_tiles[world_x][world_y]
            if direction is not None and (clicked_tile is None or isinstance(clicked_tile, tiles.Arrow)):
                arrow = tiles.Arrow(Texture.ARROW)
                arrow.direction = direction
                game.world_tiles[world_x][world_y] = arrow
            else:
                if isinstance(clicked_tile, tiles.Arrow):
                    question = tiles.Question(Texture.QUESTION)
                    question.direction = enums.UP
                    game.world_tiles[world_x][world_y] = question
        else:
            game.world_tiles[world_x][world_y] = None

# x는 터치패드와 같은 기기에서 좌우로 스크롤 하는 것으로, 이 게임에서는 무시됨
# y > 0 -> 휠을 위로 돌리는 중, y < 0 -> 휠을 아래로 돌리는 중
def on_mouse_wheel(window, x: float, y: float):
    if y > 0:
        configuration.width += 0.5
    elif y < 0:
        if configuration.width >= 1:
            configuration.width -= 0.5

