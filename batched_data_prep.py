import re
from typing import List, Tuple
from itertools import product
import pickle
import os

import torch
import numpy as np
from tqdm import tqdm

from q_learning import pyc_to_torch, torch_to_pyc
from utils import SHAPE_DICT, SHAPES, SHAPE_SHAPE_REL, SHAPE_START
from evaluation import mk_besideness, mk_ontopness
from scaffolded_training import get_grids_by_number, TEST_GRIDS

STATE_KEYS = ['input_half_T_row1', 'input_half_T_row2', 'input_half_T_row3',
 'input_half_T_col1', 'input_half_T_col2', 'input_half_T_col3', 'input_mirror_L_row1', 'input_mirror_L_row2', 'input_mirror_L_row3', 'input_mirror_L_col1', 'input_mirror_L_col2', 'input_mirror_L_col3', 'input_vertical_row1', 'input_vertical_row2', 'input_vertical_row3', 'input_vertical_col1', 'input_vertical_col2', 'input_vertical_col3', 'input_horizontal_row1', 'input_horizontal_row2', 'input_horizontal_row3', 'input_horizontal_col1', 'input_horizontal_col2', 'input_horizontal_col3', 'target_half_T_row1', 'target_half_T_row2', 'target_half_T_row3', 'target_half_T_col1', 'target_half_T_col2', 'target_half_T_col3', 'target_mirror_L_row1', 'target_mirror_L_row2', 'target_mirror_L_row3', 'target_mirror_L_col1', 'target_mirror_L_col2', 'target_mirror_L_col3', 'target_vertical_row1', 'target_vertical_row2', 'target_vertical_row3', 'target_vertical_col1', 'target_vertical_col2', 'target_vertical_col3', 'target_horizontal_row1', 'target_horizontal_row2', 'target_horizontal_row3', 'target_horizontal_col1', 'target_horizontal_col2', 'target_horizontal_col3']
ACTION_KEYS = ['half_T_start', 'mirror_L_start', 'vertical_start',
 'horizontal_start', 'half_T_horizontal_left', 'half_T_horizontal_right', 'half_T_horizontal_above', 'half_T_horizontal_below', 'horizontal_half_T_left', 'horizontal_half_T_right', 'horizontal_half_T_above', 'horizontal_half_T_below', 'half_T_vertical_left', 'half_T_vertical_right', 'half_T_vertical_above', 'half_T_vertical_below', 'vertical_half_T_left', 'vertical_half_T_right', 'vertical_half_T_above', 'vertical_half_T_below', 'half_T_mirror_L_left', 'half_T_mirror_L_right', 'half_T_mirror_L_above', 'half_T_mirror_L_below', 'mirror_L_half_T_left', 'mirror_L_half_T_right', 'mirror_L_half_T_above', 'mirror_L_half_T_below', 'mirror_L_horizontal_left', 'mirror_L_horizontal_right', 'mirror_L_horizontal_above', 'mirror_L_horizontal_below', 'horizontal_mirror_L_left', 'horizontal_mirror_L_right', 'horizontal_mirror_L_above', 'horizontal_mirror_L_below', 'mirror_L_vertical_left', 'mirror_L_vertical_right', 'mirror_L_vertical_above', 'mirror_L_vertical_below', 'vertical_mirror_L_left', 'vertical_mirror_L_right', 'vertical_mirror_L_above', 'vertical_mirror_L_below', 'vertical_horizontal_left', 'vertical_horizontal_right', 'vertical_horizontal_above', 'vertical_horizontal_below', 'horizontal_vertical_left', 'horizontal_vertical_right', 'horizontal_vertical_above', 'horizontal_vertical_below']

def make_mlp_dict(grid: dict[str, int], target=False) -> torch.tensor:
    mlp_input = {}
    grid_shapes = (t := np.unique(grid))[t != 0].tolist()
    name = "target" if target else "input"
    for shape in grid_shapes:
        shape_name = SHAPES[int(shape) - 1]
        rows, cols = np.where(grid == int(shape))
        for i in range(3):
            mlp_input[(f"{name}_{shape_name}_row{i+1}", f"{int(rows[i]) + 1}")] = 1
            mlp_input[(f"{name}_{shape_name}_col{i+1}", f"{int(cols[i]) + 1}")] = 1
    return pyc_to_torch(mlp_input, indices=STATE_KEYS)

def make_mlp_input(gridname: str) -> Tuple[dict[str, int], torch.tensor]:
    mlp_input = {}
    grid = np.load(gridname)
    return grid, make_mlp_dict(grid)

def make_grid_after_action(grid: np.array, target_grid: np.array, action: str) -> np.array:

    if "start" in action:
        shape = re.match(SHAPE_START, action).group(1)
    else:
        shape = re.match(SHAPE_SHAPE_REL, action).group(2)
    new_grid = np.zeros_like(grid)
    new_grid += target_grid
    new_grid += grid * (grid == SHAPE_DICT[shape])
        
    return new_grid

def action_is_right(input_grid: np.array, target_grid: np.array, action: str) -> bool:
    if (t:= re.match(SHAPE_START, action)) and not (np.unique(target_grid).size - 1 ):
        return np.count_nonzero(input_grid == SHAPE_DICT[t.group(1)]) != 0
    elif (t:= re.match(SHAPE_START, action)): return False
    else:
        t = re.match(SHAPE_SHAPE_REL, action)
        shape1, shape2, rel = t.group(1), t.group(2), t.group(3)
        check_grid = input_grid * (input_grid == SHAPE_DICT[shape1])
        check_grid += input_grid * (input_grid == SHAPE_DICT[shape2])

        if (np.count_nonzero(input_grid == SHAPE_DICT[shape1]) != 0
            and np.count_nonzero(input_grid == SHAPE_DICT[shape2]) != 0
            and np.count_nonzero(target_grid == SHAPE_DICT[shape1]) != 0
            and np.count_nonzero(target_grid == SHAPE_DICT[shape2]) == 0):

            correct_rel = False
            if rel in ("above", "below"):
                ontopness, _, ontop, below = mk_ontopness(check_grid)
                if ontopness:
                    correct_rel = ((SHAPES[ontop.item() - 1] == shape1 and SHAPES[below.item() - 1] == shape2) if rel == "above" else (SHAPES[ontop.item() - 1] == shape2 and SHAPES[below.item() - 1] == shape1))
            else:
                besideness, _, left, right = mk_besideness(check_grid)
                if besideness:
                    correct_rel = ((SHAPES[left.item() - 1] == shape1 and SHAPES[right.item() - 1] == shape2) if rel == "left" else (SHAPES[left.item() - 1] == shape2 and SHAPES[right.item() - 1] == shape1))
            return correct_rel
        else: return False

def make_transitions_for_grid(grid: np.array, 
                              target_grid: np.array, 
                              grid_tensor: torch.tensor) -> List[torch.tensor]:
    
    dataset = []
    grid_shapes = (t := np.unique(grid))[t != 0].tolist()
    target_grid_shapes = (t := np.unique(target_grid))[t != 0].tolist()
    num_steps = len(grid_shapes) - len(target_grid_shapes)
    # first move, only start allowed. 
    for a, action in enumerate(ACTION_KEYS):
        reward = -1
        new_state = torch.clone(grid_tensor)
        if action_is_right(grid, target_grid, action):
            reward = 1 if (num_steps == 1) else -0.1
            new_grid = make_grid_after_action(grid, target_grid, action)
            new_state += make_mlp_dict(new_grid, target=True)
            new_state[new_state > 1] = 1
            if reward != 1:
                dataset.extend(
                        make_transitions_for_grid(grid, new_grid, new_state)
                    )
        dataset.append([grid_tensor, a, reward, new_state])
    return dataset

if __name__ == "__main__":
    STATE_KEYS = list(product(STATE_KEYS, 
                      ["1", "2", "3", "4", "5", "6"]))
    
    grid_names = os.listdir("data/processed/train_data/train_stims/")
    grid_names = [g for g in grid_names if g[:2] != "._"]
    gn = get_grids_by_number(grid_names)
    i = 0
    for files in gn:
        print(files)
        test_files = TEST_GRIDS[i+1]
        files = list(set(files).difference(test_files))
        dataset = []
        for filename in tqdm(files):
            filename='GRID19.npy'
            grid, grid_tensor = make_mlp_input(f"data/processed/train_data/train_stims/{filename}")
            dataset += make_transitions_for_grid(grid, np.zeros_like(grid), grid_tensor)
        print(len(dataset))
        f = open(f"train_dataset_b{i+1}.pkl", "wb")
        pickle.dump(dataset, f)
        f.close()
        dataset = []
        for filename in tqdm(test_files):
            grid, grid_tensor = make_mlp_input(f"data/processed/train_data/train_stims/{filename}")
            dataset += make_transitions_for_grid(grid, np.zeros_like(grid), grid_tensor)
        print(len(dataset))
        f = open(f"test_dataset_b{i+1}.pkl", "wb")
        pickle.dump(dataset, f)
        f.close()

        i+=1