from math import floor
import glfw
import game
from global_variables import *


def on_key(window, key: int, scancode: int, action: int, mods: int):
    is_press = action == glfw.PRESS
    if is_press:
        if key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)
        if key == glfw.KEY_UP:
            set_width(get_width() + 0.5)
        if key == glfw.KEY_DOWN:
            if get_width() >= 1:
                set_width(get_width() - 0.5)


def on_mouse(window, button: int, action: int, mods: int):
    is_left = button == glfw.MOUSE_BUTTON_LEFT
    is_press = action == glfw.PRESS
    x, y = glfw.get_cursor_pos(window)

    flipped_y = y # y 좌표를 위아래로 뒤집음. 그렇지 않으면 월드 좌표와 맞지 않음.

    world_x = int(floor(x / 120))
    world_y = int(floor(flipped_y / 120))
    if is_left and is_press:
        print("위치: (" + str(x) + ", " + str(flipped_y) + ")")
        print("타일: (" + str(world_x) + ", " + str(world_y) + ")")
        game.world[world_x][world_y] += 1
        game.world[world_x][world_y] %= len(created)

