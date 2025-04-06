from pyClarion import (Agent, Input, Choice, ChunkStore, FixedRules, 
    Family, Atoms, Atom, BaseLevel, Pool, NumDict, Event, Priority)

from typing import *

class Brick(Atoms):
    horizontal: Atom
    vertical: Atom
    mirror_L: Atom
    half_T: Atom

class Numbers(Atoms):
    n1: Atom
    n2: Atom
    n3: Atom
    n4: Atom
    n5: Atom
    n6: Atom

class Rel(Atoms):
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

class MLPConstructionIO(Atoms):
    # strictly speaking, only need the input shape rows and target shape rows and cols
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

