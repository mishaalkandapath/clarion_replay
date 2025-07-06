from utils import SHAPE_DICT    
import numpy as np
import time

for shape in SHAPE_DICT:
        if shape == "mirror_L":
            for row in range(0, 5):
                for col in range(1,6):
                    grid = np.zeros((6, 6))
                    
                    grid[[row, row+1, row+1], [col, col, col-1]] = SHAPE_DICT[shape]
                    print([row, row+1, row+1], [col, col, col-1])
                    print(grid)
                    time.sleep(5)