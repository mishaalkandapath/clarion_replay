from pyClarion import (Agent, Input, Choice, ChunkStore, FixedRules, 
    Family, Atoms, Atom, BaseLevel, Pool, NumDict, Event, Priority, Site, IDN, Train)
from pyClarion.components.stats import MatchStats
from datetime import timedelta

import logging
import sys, os, random

import numpy as np
import pandas as pd
from typing import *

from utils import *
from knowledge_init import *
from rule_defs import * 
from base_participant import *
from evaluation import * 
import math

# plotting 
import seaborn as sns
from matplotlib import pyplot as plt

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s')

logger = logging.getLogger("pyClarion.system")
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
# handler.setFormatter(formatter)
logger.addHandler(handler)


def present_stimulus(d:BrickConstructionTask, stim_grid: np.ndarray, mlp_space_1: MLPConstructionIO, mlp_space_2: Numbers):
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
            mlp_send_val = (
                           + mlp_space_1[brick_row_map[brick][1]] ** mlp_space_2[f"n{row_indices[0]}"]
                           + mlp_space_1[brick_row_map[brick][2]] ** mlp_space_2[f"n{row_indices[1]}"]
                           + mlp_space_1[brick_row_map[brick][3]] ** mlp_space_2[f"n{row_indices[2]}"]
                           + mlp_space_1[brick_col_map[brick][1]] ** mlp_space_2[f"n{col_indices[0]}"]
                           + mlp_space_1[brick_col_map[brick][2]] ** mlp_space_2[f"n{col_indices[1]}"]
                           + mlp_space_1[brick_col_map[brick][3]] ** mlp_space_2[f"n{col_indices[2]}"])
        else:
            in_send_val = (in_send_val
                            + d.io[shape_brick_map[brick]] ** d.response.yes
                            + d.io[brick_row_map[brick][1]] ** d.numbers[f"n{row_indices[0]}"]
                            + d.io[brick_row_map[brick][2]] ** d.numbers[f"n{row_indices[1]}"]
                            + d.io[brick_row_map[brick][3]] ** d.numbers[f"n{row_indices[2]}"]
                            + d.io[brick_col_map[brick][1]] ** d.numbers[f"n{col_indices[0]}"]
                            + d.io[brick_col_map[brick][2]] ** d.numbers[f"n{col_indices[1]}"]
                            + d.io[brick_col_map[brick][3]] ** d.numbers[f"n{col_indices[2]}"])
            
            mlp_send_val = (mlp_send_val
                            + mlp_space_1[brick_row_map[brick][1]] ** mlp_space_2[f"n{row_indices[0]}"]
                            + mlp_space_1[brick_row_map[brick][2]] ** mlp_space_2[f"n{row_indices[1]}"]
                            + mlp_space_1[brick_row_map[brick][3]] ** mlp_space_2[f"n{row_indices[2]}"]
                            + mlp_space_1[brick_col_map[brick][1]] ** mlp_space_2[f"n{col_indices[0]}"]
                            + mlp_space_1[brick_col_map[brick][2]] ** mlp_space_2[f"n{col_indices[1]}"]
                            + mlp_space_1[brick_col_map[brick][3]] ** mlp_space_2[f"n{col_indices[2]}"])
            
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

def load_trial(construction_space: BrickConstructionTask | BrickConstructionTaskAbstractParticipant, response_space: BrickResponseTask,
               mlp_space_1: MLPConstructionIO, mlp_space_2: Numbers,
                trial: pd.Series, t_type="test", q_type="query"):
    d = response_space
    
    grid_name = trial["Grid_Name"]
    
    stim_grid = np.load(f"/Users/mishaal/personalproj/clarion_replay/processed/{t_type}_data/{t_type}_stims/{grid_name}.npy")         
    chunk_grid, chunk_grid_mlp = present_stimulus(construction_space, stim_grid, mlp_space_1, mlp_space_2)
    
    query_map = {1: d.query_rel.left, 2: d.query_rel.above, 3: d.query_rel.right, 4: d.query_rel.below}
    query_col_map = {1: "left_element", 2: "ontop_element", 3: "right_element", 4: "below_element"}
    brick_map = {1: d.bricks.half_T, 2: d.bricks.mirror_L, 3: d.bricks.vertical, 4: d.bricks.horizontal}

    choice_is_yes = None

    print("Stimulus grid: \n", stim_grid)

    if t_type == "test":
        chunk_test = ( + d.io.query_relation ** query_map[trial["Q_Relation"]] 
                      + d.io.query_block_reference ** brick_map[trial["Q_Brick_Left"]]
                      + d.io.query_block ** brick_map[trial["Q_Brick_Middle"]])

        choice_is_yes = trial[query_col_map[trial["Q_Relation"]]] == brick_map[trial["Q_Brick_Left"]] and trial[query_col_map[trial["Q_Relation"] - 2 if trial["Q_Relation"] > 2 else trial["Q_Relation"]+2]] == brick_map[trial["Q_Brick_Middle"]]
    elif t_type == "train" and q_type == "query":
        #get connection structure 
        # choose 2 blocks randomly
        blocks = np.random.choice((t := np.unique(stim_grid))[t != 0], 2, replace=False)
        # choose a relation randomly
        relation = np.random.choice([1, 2, 3, 4], 1)
        chunk_test = ( + d.io.query_relation ** query_map[relation[0]] 
                      + d.io.query_block ** brick_map[blocks[0]]
                      + d.io.query_block_reference ** brick_map[blocks[1]])

        if blocks[0] in stim_grid and blocks[1] in stim_grid:
            _, brick_conn = brick_connectedness(np.where((stim_grid == blocks[0]) | (stim_grid == blocks[1]), stim_grid, 0))
            choice_is_yes = brick_conn[relation[0] - 1] == blocks[0] and brick_conn[relation[0] - 3 if relation[0] in (3, 4) else relation[0] + 1] == blocks[1]
        else:
            choice_is_yes = False

    else: chunk_test = ()
    
    if q_type == "query" and t_type == "test":
        print("Query brick 1: ", trial["Q_Brick_Left"])
        print("Query brick 2: ", trial["Q_Brick_Middle"])
        print("Query relation: ", trial["Q_Relation"])
    elif q_type == "query":
        print("Query brick 1: ", blocks[0])
        print("Query brick 2: ", blocks[1])
        print("Query relation: ", relation[0])

    return stim_grid, chunk_grid, chunk_grid_mlp, chunk_test, choice_is_yes

def run_participant_session(participant: BaseParticipant, session_df: pd.DataFrame, session_type="train", q_type="query"):
    global rule_defs
    # some results
    results, construction_correctness, all_rule_history, all_rule_lhs_history = [], [], [], []
    # neural network training stats:
    construction_reward_vals, construction_q_vals, construction_action_vals = [], [], []   
    trials = []
    # Knowledge initialization
    init_participant_response_rules(participant)
    if type(participant) is LowLevelParticipant:
        init_participant_construction_rules(participant)
    elif type(participant) is AbstractParticipant:
        init_participant_construction_rule_w_abstract(participant)
    
    for _, trial in session_df.iterrows():
        trials.append(trial)
        break # testing
    
    participant.start_construct_trial(timedelta(seconds=1))
    last_end_construction_time = None
    while participant.system.queue:
        event = participant.system.advance()
        if event.source == participant.start_construct_trial:
            if not trials: break
            #load the next trial
            trial = trials.pop(0)
            grid_stimulus_np, grid_stimulus, grid_stimulus_mlp, test_query, choice_is_yes = load_trial(participant.construction_space, participant.response_space,
                                                                                                       participant.mlp_space_1, participant.mlp_space_2,
                                                                                                       trial, t_type=session_type, q_type=q_type,)
            participant.mlp_construction_input.send(grid_stimulus_mlp, flip=True)
            participant.construction_input.send(grid_stimulus, flip=True) # TODO: have a timeout somehow: but how to do timeout wihout proper timinmg constraints for the various events in the queue?
        elif event.source == participant.end_construction:
            correctness = np.all(grid_stimulus_np == numpify_grid(participant.construction_input.main[0]))
            construction_correctness.append(correctness)
            if session_type == "train":
                print("Construction was ", "correct" if correctness else "incorrect")
                participant.propagate_feedback(correct = float(correctness))
                participant.end_construction_feedback()
            else:
                participant.start_response_trial(timedelta()) #TODO: checkout the actual time delays
        elif event.source == participant.goal_net.error.update:
            #plot the current bit:        
            plt.plot(participant.construction_net_training_results)
            plt.savefig("figures/construction_net_training.png")
        elif event.source == participant.end_construction_feedback:
            participant.start_response_trial(timedelta())
        elif event.source == participant.start_response_trial:
            participant.response_input.send(test_query, flip=True) # dont reset, just add
            last_end_construction_time = event.time
        elif event.source == participant.response_rules.rules.rhs.td.update:
            participant.response_choice.select()
        elif event.source == participant.response_choice.select:
            results.append(((event.time - last_end_construction_time).total_seconds(), 
                            (participant.response_choice.poll()[~participant.response_space.io.output * ~participant.response_space.response] == ~participant.response_space.io.output * ~participant.response_space.response.yes) == choice_is_yes)) #TODO: come up with a way to save the sequences of search space rules that were activated -- is there in sample attribute of the choice in a rule i believe?
            last_end_construction_time = None
            participant.finish_response_trial(timedelta())
        elif event.source == participant.finish_response_trial:
            all_rule_history.append(participant.all_rule_history)
            all_rule_lhs_history.append(participant.all_rule_lhs_history)
            participant.start_construct_trial(timedelta())
    return results, construction_correctness, all_rule_history, all_rule_lhs_history

# trials_df = pd.read_csv("~/personalproj/clarion_replay/processed/test_data/all_test_data.csv")
# run_participant_session(LowLevelParticipant("p1"), trials_df)

def run_experiment(num_train_trials=100, num_test_trials=20, run_train_only=False):

    grid_names = os.listdir("processed/train_data/train_stims/")
    test_trials = pd.read_csv("processed/test_data/all_test_data.csv")
    participant = AbstractParticipant("p1")

    if num_train_trials:
        train_grids = random.choices(grid_names, k=num_train_trials)
        train_grids = [grid_name.split(".")[0] for grid_name in train_grids]
        #make this list a pandas dataframe
        train_trials = pd.DataFrame(train_grids, columns=["Grid_Name"])
        train_results, train_construction_correctness, _, _ = run_participant_session(participant, train_trials)

        train_results_df = pd.DataFrame(train_results, columns=["rt", "response_correctness"])
        train_results_df["construction_correctness"] = train_construction_correctness
        train_results_df["trial #"] = list(range(1, len(train_results_df) + 1))

        # ---- Plotting ---- 
        sns.scatterplot(train_results_df, x="trial #", y="construction_correctness")
        plt.savefig("figures/train_construction_correctness.png")
        plt.clf()

        sns.scatterplot(train_results_df, x="trial #", y="rt")
        sns.lineplot(train_results_df, x="trial #", y="rt", color="red")
        plt.savefig("figures/train_rt.png")
        plt.clf()

        sns.scatterplot(train_results_df, x="trial #", y="response_correctness")
        plt.savefig("figures/train_response_correctness.png")
        plt.clf()

    if run_train_only: return

    test_trial_indices = random.sample(test_trials['PID'].unique().tolist(), num_test_trials)
    test_trials = test_trials[test_trials["PID"].isin(test_trial_indices)]

    test_grid_names = test_trials["Grid_Name"].tolist()
    test_grids = [np.load(f"processed/test_data/test_stims/{grid_name}.npy") for grid_name in test_grid_names]

    test_results, test_construction_correctness, test_rule_choices, test_rule_lhs_information = run_participant_session(participant, test_trials, session_type="test", q_type="query")

    test_results_df = pd.DataFrame(test_results, columns=["rt", "response_correctness"])
    test_results_df["construction_correctness"] = test_construction_correctness
    test_results_df["trial #"] = list(range(1, len(test_results_df) + 1))

    # --- Plotting ---

    sns.scatterplot(test_results_df, x="trial #", y="construction_correctness")
    plt.savefig("figures/test_construction_correctness.png")
    plt.clf()

    sns.scatterplot(test_results_df, x="trial #", y="rt")
    sns.lineplot(test_results_df, x="trial #", y="rt", color="red")
    plt.savefig("figrues/test_rt.png")
    plt.clf()

    sns.scatterplot(test_results_df, x="trial #", y="response_correctness")
    plt.savefig("figures/test_response_correctness.png")
    plt.clf()

    # delayed effects data:
    n_stable_to_present, n_present_to_stable, n_distant_to_stable, n_stable_to_distant, n_present_to_present = simple_sequenceness(test_rule_choices, test_rule_lhs_information, test_grids)
    n_stable_to_present = n_stable_to_present.mean(axis=0)
    n_present_to_stable = n_present_to_stable.mean(axis=0)
    n_distant_to_stable = n_distant_to_stable.mean(axis=0)
    n_stable_to_distant = n_stable_to_distant.mean(axis=0)
    n_present_to_present = n_present_to_present.mean(axis=0)
    # plot the delayed effects
    plt.figure(figsize=(8, 4))
    plt.plot(n_stable_to_present, label='Stable to Present', color='C0')
    plt.plot(n_present_to_stable, label='Present to Stable', color='C1')
    plt.plot(n_distant_to_stable, label='Distant to Stable', color='C2')
    plt.plot(n_stable_to_distant, label='Stable to Distant', color='C3')
    plt.plot(n_present_to_present, label='Present to Present', color='C4')
    plt.xlabel('Time steps')
    plt.ylabel('Sequence occurence average')
    plt.title("Sequences across steps")
    plt.legend()
    plt.savefig("figures/sequences_simple.png")

    # n_lags, betas, pvals = calculate_delayed_effects(test_rule_choices, max_lag=10)
    # time_ms = np.arange(n_lags) * 10  # adjust if your step ≠10ms

    # plt.figure(figsize=(8, 4))
    # plt.plot(time_ms, betas, label='GLM β (data ← theory)', color='C2')
    # plt.axhline(0, color='k', linestyle='--', linewidth=0.8)

    # # Optionally, mark timepoints with p<0.05
    # sig = pvals < 0.05
    # plt.scatter(time_ms[sig], betas[sig], color='red', s=20, label='p < 0.05')

    # plt.xlabel('Time lag (ms)')
    # plt.ylabel('Regression β')
    # plt.title('Sequenceness β‑weights (empirical vs. theoretical)')
    # plt.legend()
    # plt.tight_layout()
    # plt.show()

if __name__ == "__main__":
    run_experiment(num_train_trials=10, num_test_trials=2)