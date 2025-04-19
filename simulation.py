from pyClarion import (Agent, Input, Choice, ChunkStore, FixedRules, 
    Family, Atoms, Atom, BaseLevel, Pool, NumDict, Event, Priority, Site, IDN, Train)
from pyClarion.components.stats import MatchStats
from datetime import timedelta

import logging
import sys

import numpy as np
import pandas as pd
from typing import *

from utils import *
from knowledge_init import *
from rule_defs import * 
from base_participant import *
import math

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s')

logger = logging.getLogger("pyClarion.system")
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
# handler.setFormatter(formatter)
logger.addHandler(handler)


def present_stimulus(d:BrickConstructionTask, stim_grid: np.ndarray):
    stim_bricks = np.unique(stim_grid)
    stim_bricks = stim_bricks[stim_bricks != 0]
    
    brick_row_map = {1: {1: "input_half_T_row1", 2: "input_half_T_row2", 3: "input_half_T_row3"}, 2: {1: "input_mirror_L_row1", 2: "input_mirror_L_row2", 3: "input_mirror_L_row3"}, 3: {1: "input_vertical_row1", 2: "input_vertical_row2", 3: "input_vertical_row3"}, 4: {1: "input_horizontal_row1", 2: "input_horizontal_row2", 3: "input_horizontal_row3"}}
    brick_col_map = {1: {1: "input_half_T_col1", 2: "input_half_T_col2", 3: "input_half_T_col3"}, 2: {1: "input_mirror_L_col1", 2: "input_mirror_L_col2", 3: "input_mirror_L_col3"}, 3: {1: "input_vertical_col1", 2: "input_vertical_col2", 3: "input_vertical_col3"}, 4: {1: "input_horizontal_col1", 2: "input_horizontal_col2", 3: "input_horizontal_col3"}}
    shape_brick_map = {1: "input_half_T", 2: "input_mirror_L", 3: "input_vertical", 4: "input_horizontal"}
    
    in_send_val = None
    mlp_send_val = None
    for i, brick in enumerate(stim_bricks):
        # brick row indices: 
        row_indices = np.where(stim_grid == brick)[0] + 1
        col_indices = np.where(stim_grid == brick)[1] + 1

        if not in_send_val:
            in_send_val = (+ d.io[shape_brick_map[brick]] ** d.response.yes
                           + d.io[brick_row_map[brick][1]] ** d.numbers[f"n{row_indices[0]}"] 
                           + d.io[brick_row_map[brick][2]] **  d.numbers[f"n{row_indices[1]}"]
                           + d.io[brick_row_map[brick][3]] ** d.numbers[f"n{row_indices[2]}"]
                           + d.io[brick_col_map[brick][1]] ** d.numbers[f"n{col_indices[0]}"]
                           + d.io[brick_col_map[brick][2]] ** d.numbers[f"n{col_indices[1]}"]
                           + d.io[brick_col_map[brick][3]] ** d.numbers[f"n{col_indices[2]}"])
        else:
            in_send_val = (in_send_val
                            + d.io[shape_brick_map[brick]] ** d.response.yes
                            + d.io[brick_row_map[brick][1]] ** d.numbers[f"n{row_indices[0]}"]
                            + d.io[brick_row_map[brick][2]] ** d.numbers[f"n{row_indices[1]}"]
                            + d.io[brick_row_map[brick][3]] ** d.numbers[f"n{row_indices[2]}"]
                            + d.io[brick_col_map[brick][1]] ** d.numbers[f"n{col_indices[0]}"]
                            + d.io[brick_col_map[brick][2]] ** d.numbers[f"n{col_indices[1]}"]
                            + d.io[brick_col_map[brick][3]] ** d.numbers[f"n{col_indices[2]}"])
    in_send_val = (in_send_val
                   + d.io.target_half_T ** d.response.no
                   + d.io.target_mirror_L ** d.response.no
                   + d.io.target_vertical ** d.response.no
                   + d.io.target_horizontal ** d.response.no)
            
    # get the shapes that were not used and set their response to no
    for i in range(1, 5):
        if i not in stim_bricks:
            in_send_val = (in_send_val
                           + d.io[shape_brick_map[i]] ** d.response.no)
            
    return in_send_val, mlp_send_val

def load_trial(construction_space: BrickConstructionTask, response_space: BrickResponseTask,
                trial: pd.Series, t_type="test", q_type="query"):
    d = response_space
    
    grid_name = trial["Grid_Name"]
    
    stim_grid = np.load(f"/Users/mishaal/personalproj/clarion_replay/processed/{t_type}_data/{t_type}_stims/{grid_name}.npy")         
    chunk_grid, chunk_grid_mlp = present_stimulus(construction_space, stim_grid)
    
    query_map = {1: d.query_rel.left, 2: d.query_rel.above, 3: d.query_rel.right, 4: d.query_rel.below}
    brick_map = {1: d.bricks.half_T, 2: d.bricks.mirror_L, 3: d.bricks.vertical, 4: d.bricks.horizontal}

    if t_type == "test":
        chunk_test = ( + d.io.query_relation ** query_map[trial["Q_Relation"]] 
                      + d.io.query_block ** brick_map[trial["Q_Brick_Left"]]
                      + d.io.query_block_reference ** brick_map[trial["Q_Brick_Right"]])
    elif t_type == "train" and q_type == "query":
        # choose 2 blocks randomly
        blocks = np.random.choice((t := np.unique(stim_grid))[t != 0], 2, replace=False)
        # choose a relation randomly
        relation = np.random.choice([1, 2, 3, 4], 1)
        chunk_test = ( + d.io.query_relation ** query_map[relation[0]] 
                      + d.io.query_block ** brick_map[blocks[0]]
                      + d.io.query_block_reference ** brick_map[blocks[1]])
    else: chunk_test = ()

    print("Stimulus grid: ", stim_grid)
    if q_type == "query" and t_type == "test":
        print("Query brick 1: ", trial["Q_Brick_Left"])
        print("Query brick 2: ", trial["Q_Brick_Right"])
        print("Query relation: ", trial["Q_Relation"])
    elif q_type == "query":
        print("Query brick 1: ", blocks[0])
        print("Query brick 2: ", blocks[1])
        print("Query relation: ", relation[0])

    return stim_grid, chunk_grid, chunk_grid_mlp, chunk_test

def run_participant_session(participant: BaseParticipant, session_df: pd.DataFrame, session_type="train", q_type="query"):
    global rule_defs
    results = []
    trials = []
    # Knowledge initialization
    init_participant_response_rules(participant)
    init_participant_construction_rules(participant)
    
    for _, trial in session_df.iterrows():
        trials.append(trial)
        break # testing
    
    participant.start_construct_trial(timedelta(seconds=1))
    while participant.system.queue:
        event = participant.system.advance()
        if event.source == participant.start_construct_trial:
            if not trials: break
            #load the next trial
            trial = trials.pop(0)
            grid_stimulus_np, grid_stimulus, grid_stimulus_mlp, test_query = load_trial(participant.construction_space, participant.response_space, trial, t_type=session_type, q_type=q_type)
            participant.construction_input.send(grid_stimulus) # TODO: have a timeout somehow: but how to do timeout wihout proper timinmg constraints for the various events in the queue?
        elif event.source == participant.end_construction:
            if session_type == "train":
                print("Construction was ", "correct" if np.all(grid_stimulus_np == numpify_grid(participant.construction_input.main[0])) else "incorrect")
                participant.propagate_feedback(correct = np.all(grid_stimulus_np == numpify_grid(participant.construction_input.main[0])))
            else:
                participant.start_response_trial(timedelta()) #TODO: checkout the actual time delays
        elif event.source == participant.end_construction_feedback:
            participant.start_response_trial(timedelta())
        elif event.source == participant.start_response_trial:
            participant.response_input.send(test_query, flip=True) # dont reset, just add
        elif event.source == participant.response_rules.rules.rhs.td.update:
            participant.response_choice.select()
        elif event.source == participant.response_choice.select:
            results.append((event.time, participant.response_choice.poll())) #TODO: come up with a way to save the sequences of search space rules that were activated -- is there in sample attribute of the choice in a rule i believe?
            participant.finish_response_trial(timedelta())
        elif event.source == participant.finish_response_trial:
            participant.start_construct_trial(timedelta())

trials_df = pd.read_csv("~/personalproj/clarion_replay/processed/test_data/all_test_data.csv")
run_participant_session(LowLevelParticipant("p1"), trials_df)