import random
from math import floor
import glfw
import global_variables
import game
from global_variables import *
import tiles
import enums


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
        if key == glfw.KEY_K:
            if get_game_speed() < 2.5:
                set_game_speed(get_game_speed() + 0.5)
        if key == glfw.KEY_L:
            if get_game_speed() > 0.5:
                set_game_speed(get_game_speed() - 0.5)
        if key == glfw.KEY_SPACE:
            set_ticking(not is_ticking())


def on_mouse(window, button: int, action: int, mods: int):
    is_left = button == glfw.MOUSE_BUTTON_LEFT
    is_press = action == glfw.PRESS
    x, y = glfw.get_cursor_pos(window)

    world_x = int(floor(x / 120))
    world_y = int(floor(y / 120))
    if is_left and is_press:
        print("위치: (" + str(x) + ", " + str(y) + ")")
        print("타일: (" + str(world_x) + ", " + str(world_y) + ")")
        if game.world_tiles[world_x][world_y] is None:
            arrow = tiles.Arrow(global_variables.registered_textures[1])
            arrow.direction = random.randint(enums.UP, enums.LEFT)
            game.world_tiles[world_x][world_y] = arrow
        else:
            tile = game.world_tiles[world_x][world_y]
            if type(tile) == tiles.Arrow:
                question = tiles.Question(global_variables.registered_textures[2])
                question.direction = enums.UP
                game.world_tiles[world_x][world_y] = question


