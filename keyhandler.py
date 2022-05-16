import glfw


def on_key(window, key, scancode, action, mods):
    is_press = action == glfw.PRESS
    if is_press:
        if key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)
