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
    continue_construction: Atom
    stop_construction: Atom
    backtrack_construction: Atom

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
    backtrack: Atom

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

class ConstructionIOwAbstract(Atoms):
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

    start: Atom
    stop: Atom
    left: Atom
    right: Atom
    above: Atom
    below: Atom

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

class HighLevelConstructionSignals(Atoms):
    # stop: Atom
    # start: Atom
    # left: Atom
    # right: Atom
    # above: Atom
    # below: Atom
    half_T_start: Atom
    mirror_L_start: Atom
    vertical_start: Atom
    horizontal_start: Atom

    half_T_horizontal_left: Atom # reference, new block, relation
    half_T_horizontal_right: Atom 
    half_T_horizontal_above: Atom
    half_T_horizontal_below: Atom
    horizontal_half_T_left: Atom
    horizontal_half_T_right: Atom
    horizontal_half_T_above: Atom
    horizontal_half_T_below: Atom

    half_T_vertical_left: Atom
    half_T_vertical_right: Atom
    half_T_vertical_above: Atom
    half_T_vertical_below: Atom
    vertical_half_T_left: Atom
    vertical_half_T_right: Atom
    vertical_half_T_above: Atom
    vertical_half_T_below: Atom

    half_T_mirror_L_left: Atom
    half_T_mirror_L_right: Atom
    half_T_mirror_L_above: Atom
    half_T_mirror_L_below: Atom
    mirror_L_half_T_left: Atom
    mirror_L_half_T_right: Atom
    mirror_L_half_T_above: Atom
    mirror_L_half_T_below: Atom

    mirror_L_horizontal_left: Atom
    mirror_L_horizontal_right: Atom
    mirror_L_horizontal_above: Atom
    mirror_L_horizontal_below: Atom
    horizontal_mirror_L_left: Atom
    horizontal_mirror_L_right: Atom
    horizontal_mirror_L_above: Atom
    horizontal_mirror_L_below: Atom

    mirror_L_vertical_left: Atom
    mirror_L_vertical_right: Atom
    mirror_L_vertical_above: Atom
    mirror_L_vertical_below: Atom
    vertical_mirror_L_left: Atom
    vertical_mirror_L_right: Atom
    vertical_mirror_L_above: Atom
    vertical_mirror_L_below: Atom

    vertical_horizontal_left: Atom
    vertical_horizontal_right: Atom
    vertical_horizontal_above: Atom
    vertical_horizontal_below: Atom
    horizontal_vertical_left: Atom
    horizontal_vertical_right: Atom
    horizontal_vertical_above: Atom
    horizontal_vertical_below: Atom

    stop: Atom

class JustYes(Atoms):
    yes: Atom

class GoalMLPOutputSpace(Family):
    construction_signal: HighLevelConstructionSignals
    response: JustYes

class BrickConstructionTask(Family):
    numbers: Numbers
    signal_tokens: SignalTokens
    io: ConstructionIO
    response: Response

class BrickConstructionTaskAbstractParticipant(Family):
    numbers: Numbers
    io: ConstructionIOwAbstract
    response: HighLevelResponse

class BrickResponseTask(Family):
    bricks: Brick
    numbers: Numbers
    query_rel: Rel
    io: ResponseIO
    response: Response

class MLPConstructionSubTask(Family):
    io: MLPConstructionIO
    numbers: Numbers

class HighLevelConstruction(Family):
    io: HighLevelConstructionConditions
    response: HighLevelResponse