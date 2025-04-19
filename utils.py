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
        method = Site.push if reset else Site.write_inplace
        self.system.schedule(self.send, 
                             self.main.update(data, method),
                             dt=dt, priority=priority)

def numpify_grid(grid: NumDict) -> np.ndarray:
    data = grid._d
    data_dict = {}
    array_grid = np.zeros((6, 6))

    #row specifications are of the form input_shapeA_rowB, where A is the shape number and B is the row number
    #extract shape number and row number using regex
    shape_and_rowidx_extractor = re.compile(r".*target_shape(\d+)_row(\d+)")
    shape_and_colidx_extractor = re.compile(r".*target_shape(\d+)_col(\d+)")

    row_extractor = re.compile(r".*r(\d+)")
    col_extractor = re.compile(r".*c(\d+)")

    for k in data:
        k = str(k).split(":")[-1]
        a, b = k.split(",")
        a, b = a[1:], b[:-1]
        if re.match(shape_and_rowidx_extractor, a):
            shape_num = int(shape_and_rowidx_extractor.match(a).group(1))
            row_idx = int(shape_and_rowidx_extractor.match(a).group(2))
            row_num = int(row_extractor.match(b).group(1))

            if shape_num not in data_dict:
                data_dict[shape_num] = {}
            data_dict[shape_num][f"r{row_idx}"] = row_num
        
        if re.match(shape_and_colidx_extractor, a):
            shape_num = int(shape_and_colidx_extractor.match(a).group(1))
            col_idx = int(shape_and_colidx_extractor.match(a).group(2))
            col_num = int(col_extractor.match(b).group(1))

            if shape_num not in data_dict:
                data_dict[shape_num] = {}
            data_dict[shape_num][f"c{col_idx}"] = col_num
        
        if re.match(shape_and_rowidx_extractor, b):
            shape_num = int(shape_and_rowidx_extractor.match(b).group(1))
            row_idx = int(shape_and_rowidx_extractor.match(b).group(2))
            row_num = int(row_extractor.match(a).group(1))

            if shape_num not in data_dict:
                data_dict[shape_num] = {}
            data_dict[shape_num][f"r{row_idx}"] = row_num
        
        if re.match(shape_and_colidx_extractor, b):
            shape_num = int(shape_and_colidx_extractor.match(b).group(1))
            col_idx = int(shape_and_colidx_extractor.match(b).group(2))
            col_num = int(col_extractor.match(a).group(1))

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
