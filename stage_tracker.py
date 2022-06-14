from tiles import Star
from global_variables import global_infos
from copy import deepcopy


class StageBase:
    def __init__(self, name: str, world, next_stage):
        self.name = name
        self.original = deepcopy(world)
        self.snapshot_before_ticking = None
        self.stars = 0
        self.cleared = False
        self.score = 200
        self.next_stage = next_stage
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
        imgui.begin(f"스테이지 {self.name} 클리어!")
        imgui.text(f"점수: {self.score}")
        if self.next_stage is not None:
            if imgui.button("다음 스테이지 불러오기"):
                global_infos.stage_tracker = self.next_stage()
        imgui.end()


class Stage1(StageBase):
    def __init__(self, world):
        super().__init__("스테이지 1", world, None)
