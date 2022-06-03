registered_textures = []
width = 1.0
frame_count = 0
game_speed = 1
ticking = False


def is_ticking():
    return ticking


def set_ticking(t):
    global ticking
    ticking = t


def get_game_speed():
    return game_speed


def set_game_speed(speed):
    global game_speed
    game_speed = speed


def set_frame_count(count):
    global frame_count
    frame_count = count


def get_frame_count():
    return frame_count


def set_width(w):
    global width
    width = w


def get_width():
    return width
