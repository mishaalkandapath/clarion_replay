from pyClarion import (Agent, Input, Choice, ChunkStore, FixedRules, 
    Family, Atoms, Atom, BaseLevel, Pool, NumDict, Event, Priority)

from typing import *

class Brick(Atoms):
    horizontal: Atom
    vertical: Atom
    mirror_L: Atom
    half_T: Atom

class NumBricksInput(Atoms):
    n1: Atom
    n2: Atom
    n3: Atom
    n4: Atom

class GridRows(Atoms):
    r1: Atom
    r2: Atom
    r3: Atom
    r4: Atom
    r5: Atom
    r6: Atom

class GridCols(Atoms):
    c1: Atom
    c2: Atom
    c3: Atom
    c4: Atom
    c5: Atom
    c6: Atom

class QueryRel(Atoms):
    left: Atom
    above: Atom
    right: Atom
    below: Atom

class SignalTokens(Atoms):
    stop_construction: Atom
    continue_construction: Atom

class ConstructionIO(Atoms):
    input_shape1: Atom
    input_shape2: Atom
    input_shape3: Atom
    input_shape4: Atom

    brick_nos: Atom

    target_shape1: Atom
    target_shape2: Atom
    target_shape3: Atom
    target_shape4: Atom

    input_shape1_row1: Atom
    input_shape1_row2: Atom
    input_shape1_row3: Atom
    input_shape1_col1: Atom
    input_shape1_col2: Atom
    input_shape1_col3: Atom
    
    input_shape2_row1: Atom
    input_shape2_row2: Atom
    input_shape2_row3: Atom
    input_shape2_col1: Atom
    input_shape2_col2: Atom
    input_shape2_col3: Atom
    
    input_shape3_row1: Atom
    input_shape3_row2: Atom
    input_shape3_row3: Atom
    input_shape3_col1: Atom
    input_shape3_col2: Atom
    input_shape3_col3: Atom
    
    input_shape4_row1: Atom
    input_shape4_row2: Atom
    input_shape4_row3: Atom
    input_shape4_col1: Atom
    input_shape4_col2: Atom
    input_shape4_col3: Atom
    
    target_shape1_row1: Atom
    target_shape1_row2: Atom
    target_shape1_row3: Atom
    target_shape1_col1: Atom
    target_shape1_col2: Atom
    target_shape1_col3: Atom

    target_shape2_row1: Atom
    target_shape2_row2: Atom
    target_shape2_row3: Atom
    target_shape2_col1: Atom
    target_shape2_col2: Atom
    target_shape2_col3: Atom

    target_shape3_row1: Atom
    target_shape3_row2: Atom
    target_shape3_row3: Atom
    target_shape3_col1: Atom
    target_shape3_col2: Atom
    target_shape3_col3: Atom
    
    target_shape4_row1: Atom
    target_shape4_row2: Atom
    target_shape4_row3: Atom
    target_shape4_col1: Atom
    target_shape4_col2: Atom
    target_shape4_col3: Atom

    construction_signal: Atom

class ResponseIO(Atoms):
    target_shape1: Atom
    target_shape2: Atom
    target_shape3: Atom
    target_shape4: Atom
    
    target_shape1_row1: Atom
    target_shape1_row2: Atom
    target_shape1_row3: Atom
    target_shape1_col1: Atom
    target_shape1_col2: Atom
    target_shape1_col3: Atom
    
    target_shape2_row1: Atom
    target_shape2_row2: Atom
    target_shape2_row3: Atom
    target_shape2_col1: Atom
    target_shape2_col2: Atom
    target_shape2_col3: Atom
    
    target_shape3_row1: Atom
    target_shape3_row2: Atom
    target_shape3_row3: Atom
    target_shape3_col1: Atom
    target_shape3_col2: Atom
    target_shape3_col3: Atom
    
    target_shape4_row1: Atom
    target_shape4_row2: Atom
    target_shape4_row3: Atom
    target_shape4_col1: Atom
    target_shape4_col2: Atom
    target_shape4_col3: Atom
    
    query_block: Atom
    query_block_reference: Atom
    query_relation: Atom
    output: Atom

class Response(Atoms):
    yes: Atom
    no: Atom