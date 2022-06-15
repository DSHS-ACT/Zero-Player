from tiles import Star
from global_variables import global_infos
from copy import deepcopy
import glfw
import game
import data


class Stage:
    def __init__(self, world, map_number: int):
        self.number = map_number
        self.original = deepcopy(world)
        self.snapshot_before_ticking = None
        self.stars = 0
        self.cleared = False
        self.score = 200
        self.tick_count = 0
        for x in range(0, 32):
            for y in range(0, 18):
                if isinstance(self.original[x][y], Star):
                    self.stars += 1

    def ticked(self):
        self.tick_count += 1

    def get_star(self):
        self.stars -= 1
        assert self.stars > -1
        if self.stars == 0:
            self.cleared = True
            global_infos.ticking = False
            self.score -= self.tick_count
            for later_x in range(0, 32):
                for later_y in range(0, 18):
                    current = self.snapshot_before_ticking[later_x][later_y]

                    if current is None:
                        continue
                    if current.is_fixed:
                        continue

                    original = self.original
                    same_thing_position = None

                    for original_x in range(0, 32):
                        for original_y in range(0, 18):
                            original_tile = original[original_x][original_y]

                            if original_tile is None:
                                continue

                            if original_tile.uuid == current.uuid:
                                same_thing_position = original_x, original_y
                                break

                        if same_thing_position is not None:
                            break

                    assert same_thing_position is not None

                    distance = abs(later_x - same_thing_position[0]) + abs(later_y - same_thing_position[1])
                    self.score -= distance


    def about_to_start(self, world):
        self.snapshot_before_ticking = deepcopy(world)

    def display_cleared_gui(self, imgui):
        imgui.begin(f"스테이지 {self.number} 클리어!")
        imgui.text(f"점수: {self.score}")
        if self.number < global_infos.final_map_number:
            if imgui.button("다음 스테이지 불러오기"):
                load_stage(self.number + 1)
            imgui.same_line()
        if imgui.button("게임 종료"):
            glfw.set_window_should_close(global_infos.window, True)
        imgui.end()


def load_stage(map_number: int):
    close_all()
    game.clear_level()
    data.deserialize_to_world(game.world_tiles, f"{map_number}.map")
    global_infos.stage_tracker = Stage(game.world_tiles, map_number)
    global_infos.is_holding_fixed = False


def close_all():
    global_infos.show_placer = False
    game.holding = None
    global_infos.show_help = False
    global_infos.show_stage_picker = False
    global_infos.show_debug_ui = False



