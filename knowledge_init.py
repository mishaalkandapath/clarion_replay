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
    input_half_T: Atom
    input_mirror_L: Atom
    input_vertical: Atom
    input_horizontal: Atom

    brick_nos: Atom

    target_half_T: Atom
    target_mirror_L: Atom
    target_vertical: Atom
    target_horizontal: Atom

    input_half_T_row1: Atom
    input_half_T_row2: Atom
    input_half_T_row3: Atom
    input_half_T_col1: Atom
    input_half_T_col2: Atom
    input_half_T_col3: Atom
    
    input_mirror_L_row1: Atom
    input_mirror_L_row2: Atom
    input_mirror_L_row3: Atom
    input_mirror_L_col1: Atom
    input_mirror_L_col2: Atom
    input_mirror_L_col3: Atom
    
    input_vertical_row1: Atom
    input_vertical_row2: Atom
    input_vertical_row3: Atom
    input_vertical_col1: Atom
    input_vertical_col2: Atom
    input_vertical_col3: Atom
    
    input_horizontal_row1: Atom
    input_horizontal_row2: Atom
    input_horizontal_row3: Atom
    input_horizontal_col1: Atom
    input_horizontal_col2: Atom
    input_horizontal_col3: Atom
    
    target_half_T_row1: Atom
    target_half_T_row2: Atom
    target_half_T_row3: Atom
    target_half_T_col1: Atom
    target_half_T_col2: Atom
    target_half_T_col3: Atom

    target_mirror_L_row1: Atom
    target_mirror_L_row2: Atom
    target_mirror_L_row3: Atom
    target_mirror_L_col1: Atom
    target_mirror_L_col2: Atom
    target_mirror_L_col3: Atom

    target_vertical_row1: Atom
    target_vertical_row2: Atom
    target_vertical_row3: Atom
    target_vertical_col1: Atom
    target_vertical_col2: Atom
    target_vertical_col3: Atom
    
    target_horizontal_row1: Atom
    target_horizontal_row2: Atom
    target_horizontal_row3: Atom
    target_horizontal_col1: Atom
    target_horizontal_col2: Atom
    target_horizontal_col3: Atom

    construction_signal: Atom

class ResponseIO(Atoms):
    target_half_T: Atom
    target_mirror_L: Atom
    target_vertical: Atom
    target_horizontal: Atom
    
    target_half_T_row1: Atom
    target_half_T_row2: Atom
    target_half_T_row3: Atom
    target_half_T_col1: Atom
    target_half_T_col2: Atom
    target_half_T_col3: Atom
    
    target_mirror_L_row1: Atom
    target_mirror_L_row2: Atom
    target_mirror_L_row3: Atom
    target_mirror_L_col1: Atom
    target_mirror_L_col2: Atom
    target_mirror_L_col3: Atom
    
    target_vertical_row1: Atom
    target_vertical_row2: Atom
    target_vertical_row3: Atom
    target_vertical_col1: Atom
    target_vertical_col2: Atom
    target_vertical_col3: Atom
    
    target_horizontal_row1: Atom
    target_horizontal_row2: Atom
    target_horizontal_row3: Atom
    target_horizontal_col1: Atom
    target_horizontal_col2: Atom
    target_horizontal_col3: Atom
    
    query_block: Atom
    query_block_reference: Atom
    query_relation: Atom
    output: Atom

class Response(Atoms):
    yes: Atom
    no: Atom

class HighLevelResponse(Atoms):
    yes: Atom
    no: Atom
    latest: Atom

class MLPConstructionIO(Atoms):
    # strictly speaking, only need the input shape rows and target shape rows and cols
    input_half_T_row1: Atom
    input_half_T_row2: Atom
    input_half_T_row3: Atom
    input_half_T_col1: Atom
    input_half_T_col2: Atom
    input_half_T_col3: Atom
    input_mirror_L_row1: Atom
    input_mirror_L_row2: Atom
    input_mirror_L_row3: Atom
    input_mirror_L_col1: Atom
    input_mirror_L_col2: Atom
    input_mirror_L_col3: Atom
    input_vertical_row1: Atom
    input_vertical_row2: Atom
    input_vertical_row3: Atom
    input_vertical_col1: Atom
    input_vertical_col2: Atom
    input_vertical_col3: Atom
    input_horizontal_row1: Atom
    input_horizontal_row2: Atom
    input_horizontal_row3: Atom
    input_horizontal_col1: Atom
    input_horizontal_col2: Atom
    input_horizontal_col3: Atom
    
    target_half_T_row1: Atom
    target_half_T_row2: Atom
    target_half_T_row3: Atom
    target_half_T_col1: Atom
    target_half_T_col2: Atom
    target_half_T_col3: Atom
    target_mirror_L_row1: Atom
    target_mirror_L_row2: Atom
    target_mirror_L_row3: Atom
    target_mirror_L_col1: Atom
    target_mirror_L_col2: Atom
    target_mirror_L_col3: Atom
    target_vertical_row1: Atom
    target_vertical_row2: Atom
    target_vertical_row3: Atom
    target_vertical_col1: Atom
    target_vertical_col2: Atom
    target_vertical_col3: Atom
    target_horizontal_row1: Atom
    target_horizontal_row2: Atom
    target_horizontal_row3: Atom
    target_horizontal_col1: Atom
    target_horizontal_col2: Atom
    target_horizontal_col3: Atom


class HighLevelConstructionConditions(Atoms):
    input_half_T: Atom
    input_mirror_L: Atom
    input_vertical: Atom
    input_horizontal: Atom

    target_half_T: Atom
    target_mirror_L: Atom
    target_vertical: Atom
    target_horizontal: Atom

    stop: Atom
    start: Atom
    left: Atom
    right: Atom
    above: Atom
    below: Atom

class AbstractParticipantLowLevelConstructionIO(Atoms):
    input_half_T: Atom
    input_mirror_L: Atom
    input_vertical: Atom
    input_horizontal: Atom

    target_half_T: Atom
    target_mirror_L: Atom
    target_vertical: Atom
    target_horizontal: Atom

    input_half_T_row1: Atom
    input_half_T_row2: Atom
    input_half_T_row3: Atom
    input_half_T_col1: Atom
    input_half_T_col2: Atom
    input_half_T_col3: Atom
    
    input_mirror_L_row1: Atom
    input_mirror_L_row2: Atom
    input_mirror_L_row3: Atom
    input_mirror_L_col1: Atom
    input_mirror_L_col2: Atom
    input_mirror_L_col3: Atom
    
    input_vertical_row1: Atom
    input_vertical_row2: Atom
    input_vertical_row3: Atom
    input_vertical_col1: Atom
    input_vertical_col2: Atom
    input_vertical_col3: Atom
    
    input_horizontal_row1: Atom
    input_horizontal_row2: Atom
    input_horizontal_row3: Atom
    input_horizontal_col1: Atom
    input_horizontal_col2: Atom
    input_horizontal_col3: Atom
    
    target_half_T_row1: Atom
    target_half_T_row2: Atom
    target_half_T_row3: Atom
    target_half_T_col1: Atom
    target_half_T_col2: Atom
    target_half_T_col3: Atom

    target_mirror_L_row1: Atom
    target_mirror_L_row2: Atom
    target_mirror_L_row3: Atom
    target_mirror_L_col1: Atom
    target_mirror_L_col2: Atom
    target_mirror_L_col3: Atom

    target_vertical_row1: Atom
    target_vertical_row2: Atom
    target_vertical_row3: Atom
    target_vertical_col1: Atom
    target_vertical_col2: Atom
    target_vertical_col3: Atom
    
    target_horizontal_row1: Atom
    target_horizontal_row2: Atom
    target_horizontal_row3: Atom
    target_horizontal_col1: Atom
    target_horizontal_col2: Atom
    target_horizontal_col3: Atom

    stop: Atom
    start: Atom
    left: Atom
    right: Atom
    above: Atom
    below: Atom