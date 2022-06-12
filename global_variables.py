class Global:
    def __init__(self):
        self.width = 1.0
        self.frame_count = 0
        self.game_speed = 1
        self.ticking = False
        self.is_wrapping = False
        self.show_debug_ui = False
        self.show_help = False
        self.show_placer = False
        self.dev_mode = True


configuration = Global()
