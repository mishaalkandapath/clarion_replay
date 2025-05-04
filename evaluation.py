import re

import numpy as np
import statsmodels.api as sm

SHAPE_MAP = {"half_T": 1, "mirror_L": 2, "vertical": 3, "horizontal": 4}
REVERSE_SHAPE_MAP = {v: k for k, v in SHAPE_MAP.items()}

# code adapated from https://github.com/schwartenbeckph/Generative-Replay/


def mk_ontopness(required_form):
    """
    Check if there is ontopness in pattern.
    """
    ontopness = False
    count_ontop = 0
    ontop = 0
    below = 0

    if required_form.size > 0:  # Check if not empty
        for i in range(1, required_form.shape[0]):
            row_current = required_form.shape[0] - i
            row_above = required_form.shape[0] - (i + 1)

            if np.any(required_form[row_current, :] -
                      required_form[row_above, :] != 0):
                index = np.where(
                    (required_form[row_current, :] - required_form[row_above, :]) != 0
                )[0]

                if np.any(
                    (
                        required_form[row_current, index]
                        * required_form[row_above, index]
                    )
                    != 0
                ):
                    ontopness = True
                    count_ontop = count_ontop + 1

                    elements_form = np.unique(required_form)
                    elements_form = elements_form[elements_form != 0]

                    row1 = np.where(required_form == elements_form[0])[0]
                    row2 = np.where(required_form == elements_form[1])[0]

                    if np.min(row1) < np.min(row2):
                        ontop = elements_form[0]
                        below = elements_form[1]
                    elif np.min(row1) > np.min(row2):
                        ontop = elements_form[1]
                        below = elements_form[0]

    return ontopness, count_ontop, ontop, below


def mk_besideness(required_form):
    """
    Check if there is besideness in pattern.
    """
    besideness = False
    count_beside = 0
    left = 0
    right = 0

    if required_form.size > 0:  # Check if not empty
        required_form = required_form.T

        for i in range(1, required_form.shape[0]):
            row_current = required_form.shape[0] - i
            row_above = required_form.shape[0] - (i + 1)

            if np.any(required_form[row_current, :] -
                      required_form[row_above, :] != 0):
                index = np.where(
                    (required_form[row_current, :] - required_form[row_above, :]) != 0
                )[0]

                if np.any(
                    (
                        required_form[row_current, index]
                        * required_form[row_above, index]
                    )
                    != 0
                ):
                    besideness = True
                    count_beside = count_beside + 1

                    elements_form = np.unique(required_form)
                    elements_form = elements_form[elements_form != 0]

                    row1 = np.where(required_form == elements_form[0])[0]
                    row2 = np.where(required_form == elements_form[1])[0]

                    if np.min(row1) < np.min(row2):
                        left = elements_form[0]
                        right = elements_form[1]
                    elif np.min(row1) > np.min(row2):
                        left = elements_form[1]
                        right = elements_form[0]

    return besideness, count_beside, left, right


def brick_connectedness(stim_grid):
    # Element connected to middle via besideness | middle Element | Element
    # connected to middle via ontopness
    bricks_conn_trial = [0, 0, 0]
    # left element | ontop element | right element | below element
    bricks_rel_trial = [0, 0, 0, 0]

    bricks = np.unique(stim_grid)[1:]  # dont need 0

    if len(bricks) == 2:
        bricks = np.array([bricks[0], bricks[1], 5])

    part1 = np.copy(stim_grid)
    part1[part1 == bricks[0]] = 0
    part2 = np.copy(stim_grid)
    part2[part1 == bricks[1]] = 0
    part3 = np.copy(stim_grid)
    part3[part1 == bricks[2]] = 0

    bricks_order = np.array(
        [
            [
                mk_ontopness(part3)[0] + mk_ontopness(part2)[0],
                mk_ontopness(part1)[0] + mk_ontopness(part3)[0],
                mk_ontopness(part1)[0] + mk_ontopness(part2)[0],
            ],
            [
                mk_besideness(part3)[0] + mk_besideness(part2)[0],
                mk_besideness(part1)[0] + mk_besideness(part3)[0],
                mk_besideness(part1)[0] + mk_besideness(part2)[0],
            ],
        ]
    )
    bricks_order = [
        np.where(~bricks_order[0, :] & bricks_order[1, :])[0],
        np.where(bricks_order[0, :] & bricks_order[1, :])[0],
        np.where(bricks_order[0, :] & ~bricks_order[1, :])[0],
    ]
    try:
        bricks_conn_trial = bricks[bricks_order].T
    except Exception as e:
        print(f"{e} \n Because of incorrectly configured grid")

    if mk_ontopness(part1)[0]:
        _, _, bricks_rel_trial[1], bricks_rel_trial[3] = mk_ontopness(part1)
    elif mk_ontopness(part2)[0]:
        _, _, bricks_rel_trial[1], bricks_rel_trial[3] = mk_ontopness(part2)
    elif mk_ontopness(part3)[0]:
        _, _, bricks_rel_trial[1], bricks_rel_trial[3] = mk_ontopness(part3)

    if mk_besideness(part1)[0]:
        _, _, bricks_rel_trial[0], bricks_rel_trial[2] = mk_besideness(part1)
    elif mk_besideness(part2)[0]:
        _, _, bricks_rel_trial[0], bricks_rel_trial[2] = mk_besideness(part2)
    elif mk_besideness(part3)[0]:
        _, _, bricks_rel_trial[0], bricks_rel_trial[2] = mk_besideness(part3)

    return (
        bricks_conn_trial.flatten() if 5 not in bricks else bricks_conn_trial,
        bricks_rel_trial,
    )


def calculate_delayed_effects(normal_search_stats, mlp_search_stats):
    """
    bascially one - zero vectors of categorie of rules, plot em to get a plot like the one in the paper.
    normal search stats is treated as the theoretical transitions matrix
    """
    (
        n_stable_to_present,
        n_present_to_stable,
        n_distant_to_stable,
        n_stable_to_distant,
        n_present_to_present,
    ) = normal_search_stats
    (
        m_stable_to_present,
        m_present_to_stable,
        m_distant_to_stable,
        m_stable_to_distant,
        m_present_to_present,
    ) = mlp_search_stats

    # -----------------------------------------------------------------------------
    # Step 1: Stack your theoretical (n_*) and empirical (m_*) arrays
    # -----------------------------------------------------------------------------
    # Build (5 x n_lags) arrays
    theory = np.vstack(
        [
            n_stable_to_present,
            n_present_to_stable,
            n_distant_to_stable,
            n_stable_to_distant,
            n_present_to_present,
        ]
    )  # shape = (5, n_lags)

    data = np.vstack(
        [
            m_stable_to_present,
            m_present_to_stable,
            m_distant_to_stable,
            m_stable_to_distant,
            m_present_to_present,
        ]
    )  # shape = (5, n_lags)

    # -----------------------------------------------------------------------------
    # Step 2: For each lag, run a simple regression: m[:, t] ~ 1 + n[:, t]
    # -----------------------------------------------------------------------------
    n_lags = theory.shape[1]
    betas = np.zeros(n_lags)
    pvals = np.zeros(n_lags)

    for t in range(n_lags):
        y = data[:, t]  # empirical sequenceness at lag t
        x = sm.add_constant(theory[:, t])  # design: [intercept, theoretical]
        res = sm.OLS(y, x).fit()
        betas[t] = res.params[1]  # coefficient for the theoretical regressor
        pvals[t] = res.pvalues[1]  # p-value for that coefficient

    return n_lags, betas, pvals


def simple_sequenceness(rule_choices, rule_lhs_information, grids):
    # filter ruke choices and rule_lhs_information
    good_indices = [i for i in range(len(rule_choices)) if rule_choices[i]]
    rule_choices = [rule_choices[i] for i in good_indices]
    rule_lhs_information = [
        rule_lhs_information[i] for i in good_indices
    ]
    grids = [grids[i] for i in good_indices]

    max_len = max([len(g) for g in rule_choices]) - 1
    stable_to_present = np.zeros((len(rule_choices), max_len))
    present_to_stable = np.zeros((len(rule_choices), max_len))  # backtracking
    distant_to_stable = np.zeros((len(rule_choices), max_len))
    stable_to_distant = np.zeros((len(rule_choices), max_len))
    present_to_present = np.zeros((len(rule_choices), max_len))

    sequences = {
        "Stable to present": stable_to_present,
        "Present to stable": present_to_stable,
        "Distant to stable": distant_to_stable,
        "Stable to distant": stable_to_distant,
        "Present to present": present_to_present,
    }

    for i, choices_in_trial in enumerate(rule_choices):
        stable_block = [
            str(k).split(":")[-1]
            for k in choices_in_trial[0]
            if re.fullmatch(
                r"target_(mirror_L|half_T|horizontal|vertical)",
                str(k).split(":")[-1].split(",")[0][1:],
            )
        ][0].split(",")[0][1:]
        stable_block = str(stable_block)[len("target_"):]

        # now is it a present, present typa situation or a present, distant
        # present typa situation.
        _, brick_rel = brick_connectedness(grids[i])
        only_presents = brick_rel.count(SHAPE_MAP[stable_block]) == 2
        t = brick_rel.index(SHAPE_MAP[stable_block])
        present = brick_rel[t - 2 if t >= 2 else t + 2]
        present2 = np.unique(grids[i])[
            (np.unique(grids[i]) != present)
            & (np.unique(grids[i]) != SHAPE_MAP[stable_block])
            & (np.unique(grids[i]) != 0)
        ].item()
        present_block = REVERSE_SHAPE_MAP[present]
        present2_block = REVERSE_SHAPE_MAP[present2]

        for j, _ in enumerate(choices_in_trial[1:]):
            other_blocks = [
                (str((~(k[0]))).split(":")[-1], str((~(k[1]))).split(":")[-1])
                for k in rule_lhs_information[i][j + 1]._dyads_
                if re.fullmatch(
                    r"(target_(mirror_L|half_T|horizontal|vertical))",
                    str((~(k[0]))).split(":")[-1],
                )
            ]

            if only_presents:
                if stable_block in [
                    k[0][len("target_"):] for k in other_blocks
                ] and "yes" in [k[1] for k in other_blocks if k[0][len("target_"):]]:
                    stable_to_present[i, j] = 1
                elif stable_block in [k[0][len("target_"):] for k in other_blocks]:
                    present_to_stable[i, j] = (
                        1  # this prolly will never happen -- but curious to see
                    )
                else:
                    present_to_present[i, j] = 1
            else:
                if (
                    stable_block in [k[0][len("target_"):] for k in other_blocks]
                    and "yes" in [k[1] for k in other_blocks if k[0][len("target_"):]]
                    and present_block in [k[0][len("target_"):] for k in other_blocks]
                ):
                    stable_to_present[i, j] = 1
                elif (
                    stable_block in [k[0][len("target_"):] for k in other_blocks]
                    and "yes" in [k[1] for k in other_blocks if k[0][len("target_"):]]
                    and present2_block in [k[0][len("target_"):] for k in other_blocks]
                ):
                    stable_to_distant[i, j] = 1
                elif stable_block in [
                    k[0][len("target_"):] for k in other_blocks
                ] and present_block in [k[0][len("target_"):] for k in other_blocks]:
                    present_to_stable[i, j] = 1
                elif stable_block in [
                    k[0][len("target_"):] for k in other_blocks
                ] and present2_block in [k[0][len("target_"):] for k in other_blocks]:
                    distant_to_stable[i, j] = 1
                else:
                    present_to_present[i, j] = 1

    return sequences


def simple_goal_sequencessness(goals, grids):
    # filter goals
    good_indices = [i for i in range(len(goals)) if goals[i]]
    goals = [goals[i] for i in good_indices]
    grids = [grids[i] for i in good_indices]

    max_len = max([len(g) for g in goals]) - 1
    stable_to_present = np.zeros((len(goals), max_len))
    present_to_stable = np.zeros((len(goals), max_len))  # backtracking
    present_to_present = np.zeros((len(goals), max_len))
    stable_to_absent = np.zeros((len(goals), max_len))
    present_to_absent = np.zeros((len(goals), max_len))
    absent_to_present = np.zeros((len(goals), max_len))
    absent_to_stable = np.zeros((len(goals), max_len))

    sequences = {
        "Stable to present": stable_to_present,
        "Present to stable": present_to_stable,
        "Present to present": present_to_present,
        "Stable to absent": stable_to_absent,
        "Present to absent": present_to_absent,
        "Absent to present": absent_to_present,
        "Absent to stable": absent_to_stable,
    }

    for i, choices_in_trial in enumerate(goals):
        stable_block = choices_in_trial[0][0]

        # now is it a present, present typa situation or a present, distant
        # present typa situation.
        _, brick_rel = brick_connectedness(grids[i])
        t = brick_rel.index(SHAPE_MAP[stable_block])
        present = brick_rel[t - 2 if t >= 2 else t + 2]
        present2 = np.unique(grids[i])[
            (np.unique(grids[i]) != present)
            & (np.unique(grids[i]) != SHAPE_MAP[stable_block])
            & (np.unique(grids[i]) != 0)
        ].item()
        present_block = REVERSE_SHAPE_MAP[present]
        present2_block = REVERSE_SHAPE_MAP[present2]

        for j, other_blocks in enumerate(choices_in_trial[1:]):
            if len(other_blocks) == 2:
                block1, block2 = other_blocks
            else:
                continue
            if block1 == stable_block and block2 == present_block:
                stable_to_present[i, j] = 1
            elif block1 == stable_block and block2 == present2_block:
                stable_to_present[i, j] = 1
            elif block1 == present_block and block2 == stable_block:
                present_to_stable[i, j] = 1
            elif block1 == present2_block and block2 == stable_block:
                present_to_stable[i, j] = 1
            elif block1 == present_block and block2 == present2_block:
                present_to_present[i, j] = 1
            elif block1 == present2_block and block2 == present_block:
                present_to_present[i, j] = 1
            elif block1 == stable_block:  # and block2 is anything else
                stable_to_absent[i, j] = 1
            elif block2 == stable_block:  # and block1 is anything else
                absent_to_stable[i, j] = 1
            elif block1 == present_block:  # and block2 is anything else
                present_to_absent[i, j] = 1
            elif block2 == present_block:  # and block1 is anything else
                absent_to_present[i, j] = 1
            elif block1 == present2_block:  # and block2 is anything else
                present_to_absent[i, j] = 1
            elif block2 == present2_block:  # and block1 is anything else
                absent_to_present[i, j] = 1

    return sequences


if __name__ == "__main__":
    sample_array = [
        [0, 0, 0, 0, 0, 0],
        [0, 1, 1, 4, 4, 4],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
    ]
    sample_array = np.array(sample_array)

    # sample_deviant_array = [[0, 0, 0, 0, 0, 0],
    #                         [0, 0, 0, 0, 0, 0],
    #                         [0, 0, 0, 0, 0, 0],
    #                         [0, 0, 0, 0, 0, 0],
    #                     [0, 1, 1, 0, 0, 0],
    #                     [0, 1, 4, 4, 4, 0]]
    # sample_deviant_array = np.array(sample_deviant_array)
    # # is this present in train trials?
    import os

    for file in os.listdir("processed/train_data/train_stims/"):
        if file.endswith("_d.npy"):
            stim = np.load(
                os.path.join(
                    "processed/train_data/train_stims/",
                    file))
            if len(np.unique(stim)) == 5:
                os.rename(
                    os.path.join("processed/train_data/train_stims/", file),
                    os.path.join(
                        "processed/train_data/train_stims/", file[:-5] + ".npy"
                    ),
                )
