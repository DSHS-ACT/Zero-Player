import numpy as np
world = np.zeros((16, 9), dtype=np.int32)

texture_list = ["0.png", "1.png", "2.png", "3.png", "4.png"]

def get_gpu_world():
    return world.flatten(order="F")
