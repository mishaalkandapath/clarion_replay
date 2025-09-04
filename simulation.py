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
from knowledge_init import (
    Numbers,
    BrickResponseTask,
    BrickConstructionTask,
    BrickConstructionTaskAbstractParticipant,
    MLPConstructionIO,
)
from rule_defs import (
    init_participant_response_rules,
    init_participant_construction_rules,
    init_participant_construction_rule_w_abstract,
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
from simulation_viz import SimulationVisualizer
from plotting import (simple_plotting, simple_snsplot, 
                      plot_sequences, plot_rl_stats)


def present_stimulus(
    d: BrickConstructionTask,
    stim_grid: np.ndarray,
    mlp_space_1: MLPConstructionIO,
    mlp_space_2: Numbers,
):
    stim_bricks = np.unique(stim_grid)
    stim_bricks = stim_bricks[stim_bricks != 0]
    brick_row_map = {1: {1: "input_half_T_row1",
                         2: "input_half_T_row2",
                         3: "input_half_T_row3"},
                     2: {1: "input_mirror_L_row1",
                         2: "input_mirror_L_row2",
                         3: "input_mirror_L_row3",
                         },
                     3: {1: "input_vertical_row1",
                         2: "input_vertical_row2",
                         3: "input_vertical_row3",
                         },
                     4: {1: "input_horizontal_row1",
                         2: "input_horizontal_row2",
                         3: "input_horizontal_row3",
                         },
                     }
    brick_col_map = {1: {1: "input_half_T_col1",
                         2: "input_half_T_col2",
                         3: "input_half_T_col3"},
                     2: {1: "input_mirror_L_col1",
                         2: "input_mirror_L_col2",
                         3: "input_mirror_L_col3",
                         },
                     3: {1: "input_vertical_col1",
                         2: "input_vertical_col2",
                         3: "input_vertical_col3",
                         },
                     4: {1: "input_horizontal_col1",
                         2: "input_horizontal_col2",
                         3: "input_horizontal_col3",
                         },
                     }
    shape_brick_map = {
        1: "input_half_T",
        2: "input_mirror_L",
        3: "input_vertical",
        4: "input_horizontal",
    }
    in_send_val = None
    mlp_send_val = None
    for i, brick in enumerate(stim_bricks):
        # brick row indices:
        row_indices = np.where(stim_grid == brick)[0] + 1
        col_indices = np.where(stim_grid == brick)[1] + 1
        if not in_send_val:
            in_send_val = (
                + d.io[shape_brick_map[brick]] ** d.response.yes
                + d.io[brick_row_map[brick][1]] ** d.numbers[f"n{row_indices[0]}"]
                + d.io[brick_row_map[brick][2]] ** d.numbers[f"n{row_indices[1]}"]
                + d.io[brick_row_map[brick][3]] ** d.numbers[f"n{row_indices[2]}"]
                + d.io[brick_col_map[brick][1]] ** d.numbers[f"n{col_indices[0]}"]
                + d.io[brick_col_map[brick][2]] ** d.numbers[f"n{col_indices[1]}"]
                + d.io[brick_col_map[brick][3]] ** d.numbers[f"n{col_indices[2]}"]
            )
            mlp_send_val = (
                +(
                    mlp_space_1[brick_row_map[brick][1]]
                    ** mlp_space_2[f"n{row_indices[0]}"]
                )
                + mlp_space_1[brick_row_map[brick][2]]
                ** mlp_space_2[f"n{row_indices[1]}"]
                + mlp_space_1[brick_row_map[brick][3]]
                ** mlp_space_2[f"n{row_indices[2]}"]
                + mlp_space_1[brick_col_map[brick][1]]
                ** mlp_space_2[f"n{col_indices[0]}"]
                + mlp_space_1[brick_col_map[brick][2]]
                ** mlp_space_2[f"n{col_indices[1]}"]
                + mlp_space_1[brick_col_map[brick][3]]
                ** mlp_space_2[f"n{col_indices[2]}"]
            )
        else:
            in_send_val = (in_send_val +
                           d.io[shape_brick_map[brick]] ** d.response.yes +
                           d.io[brick_row_map[brick][1]] ** d.numbers[f"n{row_indices[0]}"] +
                           d.io[brick_row_map[brick][2]] ** d.numbers[f"n{row_indices[1]}"] +
                           d.io[brick_row_map[brick][3]] ** d.numbers[f"n{row_indices[2]}"] +
                           d.io[brick_col_map[brick][1]] ** d.numbers[f"n{col_indices[0]}"] +
                           d.io[brick_col_map[brick][2]] ** d.numbers[f"n{col_indices[1]}"] +
                           d.io[brick_col_map[brick][3]] ** d.numbers[f"n{col_indices[2]}"])
            mlp_send_val = (
                mlp_send_val
                + mlp_space_1[brick_row_map[brick][1]]
                ** mlp_space_2[f"n{row_indices[0]}"]
                + mlp_space_1[brick_row_map[brick][2]]
                ** mlp_space_2[f"n{row_indices[1]}"]
                + mlp_space_1[brick_row_map[brick][3]]
                ** mlp_space_2[f"n{row_indices[2]}"]
                + mlp_space_1[brick_col_map[brick][1]]
                ** mlp_space_2[f"n{col_indices[0]}"]
                + mlp_space_1[brick_col_map[brick][2]]
                ** mlp_space_2[f"n{col_indices[1]}"]
                + mlp_space_1[brick_col_map[brick][3]]
                ** mlp_space_2[f"n{col_indices[2]}"]
            )
        in_send_val = (
            in_send_val
            + d.io.target_half_T**d.response.no
            + d.io.target_mirror_L**d.response.no
            + d.io.target_vertical**d.response.no
            + d.io.target_horizontal**d.response.no
        )
    # get the shapes that were not used and set their response to no
    for i in range(1, 5):
        if i not in stim_bricks:
            in_send_val = in_send_val + \
                d.io[shape_brick_map[i]] ** d.response.no
    return in_send_val, mlp_send_val


def load_trial(
    construction_space: BrickConstructionTask
    | BrickConstructionTaskAbstractParticipant,
    response_space: BrickResponseTask,
    mlp_space_1: MLPConstructionIO,
    mlp_space_2: Numbers,
    trial: pd.Series,
    t_type="test",
    q_type="query",
):
    grid_name = trial["Grid_Name"]
    stim_grid = np.load(
        f"data/processed/{t_type}_data/{t_type}_stims/{grid_name}.npy"
    )
    chunk_grid, chunk_grid_mlp = present_stimulus(
        construction_space, stim_grid, mlp_space_1, mlp_space_2
    )

    query_map = {
        1: response_space.query_rel.left,
        2: response_space.query_rel.above,
        3: response_space.query_rel.right,
        4: response_space.query_rel.below,
    }
    query_col_map = {
        1: "left_element",
        2: "ontop_element",
        3: "right_element",
        4: "below_element",
    }
    brick_map = {
        1: response_space.bricks.half_T,
        2: response_space.bricks.mirror_L,
        3: response_space.bricks.vertical,
        4: response_space.bricks.horizontal,
    }
    choice_is_yes = None
    # print("Stimulus grid: \n", stim_grid)
    if t_type == "test":
        chunk_test = (
            +(response_space.io.query_relation ** query_map[trial["Q_Relation"]])
            + response_space.io.query_block_reference
            ** brick_map[trial["Q_Brick_Left"]]
            + response_space.io.query_block ** brick_map[trial["Q_Brick_Middle"]]
        )
        choice_is_yes = (
            trial[query_col_map[trial["Q_Relation"]]]
            == brick_map[trial["Q_Brick_Left"]]
            and trial[
                query_col_map[
                    trial["Q_Relation"] - 2
                    if trial["Q_Relation"] > 2
                    else trial["Q_Relation"] + 2
                ]
            ]
            == brick_map[trial["Q_Brick_Middle"]]
        )
    elif t_type == "train" and q_type == "query":
        # get connection structure
        # choose 2 blocks randomly
        blocks = np.random.choice(
            (t := np.unique(stim_grid))[
                t != 0], 2, replace=False)
        # choose a relation randomly
        relation = np.random.choice([1, 2, 3, 4], 1)
        chunk_test = (
            +(response_space.io.query_relation ** query_map[relation[0]])
            + response_space.io.query_block ** brick_map[blocks[0]]
            + response_space.io.query_block_reference ** brick_map[blocks[1]]
        )
        if blocks[0] in stim_grid and blocks[1] in stim_grid:
            (_, brick_conn) = brick_connectedness(
                np.where(
                    (stim_grid == blocks[0]) | (stim_grid == blocks[1]), stim_grid, 0
                )
            )
            choice_is_yes = (
                brick_conn[relation[0] - 1] == blocks[0]
                and brick_conn[relation[0] - 3
                               if relation[0] in (3, 4) else
                               relation[0] + 1]
                == blocks[1]
            )
        else:
            choice_is_yes = False
    else:
        chunk_test = ()
        choice_is_yes = None
    # if q_type == "query" and t_type == "test":
    #     print("Query brick 1: ", trial["Q_Brick_Left"])
    #     print("Query brick 2: ", trial["Q_Brick_Middle"])
    #     print("Query relation: ", trial["Q_Relation"])
    # elif q_type == "query":
    #     print("Query brick 1: ", blocks[0])
    #     print("Query brick 2: ", blocks[1])
    #     print("Query relation: ", relation[0])
    return stim_grid, chunk_grid, chunk_grid_mlp, chunk_test, choice_is_yes


def run_participant_session(
    participant: BaseParticipant,
    session_df: pd.DataFrame,
    session_type="train",
    q_type="query",
    init_rules=True,
):
    per_trial_time = 3.5 if session_type != "train" else 6
    # some results
    (
        results,
        construction_accuracy,
        construction_correctness,
        all_constructions,
        all_rule_history,
        all_rule_lhs_history,
        all_goal_choices
    ) = [], [], [], [], [], [], []
    all_grids = []
    # Knowledge initialization
    if init_rules:
        init_participant_response_rules(participant)
        if isinstance(participant, LowLevelParticipant):
            init_participant_construction_rules(participant)
        elif isinstance(participant, AbstractParticipant):
            init_participant_construction_rule_w_abstract(participant)
    trials = []
    for _, trial in session_df.iterrows():
        trials.append(trial)
    original_length = len(trials)
    done_count = 0
    viz = SimulationVisualizer()
    viz.init_progress(original_length)
    participant.start_construct_trial(timedelta())
    last_end_construction_time = None
    start_time = timedelta(0)
    real_start_time = datetime.now()
    pbar = tqdm.tqdm(total=original_length, desc="backtracks")
    while participant.system.queue:
        event = participant.system.advance()
        pbar.set_description(f"Backtracks: {participant.backtracks}")
        viz.update_time(event.time)
        if event.source == participant.start_construct_trial:
            if not trials:
                break
            # load the next trial
            trial = trials.pop(0)
            (
                grid_stimulus_np,
                grid_stimulus,
                grid_stimulus_mlp,
                test_query,
                choice_is_yes,
            ) = load_trial(
                participant.construction_space,
                participant.response_space,
                participant.mlp_space_1,
                participant.mlp_space_2,
                trial,
                t_type=session_type,
                q_type=q_type,
            )
            participant.mlp_construction_input.send(
                grid_stimulus_mlp, flip=True)
            participant.construction_input.send(grid_stimulus, flip=True)
            all_grids.append(grid_stimulus_np)
            viz.start_trial()
            viz.update_input(grid_stimulus_np)
            start_time = event.time
        elif event.source == participant.construction_input.send:
            viz.update_work(
                numpify_grid(
                    participant.construction_input.main[0]))
            if participant.past_chosen_goals:
                chosen_goal = participant.past_chosen_goals[-1]
                chosen_goal = str(chosen_goal).split(":")[-1].split(",")[-1]
                if re.match(SHAPE_SHAPE_REL, chosen_goal):
                    chosen_goal = re.match(SHAPE_SHAPE_REL, chosen_goal)
                    viz.update_status(
                        chosen_goal.group(3),
                        chosen_goal.group(1),
                        chosen_goal.group(2),
                        (
                            "TBD"
                            if (
                                not participant.transition_store
                                or not isinstance(participant.transition_store[-1], float)
                            )
                            else participant.transition_store[-1]
                        ),
                    )
                else:
                    chosen_goal = re.match(SHAPE_START, chosen_goal)
                    viz.update_status(
                        "start",
                        "",
                        chosen_goal.group(1),
                        (
                            "TBD"
                            if (
                                not participant.transition_store
                                or not isinstance(participant.transition_store[-1], float)
                            )
                            else (participant.transition_store[-1])
                        ),
                    )
        elif event.source == participant.end_construction:
            accuracy = acc(
                grid_stimulus_np, numpify_grid(
                    participant.construction_input.main[0]))
            construction_accuracy.append(accuracy)
            correctness = 1 if accuracy == 1 else 0
            construction_correctness.append(correctness)
            if session_type == "train":
                # print(
                #     "Construction was ",
                #     "correct" if correctness == 1 else "incorrect")
                # participant.propagate_feedback(correct=float(correctness)) #TODO: GET THIS BACK IF U NEED IT
                participant.end_construction_feedback()
            else:
                participant.start_response_trial(timedelta())
        elif event.source == participant.backward_qnet:
            # plot the current bit:
            simple_plotting(
                participant.construction_net_training_results,
                "Steps",
                "Loss",
                "data/figures/construction_net_training.png",
                viz.fig.number,
            )
        elif event.source == participant.end_construction_feedback:
            if q_type == "query": participant.start_response_trial(timedelta())
            else: 
                all_rule_history.append(participant.all_rule_history)
                all_rule_lhs_history.append(participant.all_rule_lhs_history)
                all_constructions.append(participant.all_constructions)
                all_goal_choices.append(participant.all_goal_history[:-1])
                participant.finish_response_trial(timedelta())
        elif event.source == participant.start_response_trial:
            participant.response_input.send(
                test_query, flip=True
            )  # dont reset, just add
            last_end_construction_time = event.time
            match = re.match(QUERY_REL_PATTERN, str(test_query), re.DOTALL)
            # viz.start_response(SHAPE_DICT[match.group(
            #     2)], SHAPE_DICT[match.group(3)], match.group(1))
        elif event.source == participant.response_choice.select:
            results.append(
                (
                    (event.time - last_end_construction_time).total_seconds(),
                    (
                        participant.response_choice.poll()[
                            ~participant.response_space.io.output
                            * ~participant.response_space.response
                        ]
                        == ~participant.response_space.io.output
                        * ~participant.response_space.response.yes
                    )
                    == choice_is_yes,
                )
            )
            last_end_construction_time = None
            viz.choose_response(
                "yes"
                if (
                    participant.response_choice.poll()[
                        ~participant.response_space.io.output
                        * ~participant.response_space.response
                    ]
                    == ~participant.response_space.io.output
                    * ~participant.response_space.response.yes
                )
                else "no"
            )
            all_rule_history.append(participant.all_rule_history)
            all_rule_lhs_history.append(participant.all_rule_lhs_history)
            all_constructions.append(participant.all_constructions)
            all_goal_choices.append(participant.all_goal_history[:-1])
            participant.finish_response_trial(timedelta())
        elif event.source == participant.finish_response_trial:
            if original_length - len(trials) == 20 and session_type == "train":
                # its a session break
                # 35 slightly smaller than 50 to account for lesser trials
                original_length = len(trials)
                participant.replay_optimize_qnet()
                continue
            simple_plotting(
                construction_correctness,
                "trial #",
                "construction correctness",
                "data/figures/construction_correctness.png"
            )
            simple_plotting(
                construction_accuracy,
                "trial #",
                "construction accuracy",
                "data/figures/construction_accuracy.png"
            )
            simple_plotting(
                [r[1] for r in results],
                "trial #",
                "response correctness",
                "data/figures/response_correctness.png"
            )
            simple_plotting(
                [r[0] for r in results],
                "trial #",
                "response time",
                "data/figures/response_time.png"
            )
            simple_plotting(
                [len(t) for t in all_goal_choices],
                "trial #",
                "goal choices",
                "data/figures/goal_choices.png",
            )
            if len(participant.construction_reward_vals) >= 10:
                plot_rl_stats(
                            10,
                            participant.construction_qvals,
                            "data/figures/qvals.png"
                )
                plot_rl_stats(
                            10,
                            participant.construction_reward_vals,
                            "data/figures/rewards.png"
                )

            if session_type == "test" and len(all_goal_choices):
                goal_sequences = simple_goal_sequencessness(
                    all_goal_choices,
                    all_grids
                )
                plot_sequences(goal_sequences)

            participant.start_construct_trial(timedelta())
            done_count += 1
            pbar.update(1)

            viz.update_progress(
                done_count, datetime.now() - real_start_time)
        elif event.source == participant.replay_optimize_qnet:
            simple_plotting(
                participant.construction_net_training_results,
                "Steps",
                "Loss",
                "data/figures/construction_net_training.png",
                viz.fig.number,
            )
            simple_plotting(
                construction_correctness,
                "trial #",
                "construction correctness",
                "data/figures/construction_correctness.png"
            )
            simple_plotting(
                construction_accuracy,
                "trial #",
                "construction accuracy",
                "data/figures/construction_accuracy.png"
            )
            simple_plotting(
                [r[1] for r in results],
                "trial #",
                "response correctness",
                "data/figures/response_correctness.png"
            )
            simple_plotting(
                [r[0] for r in results],
                "trial #",
                "response time",
                "data/figures/response_time.png"
            )
            simple_plotting(
                [len(t) for t in all_goal_choices],
                "trial #",
                "goal choices",
                "data/figures/goal_choices.png",
            )
            if session_type == "test":
                n_sequences = simple_sequenceness(
                    all_rule_history, all_rule_lhs_history, all_grids
                )
                plot_sequences(n_sequences)
                goal_sequences = simple_goal_sequencessness(all_goal_choices, all_grids)
                plot_sequences(goal_sequences)
            participant.start_construct_trial(timedelta())
            done_count += 1
            pbar.update(1)
            viz.update_progress(done_count, datetime.now() - real_start_time)
        if (event.time - start_time) > timedelta(
            seconds=per_trial_time
        ) and not participant.trigger_response:  # trial expired?
            print("premature end of trial")
            start_time = event.time  # temporarily
            participant.end_construction()
    if session_type == "train":
        with open("data/processed/train_data/construction_training_results.pkl", "wb") as f:
            p.dump(participant.construction_net_training_results, f)
    return (
        results,
        construction_correctness,
        construction_accuracy,
        all_rule_history,
        all_rule_lhs_history,
        all_constructions,
        all_goal_choices,
    )


def run_experiment(
        num_train_sessions=100,
        num_test_sessions=20,
        test_model_path=None,
        layers=8):
    grid_names = os.listdir("data/processed/train_data/train_stims/")
    test_trials = pd.read_csv("data/processed/test_data/all_test_data.csv")
    participant = AbstractParticipant("p1", layers=layers)

    if num_train_sessions:
        name_dir = len(os.listdir("data/run_data/"))//2 + 1
        os.makedirs(f"data/run_data/run_{name_dir}/figures", exist_ok=True)
        train_grids = random.choices(grid_names, k=num_train_sessions * 50)
        train_grids = [grid_name.split(".")[0] for grid_name in train_grids]

        train_trials = pd.DataFrame(train_grids, columns=["Grid_Name"])
        train_results, train_construction_correctness, train_construction_accuracy, _, _, _, train_goal_choices = (
            run_participant_session(participant, train_trials))

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
    else:
        # load the model
        participant.goal_net.load_state_dict(
            torch.load(test_model_path))
        participant.training = False
    if not num_test_sessions:
        return
    name_dir = name_dir+1 if num_train_sessions else (len(os.listdir("data/run_data/"))//2 + 1)
    os.makedirs(f"data/run_data/run_{name_dir}/figures", exist_ok=True)
    test_trial_indices = random.sample(
        test_trials["PID"].unique().tolist(), num_test_sessions
    )
    test_trials = test_trials[test_trials["PID"].isin(test_trial_indices)]

    test_grid_names = test_trials["Grid_Name"].tolist()
    test_grids = [
        np.load(f"data/processed/test_data/test_stims/{grid_name}.npy")
        for grid_name in test_grid_names
    ]

    (test_results,
     test_construction_correctness,
     test_construction_accuracy,
     test_rule_choices,
     test_rule_lhs_information,
     _,
     test_goal_choices,
     ) = run_participant_session(participant,
                                 test_trials[:100],
                                 session_type="test",
                                 q_type="query",
                                 init_rules=not num_train_sessions)

    # pickle it all
    with open(f"data/run_data/run_{name_dir}/test_grids.pkl", "wb") as f:
        p.dump(test_grid_names, f)
    with open(f"data/run_data/run_{name_dir}/test_results.pkl", "wb") as f:
        p.dump(test_results, f)
    with open(f"data/run_data/run_{name_dir}/test_construction_correctness.pkl", "wb") as f:
        p.dump(test_construction_correctness, f)
    with open(f"data/run_data/run_{name_dir}/test_construction_accuracy.pkl", "wb") as f:
        p.dump(test_construction_accuracy, f)
    with open(f"data/run_data/run_{name_dir}/test_rule_choices.pkl", "wb") as f:
        p.dump(test_rule_choices, f)
    with open(f"data/run_data/run_{name_dir}/test_goal_choices.pkl", "wb") as f:
        p.dump(test_goal_choices, f)

    test_results_df = pd.DataFrame(
        test_results, columns=[
            "rt", "response_correctness"])
    test_results_df["construction_correctness"] = test_construction_correctness
    test_results_df["goal_choices"] = [len(t) for t in test_goal_choices]
    test_results_df["trial #"] = list(range(1, len(test_results_df) + 1))

    # --- Plotting ---

    simple_snsplot(
        test_results_df,
        "trial #",
        "construction_correctness",
        f"data/run_data/run_{name_dir}/figures/test_construction_correctness.png",
    )
    simple_snsplot(
        test_results_df,
        "trial #",
        "rt",
        f"data/run_data/run_{name_dir}/figures/test_rt.png",
        line=True)
    simple_snsplot(
        test_results_df,
        "trial #",
        "goal_choices",
        f"data/run_data/run_{name_dir}/figures/test_goal_choices.png")
    simple_snsplot(
        test_results_df,
        "trial #",
        "response_correctness",
        f"data/run_data/run_{name_dir}/figures/test_response_correctness.png",
    )

    goal_sequences = simple_goal_sequencessness_elaborate(test_goal_choices, test_grids)
    plot_sequences(
        goal_sequences, 
        path=f"data/run_data/run_{name_dir}/figures/test_goal_sequences.png"
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Run in debug mode")
    parser.add_argument(
        "--train_sessions",
        type=int,
        default=3,
    )
    parser.add_argument(
        "--test_sessions",
        type=int,
        default=2,
    )
    parser.add_argument(
        "--test_path",
        type=str,
        default=None,
        help="Path to nn weights for testing"
    )
    parser.add_argument(
        "--no_show_viz",
        action="store_true",
        help="do not show the visualization while running the program"
    )
    parser.add_argument(
        "--layers",
        type=int,
        required=True,
    )

    args = parser.parse_args()
    if args.debug:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s"
        )
        logger = logging.getLogger("pyClarion.system")
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(handler)
    
    os.environ["VIZ_SHOW"] = "false" if args.no_show_viz else "true"
    run_experiment(
        num_train_sessions=0 if args.test_path else args.train_sessions, num_test_sessions=args.test_sessions,
        test_model_path=args.test_path,
        layers=args.layers,
    )

"""
python scaffolded_training.py --start_from 2 --model "/Users/mishaal/personalproj/clarion_replay/data/run_data/run_6/goal_net.pt"
"""