import numpy as np
world = np.zeros((16, 9), dtype=np.int32)

def get_gpu_world():
    return world.flatten(order="F")
