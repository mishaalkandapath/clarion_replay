from pyClarion import FixedRules, Choice, NumDict, numdict, Index, Chunk, Priority
from pyClarion import Site, RuleStore, Choice, KeyForm, Family, Sort, Atom, Input, Key

from typing import *
from datetime import timedelta

import numpy as np
import re

class RuleWBLA(FixedRules):
    main: Site
    rules: RuleStore
    choice: Choice
    by: KeyForm
    updated_main: Site

    def __init__(self, 
        name: str, 
        p: Family,
        r: Family,
        c: Family, 
        d: Family | Sort | Atom, 
        v: Family | Sort,
        *,
        sd: float = 1.0
    ) -> None:
        
        super().__init__(name, p=p, r=r, c=c, d=d, v=v, sd=sd)
        self.bla_main = Site(self.rules.main.index, {}, 0.0)
        self.choice.input = self.bla_main

class FlippableInput(Input):

    @override
    def send(self,
            d: dict | Chunk,
            dt: timedelta = timedelta(),
            priority: int = Priority.PROPAGATION,
            flip: bool = False):
        reset = self.reset if not flip else not self.reset
        data = self._parse_input(d)
        method = Site.push if reset else FlippableInput.write_inplace_consistent
        self.system.schedule(self.send, 
                             self.main.update(data, method),
                             dt=dt, priority=priority)
    
    def write_inplace_consistent(site: Site,
                                data:NumDict,
                                index: int = 0,
                                grad: bool = False) -> None:
        d = site.grad if grad else site.data
        with d[index].mutable():
            new_keys = data.d.keys()
            to_del = []
            #consistency checking
            for k in d[index].d:
                if any(conflicting_keys(str(k)).match(str(k_)) for k_ in new_keys) and k not in new_keys:
                    to_del.append(k)
            with data.mutable():
                for k in to_del:
                    data.update({k: 0.0})      
            #update
            d[index].update(data.d)


def numpify_grid(grid: NumDict) -> np.ndarray:
    data = grid._d
    data_dict = {}
    array_grid = np.zeros((6, 6))

    shape_map = {"mirror_L": 2, "half_T": 1, "vertical": 3, "horizontal": 4}

    #row specifications are of the form input_shapeA_rowB, where A is the shape number and B is the row number
    #extract shape number and row number using regex
    shape_and_rowidx_extractor = re.compile(r".*target_(mirror_L|half_T|horizontal|vertical)_row(\d+)")
    shape_and_colidx_extractor = re.compile(r".*target_(mirror_L|half_T|horizontal|vertical)_col(\d+)")

    row_col_extractor = re.compile(r".*n(\d+)")

    for k in data:
        k = str(k).split(":")[-1]
        a, b = k.split(",")
        a, b = a[1:], b[:-1]
        if re.match(shape_and_rowidx_extractor, a):
            shape_num = shape_map[(shape_and_rowidx_extractor.match(a).group(1))]
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
            array_grid[data_dict[shape][f"r{i}"]-1, data_dict[shape][f"c{i}"]-1] = shape

    return array_grid
        

def mlpify(cur_working_space: NumDict, index: Index) -> NumDict:
    """
    Convert keys of the form (construction_space,construction_space):(io,bricks):(input_shape2_row_2, n2)
    to the form (mlp_space_1, mlp_space_2): (input_shape2_row_2, n2)

    ignore other keys
    """

    data = cur_working_space._d
    data_dict = {}
    for k_ in data:
        k = str(k_).split(":")[-1]
        a, b = k.split(",")
        a, b = a[1:], b[:-1]
        if re.match(r".*input_shape\d+_row\d+", a):
            shape_num = int(re.match(r".*input_shape(\d+)_row\d+", a).group(1))
            row_num = int(re.match(r".*row(\d+)", a).group(1))
            data_dict[f"(mlp_space_1, mlp_space_2):(input_shape{shape_num}_row{row_num})"] = data[k_]
        elif re.match(r".*input_shape\d+_col\d+", a):
            shape_num = int(re.match(r".*input_shape(\d+)_col\d+", a).group(1))
            col_num = int(re.match(r".*col(\d+)", a).group(1))
            data_dict[f"(mlp_space_1, mlp_space_2):(input_shape{shape_num}_col{col_num})"] = data[k_]
    

    return numdict(index ,data_dict, c=0.0)

def filter_keys_by_rule_chunk(rule_rhs_chunk: Chunk, choice_main: dict) -> dict:
    key_filter = []
    for (d, v), _ in rule_rhs_chunk._dyads_.items():
        k1, k2 = ~d, ~v
        p1, p2 = [label for label, _ in k1[-2:]], [label for label, _ in k2[-2:]]
        key_filter.append(Key(f"(construction_space,construction_space):({p1[0]+","+p2[0]}):({p1[1]+","+p2[1]})"))
    new_choice_main = {}
    for k in choice_main:
        if k in key_filter:
            new_choice_main[k] = choice_main[k]
    return new_choice_main

def conflicting_keys(ref: str) -> re.Pattern:
    ref_pairs = re.findall(r'\(([^,]+),([^)]+)\)', ref)
    pattern = ""

    for first, second in ref_pairs[:-1]:
        pattern += r'\(' + re.escape(first) + r',' + re.escape(second) + r'\):'
    
    last_first = ref_pairs[-1][0]
    pattern += r'\(' + re.escape(last_first) + r',[^)]+\)'

    matcher = re.compile('^' + pattern + '$')

    return matcher

def make_response_input(cur_working_space: NumDict, response_index: Index) -> NumDict:
    response_data = {}

    for k_ in cur_working_space.d:
        k = str(k_)
        k = k.replace("construction_space", "response_space")
        if "input" in k or "construction_signal" in k:
            # this has something to do with an input, not a consideration for repsonses:
            continue
        response_data[Key(k)] = cur_working_space[k_]
    return numdict(response_index, response_data, c=0.0)