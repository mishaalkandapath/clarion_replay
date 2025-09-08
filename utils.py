import re
import random

import numpy as np
from pyClarion import NumDict, numdict, Index, Chunk, Site, Key

SHAPES = ["half_T", "mirror_L", "vertical", "horizontal"]
RELS = ["start", "left", "right", "above", "below"]

def write_inplace_consistent(
    site: Site, data: NumDict, index: int = 0, grad: bool = False
) -> None:
    """
    Make sure that when writing in place,
    any inccompatible keys are removed
    """

    d = site.grad if grad else site.data
    with d[index].mutable():
        new_keys = data.d.keys()
        to_del = []
        # consistency checking
        for k in d[index].d:
            if (
                any(conflicting_keys(str(k)).match(str(k_)) for k_ in new_keys)
                and k not in new_keys
            ):
                to_del.append(k)
        with data.mutable():
            for k in to_del:
                data.update({k: 0.0})
        # update
        d[index].update(data.d)


def numpify_grid(grid: NumDict) -> np.ndarray:
    data = grid._d
    data_dict = {}
    array_grid = np.zeros((6, 6))

    shape_map = {"mirror_L": 2, "half_T": 1, "vertical": 3, "horizontal": 4}

    # row specifications are of the form input_shapeA_rowB, where A is the shape number and B is the row number
    # extract shape number and row number using regex
    shape_and_rowidx_extractor = re.compile(
        r".*target_(mirror_L|half_T|horizontal|vertical)_row(\d+)"
    )
    shape_and_colidx_extractor = re.compile(
        r".*target_(mirror_L|half_T|horizontal|vertical)_col(\d+)"
    )

    row_col_extractor = re.compile(r".*n(\d+)")

    for k in data:
        k = str(k).split(":")[-1]
        a, b = k.split(",")
        a, b = a[1:], b[:-1]
        if re.match(shape_and_rowidx_extractor, a):
            shape_num = shape_map[(
                shape_and_rowidx_extractor.match(a).group(1))]
            row_idx = int(shape_and_rowidx_extractor.match(a).group(2))
            row_num = int(row_col_extractor.match(b).group(1))

            if shape_num not in data_dict:
                data_dict[shape_num] = {}
            data_dict[shape_num][f"r{row_idx}"] = row_num

        if re.match(shape_and_colidx_extractor, a):
            shape_num = shape_map[shape_and_colidx_extractor.match(a).group(1)]
            col_idx = int(shape_and_colidx_extractor.match(a).group(2))
            col_num = int(row_col_extractor.match(b).group(1))

            if shape_num not in data_dict:
                data_dict[shape_num] = {}
            data_dict[shape_num][f"c{col_idx}"] = col_num

        if re.match(shape_and_rowidx_extractor, b):
            shape_num = shape_map[shape_and_rowidx_extractor.match(b).group(1)]
            row_idx = int(shape_and_rowidx_extractor.match(b).group(2))
            row_num = int(row_col_extractor.match(a).group(1))

            if shape_num not in data_dict:
                data_dict[shape_num] = {}
            data_dict[shape_num][f"r{row_idx}"] = row_num

        if re.match(shape_and_colidx_extractor, b):
            shape_num = shape_map[shape_and_colidx_extractor.match(b).group(1)]
            col_idx = int(shape_and_colidx_extractor.match(b).group(2))
            col_num = int(row_col_extractor.match(a).group(1))

            if shape_num not in data_dict:
                data_dict[shape_num] = {}
            data_dict[shape_num][f"c{col_idx}"] = col_num

    for shape in data_dict:
        for i in range(1, 4):
            array_grid[data_dict[shape][f"r{i}"] - 1,
                       data_dict[shape][f"c{i}"] - 1] = shape

    return array_grid


def mlpify(cur_working_space: NumDict) -> NumDict:
    """
    Convert keys of the form (construction_space,construction_space):(io,bricks):(input_shape2_row_2, n2)
    to the form (mlp_space_1, mlp_space_2): (input_shape2_row_2, n2)

    ignore other keys
    """

    data = (cur_working_space.d if isinstance(cur_working_space, NumDict)
            else cur_working_space)
    data_dict = {}
    for k_ in data:
        k = str(k_).split(":")[-1]
        a, b = k.split(",")
        a, b = a[1:], b[:-1]
        if re.match(
            r".*input_(mirror_L|half_T|horizontal|vertical)_(row|col)(\d+)",
                a):
            keyname = re.match(
                r".*input_(mirror_L|half_T|horizontal|vertical)_(row|col)(\d+)",
                a).group(0)
            data_dict[f"(mlp_space_1,mlp_space_2):({keyname},{b})"] = data[k_]
        if re.match(
            r".*target_(mirror_L|half_T|horizontal|vertical)_(row|col)(\d+)", a
        ):
            keyname = re.match(
                r".*target_(mirror_L|half_T|horizontal|vertical)_(row|col)(\d+)",
                a).group(0)
            data_dict[f"(mlp_space_1,mlp_space_2):({keyname},{b})"] = data[k_]

    return data_dict


def filter_keys_by_rule_chunk(
    rule_rhs_chunk: Chunk, choice_main: dict, space_descr="construction_space"
) -> dict:
    """
    Extract additions from thre rule_rhs_chunk
    and filter the keys in choice_main to only include these
    """
    key_filter = []
    for (d, v), _ in rule_rhs_chunk._dyads_.items():
        k1, k2 = ~d, ~v
        p1, p2 = [label for label, _ in k1[-2:]
                  ], [label for label, _ in k2[-2:]]
        key_filter.append(Key(
            f"({space_descr},{space_descr}):({p1[0] + ',' + p2[0]}):({p1[1] + ',' + p2[1]})"))
    new_choice_main = {}
    for k in choice_main:
        if k in key_filter:
            new_choice_main[k] = choice_main[k]
    return new_choice_main


def conflicting_keys(ref: str) -> re.Pattern:
    ref_pairs = re.findall(r"\(([^,]+),([^)]+)\)", ref)
    pattern = ""

    for first, second in ref_pairs[:-1]:
        pattern += r"\(" + re.escape(first) + r"," + re.escape(second) + r"\):"

    last_first = ref_pairs[-1][0]
    pattern += r"\(" + re.escape(last_first) + r",[^)]+\)"

    matcher = re.compile("^" + pattern + "$")

    return matcher


def make_response_input(
        cur_working_space: NumDict,
        response_index: Index) -> NumDict:
    """
    make current working space data compatible with response space index
    """

    response_data = {}

    for k_ in cur_working_space.d:
        k = str(k_)
        k = k.replace("construction_space", "response_space")
        if (
            re.match(
                r".*(input|construction_signal|latest|reference|left|right|below|above|stop|start).*",
                k,
            )
            and cur_working_space[k_]
        ):
            # this has something to do with an input, not a consideration for
            # repsonses:
            continue
        response_data[Key(k)] = cur_working_space[k_]
    return numdict(response_index, response_data, c=0.0)


def make_goal_outputs_construction_input(
    cur_working_space: NumDict, goal_outputs: NumDict
):
    """
    send goals to construction space
    """

    key_template = (
        lambda shape,
        response: f"(construction_space,construction_space):(io,response):(target_{shape},{response})"
    )
    rel_key_template = (
        lambda rel,
        response: f"(construction_space,construction_space):(io,response):({rel},{response})"
    )

    new_working_space = cur_working_space.d.copy()
    for shape in SHAPES:
        reference_key = Key(key_template(shape, "reference"))
        latest_key = Key(key_template(shape, "latest"))
        if reference_key in new_working_space:
            del new_working_space[reference_key]
        if latest_key in new_working_space:
            del new_working_space[latest_key]

    for rel in RELS:
        yes_key = Key(rel_key_template(rel, "yes"))
        no_key = Key(rel_key_template(rel, "no"))
        if yes_key in new_working_space:
            del new_working_space[yes_key]
        if no_key in new_working_space:
            del new_working_space[no_key]

    cur_state = str(list(goal_outputs.values())[0][-1][0])
    if "start" not in cur_state:
        cur_state = cur_state.split("_")
        if len(cur_state) > 3:
            t = [i for i in range(len(cur_state)) if len(cur_state[i]) == 1]
            for i in t:
                cur_state[i - 1] = cur_state[i - 1] + "_" + cur_state[i]
            cur_state = (
                cur_state[: min(t)]
                + cur_state[min(t) + 1: max(t)]
                + cur_state[max(t) + 1:]
            )

        cur_reference, cur_latest, cur_relation = cur_state

        if Key(key_template(cur_reference, "yes")) in new_working_space:
            del new_working_space[Key(key_template(cur_reference, "yes"))]
        if Key(key_template(cur_latest, "no")) in new_working_space:
            del new_working_space[Key(key_template(cur_latest, "no"))]

        new_working_space.update(
            {Key(key_template(cur_reference, "reference")): 1.0})
        new_working_space.update(
            {Key(key_template(cur_latest, "latest")): 1.0})
    else:
        cur_state = cur_state.split("_")
        if len(cur_state) > 2:
            t = [i for i in range(len(cur_state)) if len(cur_state[i]) == 1][0]
            cur_state[t - 1] = cur_state[t - 1] + "_" + cur_state[t]
            cur_state = cur_state[:t] + cur_state[t + 1:]

        cur_latest, cur_relation = cur_state
        if Key(key_template(cur_latest, "no")) in new_working_space:
            del new_working_space[Key(key_template(cur_latest, "no"))]

        new_working_space.update(
            {Key(key_template(cur_latest, "latest")): 1.0})

    new_working_space.update({Key(rel_key_template(cur_relation, "yes")): 1.0})
    for rel in RELS:
        if rel != cur_relation:
            new_working_space.update({Key(rel_key_template(rel, "no")): 1.0})

    return new_working_space


def clean_construction_input(data_dict, leave_only_inputs=False):
    """
    Clean any goal data from the construction input
    """
    yes_key_lambda = lambda shape: Key(
        f"(construction_space,construction_space):(io,response):({shape},yes)"
    )
    no_key_lambda = lambda shape: Key(
        f"(construction_space,construction_space):(io,response):({shape},no)"
    )

    if leave_only_inputs:
        # leave only keys with "input" in them
        data_dict = {k: v for k, v in data_dict.items() if "input" in str(k)}
        # add target_block, no keys

        for shape in [
            "target_half_T",
            "target_mirror_L",
            "target_vertical",
            "target_horizontal",
        ]:
            data_dict[Key(f"{no_key_lambda(shape)}")] = 1.0
    else:
        new_data_dict = {
            k: v for k,
            v in data_dict.items() if "input" in str(k)}

        # add target_block, yes if there is target_block_row etc keys:

        key_matcher = r".*target_(mirror_L|half_T|horizontal|vertical)_(row|col)(\d+)"

        reserve_set = set()
        for k in data_dict:
            if re.match(key_matcher, str(k)):
                new_data_dict[k] = data_dict[k]
                shape = re.match(key_matcher, str(k)).group(1)
                if shape not in reserve_set:
                    new_data_dict[Key(
                        f"{yes_key_lambda('target_' + shape)}")] = 1.0
                    reserve_set.add("target_" + shape)

        for shape in [
            "target_half_T",
            "target_mirror_L",
            "target_vertical",
            "target_horizontal",
        ]:
            if shape not in reserve_set:
                new_data_dict[Key(f"{no_key_lambda(shape)}")] = 1.0
                reserve_set.add(shape)

        data_dict = new_data_dict

    return data_dict

def goal_shape_extractor(goal):
    if "start" in goal:
        pattern = r"(mirror_L|half_T|horizontal|vertical)_start"
        return [re.match(pattern, goal).group(1)]
    pattern = r"(mirror_L|half_T|horizontal|vertical)_(mirror_L|half_T|horizontal|vertical)_(left|right|above|below)"
    match = re.match(pattern, goal)
    return [match.group(1), match.group(2)]


def acc(pred_grid, true_grid):
    return (pred_grid == true_grid).sum() / \
        (pred_grid.shape[0] * pred_grid.shape[1])


def check_construction_input_match(mlp_input):
    for shape in mlp_input:
        if "input" in str(shape):
            shape = str(shape)
            if Key(shape.replace("input", "target")) not in mlp_input:
                return False
            if (mlp_input[Key(shape.replace("input", "target"))] 
                != 
                mlp_input[Key(shape)]):
                return False
    return True

def weighted_sample_without_replacement(population, weights=None, k=1, rng=random):
    if not weights:
        weights = [1/len(population)]*len(population)
    v = [rng.random() ** (1 / w) for w in weights]
    order = sorted(range(len(population)), key=lambda i: v[i])
    return [population[i] for i in order[-k:]]

            

# useful patterns and dicts
SHAPE_SHAPE_REL = r"(half_T|mirror_L|vertical|horizontal)_(half_T|mirror_L|vertical|horizontal)_(left|right|above|below)"
SHAPE_START = r"(half_T|mirror_L|vertical|horizontal)_start"
QUERY_REL_PATTERN = r".*query_rel\.(left|right|below|above).*bricks\.(mirror_L|half_T|vertical|horizontal).*bricks\.(mirror_L|half_T|vertical|horizontal).*"
SHAPE_DICT = {"half_T": 1, "mirror_L": 2, "vertical": 3, "horizontal": 4}
