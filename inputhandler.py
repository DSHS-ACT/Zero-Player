from math import floor

import glfw
import main
import game


def on_key(window, key: int, scancode: int, action: int, mods: int):
    is_press = action == glfw.PRESS
    if is_press:
        if key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)
        if key == glfw.KEY_UP:
            main.width += 0.5
        if key == glfw.KEY_DOWN:
            if main.width >= 1:
                main.width -= 0.5


def on_mouse(window, button: int, action: int, mods: int):
    is_left = button == glfw.MOUSE_BUTTON_LEFT
    is_press = action == glfw.PRESS
    x, y = glfw.get_cursor_pos(window)

    flipped_y = y

    world_x = int(floor(x / 120))
    world_y = int(floor(flipped_y / 120))
    if is_left and is_press:
        print("위치: (" + str(x) + ", " + str(flipped_y) + ")")
        print("타일: (" + str(world_x) + ", " + str(world_y) + ")")
        game.world[world_x][world_y] += 1
        game.world[world_x][world_y] %= 5
    print("월드: [" + str(game.world[0][0]) + " " + str(game.world[1][0]) + " " + str(game.world[2][0]))

