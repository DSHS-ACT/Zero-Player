class Global:
    def __init__(self):
        self.width = 1.0
        self.frame_count = 0
        self.game_speed = 1
        self.ticking = False
        self.is_wrapping = True
        self.show_debug_ui = False
        self.show_help = False
        self.show_placer = False
        self.is_holding_fixed = False
        self.stage_tracker = None
        self.show_stage_picker = False
        self.imgui_io = None


global_infos = Global()
