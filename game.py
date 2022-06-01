import numpy as np

world = np.zeros((16, 9), dtype=np.int32)

texture_list = ["0.png", "1.png", "2.png", "3.png", "4.png"]

# TODO 화살표 방향으로 이동하는 타일, 키보드 방향키를 눌러 방향을 고른다
# TODO 무작위로 움직이는 타일
# TODO 배속시키는 키보드 키

def get_gpu_world():
    return world.flatten(order="F")

def tick():
    print("tick")
