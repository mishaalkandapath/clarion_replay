from pyClarion import FixedRules, Choice
from pyClarion import Site, RuleStore, Choice, KeyForm, Family, Sort, Atom, Chunk, Key, Var, Term, System

from typing import *

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

def numpify_grid(grid: Chunk):
    data = grid.__dyads__
    data_dict = {}
    array_grid = np.zeros((9, 9))

    #row specifications are of the form input_shapeA_rowB, where A is the shape number and B is the row number
    #extract shape number and row number using regex
    shape_and_rowidx_extractor = re.compile(r".*input_shape(\d+)_row(\d+)")
    shape_and_colidx_extractor = re.compile(r".*input_shape(\d+)_col(\d+)")

    row_extractor = re.compile(r".*r(\d+)")
    col_extractor = re.compile(r".*c(\d+)")

    for a, b in data:
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
        

        
