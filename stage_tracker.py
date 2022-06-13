from tiles import Star
from global_variables import configuration
from copy import deepcopy


class StageBase:
    def __init__(self, name: str, world, next_stage):
        self.name = name
        self.original = deepcopy(world)
        self.snapshot_before_ticking = None
        self.stars = 0
        self.cleared = False
        self.score = 100
        self.next_stage = next_stage
        for x in range(0, 32):
            for y in range(0, 18):
                if isinstance(self.original[x][y], Star):
                    self.stars += 1

    def get_star(self):
        self.stars -= 1
        assert self.stars > -1
        if self.stars == 0:
            self.cleared = True
            for later_x in range(0, 32):
                for later_y in range(0, 18):
                    current = self.snapshot_before_ticking[later_x][later_y]
                    if current is not None and not current.is_fixed:
                        original = self.original
                        same_thing = original[original.uuid == current.uuid]

    def about_to_start(self, world):
        self.snapshot_before_ticking = deepcopy(world)

    def display_cleared_gui(self, imgui):
        imgui.begin(f"스테이지 {self.name} 클리어!")
        if self.next_stage is not None:
            if imgui.button("다음 스테이지 불러오기"):
                configuration.stage_tracker = self.next_stage()


class Stage1(StageBase):
    def __init__(self, world):
        super().__init__("스테이지 1", world, None)
