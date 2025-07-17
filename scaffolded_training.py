from datetime import timedelta, datetime
import logging
import sys
import os
import pickle as p
import random
import re

import torch
import numpy as np
import pandas as pd
import tqdm as tqdm

from utils import (
    numpify_grid,
    SHAPE_SHAPE_REL,
    SHAPE_START,
    QUERY_REL_PATTERN,
    SHAPE_DICT,
    acc,
)
from base_participant import (
    BaseParticipant,
    LowLevelParticipant,
    AbstractParticipant
)
from evaluation import (
    simple_sequenceness,
    simple_goal_sequencessness,
    simple_goal_sequencessness_elaborate,
    brick_connectedness,
)
from plotting import simple_plotting, simple_snsplot, plot_sequences
from simulation import run_participant_session

TEST_GRID_ONES = ['GRID_489', 'GRID_565', 'GRID_504', 'GRID_507', 'GRID_524', 'GRID_500', 'GRID_535', 'GRID_555', 'GRID_528', 'GRID_542', 'GRID_518', 'GRID_525', 'GRID_503', 'GRID_483', 'GRID_549', 'GRID_547', 'GRID_551']
TEST_GRID_TWOS = ['GRID19', 'GRID108', 'GRID53', 'GRID98', 'GRID122']

TEST_GRIDS = {1: TEST_GRID_ONES, 2: TEST_GRID_TWOS}

def make_special_one_grid():
    running_count = 472
    for shape in SHAPE_DICT:
        if shape == "mirror_L":
            for row in range(0, 5):
                for col in range(1,6):
                    grid = np.zeros((6, 6))
                    
                    grid[[row, row+1, row+1], [col, col, col-1]] = SHAPE_DICT[shape]
                    np.save(f"/Users/mishaal/personalproj/clarion_replay/data/processed/train_data/train_stims/GRID_{running_count}.npy", grid)
                    running_count += 1
        elif shape == "half_T":
            for row in range(0, 5):
                for col in range(0, 5):
                    grid = np.zeros((6, 6))
                    
                    grid[[row, row+1, row], [col, col, col+1]] = SHAPE_DICT[shape]
                    np.save(f"/Users/mishaal/personalproj/clarion_replay/data/processed/train_data/train_stims/GRID_{running_count}.npy", grid)
                    running_count += 1
        elif shape == "horizontal":
            for row in range(0, 6):
                for col in range(0, 4):
                    grid = np.zeros((6, 6))
                    
                    grid[[row, row, row], [col, col+1, col+2]] = SHAPE_DICT[shape]
                    np.save(f"/Users/mishaal/personalproj/clarion_replay/data/processed/train_data/train_stims/GRID_{running_count}.npy", grid)
                    running_count += 1
        else:
            for row in range(0, 4):
                for col in range(0, 6):
                    grid = np.zeros((6, 6))
                    
                    grid[[row, row+1, row+2], [col, col, col]] = SHAPE_DICT[shape]
                    np.save(f"/Users/mishaal/personalproj/clarion_replay/data/processed/train_data/train_stims/GRID_{running_count}.npy", grid)
                    running_count += 1


def get_grids_by_number(grid_names, start_from=1, end_at=5):
    g_n = {1:[], 2:[], 3:[], 4:[]}
    for grid_name in grid_names:
        stim_grid = np.load(f"/Users/mishaal/personalproj/clarion_replay/data/processed/train_data/train_stims/{grid_name}")
        g_n[len(np.unique(stim_grid))-1].append(grid_name)
    for k in range(start_from, end_at):
        yield g_n[k]

def run_experiment(
        num_train_sessions=3,
        start_from=1,
        model_path=None):
    grid_names = os.listdir("data/processed/train_data/train_stims/")
    participant = AbstractParticipant("p1")

    if model_path:
        # load the model
        participant.goal_net.load_state_dict(
            torch.load(model_path))
    
    g_n = get_grids_by_number(grid_names, 
                              start_from=start_from)
    first = True
    for grid_names in g_n:
        name_dir = len(os.listdir("data/run_data/"))
        os.makedirs(f"data/run_data/run_{name_dir}/figures", exist_ok=True)
        train_grids = [grid_name.split(".")[0] for grid_name in grid_names if grid_name.split(".")[0] not in TEST_GRIDS[start_from]]
        train_grids = random.choices(train_grids, k=num_train_sessions * 50)
        print(train_grids)
        train_trials = pd.DataFrame(train_grids, columns=["Grid_Name"])
        train_results, train_construction_correctness, train_construction_accuracy, _, _, _, train_goal_choices = (
            run_participant_session(participant, train_trials,
                                    q_type="booom", init_rules = first))

        with open(f"data/run_data/run_{name_dir}/positive_buf.pkl", "wb") as f:
            p.dump(participant.goal_net_memory.positive_memory, f)
        with open(f"data/run_data/run_{name_dir}/negative_buf.pkl", "wb") as f:
            p.dump(participant.goal_net_memory.negative_memory, f)
        
        with open(f"data/run_data/run_{name_dir}/train_grids.pkl", "wb") as f:
            p.dump(train_grids, f)
        with open(f"data/run_data/run_{name_dir}/train_results.pkl", "wb") as f:
            p.dump(train_results, f)
        with open(f"data/run_data/run_{name_dir}/train_construction_correctness.pkl", "wb") as f:
            p.dump(train_construction_correctness, f)
        with open(f"data/run_data/run_{name_dir}/train_construction_accuracy.pkl", "wb") as f:
            p.dump(train_construction_accuracy, f)
        with open(f"data/run_data/run_{name_dir}/train_goal_choices.pkl", "wb") as f:
            p.dump(train_goal_choices, f)
        torch.save(participant.goal_net.state_dict(),
                    f"data/run_data/run_{name_dir}/goal_net.pt")

        train_results_df = pd.DataFrame(
            train_results, columns=["rt", "response_correctness"]
        )
        train_results_df["construction_correctness"] = train_construction_correctness
        train_results_df["goal_choices"] = [len(t) for t in train_goal_choices]
        train_results_df["trial #"] = list(range(1, len(train_results_df) + 1))

        # ---- Plotting ----
        simple_snsplot(
            train_results_df,
            "trial #",
            "construction_correctness",
            f"data/run_data/run_{name_dir}/figures/train_construction_correctness.png",
        )
        simple_snsplot(
            train_results_df,
            "trial #",
            "rt",
            f"data/run_data/run_{name_dir}/figures/train_rt.png",
            line=True)
        simple_snsplot(
            train_results_df,
            "trial #",
            "goal_choices",
            f"data/run_data/run_{name_dir}/figures/train_goal_choices.png",
        )
        simple_snsplot(
            train_results_df,
            "trial #",
            "response_correctness",
            f"data/run_data/run_{name_dir}/figures/train_response_correctness.png",
        )

        first = False
        break

def run_tests(test_grids, model_path):
    participant = AbstractParticipant("p1")
    # load the model
    participant.goal_net.load_state_dict(
        torch.load(model_path))
    participant.toggle_training()

    name_dir = len(os.listdir("data/run_data/"))
    os.makedirs(f"data/run_data/run_{name_dir}/figures", exist_ok=True)
    test_grids = [grid_name.split(".")[0] for grid_name in test_grids]
    test_trials = pd.DataFrame(test_grids, columns=["Grid_Name"])
    test_results, test_construction_correctness, test_construction_accuracy, _, _, _, test_goal_choices = (
        run_participant_session(participant, test_trials,
                                q_type="booom"))
    participant.toggle_training()



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--train_sessions",
        type=int,
        default=3,
    )
    parser.add_argument(
        "--test",
        action="store_true"
    )
    parser.add_argument(
        "--start_from",
        type=int,
        default=1
    )
    parser.add_argument(
        "--model",
        default=None
    )
    parser.add_argument(
        "--no_show_viz",
        action="store_true",
        help="do not show the visualization while running the program"
    )

    args = parser.parse_args()

    random.seed(0)
    os.environ["VIZ_SHOW"] = "false" if args.no_show_viz else "true"

    if not args.test:
        print(f"Num Train Sesh: {args.train_sessions}\nStart From: {args.start_from}\nModel Path: {args.model}\nNo Show Viz: {args.no_show_viz}\n")
        run_experiment(num_train_sessions=args.train_sessions,
                        start_from=args.start_from,
                        model_path=args.model)
    else:
        assert args.model
        run_tests(TEST_GRID_ONES, args.model)

# natural test for grid ones: ['GRID_489', 'GRID_565', 'GRID_504', 'GRID_507', 'GRID_524', 'GRID_500', 'GRID_535', 'GRID_555', 'GRID_528', 'GRID_542', 'GRID_518', 'GRID_525', 'GRID_503', 'GRID_483', 'GRID_549', 'GRID_547', 'GRID_551']