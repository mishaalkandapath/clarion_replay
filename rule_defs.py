from pyClarion import (Agent, Input, Choice, ChunkStore, FixedRules, 
    Family, Atoms, Atom, BaseLevel, Pool, NumDict, Event, Priority)

from typing import *
import math
import itertools

SHAPES = ["horizontal", "vertical", "half_T", "mirror_L"]

def init_participant_response_rules(participant) -> None:
    d = participant.response_space
    io = d.io
    bricks = d.bricks
    numbers = d.numbers
    query_rel = d.query_rel
    response = d.response

    #response rules when given a query and some blocks
    
    # HALF_T X HORIZONTAL
    #i = 0, horizontal is next to the potruding part of the shape, else it is next to the flat part at the bottom
    half_T_left_of_horizontal = [
        (+ io.query_block ** (bricks.half_T if not switcharoo else bricks.horizontal)
        + io.query_block_reference ** (bricks.horizontal if not switcharoo else bricks.half_T)
        + io.query_relation ** (query_rel.left if not switcharoo else query_rel.right)
        + io.target_half_T ** bricks.half_T
        + io.target_horizontal ** bricks.horizontal
        + io.target_half_T_row1 ** numbers[f"n{row}"]
        + io.target_half_T_row2 ** numbers[f"n{row}"]
        + io.target_half_T_row3 ** numbers[f"n{row+1}"]
        + io.target_half_T_col1 ** numbers[f"n{col}"]
        + io.target_half_T_col2 ** numbers[f"n{col+1}"]
        + io.target_half_T_col3 ** numbers[f"n{col}"]
        + io.target_horizontal_row1 ** numbers[f"n{row+i}"]
        + io.target_horizontal_row2 ** numbers[f"n{row+i}"]
        + io.target_horizontal_row3 ** numbers[f"n{row+i}"]
        + io.target_horizontal_col1 ** numbers[f"n{col+2-i}"]
        + io.target_horizontal_col2 ** numbers[f"n{col+3-i}"]
        + io.target_horizontal_col3 ** numbers[f"n{col+4-i}"]
        >>
        + io.output ** response.yes) for switcharoo in (True, False) for i in range(2) for row in range(1, 6) for col in range(1, 3 + i)
    ]

    half_T_right_of_horizontal = [
        (+ io.query_block ** (bricks.half_T if not switcharoo else bricks.horizontal)
        + io.query_block_reference ** (bricks.horizontal if not switcharoo else bricks.half_T)
        + io.query_relation ** (query_rel.right if not switcharoo else query_rel.left)
        + io.target_half_T ** bricks.half_T
        + io.target_horizontal ** bricks.horizontal
        + io.target_half_T_row1 ** numbers[f"n{row}"]
        + io.target_half_T_row2 ** numbers[f"n{row}"]
        + io.target_half_T_row3 ** numbers[f"n{row+1}"]
        + io.target_half_T_col1 ** numbers[f"n{col}"]
        + io.target_half_T_col2 ** numbers[f"n{col+1}"]
        + io.target_half_T_col3 ** numbers[f"n{col}"]
        + io.target_horizontal_row1 ** numbers[f"n{row+i}"]
        + io.target_horizontal_row2 ** numbers[f"n{row+i}"]
        + io.target_horizontal_row3 ** numbers[f"n{row+i}"]
        + io.target_horizontal_col1 ** numbers[f"n{col-3}"]
        + io.target_horizontal_col2 ** numbers[f"n{col-2}"]
        + io.target_horizontal_col3 ** numbers[f"n{col-1}"]
        >>
        + io.output ** response.yes) for switcharoo in (True, False) for i in range(2) for row in range(1, 6) for col in range(4, 6)
    ]
    """
    TODO:
    Check the actual relation for
    1 1
    1 2 2 2 is this ontopness or beside? 
    TODO: Similarly for the other relations involving L like shapes
    """

    half_T_below_horizontal = [
        (+ io.query_block ** (bricks.half_T if not switcharoo else bricks.horizontal)
        + io.query_block_reference ** (bricks.horizontal if not switcharoo else bricks.half_T)
        + io.query_relation ** (query_rel.below if not switcharoo else query_rel.above)
        + io.target_half_T ** bricks.half_T
        + io.target_horizontal ** bricks.horizontal
        + io.target_half_T_row1 ** numbers[f"n{row}"]
        + io.target_half_T_row2 ** numbers[f"n{row}"]
        + io.target_half_T_row3 ** numbers[f"n{row+1}"]
        + io.target_half_T_col1 ** numbers[f"n{col}"]
        + io.target_half_T_col2 ** numbers[f"n{col+1}"]
        + io.target_half_T_col3 ** numbers[f"n{col}"]
        + io.target_horizontal_row1 ** numbers[f"n{row-1}"]
        + io.target_horizontal_row2 ** numbers[f"n{row-1}"]
        + io.target_horizontal_row3 ** numbers[f"n{row-1}"]
        + io.target_horizontal_col1 ** numbers[f"n{col-1+i}"]
        + io.target_horizontal_col2 ** numbers[f"n{col+i}"]
        + io.target_horizontal_col3 ** numbers[f"n{col+1+i}"]
        >>
        + io.output ** response.yes) for switcharoo in (True, False) for i in range(3) for row in range(2, 6) for col in range(1 + (i == 0), 6-i)
    ]

    half_T_above_horizontal = [
        (+ io.query_block ** (bricks.half_T if not switcharoo else bricks.horizontal)
        + io.query_block_reference ** (bricks.horizontal if not switcharoo else bricks.half_T)
        + io.query_relation ** (query_rel.above if not switcharoo else query_rel.below)
        + io.target_half_T ** bricks.half_T
        + io.target_horizontal ** bricks.horizontal
        + io.target_half_T_row1 ** numbers[f"n{row}"]
        + io.target_half_T_row2 ** numbers[f"n{row}"]
        + io.target_half_T_row3 ** numbers[f"n{row+1}"]
        + io.target_half_T_col1 ** numbers[f"n{col}"]
        + io.target_half_T_col2 ** numbers[f"n{col+1}"]
        + io.target_half_T_col3 ** numbers[f"n{col}"]
        + io.target_horizontal_row1 ** numbers[f"n{row+2}"]
        + io.target_horizontal_row2 ** numbers[f"n{row+2}"]
        + io.target_horizontal_row3 ** numbers[f"n{row+2}"]
        + io.target_horizontal_col1 ** numbers[f"n{col-2+i}"]
        + io.target_horizontal_col2 ** numbers[f"n{col-1+i}"]
        + io.target_horizontal_col3 ** numbers[f"n{col+i}"]
        >>
        + io.output ** response.yes) for i in range(3) for switcharoo in (True, False) for row in range(1, 5) for col in range(3-i, 6-(i==2))
]

    #HALF_T X VERTICAL

    half_T_left_vertical = [
        (+ io.query_block ** (bricks.half_T if not switcharoo else bricks.vertical)
        + io.query_block_reference ** (bricks.vertical if not switcharoo else bricks.half_T)
        + io.query_relation ** (query_rel.left if not switcharoo else query_rel.right)
        + io.target_half_T ** bricks.half_T
        + io.target_vertical ** bricks.vertical
        + io.target_half_T_row1 ** numbers[f"n{row}"]
        + io.target_half_T_row2 ** numbers[f"n{row}"]
        + io.target_half_T_row3 ** numbers[f"n{row+1}"]
        + io.target_half_T_col1 ** numbers[f"n{col}"]
        + io.target_half_T_col2 ** numbers[f"n{col+1}"]
        + io.target_half_T_col3 ** numbers[f"n{col}"]
        + io.target_vertical_row1 ** numbers[f"n{row+1-i}"]
        + io.target_vertical_row2 ** numbers[f"n{row+2-i}"]
        + io.target_vertical_row3 ** numbers[f"n{row+3-i}"]
        + io.target_vertical_col1 ** numbers[f"n{col+2- (i == 0)}"]
        + io.target_vertical_col2 ** numbers[f"n{col+2 - (i == 0)}"]
        + io.target_vertical_col3 ** numbers[f"n{col+2 - (i == 0)}"]
        >>
        + io.output ** response.yes) for switcharoo in (True, False) for i in range(4) for row in range(1+(i-1 if i > 1 else 0), 4 + (math.ceil(i/2))) for col in range(1, 6-(i > 0))
    ]

    half_T_right_vertical = [
        (+ io.query_block ** (bricks.half_T if not switcharoo else bricks.vertical)
        + io.query_block_reference ** (bricks.vertical if not switcharoo else bricks.half_T)
        + io.query_relation ** (query_rel.right if not switcharoo else query_rel.left)
        + io.target_half_T ** bricks.half_T
        + io.target_vertical ** bricks.vertical
        + io.target_half_T_row1 ** numbers[f"n{row}"]
        + io.target_half_T_row2 ** numbers[f"n{row}"]
        + io.target_half_T_row3 ** numbers[f"n{row+1}"]
        + io.target_half_T_col1 ** numbers[f"n{col}"]
        + io.target_half_T_col2 ** numbers[f"n{col+1}"]
        + io.target_half_T_col3 ** numbers[f"n{col}"]
        + io.target_vertical_row1 ** numbers[f"n{row-2+i}"]
        + io.target_vertical_row2 ** numbers[f"n{row-1+i}"]
        + io.target_vertical_row3 ** numbers[f"n{row+i}"]
        + io.target_vertical_col1 ** numbers[f"n{col-1}"]
        + io.target_vertical_col2 ** numbers[f"n{col-1}"]
        + io.target_vertical_col3 ** numbers[f"n{col-1}"]
        >>
        + io.output ** response.yes) for switcharoo in (True, False) for i in range(4) for row in range(max(1, 3-i), 6-max(0, i-1)) for col in range(2, 6)
    ]

    half_T_below_vertical = [
        (+ io.query_block ** (bricks.half_T if not switcharoo else bricks.vertical)
        + io.query_block_reference ** (bricks.vertical if not switcharoo else bricks.half_T)
        + io.query_relation ** (query_rel.below if not switcharoo else query_rel.above)
        + io.target_half_T ** bricks.half_T
        + io.target_vertical ** bricks.vertical
        + io.target_half_T_row1 ** numbers[f"n{row}"]
        + io.target_half_T_row2 ** numbers[f"n{row}"]
        + io.target_half_T_row3 ** numbers[f"n{row+1}"]
        + io.target_half_T_col1 ** numbers[f"n{col}"]
        + io.target_half_T_col2 ** numbers[f"n{col+1}"]
        + io.target_half_T_col3 ** numbers[f"n{col}"]
        + io.target_vertical_row1 ** numbers[f"n{row-3}"]
        + io.target_vertical_row2 ** numbers[f"n{row-2}"]
        + io.target_vertical_row3 ** numbers[f"n{row-3}"]
        + io.target_vertical_col1 ** numbers[f"n{col+i}"]
        + io.target_vertical_col2 ** numbers[f"n{col+i}"]
        + io.target_vertical_col3 ** numbers[f"n{col+i}"]
        >>
        + io.output ** response.yes) for switcharoo in (True, False) for i in range(2) for row in range(4, 6) for col in range(1, 6)
    ]

    half_T_above_vertical = [
        (+ io.query_block ** (bricks.half_T if not switcharoo else bricks.vertical)
        + io.query_block_reference ** (bricks.vertical if not switcharoo else bricks.half_T)
        + io.query_relation ** (query_rel.above if not switcharoo else query_rel.below)
        + io.target_half_T ** bricks.half_T
        + io.target_vertical ** bricks.vertical
        + io.target_half_T_row1 ** numbers[f"n{row}"]
        + io.target_half_T_row2 ** numbers[f"n{row}"]
        + io.target_half_T_row3 ** numbers[f"n{row+1}"]
        + io.target_half_T_col1 ** numbers[f"n{col}"]
        + io.target_half_T_col2 ** numbers[f"n{col+1}"]
        + io.target_half_T_col3 ** numbers[f"n{col}"]
        + io.target_vertical_row1 ** numbers[f"n{row+1}"]
        + io.target_vertical_row2 ** numbers[f"n{row+2}"]
        + io.target_vertical_row3 ** numbers[f"n{row+3}"]
        + io.target_vertical_col1 ** numbers[f"n{col}"]
        + io.target_vertical_col2 ** numbers[f"n{col}"]
        + io.target_vertical_col3 ** numbers[f"n{col}"]
        >>
        + io.output ** response.yes) for switcharoo in (True, False) for row in range(1, 3) for col in range(1, 6)
    ]

    #HALF_T X MIRROR_L
    half_T_left_mirror_L = [
        (+ io.query_block ** (bricks.half_T if not switcharoo else bricks.mirror_L)
        + io.query_block_reference ** (bricks.mirror_L if not switcharoo else bricks.half_T)
        + io.query_relation ** (query_rel.left if not switcharoo else query_rel.right)
        + io.target_half_T ** bricks.half_T
        + io.target_mirror_L ** bricks.mirror_L
        + io.target_half_T_row1 ** numbers[f"n{row}"]
        + io.target_half_T_row2 ** numbers[f"n{row}"]
        + io.target_half_T_row3 ** numbers[f"n{row+1}"]
        + io.target_half_T_col1 ** numbers[f"n{col}"]
        + io.target_half_T_col2 ** numbers[f"n{col+1}"]
        + io.target_half_T_col3 ** numbers[f"n{col}"]
        + io.target_mirror_L_row1 ** numbers[f"n{row-i}"]
        + io.target_mirror_L_row2 ** numbers[f"n{row+1-i}"]
        + io.target_mirror_L_row3 ** numbers[f"n{row+1-i}"]
        + io.target_mirror_L_col1 ** numbers[f"n{col+2+i}"]
        + io.target_mirror_L_col2 ** numbers[f"n{col+1+i}"]
        + io.target_mirror_L_col3 ** numbers[f"n{col+2+i}"]
        >>
        + io.output ** response.yes) for switcharoo in (True, False) for i in range(2) for row in range(1+i, 6) for col in range(1, 5-i)
    ]

    """  
    # 1 1 2
    # 1 2 2

    #       2
    # 1 1 2 2
    # 1
    """
    half_T_right_mirror_L = [
        (+ io.query_block ** (bricks.half_T if not switcharoo else bricks.mirror_L)
        + io.query_block_reference ** (bricks.mirror_L if not switcharoo else bricks.half_T)
        + io.query_relation ** (query_rel.right if not switcharoo else query_rel.left)
        + io.target_half_T ** bricks.half_T
        + io.target_mirror_L ** bricks.mirror_L
        + io.target_half_T_row1 ** numbers[f"n{row}"]
        + io.target_half_T_row2 ** numbers[f"n{row}"]
        + io.target_half_T_row3 ** numbers[f"n{row+1}"]
        + io.target_half_T_col1 ** numbers[f"n{col}"]
        + io.target_half_T_col2 ** numbers[f"n{col+1}"]
        + io.target_half_T_col3 ** numbers[f"n{col}"]
        + io.target_mirror_L_row1 ** numbers[f"n{row + (-1 if i== 0 else 1)*(i%2 == 0)}"] # 1 up, no up, 1 down.
        + io.target_mirror_L_row2 ** numbers[f"n{row + i}"]
        + io.target_mirror_L_row3 ** numbers[f"n{row+i}"]
        + io.target_mirror_L_col1 ** numbers[f"n{col-1}"]
        + io.target_mirror_L_col2 ** numbers[f"n{col-2}"]
        + io.target_mirror_L_col3 ** numbers[f"n{col-1}"]
        >>
        + io.output ** response.yes) for switcharoo in (True, False) for i in range(3) for row in range(1+(i==0), 6-(i==2)) for col in range(3, 6)
    ]

    half_T_below_mirror_L = [
        (+ io.query_block ** (bricks.half_T if not switcharoo else bricks.mirror_L)
        + io.query_block_reference ** (bricks.mirror_L if not switcharoo else bricks.half_T)
        + io.query_relation ** (query_rel.below if not switcharoo else query_rel.above)
        + io.target_half_T ** bricks.half_T
        + io.target_mirror_L ** bricks.mirror_L
        + io.target_half_T_row1 ** numbers[f"n{row}"]
        + io.target_half_T_row2 ** numbers[f"n{row}"]
        + io.target_half_T_row3 ** numbers[f"n{row+1}"]
        + io.target_half_T_col1 ** numbers[f"n{col}"]
        + io.target_half_T_col2 ** numbers[f"n{col+1}"]
        + io.target_half_T_col3 ** numbers[f"n{col}"]
        + io.target_mirror_L_row1 ** numbers[f"n{row-2}"]
        + io.target_mirror_L_row2 ** numbers[f"n{row-1}"]
        + io.target_mirror_L_row3 ** numbers[f"n{row-1}"]
        + io.target_mirror_L_col1 ** numbers[f"n{col+1+i}"]
        + io.target_mirror_L_col2 ** numbers[f"n{col+i}"]
        + io.target_mirror_L_col3 ** numbers[f"n{col+1+i}"]
        >>
        + io.output ** response.yes) for i in range(2) for switcharoo in (True, False) for row in range(3, 6) for col in range(1, 6-i)
    ]

    half_T_above_mirror_L = [
        (+ io.query_block ** (bricks.half_T if not switcharoo else bricks.mirror_L)
        + io.query_block_reference ** (bricks.mirror_L if not switcharoo else bricks.half_T)
        + io.query_relation ** (query_rel.above if not switcharoo else query_rel.below)
        + io.target_half_T ** bricks.half_T
        + io.target_mirror_L ** bricks.mirror_L
        + io.target_half_T_row1 ** numbers[f"n{row}"]
        + io.target_half_T_row2 ** numbers[f"n{row}"]
        + io.target_half_T_row3 ** numbers[f"n{row+1}"]
        + io.target_half_T_col1 ** numbers[f"n{col}"]
        + io.target_half_T_col2 ** numbers[f"n{col+1}"]
        + io.target_half_T_col3 ** numbers[f"n{col}"]
        + io.target_mirror_L_row1 ** numbers[f"n{row+2}"]
        + io.target_mirror_L_row2 ** numbers[f"n{row+3}"]
        + io.target_mirror_L_row3 ** numbers[f"n{row+3}"]
        + io.target_mirror_L_col1 ** numbers[f"n{col}"]
        + io.target_mirror_L_col2 ** numbers[f"n{col-1}"]
        + io.target_mirror_L_col3 ** numbers[f"n{col}"]
        >>
        + io.output ** response.yes) for switcharoo in (True, False) for row in range(1, 4) for col in range(2, 6)
    ]

    #MIRROR_L X HORIZONTAL
    mirror_L_left_horizontal  = [
        (+ io.query_block ** (bricks.mirror_L if not switcharoo else bricks.horizontal)
        + io.query_block_reference ** (bricks.horizontal if not switcharoo else bricks.mirror_L)
        + io.query_relation ** (query_rel.left if not switcharoo else query_rel.right)
        + io.target_mirror_L ** bricks.mirror_L
        + io.target_horizontal ** bricks.horizontal
        + io.target_mirror_L_row1 ** numbers[f"n{row}"]
        + io.target_mirror_L_row2 ** numbers[f"n{row+1}"]
        + io.target_mirror_L_row3 ** numbers[f"n{row+1}"]
        + io.target_mirror_L_col1 ** numbers[f"n{col}"]
        + io.target_mirror_L_col2 ** numbers[f"n{col-1}"]
        + io.target_mirror_L_col3 ** numbers[f"n{col}"]
        + io.target_horizontal_row1 ** numbers[f"n{row+i}"]
        + io.target_horizontal_row2 ** numbers[f"n{row+i}"]
        + io.target_horizontal_row3 ** numbers[f"n{row+i}"]
        + io.target_horizontal_col1 ** numbers[f"n{col+1}"]
        + io.target_horizontal_col2 ** numbers[f"n{col+2}"]
        + io.target_horizontal_col3 ** numbers[f"n{col+3}"]
        >>
        + io.output ** response.yes) for switcharoo in (True, False) for i in range(2) for row in range(1, 6) for col in range(2, 4)
    ]

    mirror_L_right_horizontal = [
        (+ io.query_block ** (bricks.mirror_L if not switcharoo else bricks.horizontal)
        + io.query_block_reference ** (bricks.horizontal if not switcharoo else bricks.mirror_L)
        + io.query_relation ** (query_rel.right if not switcharoo else query_rel.left)
        + io.target_mirror_L ** bricks.mirror_L
        + io.target_horizontal ** bricks.horizontal
        + io.target_mirror_L_row1 ** numbers[f"n{row}"]
        + io.target_mirror_L_row2 ** numbers[f"n{row+1}"]
        + io.target_mirror_L_row3 ** numbers[f"n{row+1}"]
        + io.target_mirror_L_col1 ** numbers[f"n{col}"]
        + io.target_mirror_L_col2 ** numbers[f"n{col-1}"]
        + io.target_mirror_L_col3 ** numbers[f"n{col}"]
        + io.target_horizontal_row1 ** numbers[f"n{row+i}"]
        + io.target_horizontal_row2 ** numbers[f"n{row+i}"]
        + io.target_horizontal_row3 ** numbers[f"n{row+i}"]
        + io.target_horizontal_col1 ** numbers[f"n{col-3-i}"]
        + io.target_horizontal_col2 ** numbers[f"n{col-2-i}"]
        + io.target_horizontal_col3 ** numbers[f"n{col-1-i}"]
        >>
        + io.output ** response.yes) for switcharoo in (True, False) for i in range(2) for row in range(1, 6) for col in range(4+i, 7)
    ]
    """
    2 2 2 1
        1 1

            1
    2 2 2 1 1
    """

    mirror_L_above_horizontal = [
        (+ io.query_block ** (bricks.mirror_L if not switcharoo else bricks.horizontal)
        + io.query_block_reference ** (bricks.horizontal if not switcharoo else bricks.mirror_L)
        + io.query_relation ** (query_rel.below if not switcharoo else query_rel.above)
        + io.target_mirror_L ** bricks.mirror_L
        + io.target_horizontal ** bricks.horizontal
        + io.target_mirror_L_row1 ** numbers[f"n{row}"]
        + io.target_mirror_L_row2 ** numbers[f"n{row+1}"]
        + io.target_mirror_L_row3 ** numbers[f"n{row+1}"]
        + io.target_mirror_L_col1 ** numbers[f"n{col}"]
        + io.target_mirror_L_col2 ** numbers[f"n{col-1}"]
        + io.target_mirror_L_col3 ** numbers[f"n{col}"]
        + io.target_horizontal_row1 ** numbers[f"n{row+2}"]
        + io.target_horizontal_row2 ** numbers[f"n{row+2}"]
        + io.target_horizontal_row3 ** numbers[f"n{row+2}"]
        + io.target_horizontal_col1 ** numbers[f"n{col-2+i}"]
        + io.target_horizontal_col2 ** numbers[f"n{col-1+i}"]
        + io.target_horizontal_col3 ** numbers[f"n{col+i}"]
        >>
        + io.output ** response.yes) for switcharoo in (True, False) for i in range(3) for row in range(1, 5) for col in range(2 + (i == 0), 7-i)
    ]
    """
        1
      1 1
    2 2 2
    
      1
    1 1
    2 2 2

    1
    1 1
      2 2 2
    """

    mirror_L_below_horizontal = [
        (+ io.query_block ** (bricks.mirror_L if not switcharoo else bricks.horizontal)
        + io.query_block_reference ** (bricks.horizontal if not switcharoo else bricks.mirror_L)
        + io.query_relation ** (query_rel.below if not switcharoo else query_rel.above)
        + io.target_mirror_L ** bricks.mirror_L
        + io.target_horizontal ** bricks.horizontal
        + io.target_mirror_L_row1 ** numbers[f"n{row}"]
        + io.target_mirror_L_row2 ** numbers[f"n{row+1}"]
        + io.target_mirror_L_row3 ** numbers[f"n{row+1}"]
        + io.target_mirror_L_col1 ** numbers[f"n{col}"]
        + io.target_mirror_L_col2 ** numbers[f"n{col-1}"]
        + io.target_mirror_L_col3 ** numbers[f"n{col}"]
        + io.target_horizontal_row1 ** numbers[f"n{row-1}"]
        + io.target_horizontal_row2 ** numbers[f"n{row-1}"]
        + io.target_horizontal_row3 ** numbers[f"n{row-1}"]
        + io.target_horizontal_col1 ** numbers[f"n{col-2+i}"]
        + io.target_horizontal_col2 ** numbers[f"n{col-1+i}"]
        + io.target_horizontal_col3 ** numbers[f"n{col+i}"]
        >>
        + io.output ** response.yes) for switcharoo in (True, False) for i in range (3) for row in range(2, 6) for col in range(3-(i != 0), 7-i)
    ]
    """
    2 2 2
        1
      1 1
    """

    #MIRROR_L X VERTICAL
    mirror_L_left_vertical  = [
        (+ io.query_block ** (bricks.mirror_L if not switcharoo else bricks.vertical)
        + io.query_block_reference ** (bricks.vertical if not switcharoo else bricks.mirror_L)
        + io.query_relation ** (query_rel.left if not switcharoo else query_rel.right)
        + io.target_mirror_L ** bricks.mirror_L
        + io.target_vertical ** bricks.vertical
        + io.target_mirror_L_row1 ** numbers[f"n{row}"]
        + io.target_mirror_L_row2 ** numbers[f"n{row+1}"]
        + io.target_mirror_L_row3 ** numbers[f"n{row+1}"]
        + io.target_mirror_L_col1 ** numbers[f"n{col}"]
        + io.target_mirror_L_col2 ** numbers[f"n{col-1}"]
        + io.target_mirror_L_col3 ** numbers[f"n{col}"]
        + io.target_vertical_row1 ** numbers[f"n{row-1+i}"]
        + io.target_vertical_row2 ** numbers[f"n{row+i}"]
        + io.target_vertical_row3 ** numbers[f"n{row+1+i}"]
        + io.target_vertical_col1 ** numbers[f"n{col+1}"]
        + io.target_vertical_col2 ** numbers[f"n{col+1}"]
        + io.target_vertical_col3 ** numbers[f"n{col+1}"]
        >>
        + io.output ** response.yes) 
        for switcharoo in (True, False) for i in range(3) for row in range(1+(i==0), 6-i) for col in range(2, 6)
    ]

    """
    1 2
    1 1 2
        2

    1 
    1 1 2
        2
        2
    """

    mirror_L_right_vertical = [
        (+ io.query_block ** (bricks.mirror_L if not switcharoo else bricks.vertical)
        + io.query_block_reference ** (bricks.vertical if not switcharoo else bricks.mirror_L)
        + io.query_relation ** (query_rel.right if not switcharoo else query_rel.left)
        + io.target_mirror_L ** bricks.mirror_L
        + io.target_vertical ** bricks.vertical
        + io.target_mirror_L_row1 ** numbers[f"n{row}"]
        + io.target_mirror_L_row2 ** numbers[f"n{row+1}"]
        + io.target_mirror_L_row3 ** numbers[f"n{row+1}"]
        + io.target_mirror_L_col1 ** numbers[f"n{col}"]
        + io.target_mirror_L_col2 ** numbers[f"n{col-1}"]
        + io.target_mirror_L_col3 ** numbers[f"n{col}"]
        + io.target_vertical_row1 ** numbers[f"n{row+1-i}"]
        + io.target_vertical_row2 ** numbers[f"n{row+2-i}"]
        + io.target_vertical_row3 ** numbers[f"n{row+3-i}"]
        + io.target_vertical_col1 ** numbers[f"n{col-2 + (i == 3)}"]
        + io.target_vertical_col2 ** numbers[f"n{col-2 + (i == 3)}"]
        + io.target_vertical_col3 ** numbers[f"n{col-2 + (i == 3)}"]
        >>
        + io.output ** response.yes) for switcharoo in (True, False) for i in range(4) for row in range(1+max(0, i-1), min(4+i, 6)) for col in range(3 - (i == 3), 7)
    ]

    """
    2   
    2   1
    2 1 1

    2   1
    2 1 1
    2

        1
    2 1 1
    2
    2

    2
    2
    2 1
    1 1
    """

    mirror_L_above_vertical = [
        (+ io.query_block ** (bricks.mirror_L if not switcharoo else bricks.vertical)
        + io.query_block_reference ** (bricks.vertical if not switcharoo else bricks.mirror_L)
        + io.query_relation ** (query_rel.above if not switcharoo else query_rel.below)
        + io.target_mirror_L ** bricks.mirror_L
        + io.target_vertical ** bricks.vertical
        + io.target_mirror_L_row1 ** numbers[f"n{row}"]
        + io.target_mirror_L_row2 ** numbers[f"n{row+1}"]
        + io.target_mirror_L_row3 ** numbers[f"n{row+1}"]
        + io.target_mirror_L_col1 ** numbers[f"n{col}"]
        + io.target_mirror_L_col2 ** numbers[f"n{col-1}"]
        + io.target_mirror_L_col3 ** numbers[f"n{col}"]
        + io.target_vertical_row1 ** numbers[f"n{row+2}"]
        + io.target_vertical_row2 ** numbers[f"n{row+3}"]
        + io.target_vertical_row3 ** numbers[f"n{row+4}"]
        + io.target_vertical_col1 ** numbers[f"n{col-1+i}"]
        + io.target_vertical_col2 ** numbers[f"n{col-1+i}"]
        + io.target_vertical_col3 ** numbers[f"n{col-1+i}"]
        >>
        + io.output ** response.yes) for switcharoo in (True, False) for i in range(2) for row in range(1, 3) for col in range(2, 7)
    ]

    """
    1
    1 1
    2
    2
    2 

    1
    1 1
      2
      2
      2
    """

    mirror_L_below_vertical = [
        (+ io.query_block ** (bricks.mirror_L if not switcharoo else bricks.vertical)
        + io.query_block_reference ** (bricks.vertical if not switcharoo else bricks.mirror_L)
        + io.query_relation ** (query_rel.below if not switcharoo else query_rel.above)
        + io.target_mirror_L ** bricks.mirror_L
        + io.target_vertical ** bricks.vertical
        + io.target_mirror_L_row1 ** numbers[f"n{row}"]
        + io.target_mirror_L_row2 ** numbers[f"n{row+1}"]
        + io.target_mirror_L_row3 ** numbers[f"n{row+1}"]
        + io.target_mirror_L_col1 ** numbers[f"n{col}"]
        + io.target_mirror_L_col2 ** numbers[f"n{col-1}"]
        + io.target_mirror_L_col3 ** numbers[f"n{col}"]
        + io.target_vertical_row1 ** numbers[f"n{row-3}"]
        + io.target_vertical_row2 ** numbers[f"n{row-2}"]
        + io.target_vertical_row3 ** numbers[f"n{row-1}"]
        + io.target_vertical_col1 ** numbers[f"n{col}"]
        + io.target_vertical_col2 ** numbers[f"n{col}"]
        + io.target_vertical_col3 ** numbers[f"n{col}"]
        >>
        + io.output ** response.yes) for switcharoo in (True, False) for row in range(4, 6) for col in range(2, 7)
    ]

    """
      2
      2
      2
      1
    1 1
    """

    #HORIZONTAL X VERTICAL
    horizontal_left_vertical  = [
        (+ io.query_block ** (bricks.horizontal if not switcharoo else bricks.vertical)
        + io.query_block_reference ** (bricks.vertical if not switcharoo else bricks.horizontal)
        + io.query_relation ** (query_rel.left if not switcharoo else query_rel.right)
        + io.target_vertical ** bricks.horizontal
        + io.target_horizontal ** bricks.vertical
        + io.target_vertical_row1 ** numbers[f"n{row}"]
        + io.target_vertical_row2 ** numbers[f"n{row}"]
        + io.target_vertical_row3 ** numbers[f"n{row}"]
        + io.target_vertical_col1 ** numbers[f"n{col}"]
        + io.target_vertical_col2 ** numbers[f"n{col+1}"] 
        + io.target_vertical_col3 ** numbers[f"n{col+2}"]
        + io.target_horizontal_row1 ** numbers[f"n{row-2+i}"]
        + io.target_horizontal_row2 ** numbers[f"n{row-1+i}"]
        + io.target_horizontal_row3 ** numbers[f"n{row+i}"]
        + io.target_horizontal_col1 ** numbers[f"n{col+3}"]
        + io.target_horizontal_col2 ** numbers[f"n{col+3}"]
        + io.target_horizontal_col3 ** numbers[f"n{col+3}"]
        >>
        + io.output ** response.yes) for switcharoo in (True, False) for i in range(3) for row in range(3-i, 7-i) for col in range(1, 4)
    ]

    """
        2
        2
    1 1 1 2

        2
    1 1 1 2
        2

    1 1 1 2
        2
        2      
    """

    horizontal_right_vertical = [
        (+ io.query_block ** (bricks.horizontal if not switcharoo else bricks.vertical)
        + io.query_block_reference ** (bricks.vertical if not switcharoo else bricks.horizontal)
        + io.query_relation ** (query_rel.right if not switcharoo else query_rel.left)
        + io.target_vertical ** bricks.horizontal
        + io.target_horizontal ** bricks.vertical
        + io.target_vertical_row1 ** numbers[f"n{row}"]
        + io.target_vertical_row2 ** numbers[f"n{row}"]
        + io.target_vertical_row3 ** numbers[f"n{row}"]
        + io.target_vertical_col1 ** numbers[f"n{col}"]
        + io.target_vertical_col2 ** numbers[f"n{col+1}"] 
        + io.target_vertical_col3 ** numbers[f"n{col+2}"]
        + io.target_horizontal_row1 ** numbers[f"n{row-2+i}"]
        + io.target_horizontal_row2 ** numbers[f"n{row-1+i}"]
        + io.target_horizontal_row3 ** numbers[f"n{row+i}"]
        + io.target_horizontal_col1 ** numbers[f"n{col-1}"]
        + io.target_horizontal_col2 ** numbers[f"n{col-1}"]
        + io.target_horizontal_col3 ** numbers[f"n{col-1}"]
        >>
        + io.output ** response.yes) for switcharoo in (True, False) for i in range(3) for row in range(3-i, 7-i) for col in range(2, 5)
    ]

    """
    2
    2
    2 1 1 1

    2
    2 1 1 1
    2

    2
    2
    2 1 1 1
    """

    horizontal_above_vertical = [
        (+ io.query_block ** (bricks.horizontal if not switcharoo else bricks.vertical)
        + io.query_block_reference ** (bricks.vertical if not switcharoo else bricks.horizontal)
        + io.query_relation ** (query_rel.above if not switcharoo else query_rel.below)
        + io.target_vertical ** bricks.horizontal
        + io.target_horizontal ** bricks.vertical
        + io.target_vertical_row1 ** numbers[f"n{row}"]
        + io.target_vertical_row2 ** numbers[f"n{row}"]
        + io.target_vertical_row3 ** numbers[f"n{row}"]
        + io.target_vertical_col1 ** numbers[f"n{col}"]
        + io.target_vertical_col2 ** numbers[f"n{col+1}"] 
        + io.target_vertical_col3 ** numbers[f"n{col+2}"]
        + io.target_horizontal_row1 ** numbers[f"n{row+1}"]
        + io.target_horizontal_row2 ** numbers[f"n{row+2}"]
        + io.target_horizontal_row3 ** numbers[f"n{row+3}"]
        + io.target_horizontal_col1 ** numbers[f"n{col+i}"]
        + io.target_horizontal_col2 ** numbers[f"n{col+i}"]
        + io.target_horizontal_col3 ** numbers[f"n{col+i}"]
        >>
        + io.output ** response.yes) for switcharoo in (True, False) for i in range(3) for row in range(1, 4) for col in range(1, 5)
    ]

    """
    1 1 1
    2
    2
    2

    1 1 1
    2
    2
    2

    1 1 1
        2
        2
        2
    """

    horizontal_below_vertical = [
        (+ io.query_block ** (bricks.horizontal if not switcharoo else bricks.vertical)
        + io.query_block_reference ** (bricks.vertical if not switcharoo else bricks.horizontal)
        + io.query_relation ** (query_rel.below if not switcharoo else query_rel.left)
        + io.target_vertical ** bricks.horizontal
        + io.target_horizontal ** bricks.vertical
        + io.target_vertical_row1 ** numbers[f"n{row}"]
        + io.target_vertical_row2 ** numbers[f"n{row}"]
        + io.target_vertical_row3 ** numbers[f"n{row}"]
        + io.target_vertical_col1 ** numbers[f"n{col}"]
        + io.target_vertical_col2 ** numbers[f"n{col+1}"] 
        + io.target_vertical_col3 ** numbers[f"n{col+2}"]
        + io.target_horizontal_row1 ** numbers[f"n{row-3}"]
        + io.target_horizontal_row2 ** numbers[f"n{row-2}"]
        + io.target_horizontal_row3 ** numbers[f"n{row-1}"]
        + io.target_horizontal_col1 ** numbers[f"n{col+i}"]
        + io.target_horizontal_col2 ** numbers[f"n{col+i}"]
        + io.target_horizontal_col3 ** numbers[f"n{col+i}"]
        >>
        + io.output ** response.yes) for switcharoo in (True, False) for i in range(3) for row in range(4, 7) for col in range(1, 5)
    ]
    """
    2
    2
    2
    1 1 1

    2
    2
    2
    1 1 1

        2
        2
        2
    1 1 1
    """

    #no rule
    no_response_rule = [
        (+ io.query_block ** q_block
        + io.query_block_reference ** q_block_ref
        + io.query_relation ** rel
        >>
        + io.output ** response.no)

        for q_block in (bricks.half_T, bricks.mirror_L, bricks.horizontal, bricks.vertical)
          for q_block_ref in (bricks.half_T, bricks.mirror_L, bricks.horizontal, bricks.vertical)
            for rel in (query_rel.left, query_rel.right, query_rel.above, query_rel.below) if q_block != q_block_ref
        
    ]

    participant.response_rules.rules.compile(*(half_T_left_of_horizontal + half_T_left_vertical + half_T_left_mirror_L + 
                                      half_T_right_of_horizontal + half_T_right_vertical + half_T_right_mirror_L +
                                      half_T_below_horizontal + half_T_below_vertical + half_T_below_mirror_L +
                                      half_T_above_horizontal + half_T_above_vertical + half_T_above_mirror_L +
                                      mirror_L_left_horizontal + mirror_L_left_vertical +
                                      mirror_L_right_horizontal + mirror_L_right_vertical +
                                      mirror_L_below_horizontal + mirror_L_below_vertical +
                                      mirror_L_above_horizontal + mirror_L_above_vertical +
                                      horizontal_left_vertical +
                                      horizontal_right_vertical +
                                      horizontal_above_vertical +
                                      horizontal_below_vertical + no_response_rule))
    
def init_participant_construction_rules(participant) -> None:
    global SHAPES
    d = participant.construction_space
    io = d.io
    con_signal = d.signal_tokens
    numbers = d.numbers
    response = d.response

    io1 = io # TODO: cleanup

    #FIRST PLACEMENT RULES
    """
    1 1
    1
    """
    half_T_first_placement_rule = [
        (   
            + io.input_half_T ** response.yes
            + io.input_half_T_row1 ** numbers[f"n{row}"]
            + io.input_half_T_row2 ** numbers[f"n{row}"]
            + io.input_half_T_row3 ** numbers[f"n{row+1}"]
            + io.input_half_T_col1 ** numbers[f"n{col}"]
            + io.input_half_T_col2 ** numbers[f"n{col+1}"]
            + io.input_half_T_col3 ** numbers[f"n{col}"]

            + io.target_half_T ** response.no

            >>
            + io.target_half_T ** response.yes
            + io.target_half_T_row1 ** numbers[f"n{row}"]
            + io.target_half_T_row2 ** numbers[f"n{row}"]
            + io.target_half_T_row3 ** numbers[f"n{row+1}"]
            + io.target_half_T_col1 ** numbers[f"n{col}"]
            + io.target_half_T_col2 ** numbers[f"n{col+1}"]
            + io.target_half_T_col3 ** numbers[f"n{col}"]
         )
         for row in range(1, 6) for col in range(1, 6)
    ]

    mirror_L_first_placement_rule = [
        ( 
            + io.input_mirror_L ** response.yes
            + io.input_mirror_L_row1 ** numbers[f"n{row}"]
            + io.input_mirror_L_row2 ** numbers[f"n{row+1}"]
            + io.input_mirror_L_row3 ** numbers[f"n{row+1}"]
            + io.input_mirror_L_col1 ** numbers[f"n{col}"]
            + io.input_mirror_L_col2 ** numbers[f"n{col-1}"]
            + io.input_mirror_L_col3 ** numbers[f"n{col}"]

            + io.target_mirror_L ** response.no
            >>
            + io.target_mirror_L ** response.yes
            + io.target_mirror_L_row1 ** numbers[f"n{row}"]
            + io.target_mirror_L_row2 ** numbers[f"n{row+1}"]
            + io.target_mirror_L_row3 ** numbers[f"n{row+1}"]
            + io.target_mirror_L_col1 ** numbers[f"n{col}"]
            + io.target_mirror_L_col2 ** numbers[f"n{col-1}"]
            + io.target_mirror_L_col3 ** numbers[f"n{col}"]  
        )
        for row in range(1, 6) for col in range(2, 7)
    ]
    """
      1
    1 1
    """

    horizontal_first_placement_rule = [
        (       + io.input_horizontal ** response.yes
                + io.input_horizontal_row1 ** numbers[f"n{row}"]
                + io.input_horizontal_row2 ** numbers[f"n{row}"]
                + io.input_horizontal_row3 ** numbers[f"n{row}"]
                + io.input_horizontal_col1 ** numbers[f"n{col}"]
                + io.input_horizontal_col2 ** numbers[f"n{col+1}"]
                + io.input_horizontal_col3 ** numbers[f"n{col+2}"]

                + io.target_horizontal ** response.no
                >>
                + io.target_horizontal ** response.yes
                + io.target_horizontal_row1 ** numbers[f"n{row}"]
                + io.target_horizontal_row2 ** numbers[f"n{row}"]
                + io.target_horizontal_row3 ** numbers[f"n{row}"]
                + io.target_horizontal_col1 ** numbers[f"n{col}"]
                + io.target_horizontal_col2 ** numbers[f"n{col+1}"]
                + io.target_horizontal_col3 ** numbers[f"n{col+2}"]  
            )
        for row in range(1, 7) for col in range(1, 5)
    ]

    vertical_first_placement_rule = [
        (       + io.input_vertical ** response.yes
                + io.input_vertical_row1 ** numbers[f"n{row}"]
                + io.input_vertical_row2 ** numbers[f"n{row+1}"]
                + io.input_vertical_row3 ** numbers[f"n{row+2}"]
                + io.input_vertical_col1 ** numbers[f"n{col}"]
                + io.input_vertical_col2 ** numbers[f"n{col}"]
                + io.input_vertical_col3 ** numbers[f"n{col}"]

                + io.target_vertical ** response.no
                >>
                + io.target_vertical ** response.yes

                + io.target_vertical_row1 ** numbers[f"n{row}"]
                + io.target_vertical_row2 ** numbers[f"n{row+1}"]
                + io.target_vertical_row3 ** numbers[f"n{row+2}"]
                + io.target_vertical_col1 ** numbers[f"n{col}"]
                + io.target_vertical_col2 ** numbers[f"n{col}"]
                + io.target_vertical_col3 ** numbers[f"n{col}"]  
            )
        for row in range(1, 5) for col in range(1, 7)
    ]

    #SUBSEQUENCE PLACEMENT RULES
    half_T_left_of_horizontal_placement_rule = [
        (
            + io.input_half_T ** response.yes
            + io.input_horizontal ** response.yes
            
            + io[f"{'target' if switcharoo else 'input'}_half_T_row1"] ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_row2"] ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_row3"] ** numbers[f"n{row+1}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col1"] ** numbers[f"n{col}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col2"]** numbers[f"n{col+1}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col3"] ** numbers[f"n{col}"]

            + io[f"{'input' if switcharoo else 'target'}_horizontal_row1"] ** numbers[f"n{row+i}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_row2"] ** numbers[f"n{row+i}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_row3"] ** numbers[f"n{row+i}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_col1"] ** numbers[f"n{col+2-i}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_col2"] ** numbers[f"n{col+3-i}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_col3"] ** numbers[f"n{col+4-i}"]

            + io[f"target_{'half_T' if switcharoo else 'horizontal'}"] ** response.no # half_T isnt already there
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}"] ** response.yes # but horizontal is

            >>
            + io[f"target_{'half_T' if switcharoo else 'horizontal'}"] ** response.yes

            + io[f"target_{'half_T' if switcharoo else 'horizontal'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+i}"])
            + io[f"target_{'half_T' if switcharoo else 'horizontal'}_row2"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+i}"])
            + io[f"target_{'half_T' if switcharoo else 'horizontal'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+i}"])
            + io[f"target_{'half_T' if switcharoo else 'horizontal'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+2-i}"])
            + io[f"target_{'half_T' if switcharoo else 'horizontal'}_col2"] ** (numbers[f"n{col+1}"] if switcharoo else numbers[f"n{col+3-i}"])
            + io[f"target_{'half_T' if switcharoo else 'horizontal'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+4-i}"])

        )
        for switcharoo in (True, False) for i in range(2) for row in range(1, 6) for col in range(1, 3 + i)
    ]

    half_T_right_of_horizontal_placement_rule = [
        (
            + io.input_half_T ** response.yes
            + io.input_horizontal ** response.yes

            + io[f"{'target' if switcharoo else 'input'}_half_T_row1"]** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_row2"] ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_row3"] ** numbers[f"n{row+1}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col1"] ** numbers[f"n{col}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col2"] ** numbers[f"n{col+1}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col3"] ** numbers[f"n{col}"]
            
            + io[f"{'input' if switcharoo else 'target'}_horizontal_row1"] ** numbers[f"n{row+i}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_row2"] ** numbers[f"n{row+i}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_row3"] ** numbers[f"n{row+i}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_col1"] ** numbers[f"n{col-3}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_col2"] ** numbers[f"n{col-2}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_col3"] ** numbers[f"n{col-1}"]

            + io[f"target_{'half_T' if switcharoo else 'horizontal'}"] ** response.no # half_T isnt already there
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}"] ** response.yes # but horizontal is

            >>
            + io[f"target_{'half_T' if switcharoo else 'horizontal'}"] ** response.yes

            + io[f"target_{'half_T' if switcharoo else 'horizontal'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+i}"])
            + io[f"target_{'half_T' if switcharoo else 'horizontal'}_row2"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+i}"])
            + io[f"target_{'half_T' if switcharoo else 'horizontal'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+i}"])
            + io[f"target_{'half_T' if switcharoo else 'horizontal'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col-3}"])
            + io[f"target_{'half_T' if switcharoo else 'horizontal'}_col2"] ** (numbers[f"n{col+1}"] if switcharoo else numbers[f"n{col-2}"])
            + io[f"target_{'half_T' if switcharoo else 'horizontal'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col-1}"])
        )
        for switcharoo in (True, False) for i in range(2) for row in range(1, 6) for col in range(4, 6)
    ]

    half_T_below_horizontal_placement_rule = [
        (
            + io.input_half_T ** response.yes
            + io.input_horizontal ** response.yes

            + io[f"{'input' if switcharoo else 'target'}_half_T_row1"] ** numbers[f"n{row}"]
            + io[f"{'input' if switcharoo else 'target'}_half_T_row2"] ** numbers[f"n{row}"]
            + io[f"{'input' if switcharoo else 'target'}_half_T_row3"] ** numbers[f"n{row+1}"]
            + io[f"{'input' if switcharoo else 'target'}_half_T_col1"] ** numbers[f"n{col}"]
            + io[f"{'input' if switcharoo else 'target'}_half_T_col2"] ** numbers[f"n{col+1}"]
            + io[f"{'input' if switcharoo else 'target'}_half_T_col3"] ** numbers[f"n{col}"]

            + io[f"{'target' if switcharoo else 'input'}_horizontal_row1"] ** numbers[f"n{row-1}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_row2"] ** numbers[f"n{row-1}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_row3"] ** numbers[f"n{row-1}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_col1"] ** numbers[f"n{col-1+i}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_col2"] ** numbers[f"n{col+i}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_col3"] ** numbers[f"n{col+1+i}"]

            + io[f"target_{'half_T' if switcharoo else 'horizontal'}"] ** response.no # half_T isnt already there
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}"] ** response.yes # but horizontal is
            >>
            + io[f"target_{'half_T' if switcharoo else 'horizontal'}"] ** response.yes

            + io[f"target_{'half_T' if switcharoo else 'horizontal'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row-1}"])
            + io[f"target_{'half_T' if switcharoo else 'horizontal'}_row2"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row-1}"])
            + io[f"target_{'half_T' if switcharoo else 'horizontal'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row-1}"])
            + io[f"target_{'half_T' if switcharoo else 'horizontal'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col-1+i}"])
            + io[f"target_{'half_T' if switcharoo else 'horizontal'}_col2"] ** (numbers[f"n{col+1}"] if switcharoo else numbers[f"n{col+i}"])
            + io[f"target_{'half_T' if switcharoo else 'horizontal'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+1+i}"])
        ) 
        for switcharoo in (True, False) for i in range(3) for row in range(2, 6) for col in range(1 + (i == 0), 6-i)
    ]

    half_T_above_horizontal_placement_rule = [
        (
            + io.input_half_T ** response.yes
            + io.input_horizontal ** response.yes

            + io[f"{'input' if switcharoo else 'target'}_half_T_row1"] ** numbers[f"n{row}"]
            + io[f"{'input' if switcharoo else 'target'}_half_T_row2"] ** numbers[f"n{row}"]
            + io[f"{'input' if switcharoo else 'target'}_half_T_row3"] ** numbers[f"n{row+1}"]
            + io[f"{'input' if switcharoo else 'target'}_half_T_col1"] ** numbers[f"n{col}"]
            + io[f"{'input' if switcharoo else 'target'}_half_T_col2"] ** numbers[f"n{col+1}"]
            + io[f"{'input' if switcharoo else 'target'}_half_T_col3"] ** numbers[f"n{col}"]

            + io[f"{'target' if switcharoo else 'input'}_horizontal_row1"] ** numbers[f"n{row+2}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_row2"] ** numbers[f"n{row+2}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_row3"] ** numbers[f"n{row+2}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_col1"] ** numbers[f"n{col-2+i}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_col2"] ** numbers[f"n{col-1+i}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_col3"] ** numbers[f"n{col+i}"]

            + io[f"target_{'half_T' if switcharoo else 'horizontal'}"] ** response.no # half_T isnt already there
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}"] ** response.yes # but horizontal is

            >>
            + io[f"target_{'half_T' if switcharoo else 'horizontal'}"] ** response.yes

            + io[f"target_{'half_T' if switcharoo else 'horizontal'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+2}"])
            + io[f"target_{'half_T' if switcharoo else 'horizontal'}_row2"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+2}"])
            + io[f"target_{'half_T' if switcharoo else 'horizontal'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+2}"])
            + io[f"target_{'half_T' if switcharoo else 'horizontal'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col-2+i}"])
            + io[f"target_{'half_T' if switcharoo else 'horizontal'}_col2"] ** (numbers[f"n{col+1}"] if switcharoo else numbers[f"n{col-1+i}"])
            + io[f"target_{'half_T' if switcharoo else 'horizontal'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+i}"])
        ) 
        for switcharoo in (True, False) for i in range(3) for row in range(1, 5) for col in range(3-i, 6-(i==2))
]

    half_T_left_vertical_placement_rule = [
        (
            + io.input_half_T ** response.yes
            + io.input_vertical ** response.yes

            + io1[f"{'target' if switcharoo else 'input'}_half_T_row1"]** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_row2"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_row3"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col1"] ** numbers[f"n{col}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col2"] ** numbers[f"n{col+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col3"] ** numbers[f"n{col}"]

            + io1[f"{'input' if switcharoo else 'target'}_vertical_row1"] ** numbers[f"n{row+1-i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row2"] ** numbers[f"n{row+2-i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row3"] ** numbers[f"n{row+3-i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col1"] ** numbers[f"n{col+2- (i == 0)}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col2"] ** numbers[f"n{col+2- (i == 0)}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col3"] ** numbers[f"n{col+2- (i == 0)}"]

            + io1[f"target_{'half_T' if switcharoo else 'vertical'}"] ** response.no # half_T isnt already there
            + io1[f"target_{'vertical' if switcharoo else 'half_T'}"] ** response.yes # but vertical is
            >>
            + io[f"target_{'half_T' if switcharoo else 'vertical'}"] ** response.yes

            + io[f"target_{'half_T' if switcharoo else 'vertical'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+1-i}"])
            + io[f"target_{'half_T' if switcharoo else 'vertical'}_row2"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+2-i}"])
            + io[f"target_{'half_T' if switcharoo else 'vertical'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+3-i}"])
            + io[f"target_{'half_T' if switcharoo else 'vertical'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+2- (i == 0)}"])
            + io[f"target_{'half_T' if switcharoo else 'vertical'}_col2"] ** (numbers[f"n{col+1}"] if switcharoo else numbers[f"n{col+2- (i == 0)}"])
            + io[f"target_{'half_T' if switcharoo else 'vertical'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+2- (i == 0)}"])
            )
            for switcharoo in (True, False) for i in range(4) for row in range(1+(i-1 if i > 1 else 0), 4 + (math.ceil(i/2))) for col in range(1, 6-(i > 0))
    ]
    
    half_T_right_vertical_placement_rule = [
        (
            + io.input_half_T ** response.yes
            + io.input_vertical ** response.yes
            
            + io1[f"{'target' if switcharoo else 'input'}_half_T_row1"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_row2"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_row3"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col1"] ** numbers[f"n{col}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col2"] ** numbers[f"n{col+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col3"] ** numbers[f"n{col}"]

            + io1[f"{'input' if switcharoo else 'target'}_vertical_row1"] ** numbers[f"n{row-2+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row2"] ** numbers[f"n{row-1+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row3"] ** numbers[f"n{row+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col1"] ** numbers[f"n{col-1}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col2"] ** numbers[f"n{col-1}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col3"] ** numbers[f"n{col-1}"]

            + io1[f"target_{'half_T' if switcharoo else 'vertical'}"] ** response.no # half_T isnt already there
            + io1[f"target_{'vertical' if switcharoo else 'half_T'}"] ** response.yes # but vertical is

            >>
            + io[f"target_{'half_T' if switcharoo else 'vertical'}"] ** response.yes

            + io[f"target_{'half_T' if switcharoo else 'vertical'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row-2+i}"])
            + io[f"target_{'half_T' if switcharoo else 'vertical'}_row2"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row-1+i}"])
            + io[f"target_{'half_T' if switcharoo else 'vertical'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+i}"])
            + io[f"target_{'half_T' if switcharoo else 'vertical'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col-1}"])
            + io[f"target_{'half_T' if switcharoo else 'vertical'}_col2"] ** (numbers[f"n{col+1}"] if switcharoo else numbers[f"n{col-1}"])
            + io[f"target_{'half_T' if switcharoo else 'vertical'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col-1}"])
        ) 
        for switcharoo in (True, False) for i in range(4) for row in range(max(1, 3-i), 6-max(0, i-1)) for col in range(2, 6)
    ]
    
    half_T_below_vertical_placement_rule = [
        (
            + io.input_half_T ** response.yes
            + io.input_vertical ** response.yes
            
            + io1[f"{'target' if switcharoo else 'input'}_half_T_row1"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_row2"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_row3"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col1"] ** numbers[f"n{col}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col2"] ** numbers[f"n{col+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col3"] ** numbers[f"n{col}"]
            
            
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row1"] ** numbers[f"n{row-3}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row2"] ** numbers[f"n{row-2}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row3"] ** numbers[f"n{row-3}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col1"] ** numbers[f"n{col+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col2"] ** numbers[f"n{col+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col3"] ** numbers[f"n{col+i}"]

            + io1[f"target_{'half_T' if switcharoo else 'vertical'}"] ** response.no # half_T isnt already there
            + io1[f"target_{'vertical' if switcharoo else 'half_T'}"] ** response.yes # but vertical is

            >>
            + io[f"target_{'half_T' if switcharoo else 'vertical'}"] ** response.yes

            + io[f"target_{'half_T' if switcharoo else 'vertical'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row-3}"])
            + io[f"target_{'half_T' if switcharoo else 'vertical'}_row2"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row-2}"])
            + io[f"target_{'half_T' if switcharoo else 'vertical'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row-3}"])
            + io[f"target_{'half_T' if switcharoo else 'vertical'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+i}"])
            + io[f"target_{'half_T' if switcharoo else 'vertical'}_col2"] ** (numbers[f"n{col+1}"] if switcharoo else numbers[f"n{col+i}"])
            + io[f"target_{'half_T' if switcharoo else 'vertical'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+i}"])
            ) 
            for switcharoo in (True, False) for i in range(2) for row in range(4, 6) for col in range(1, 6)
    ]

    half_T_above_vertical_placement_rule = [
        (
            + io.input_half_T ** response.yes
            + io.input_vertical ** response.yes

            + io1[f"{'target' if switcharoo else 'input'}_half_T_row1"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_row2"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_row3"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col1"] ** numbers[f"n{col}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col2"] ** numbers[f"n{col+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col3"] ** numbers[f"n{col}"]

            + io1[f"{'input' if switcharoo else 'target'}_vertical_row1"] ** numbers[f"n{row+1}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row2"] ** numbers[f"n{row+2}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row3"] ** numbers[f"n{row+3}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col1"] ** numbers[f"n{col}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col2"] ** numbers[f"n{col}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col3"] ** numbers[f"n{col}"]

            + io1[f"target_{'half_T' if switcharoo else 'vertical'}"] ** response.no # half_T isnt already there
            + io1[f"target_{'vertical' if switcharoo else 'half_T'}"] ** response.yes # but vertical is
            >>
            + io[f"target_{'half_T' if switcharoo else 'vertical'}"] ** response.yes

            + io[f"target_{'half_T' if switcharoo else 'vertical'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+1}"])
            + io[f"target_{'half_T' if switcharoo else 'vertical'}_row2"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+2}"])
            + io[f"target_{'half_T' if switcharoo else 'vertical'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+3}"])
            + io[f"target_{'half_T' if switcharoo else 'vertical'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col}"])
            + io[f"target_{'half_T' if switcharoo else 'vertical'}_col2"] ** (numbers[f"n{col+1}"] if switcharoo else numbers[f"n{col}"])
            + io[f"target_{'half_T' if switcharoo else 'vertical'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col}"])
            ) 
            for switcharoo in (True, False) for row in range(1, 3) for col in range(1, 6)
    ]

    half_T_left_mirror_L_placement_rule = [
        (
            + io.input_half_T ** response.yes
            + io.input_mirror_L ** response.yes

            + io1[f"{'target' if switcharoo else 'input'}_half_T_row1"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_row2"]** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_row3"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col1"] ** numbers[f"n{col}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col2"] ** numbers[f"n{col+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col3"] ** numbers[f"n{col}"]

            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_row1"] ** numbers[f"n{row-i}"]
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_row2"] ** numbers[f"n{row+1-i}"]
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_row3"] ** numbers[f"n{row+1-i}"]
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_col1"] ** numbers[f"n{col+2+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_col2"] ** numbers[f"n{col+1+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_col3"] ** numbers[f"n{col+2+i}"]

            + io1[f"target_{'half_T' if switcharoo else 'mirror_L'}"] ** response.no # half_T isnt already there
            + io1[f"target_{'mirror_L' if switcharoo else 'half_T'}"] ** response.yes # but mirror_L is
            >>
            + io[f"target_{'half_T' if switcharoo else 'mirror_L'}"] ** response.yes

            + io[f"target_{'half_T' if switcharoo else 'mirror_L'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row-i}"])
            + io[f"target_{'half_T' if switcharoo else 'mirror_L'}_row2"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+1-i}"])
            + io[f"target_{'half_T' if switcharoo else 'mirror_L'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+1-i}"])
            + io[f"target_{'half_T' if switcharoo else 'mirror_L'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+2+i}"])
            + io[f"target_{'half_T' if switcharoo else 'mirror_L'}_col2"] ** (numbers[f"n{col+1}"] if switcharoo else numbers[f"n{col+1+i}"])
            + io[f"target_{'half_T' if switcharoo else 'mirror_L'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+2+i}"])
        )
        for switcharoo in (True, False) for i in range(2) for row in range(1+i, 6) for col in range(1, 5-i)
    ]
    
    half_T_right_mirror_L_placement_rule = [
        (
            + io.input_half_T ** response.yes
            + io.input_mirror_L ** response.yes

            + io1[f"{'target' if switcharoo else 'input'}_half_T_row1"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_row2"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_row3"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col1"] ** numbers[f"n{col}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col2"] ** numbers[f"n{col+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col3"] ** numbers[f"n{col}"]

            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_row1"] ** numbers[f"n{row + (-1 if i== 0 else 1)*(i%2 == 0)}"] # 1 up, no up, 1 down.
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_row2"] ** numbers[f"n{row + i}"]
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_row3"] ** numbers[f"n{row+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_col1"] ** numbers[f"n{col-1}"]
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_col2"] ** numbers[f"n{col-2}"]
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_col3"] ** numbers[f"n{col-1}"]

            + io1[f"target_{'half_T' if switcharoo else 'mirror_L'}"] ** response.no # half_T isnt already there
            + io1[f"target_{'mirror_L' if switcharoo else 'half_T'}"] ** response.yes # but mirror_L is

            >>
            + io[f"target_{'half_T' if switcharoo else 'mirror_L'}"] ** response.yes

            + io[f"target_{'half_T' if switcharoo else 'mirror_L'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row + (-1 if i== 0 else 1)*(i%2 == 0)}"])
            + io[f"target_{'half_T' if switcharoo else 'mirror_L'}_row2"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row + i}"])
            + io[f"target_{'half_T' if switcharoo else 'mirror_L'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+i}"])
            + io[f"target_{'half_T' if switcharoo else 'mirror_L'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col-1}"])
            + io[f"target_{'half_T' if switcharoo else 'mirror_L'}_col2"] ** (numbers[f"n{col+1}"] if switcharoo else numbers[f"n{col-2}"])
            + io[f"target_{'half_T' if switcharoo else 'mirror_L'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col-1}"])
        ) 
        for switcharoo in (True, False) for i in range(3) for row in range(1+(i==0), 6-(i==2)) for col in range(3, 6)
    ]
    
    half_T_below_mirror_L_placement_rule = [
        (
            + io.input_half_T ** response.yes
            + io.input_mirror_L ** response.yes

            + io1[f"{'target' if switcharoo else 'input'}_half_T_row1"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_row2"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_row3"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col1"] ** numbers[f"n{col}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col2"] ** numbers[f"n{col+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col3"] ** numbers[f"n{col}"]
            
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_row1"] ** numbers[f"n{row-2}"]
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_row2"] ** numbers[f"n{row-1}"]
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_row3"] ** numbers[f"n{row-1}"]
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_col1"] ** numbers[f"n{col+1+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_col2"] ** numbers[f"n{col+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_col3"] ** numbers[f"n{col+1+i}"]

            + io1[f"target_{'half_T' if switcharoo else 'mirror_L'}"] ** response.no # half_T isnt already there
            + io1[f"target_{'mirror_L' if switcharoo else 'half_T'}"] ** response.yes # but mirror_L is
            >>
            + io[f"target_{'half_T' if switcharoo else 'mirror_L'}"] ** response.yes

            + io[f"target_{'half_T' if switcharoo else 'mirror_L'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row-2}"])
            + io[f"target_{'half_T' if switcharoo else 'mirror_L'}_row2"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row-1}"])
            + io[f"target_{'half_T' if switcharoo else 'mirror_L'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row-1}"])
            + io[f"target_{'half_T' if switcharoo else 'mirror_L'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+1+i}"])
            + io[f"target_{'half_T' if switcharoo else 'mirror_L'}_col2"] ** (numbers[f"n{col+1}"] if switcharoo else numbers[f"n{col+i}"])
            + io[f"target_{'half_T' if switcharoo else 'mirror_L'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+1+i}"])
        )
        for switcharoo in (True, False) for i in range(2) for row in range(3, 6) for col in range(1, 6-i)
    ]

    half_T_above_mirror_L_placement_rule = [
        (
            + io.input_half_T ** response.yes
            + io.input_mirror_L ** response.yes

             + io1[f"{'target' if switcharoo else 'input'}_half_T_row1"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_row2"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_row3"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col1"] ** numbers[f"n{col}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col2"] ** numbers[f"n{col+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col3"] ** numbers[f"n{col}"]
             
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_row1"] ** numbers[f"n{row+2}"]
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_row2"] ** numbers[f"n{row+3}"]
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_row3"] ** numbers[f"n{row+3}"]
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_col1"] ** numbers[f"n{col}"]
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_col2"] ** numbers[f"n{col-1}"]
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_col3"] ** numbers[f"n{col}"]

            + io1[f"target_{'half_T' if switcharoo else 'mirror_L'}"] ** response.no # half_T isnt already there
            + io1[f"target_{'mirror_L' if switcharoo else 'half_T'}"] ** response.yes # but mirror_L is
            >>
            + io[f"target_{'half_T' if switcharoo else 'mirror_L'}"] ** response.yes

            + io[f"target_{'half_T' if switcharoo else 'mirror_L'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+2}"])
            + io[f"target_{'half_T' if switcharoo else 'mirror_L'}_row2"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+3}"])
            + io[f"target_{'half_T' if switcharoo else 'mirror_L'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+3}"])
            + io[f"target_{'half_T' if switcharoo else 'mirror_L'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col}"])
            + io[f"target_{'half_T' if switcharoo else 'mirror_L'}_col2"] ** (numbers[f"n{col+1}"] if switcharoo else numbers[f"n{col-1}"])
            + io[f"target_{'half_T' if switcharoo else 'mirror_L'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col}"])
        ) 
        for switcharoo in (True, False) for row in range(1, 4) for col in range(2, 6)
    ]

    mirror_L_left_horizontal_placement_rule  = [
        (
            + io.input_mirror_L ** response.yes
            + io.input_horizontal ** response.yes

            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row1"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row2"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row3"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col1"] ** numbers[f"n{col}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col2"] ** numbers[f"n{col-1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col3"] ** numbers[f"n{col}"]
            
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_row1"] ** numbers[f"n{row+i}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_row2"] ** numbers[f"n{row+i}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_row3"]** numbers[f"n{row+i}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_col1"] ** numbers[f"n{col+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_col2"] ** numbers[f"n{col+2}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_col3"] ** numbers[f"n{col+3}"]

            + io1[f"target_{'mirror_L' if switcharoo else 'horizontal'}"] ** response.no # mirror_L isnt already there
            + io1[f"target_{'horizontal' if switcharoo else 'mirror_L'}"] ** response.yes # but horizontal is

            >>
            + io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"] ** response.yes

            + io[f"target_{'mirror_L' if switcharoo else 'horizontal'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+i}"])
            + io[f"target_{'mirror_L' if switcharoo else 'horizontal'}_row2"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+i}"])
            + io[f"target_{'mirror_L' if switcharoo else 'horizontal'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+i}"])
            + io[f"target_{'mirror_L' if switcharoo else 'horizontal'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+1}"])
            + io[f"target_{'mirror_L' if switcharoo else 'horizontal'}_col2"] ** (numbers[f"n{col-1}"] if switcharoo else numbers[f"n{col+2}"])
            + io[f"target_{'mirror_L' if switcharoo else 'horizontal'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+3}"])
            ) 
            for switcharoo in (True, False) for i in range(2) for row in range(1, 6) for col in range(2, 4)
    ]

    mirror_L_right_horizontal_placement_rule = [
        (
            + io.input_mirror_L ** response.yes
            + io.input_horizontal ** response.yes

            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row1"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row2"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row3"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col1"] ** numbers[f"n{col}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col2"] ** numbers[f"n{col-1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col3"] ** numbers[f"n{col}"]
            
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_row1"] ** numbers[f"n{row+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_row2"] ** numbers[f"n{row+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_row3"] ** numbers[f"n{row+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_col1"] ** numbers[f"n{col-3-i}"]
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_col2"] ** numbers[f"n{col-2-i}"]
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_col3"] ** numbers[f"n{col-1-i}"]

            + io1[f"target_{'mirror_L' if switcharoo else 'horizontal'}"] ** response.no # mirror_L isnt already there
            + io1[f"target_{'horizontal' if switcharoo else 'mirror_L'}"] ** response.yes # but horizontal is
            >>
            + io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"] ** response.yes

            + io[f"target_{'mirror_L' if switcharoo else 'horizontal'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+i}"])
            + io[f"target_{'mirror_L' if switcharoo else 'horizontal'}_row2"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+i}"])
            + io[f"target_{'mirror_L' if switcharoo else 'horizontal'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+i}"])
            + io[f"target_{'mirror_L' if switcharoo else 'horizontal'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col-3-i}"])
            + io[f"target_{'mirror_L' if switcharoo else 'horizontal'}_col2"] ** (numbers[f"n{col-1}"] if switcharoo else numbers[f"n{col-2-i}"])
            + io[f"target_{'mirror_L' if switcharoo else 'horizontal'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col-1-i}"])
        ) 
        for switcharoo in (True, False) for i in range(2) for row in range(1, 6) for col in range(4+i, 7)
    ]

    mirror_L_above_horizontal_placement_rule = [
        (
            + io.input_mirror_L ** response.yes
            + io.input_horizontal ** response.yes

            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row1"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row2"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row3"]** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col1"] ** numbers[f"n{col}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col2"] ** numbers[f"n{col-1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col3"] ** numbers[f"n{col}"]
            
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_row1"] ** numbers[f"n{row+2}"]
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_row2"] ** numbers[f"n{row+2}"]
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_row3"] ** numbers[f"n{row+2}"]
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_col1"] ** numbers[f"n{col-2+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_col2"] ** numbers[f"n{col-1+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_col3"] ** numbers[f"n{col+i}"]

            + io1[f"target_{'mirror_L' if switcharoo else 'horizontal'}"] ** response.no # mirror_L isnt already there
            + io1[f"target_{'horizontal' if switcharoo else 'mirror_L'}"] ** response.yes # but horizontal is

            >>
            + io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"] ** response.yes

            + io[f"target_{'mirror_L' if switcharoo else 'horizontal'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+2}"])
            + io[f"target_{'mirror_L' if switcharoo else 'horizontal'}_row2"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+2}"])
            + io[f"target_{'mirror_L' if switcharoo else 'horizontal'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+2}"])
            + io[f"target_{'mirror_L' if switcharoo else 'horizontal'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col-2+i}"])
            + io[f"target_{'mirror_L' if switcharoo else 'horizontal'}_col2"] ** (numbers[f"n{col-1}"] if switcharoo else numbers[f"n{col-1+i}"])
            + io[f"target_{'mirror_L' if switcharoo else 'horizontal'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+i}"])
            )
            for switcharoo in (True, False) for i in range(3) for row in range(1, 5) for col in range(2 + (i == 0), 7-i)
    ]

    mirror_L_below_horizontal_placement_rule = [
        (
            + io.input_mirror_L ** response.yes
            + io.input_horizontal ** response.yes

            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row1"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row2"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row3"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col1"] ** numbers[f"n{col}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col2"] ** numbers[f"n{col-1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col3"] ** numbers[f"n{col}"]

            + io1[f"{'input' if switcharoo else 'target'}_horizontal_row1"] ** numbers[f"n{row-1}"]
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_row2"] ** numbers[f"n{row-1}"]
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_row3"] ** numbers[f"n{row-1}"]
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_col1"] ** numbers[f"n{col-2+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_col2"] ** numbers[f"n{col-1+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_col3"] ** numbers[f"n{col+i}"]

            + io1[f"target_{'mirror_L' if switcharoo else 'horizontal'}"] ** response.no # mirror_L isnt already there
            + io1[f"target_{'horizontal' if switcharoo else 'mirror_L'}"] ** response.yes # but horizontal is
            >>
            + io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"] ** response.yes

            + io[f"target_{'mirror_L' if switcharoo else 'horizontal'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row-1}"])
            + io[f"target_{'mirror_L' if switcharoo else 'horizontal'}_row2"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row-1}"])
            + io[f"target_{'mirror_L' if switcharoo else 'horizontal'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row-1}"])
            + io[f"target_{'mirror_L' if switcharoo else 'horizontal'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col-2+i}"])
            + io[f"target_{'mirror_L' if switcharoo else 'horizontal'}_col2"] ** (numbers[f"n{col-1}"] if switcharoo else numbers[f"n{col-1+i}"])
            + io[f"target_{'mirror_L' if switcharoo else 'horizontal'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+i}"])
            ) 
            for switcharoo in (True, False) for i in range (3) for row in range(2, 6) for col in range(3-(i!=0), 7-i)
    ]

    mirror_L_left_vertical_placement_rule  = [
        (
            + io.input_mirror_L ** response.yes
            + io.input_vertical ** response.yes

            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row1"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row2"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row3"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col1"] ** numbers[f"n{col}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col2"] ** numbers[f"n{col-1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col3"] ** numbers[f"n{col}"]
            
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row1"] ** numbers[f"n{row-1+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row2"] ** numbers[f"n{row+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row3"] ** numbers[f"n{row+1+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col1"] ** numbers[f"n{col+1}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col2"] ** numbers[f"n{col+1}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col3"] ** numbers[f"n{col+1}"]

            + io1[f"target_{'mirror_L' if switcharoo else 'vertical'}"] ** response.no # mirror_L isnt already there
            + io1[f"target_{'vertical' if switcharoo else 'mirror_L'}"] ** response.yes # but vertical is
            >>
            + io[f"target_{'mirror_L' if switcharoo else 'vertical'}"] ** response.yes

            + io[f"target_{'mirror_L' if switcharoo else 'vertical'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row-1+i}"])
            + io[f"target_{'mirror_L' if switcharoo else 'vertical'}_row2"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+i}"])
            + io[f"target_{'mirror_L' if switcharoo else 'vertical'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+1+i}"])
            + io[f"target_{'mirror_L' if switcharoo else 'vertical'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+1}"])
            + io[f"target_{'mirror_L' if switcharoo else 'vertical'}_col2"] ** (numbers[f"n{col-1}"] if switcharoo else numbers[f"n{col+1}"])
            + io[f"target_{'mirror_L' if switcharoo else 'vertical'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+1}"])
            ) 
            for switcharoo in (True, False) for i in range(3) for row in range(1+(i==0), 6-i) for col in range(2, 6)
    ]

    mirror_L_right_vertical_placement_rule = [
        (
            + io.input_mirror_L ** response.yes
            + io.input_vertical ** response.yes

            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row1"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row2"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row3"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col1"] ** numbers[f"n{col}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col2"] ** numbers[f"n{col-1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col3"] ** numbers[f"n{col}"]
            
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row1"] ** numbers[f"n{row+1-i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row2"] ** numbers[f"n{row+2-i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row3"] ** numbers[f"n{row+3-i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col1"] ** numbers[f"n{col-2 + (i == 3)}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col2"] ** numbers[f"n{col-2 + (i == 3)}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col3"] ** numbers[f"n{col-2 + (i == 3)}"]

            + io1[f"target_{'mirror_L' if switcharoo else 'vertical'}"] ** response.no # mirror_L isnt already there
            + io1[f"target_{'vertical' if switcharoo else 'mirror_L'}"] ** response.yes # but vertical is
            >>
            + io[f"target_{'mirror_L' if switcharoo else 'vertical'}"] ** response.yes

            + io[f"target_{'mirror_L' if switcharoo else 'vertical'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+1-i}"])
            + io[f"target_{'mirror_L' if switcharoo else 'vertical'}_row2"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+2-i}"])
            + io[f"target_{'mirror_L' if switcharoo else 'vertical'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+3-i}"])
            + io[f"target_{'mirror_L' if switcharoo else 'vertical'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col-2 + (i == 3)}"])
            + io[f"target_{'mirror_L' if switcharoo else 'vertical'}_col2"] ** (numbers[f"n{col-1}"] if switcharoo else numbers[f"n{col-2 + (i == 3)}"])
            + io[f"target_{'mirror_L' if switcharoo else 'vertical'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col-2 + (i == 3)}"])
            )
            for switcharoo in (True, False) for i in range(4) for row in range(1+max(0, i-1), min(4+i, 6)) for col in range(3 - (i == 3), 7)
    ]

    mirror_L_above_vertical_placement_rule = [
        (
            + io.input_mirror_L ** response.yes
            + io.input_vertical ** response.yes

            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row1"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row2"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row3"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col1"] ** numbers[f"n{col}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col2"] ** numbers[f"n{col-1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col3"] ** numbers[f"n{col}"]
            
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row1"]** numbers[f"n{row+2}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row2"] ** numbers[f"n{row+3}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row3"] ** numbers[f"n{row+4}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col1"] ** numbers[f"n{col-1+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col2"] ** numbers[f"n{col-1+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col3"] ** numbers[f"n{col-1+i}"]

            + io1[f"target_{'mirror_L' if switcharoo else 'vertical'}"] ** response.no # mirror_L isnt already there
            + io1[f"target_{'vertical' if switcharoo else 'mirror_L'}"] ** response.yes # but vertical is
            >>
            + io[f"target_{'mirror_L' if switcharoo else 'vertical'}"] ** response.yes

            + io[f"target_{'mirror_L' if switcharoo else 'vertical'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+2}"])
            + io[f"target_{'mirror_L' if switcharoo else 'vertical'}_row2"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+3}"])
            + io[f"target_{'mirror_L' if switcharoo else 'vertical'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+4}"])
            + io[f"target_{'mirror_L' if switcharoo else 'vertical'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col-1+i}"])
            + io[f"target_{'mirror_L' if switcharoo else 'vertical'}_col2"] ** (numbers[f"n{col-1}"] if switcharoo else numbers[f"n{col-1+i}"])
            + io[f"target_{'mirror_L' if switcharoo else 'vertical'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col-1+i}"])
        )
        for switcharoo in (True, False) for i in range(2) for row in range(1, 3) for col in range(2, 7)
    ]

    mirror_L_below_vertical_placement_rule = [
        (
            + io.input_mirror_L ** response.yes
            + io.input_vertical ** response.yes

           + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row1"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row2"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row3"]** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col1"] ** numbers[f"n{col}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col2"] ** numbers[f"n{col-1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col3"] ** numbers[f"n{col}"]
            
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row1"] ** numbers[f"n{row-3}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row2"] ** numbers[f"n{row-2}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row3"] ** numbers[f"n{row-1}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col1"] ** numbers[f"n{col}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col2"] ** numbers[f"n{col}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col3"] ** numbers[f"n{col}"]

            + io1[f"target_{'mirror_L' if switcharoo else 'vertical'}"] ** response.no # mirror_L isnt already there
            + io1[f"target_{'vertical' if switcharoo else 'mirror_L'}"] ** response.yes # but vertical is
            >>
            + io[f"target_{'mirror_L' if switcharoo else 'vertical'}"] ** response.yes

            + io[f"target_{'mirror_L' if switcharoo else 'vertical'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row-3}"])
            + io[f"target_{'mirror_L' if switcharoo else 'vertical'}_row2"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row-2}"])
            + io[f"target_{'mirror_L' if switcharoo else 'vertical'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row-1}"])
            + io[f"target_{'mirror_L' if switcharoo else 'vertical'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col}"])
            + io[f"target_{'mirror_L' if switcharoo else 'vertical'}_col2"] ** (numbers[f"n{col-1}"] if switcharoo else numbers[f"n{col}"])
            + io[f"target_{'mirror_L' if switcharoo else 'vertical'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col}"])
            )
            for switcharoo in (True, False) for row in range(4, 6) for col in range(2, 7)
    ]

    horizontal_left_vertical_placement_rule  = [
        (
            + io.input_vertical ** response.yes
            + io.input_horizontal ** response.yes
            
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_row1"] ** numbers[f"n{row}"]
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_row2"]** numbers[f"n{row}"]
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_row3"] ** numbers[f"n{row}"]
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_col1"] ** numbers[f"n{col}"]
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_col2"] ** numbers[f"n{col+1}"] 
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_col3"] ** numbers[f"n{col+2}"]
            
            
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row1"] ** numbers[f"n{row-2+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row2"] ** numbers[f"n{row-1+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row3"] ** numbers[f"n{row+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col1"] ** numbers[f"n{col+3}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col2"] ** numbers[f"n{col+3}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col3"] ** numbers[f"n{col+3}"]

            + io1[f"target_{'horizontal' if switcharoo else 'vertical'}"] ** response.no # horizontal isnt already there
            + io1[f"target_{'vertical' if switcharoo else 'horizontal'}"] ** response.yes # but vertical is
            >>
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}"] ** response.yes
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row-2+i}"])
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}_row2"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row-1+i}"])
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}_row3"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+i}"])
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+3}"])
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}_col2"] ** (numbers[f"n{col+1}"] if switcharoo else numbers[f"n{col+3}"])
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}_col3"] ** (numbers[f"n{col+2}"] if switcharoo else numbers[f"n{col+3}"])
            ) 
            for switcharoo in (True, False) for i in range(3) for row in range(3-i, 7-i) for col in range(1, 4)
    ]

    horizontal_right_vertical_placement_rule = [
        (
            + io.input_vertical ** response.yes
            + io.input_horizontal ** response.yes

            + io1[f"{'target' if switcharoo else 'input'}_horizontal_row1"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_row2"]** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_row3"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_col1"] ** numbers[f"n{col}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_col2"] ** numbers[f"n{col+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_col3"] ** numbers[f"n{col+2}"]
            
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row1"] ** numbers[f"n{row-2+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row2"] ** numbers[f"n{row-1+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row3"] ** numbers[f"n{row+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col1"] ** numbers[f"n{col-1}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col2"] ** numbers[f"n{col-1}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col3"] ** numbers[f"n{col-1}"]

            + io1[f"target_{'horizontal' if switcharoo else 'vertical'}"] ** response.no # horizontal isnt already there
            + io1[f"target_{'vertical' if switcharoo else 'horizontal'}"] ** response.yes # but vertical is
            >>
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}"] ** response.yes

            + io[f"target_{'horizontal' if switcharoo else 'vertical'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row-2+i}"])
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}_row2"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row-1+i}"])
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}_row3"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+i}"])
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col-1}"])
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}_col2"] ** (numbers[f"n{col+1}"] if switcharoo else numbers[f"n{col-1}"])
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}_col3"] ** (numbers[f"n{col+2}"] if switcharoo else numbers[f"n{col-1}"])
            ) 
            for switcharoo in (True, False) for i in range(3) for row in range(3-i, 7-i) for col in range(2, 5)
    ]

    horizontal_above_vertical_placement_rule = [
        (
            + io.input_vertical ** response.yes
            + io.input_horizontal ** response.yes

            + io1[f"{'target' if switcharoo else 'input'}_horizontal_row1"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_row2"]** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_row3"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_col1"] ** numbers[f"n{col}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_col2"] ** numbers[f"n{col+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_col3"] ** numbers[f"n{col+2}"]

            + io1[f"{'input' if switcharoo else 'target'}_vertical_row1"] ** numbers[f"n{row+1}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row2"] ** numbers[f"n{row+2}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row3"] ** numbers[f"n{row+3}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col1"] ** numbers[f"n{col+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col2"] ** numbers[f"n{col+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col3"] ** numbers[f"n{col+i}"]

            + io1[f"target_{'horizontal' if switcharoo else 'vertical'}"] ** response.no # horizontal isnt already there
            + io1[f"target_{'vertical' if switcharoo else 'horizontal'}"] ** response.yes # but vertical is
            >>
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}"] ** response.yes

            + io[f"target_{'horizontal' if switcharoo else 'vertical'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+1}"])
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}_row2"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+2}"])
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}_row3"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+3}"])
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+i}"])
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}_col2"] ** (numbers[f"n{col+1}"] if switcharoo else numbers[f"n{col+i}"])
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}_col3"] ** (numbers[f"n{col+2}"] if switcharoo else numbers[f"n{col+i}"])
        ) 
        for switcharoo in (True, False) for i in range(3) for row in range(1, 4) for col in range(1, 5)
    ]

    horizontal_below_vertical_placement_rule = [
        (
            + io.input_vertical ** response.yes
            + io.input_horizontal ** response.yes

            + io1[f"{'target' if switcharoo else 'input'}_horizontal_row1"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_row2"]** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_row3"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_col1"] ** numbers[f"n{col}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_col2"] ** numbers[f"n{col+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_col3"] ** numbers[f"n{col+2}"]

            + io1[f"{'input' if switcharoo else 'target'}_vertical_row1"] ** numbers[f"n{row-3}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row2"] ** numbers[f"n{row-2}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row3"] ** numbers[f"n{row-1}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col1"] ** numbers[f"n{col+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col2"] ** numbers[f"n{col+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col3"] ** numbers[f"n{col+i}"]

            + io1[f"target_{'horizontal' if switcharoo else 'vertical'}"] ** response.no # horizontal isnt already there
            + io1[f"target_{'vertical' if switcharoo else 'horizontal'}"] ** response.yes # but vertical is
            >>
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}"] ** response.yes

            + io[f"target_{'horizontal' if switcharoo else 'vertical'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row-3}"])
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}_row2"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row-2}"])
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}_row3"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row-1}"])
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+i}"])
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}_col2"] ** (numbers[f"n{col+1}"] if switcharoo else numbers[f"n{col+i}"])
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}_col3"] ** (numbers[f"n{col+2}"] if switcharoo else numbers[f"n{col+i}"])
            )
            for switcharoo in (True, False) for i in range(3) for row in range(4, 7) for col in range(1, 5)
    ]

    # END_CONSTRUCTION RULE
    # if all four blocks have been used, then stop construction
    #TODO: is it possible for a dimension to not be bound with anything? that is the empty state yes? -- 0.0 activation value yea?
    stop_construction_rule_all_four = [(
        + io.target_half_T ** response.yes
        + io.target_mirror_L ** response.yes
        + io.target_vertical ** response.yes
        + io.target_horizontal ** response.yes
        >>
        + io.construction_signal ** con_signal.stop_construction)
    ]

    stop_construction_input_blocks_used_one = [(

         + io1[f"input_{shape}"] ** response.yes
            + io1[f"input_{(SHAPES[:i] + SHAPES[i+1:])[0]}"] ** response.no
            + io1[f"input_{(SHAPES[:i] + SHAPES[i+1:])[1]}"] ** response.no
            + io1[f"input_{(SHAPES[:i] + SHAPES[i+1:])[2]}"] ** response.no

            + io1[f"target_{shape}"] ** response.yes
            + io1[f"target_{(SHAPES[:i] + SHAPES[i+1:])[0]}"] ** response.no
            + io1[f"target_{(SHAPES[:i] + SHAPES[i+1:])[1]}"] ** response.no
            + io1[f"target_{(SHAPES[:i] + SHAPES[i+1:])[2]}"] ** response.no

            >>
            + io.construction_signal ** con_signal.stop_construction
        )
        for i, shape in enumerate(SHAPES)
    ]

    stop_construction_input_blocks_used_two = [
        (
            + io1[f"input_{shape}"] ** response.yes
            + io1[f"input_{other_shape}"] ** response.yes
            + io1[f"input_{[s for s in SHAPES if s not in (shape, other_shape)][0]}"] ** response.no
            + io1[f"input_{[s for s in SHAPES if s not in (shape, other_shape)][1]}"] ** response.no

            + io1[f"target_{shape}"] ** response.yes
            + io1[f"target_{other_shape}"] ** response.yes
            + io1[f"target_{[s for s in SHAPES if s not in (shape, other_shape)][0]}"] ** response.no
            + io1[f"target_{[s for s in SHAPES if s not in (shape, other_shape)][1]}"] ** response.no
            >>
            io.construction_signal ** con_signal.stop_construction
        )
        for (shape, other_shape) in itertools.combinations(SHAPES, 2)
    ]

    stop_construction_input_blocks_used_three = [
        (
            + io1[f"input_{shape}"] ** response.yes
            + io1[f"input_{other_shape}"] ** response.yes
            + io1[f"input_{other_other_shape}"] ** response.yes
            + io1[f"input_{[s for s in SHAPES if s not in (shape, other_shape, other_other_shape)][0]}"] ** response.no

            + io1[f"target_{shape}"] ** response.yes
            + io1[f"target_{other_shape}"] ** response.yes
            + io1[f"target_{other_other_shape}"] ** response.yes
            + io1[f"target_{[s for s in SHAPES if s not in (shape, other_shape, other_other_shape)][0]}"] ** response.no

            >>
            io.construction_signal ** con_signal.stop_construction
        )
        for (shape, other_shape, other_other_shape) in itertools.combinations(SHAPES, 3)
    ]
    
    participant.search_space_rules.rules.compile(
        *(
            stop_construction_rule_all_four + stop_construction_input_blocks_used_one + stop_construction_input_blocks_used_two + stop_construction_input_blocks_used_three
            + half_T_first_placement_rule + mirror_L_first_placement_rule + horizontal_first_placement_rule + vertical_first_placement_rule
            + half_T_left_of_horizontal_placement_rule + half_T_right_of_horizontal_placement_rule + half_T_above_horizontal_placement_rule + half_T_below_horizontal_placement_rule
            + half_T_left_vertical_placement_rule + half_T_right_vertical_placement_rule + half_T_above_vertical_placement_rule + half_T_below_vertical_placement_rule
            + half_T_left_mirror_L_placement_rule + half_T_right_mirror_L_placement_rule + half_T_above_mirror_L_placement_rule + half_T_below_mirror_L_placement_rule
            + mirror_L_left_horizontal_placement_rule + mirror_L_right_horizontal_placement_rule + mirror_L_above_horizontal_placement_rule + mirror_L_below_horizontal_placement_rule
            + mirror_L_left_vertical_placement_rule + mirror_L_right_vertical_placement_rule + mirror_L_above_vertical_placement_rule + mirror_L_below_vertical_placement_rule
            + horizontal_left_vertical_placement_rule + horizontal_right_vertical_placement_rule + horizontal_above_vertical_placement_rule + horizontal_below_vertical_placement_rule 
        )
    )

    # BIG_LIST = (
    #         stop_construction_rule_all_four + stop_construction_input_blocks_used_one + stop_construction_input_blocks_used_two + stop_construction_input_blocks_used_three
    #         + half_T_first_placement_rule + mirror_L_first_placement_rule + horizontal_first_placement_rule + vertical_first_placement_rule
    #         + half_T_left_of_horizontal_placement_rule + half_T_right_of_horizontal_placement_rule + half_T_above_horizontal_placement_rule + half_T_below_horizontal_placement_rule
    #         + half_T_left_vertical_placement_rule + half_T_right_vertical_placement_rule + half_T_above_vertical_placement_rule + half_T_below_vertical_placement_rule
    #         + half_T_left_mirror_L_placement_rule + half_T_right_mirror_L_placement_rule + half_T_above_mirror_L_placement_rule + half_T_below_mirror_L_placement_rule
    #         + mirror_L_left_horizontal_placement_rule + mirror_L_right_horizontal_placement_rule + mirror_L_above_horizontal_placement_rule + mirror_L_below_horizontal_placement_rule
    #         + mirror_L_left_vertical_placement_rule + mirror_L_right_vertical_placement_rule + mirror_L_above_vertical_placement_rule + mirror_L_below_vertical_placement_rule
    #         + horizontal_left_vertical_placement_rule + horizontal_right_vertical_placement_rule + horizontal_above_vertical_placement_rule + horizontal_below_vertical_placement_rule 
    #     )
    
    # [for i, c in enumerate(BIG_LIST)]

    # temporary: to evaluate the functioning of response rules
    # dummy_stop_construction_rule = [(
    #     #TODO: empty condition?
    #     + io[f"input_shape{shape_no}"] ** bricks[brick_name]
    #     >>
    #     io.construction_signal ** con_signal.stop_construction 
    # )
    #  for (shape_no, brick_name) in zip(range(1, 5), ["half_T", "mirror_L", "vertical", "horizontal"])
    # ]

    # participant.search_space_rules.rules.compile(
    #     *dummy_stop_construction_rule
    # )

def init_participant_construction_rule_w_abstract(participant):
    global SHAPES
    d = participant.construction_space
    io = d.io
    numbers = d.numbers
    response = d.response

    io1 = io

    #FIRST PLACEMENT RULES
    """
    1 1
    1
    """
    half_T_first_placement_rule_wabstract = [
        (   
            + io.start ** response.yes

            + io.input_half_T ** response.yes
            + io.input_half_T_row1 ** numbers[f"n{row}"]
            + io.input_half_T_row2 ** numbers[f"n{row}"]
            + io.input_half_T_row3 ** numbers[f"n{row+1}"]
            + io.input_half_T_col1 ** numbers[f"n{col}"]
            + io.input_half_T_col2 ** numbers[f"n{col+1}"]
            + io.input_half_T_col3 ** numbers[f"n{col}"]

            + io.target_half_T ** response.latest

            >>
            + io.target_half_T ** response.yes
            + io.target_half_T_row1 ** numbers[f"n{row}"]
            + io.target_half_T_row2 ** numbers[f"n{row}"]
            + io.target_half_T_row3 ** numbers[f"n{row+1}"]
            + io.target_half_T_col1 ** numbers[f"n{col}"]
            + io.target_half_T_col2 ** numbers[f"n{col+1}"]
            + io.target_half_T_col3 ** numbers[f"n{col}"]
         )
         for row in range(1, 6) for col in range(1, 6)
    ]

    mirror_L_first_placement_rule_wabstract = [
        ( 
            + io.start ** response.yes
            + io.input_mirror_L ** response.yes
            + io.input_mirror_L_row1 ** numbers[f"n{row}"]
            + io.input_mirror_L_row2 ** numbers[f"n{row+1}"]
            + io.input_mirror_L_row3 ** numbers[f"n{row+1}"]
            + io.input_mirror_L_col1 ** numbers[f"n{col}"]
            + io.input_mirror_L_col2 ** numbers[f"n{col-1}"]
            + io.input_mirror_L_col3 ** numbers[f"n{col}"]

            + io.target_mirror_L ** response.latest
            >>
            + io.target_mirror_L ** response.yes
            + io.target_mirror_L_row1 ** numbers[f"n{row}"]
            + io.target_mirror_L_row2 ** numbers[f"n{row+1}"]
            + io.target_mirror_L_row3 ** numbers[f"n{row+1}"]
            + io.target_mirror_L_col1 ** numbers[f"n{col}"]
            + io.target_mirror_L_col2 ** numbers[f"n{col-1}"]
            + io.target_mirror_L_col3 ** numbers[f"n{col}"]  
        )
        for row in range(1, 6) for col in range(2, 7)
    ]
    """
      1
    1 1
    """

    horizontal_first_placement_rule_wabstract = [
        (       
                + io.start ** response.yes
                + io.horizontal ** response.yes
                + io.input_horizontal_row1 ** numbers[f"n{row}"]
                + io.input_horizontal_row2 ** numbers[f"n{row}"]
                + io.input_horizontal_row3 ** numbers[f"n{row}"]
                + io.input_horizontal_col1 ** numbers[f"n{col}"]
                + io.input_horizontal_col2 ** numbers[f"n{col+1}"]
                + io.input_horizontal_col3 ** numbers[f"n{col+2}"]

                + io.target_horizontal ** response.latest
                >>
                + io.target_horizontal ** response.yes
                + io.target_horizontal_row1 ** numbers[f"n{row}"]
                + io.target_horizontal_row2 ** numbers[f"n{row}"]
                + io.target_horizontal_row3 ** numbers[f"n{row}"]
                + io.target_horizontal_col1 ** numbers[f"n{col}"]
                + io.target_horizontal_col2 ** numbers[f"n{col+1}"]
                + io.target_horizontal_col3 ** numbers[f"n{col+2}"]  
            )
        for row in range(1, 7) for col in range(1, 5)
    ]

    vertical_first_placement_rule_wabstract = [

        (   
                + io.start ** response.yes    
            +    io.input_vertical ** response.yes
                + io.input_vertical_row1 ** numbers[f"n{row}"]
                + io.input_vertical_row2 ** numbers[f"n{row+1}"]
                + io.input_vertical_row3 ** numbers[f"n{row+2}"]
                + io.input_vertical_col1 ** numbers[f"n{col}"]
                + io.input_vertical_col2 ** numbers[f"n{col}"]
                + io.input_vertical_col3 ** numbers[f"n{col}"]

                + io.target_vertical ** response.latest
                >>
                + io.target_vertical ** response.yes

                + io.target_vertical_row1 ** numbers[f"n{row}"]
                + io.target_vertical_row2 ** numbers[f"n{row+1}"]
                + io.target_vertical_row3 ** numbers[f"n{row+2}"]
                + io.target_vertical_col1 ** numbers[f"n{col}"]
                + io.target_vertical_col2 ** numbers[f"n{col}"]
                + io.target_vertical_col3 ** numbers[f"n{col}"]  
            )
        for row in range(1, 5) for col in range(1, 7)
    ]

    #SUBSEQUENCE PLACEMENT RULES
    half_T_left_of_horizontal_placement_rule_wabstract = [
        (

            + io["left" if switcharoo else "right"] ** response.yes
            + io.input_half_T ** response.yes
            + io.input_horizontal ** response.yes
            
            + io[f"{'target' if switcharoo else 'input'}_half_T_row1"] ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_row2"] ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_row3"] ** numbers[f"n{row+1}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col1"] ** numbers[f"n{col}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col2"]** numbers[f"n{col+1}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col3"] ** numbers[f"n{col}"]

            + io[f"{'input' if switcharoo else 'target'}_horizontal_row1"] ** numbers[f"n{row+i}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_row2"] ** numbers[f"n{row+i}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_row3"] ** numbers[f"n{row+i}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_col1"] ** numbers[f"n{col+2-i}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_col2"] ** numbers[f"n{col+3-i}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_col3"] ** numbers[f"n{col+4-i}"]

            + io[f"target_shape{'half_T' if switcharoo else 'horizontal'}"] ** response.latest # half_T isnt already there
            + io[f"target_shape{'horizontal' if switcharoo else 'half_T'}"] ** response.yes # but horizontal is

            >>
            + io[f"target_shape{'half_T' if switcharoo else 'horizontal'}"] ** response.yes

            + io[f"target_shape{'half_T' if switcharoo else 'horizontal'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+i}"])
            + io[f"target_shape{'half_T' if switcharoo else 'horizontal'}_row2"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+i}"])
            + io[f"target_shape{'half_T' if switcharoo else 'horizontal'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+i}"])
            + io[f"target_shape{'half_T' if switcharoo else 'horizontal'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+2-i}"])
            + io[f"target_shape{'half_T' if switcharoo else 'horizontal'}_col2"] ** (numbers[f"n{col+1}"] if switcharoo else numbers[f"n{col+3-i}"])
            + io[f"target_shape{'half_T' if switcharoo else 'horizontal'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+4-i}"])

        )
        for switcharoo in (True, False) for i in range(2) for row in range(1, 6) for col in range(1, 3 + i)
    ]

    half_T_right_of_horizontal_placement_rule_wabstract = [
        (
            + io["right" if switcharoo else "left"] ** response.yes
            + io.input_half_T ** response.yes
            + io.input_horizontal ** response.yes

            + io[f"{'target' if switcharoo else 'input'}_half_T_row1"] ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_row2"] ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_row3"] ** numbers[f"n{row+1}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col1"] ** numbers[f"n{col}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col2"] ** numbers[f"n{col+1}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col3"] ** numbers[f"n{col}"]
            
            + io[f"{'input' if switcharoo else 'target'}_horizontal_row1"] ** numbers[f"n{row+i}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_row2"] ** numbers[f"n{row+i}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_row3"] ** numbers[f"n{row+i}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_col1"] ** numbers[f"n{col-3}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_col2"] ** numbers[f"n{col-2}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_col3"] ** numbers[f"n{col-1}"]

            + io[f"target_shape{'half_T' if switcharoo else 'horizontal'}"] ** response.latest # half_T isnt already there
            + io[f"target_shape{'horizontal' if switcharoo else 'half_T'}"] ** response.yes # but horizontal is

            >>
            + io[f"target_shape{'half_T' if switcharoo else 'horizontal'}"] ** response.yes

            + io[f"target_shape{'half_T' if switcharoo else 'horizontal'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+i}"])
            + io[f"target_shape{'half_T' if switcharoo else 'horizontal'}_row2"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+i}"])
            + io[f"target_shape{'half_T' if switcharoo else 'horizontal'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+i}"])
            + io[f"target_shape{'half_T' if switcharoo else 'horizontal'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col-3}"])
            + io[f"target_shape{'half_T' if switcharoo else 'horizontal'}_col2"] ** (numbers[f"n{col+1}"] if switcharoo else numbers[f"n{col-2}"])
            + io[f"target_shape{'half_T' if switcharoo else 'horizontal'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col-1}"])
        )
        for switcharoo in (True, False) for i in range(2) for row in range(1, 6) for col in range(4, 6)
    ]

    half_T_below_horizontal_placement_rule_wabstract = [
        (
            + io["below" if switcharoo else "above"] ** response.yes
            + io.input_half_T ** response.yes
            + io.input_horizontal ** response.yes

            + io[f"{'input' if switcharoo else 'target'}_half_T_row1"] ** numbers[f"n{row}"]
            + io[f"{'input' if switcharoo else 'target'}_half_T_row2"] ** numbers[f"n{row}"]
            + io[f"{'input' if switcharoo else 'target'}_half_T_row3"] ** numbers[f"n{row+1}"]
            + io[f"{'input' if switcharoo else 'target'}_half_T_row1"] ** numbers[f"n{col}"]
            + io[f"{'input' if switcharoo else 'target'}_half_T_col2"] ** numbers[f"n{col+1}"]
            + io[f"{'input' if switcharoo else 'target'}_half_T_col3"] ** numbers[f"n{col}"]

            + io[f"{'target' if switcharoo else 'input'}_horizontal_row1"] ** numbers[f"n{row-1}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_row2"] ** numbers[f"n{row-1}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_row3"] ** numbers[f"n{row-1}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_col1"] ** numbers[f"n{col-1+i}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_col2"] ** numbers[f"n{col+i}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_col3"] ** numbers[f"n{col+1+i}"]

            + io[f"target_shape{'half_T' if switcharoo else 'horizontal'}"] ** response.latest # half_T isnt already there
            + io[f"target_shape{'horizontal' if switcharoo else 'half_T'}"] ** response.yes # but horizontal is
            >>
            + io[f"target_shape{'half_T' if switcharoo else 'horizontal'}"] ** response.yes

            + io[f"target_shape{'half_T' if switcharoo else 'horizontal'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row-1}"])
            + io[f"target_shape{'half_T' if switcharoo else 'horizontal'}_row2"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row-1}"])
            + io[f"target_shape{'half_T' if switcharoo else 'horizontal'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row-1}"])
            + io[f"target_shape{'half_T' if switcharoo else 'horizontal'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col-1+i}"])
            + io[f"target_shape{'half_T' if switcharoo else 'horizontal'}_col2"] ** (numbers[f"n{col+1}"] if switcharoo else numbers[f"n{col+i}"])
            + io[f"target_shape{'half_T' if switcharoo else 'horizontal'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+1+i}"])
        ) 
        for switcharoo in (True, False) for i in range(3) for row in range(2, 6) for col in range(1 + (i == 0), 6-i)
    ]

    half_T_above_horizontal_placement_rule_wabstract = [
        (
            + io["above" if switcharoo else "below"] ** response.yes
            + io.input_half_T ** response.yes
            + io.input_horizontal ** response.yes

            + io[f"{'input' if switcharoo else 'target'}_half_T_row1"] ** numbers[f"n{row}"]
            + io[f"{'input' if switcharoo else 'target'}_half_T_row2"] ** numbers[f"n{row}"]
            + io[f"{'input' if switcharoo else 'target'}_half_T_row3"] ** numbers[f"n{row+1}"]
            + io[f"{'input' if switcharoo else 'target'}_half_T_col1"] ** numbers[f"n{col}"]
            + io[f"{'input' if switcharoo else 'target'}_half_T_col2"] ** numbers[f"n{col+1}"]
            + io[f"{'input' if switcharoo else 'target'}_half_T_col3"] ** numbers[f"n{col}"]

            + io[f"{'target' if switcharoo else 'input'}_horizontal_row1"] ** numbers[f"n{row+2}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_row2"] ** numbers[f"n{row+2}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_row3"] ** numbers[f"n{row+2}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_col1"] ** numbers[f"n{col-2+i}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_col2"] ** numbers[f"n{col-1+i}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_col3"] ** numbers[f"n{col+i}"]

            + io[f"target_shape{'half_T' if switcharoo else 'horizontal'}"] ** response.latest # half_T isnt already there
            + io[f"target_shape{'horizontal' if switcharoo else 'half_T'}"] ** response.yes # but horizontal is

            >>
            + io[f"target_shape{'half_T' if switcharoo else 'horizontal'}"] ** response.yes

            + io[f"target_shape{'half_T' if switcharoo else 'horizontal'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+2}"])
            + io[f"target_shape{'half_T' if switcharoo else 'horizontal'}_row2"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+2}"])
            + io[f"target_shape{'half_T' if switcharoo else 'horizontal'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+2}"])
            + io[f"target_shape{'half_T' if switcharoo else 'horizontal'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col-2+i}"])
            + io[f"target_shape{'half_T' if switcharoo else 'horizontal'}_col2"] ** (numbers[f"n{col+1}"] if switcharoo else numbers[f"n{col-1+i}"])
            + io[f"target_shape{'half_T' if switcharoo else 'horizontal'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+i}"])
        ) 
        for switcharoo in (True, False) for i in range(3) for row in range(1, 5) for col in range(3-i, 6-(i==2))
]

    half_T_left_vertical_placement_rule_wabstract = [
        (
            + io["left" if switcharoo else "right"] ** response.yes
            + io.input_half_T ** response.yes
            + io.input_vertical ** response.yes

            + io1[f"{'target' if switcharoo else 'input'}_half_T_row1"]** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_row2"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_row3"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col1"] ** numbers[f"n{col}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col2"] ** numbers[f"n{col+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col3"] ** numbers[f"n{col}"]

            + io1[f"{'input' if switcharoo else 'target'}_vertical_row1"] ** numbers[f"n{row+1-i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row2"] ** numbers[f"n{row+2-i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row3"] ** numbers[f"n{row+3-i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col1"] ** numbers[f"n{col+2- (i == 0)}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col2"] ** numbers[f"n{col+2- (i == 0)}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col3"] ** numbers[f"n{col+2- (i == 0)}"]

            + io1[f"target_shape{'half_T' if switcharoo else 'vertical'}"] ** response.latest # half_T isnt already there
            + io1[f"target_shape{'vertical' if switcharoo else 'half_T'}"] ** response.yes # but vertical is
            >>
            + io[f"target_shape{'half_T' if switcharoo else 'vertical'}"] ** response.yes

            + io[f"target_shape{'half_T' if switcharoo else 'vertical'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+1-i}"])
            + io[f"target_shape{'half_T' if switcharoo else 'vertical'}_row2"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+2-i}"])
            + io[f"target_shape{'half_T' if switcharoo else 'vertical'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+3-i}"])
            + io[f"target_shape{'half_T' if switcharoo else 'vertical'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+2- (i == 0)}"])
            + io[f"target_shape{'half_T' if switcharoo else 'vertical'}_col2"] ** (numbers[f"n{col+1}"] if switcharoo else numbers[f"n{col+2- (i == 0)}"])
            + io[f"target_shape{'half_T' if switcharoo else 'vertical'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+2- (i == 0)}"])
            )
            for switcharoo in (True, False) for i in range(4) for row in range(1+(i-1 if i > 1 else 0), 4 + (math.ceil(i/2))) for col in range(1, 6-(i > 0))
    ]
    
    half_T_right_vertical_placement_rule_wabstract = [
        (
            + io["right" if switcharoo else "left"] ** response.yes
            + io.input_half_T ** response.yes
            + io.input_vertical ** response.yes
            
            + io1[f"{'target' if switcharoo else 'input'}_half_T_row1"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_row2"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_row3"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col1"] ** numbers[f"n{col}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col2"] ** numbers[f"n{col+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col3"] ** numbers[f"n{col}"]

            + io1[f"{'input' if switcharoo else 'target'}_vertical_row1"] ** numbers[f"n{row-2+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row2"] ** numbers[f"n{row-1+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row3"] ** numbers[f"n{row+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col1"] ** numbers[f"n{col-1}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col2"] ** numbers[f"n{col-1}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col3"] ** numbers[f"n{col-1}"]

            + io1[f"target_shape{'half_T' if switcharoo else 'vertical'}"] ** response.latest # half_T isnt already there
            + io1[f"target_shape{'vertical' if switcharoo else 'half_T'}"] ** response.yes # but vertical is

            >>
            + io[f"target_shape{'half_T' if switcharoo else 'vertical'}"] ** response.yes

            + io[f"target_shape{'half_T' if switcharoo else 'vertical'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row-2+i}"])
            + io[f"target_shape{'half_T' if switcharoo else 'vertical'}_row2"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row-1+i}"])
            + io[f"target_shape{'half_T' if switcharoo else 'vertical'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+i}"])
            + io[f"target_shape{'half_T' if switcharoo else 'vertical'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col-1}"])
            + io[f"target_shape{'half_T' if switcharoo else 'vertical'}_col2"] ** (numbers[f"n{col+1}"] if switcharoo else numbers[f"n{col-1}"])
            + io[f"target_shape{'half_T' if switcharoo else 'vertical'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col-1}"])
        ) 
        for switcharoo in (True, False) for i in range(4) for row in range(max(1, 3-i), 6-max(0, i-1)) for col in range(2, 6)
    ]
    
    half_T_below_vertical_placement_rule_wabstract = [
        (
            + io["below" if switcharoo else "above"] ** response.yes
            + io.input_half_T ** response.yes
            + io.input_vertical ** response.yes
            
            + io1[f"{'target' if switcharoo else 'input'}_half_T_row1"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_row2"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_row3"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col1"] ** numbers[f"n{col}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col2"] ** numbers[f"n{col+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col3"] ** numbers[f"n{col}"]
            
            
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row1"] ** numbers[f"n{row-3}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row2"] ** numbers[f"n{row-2}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row3"] ** numbers[f"n{row-3}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col1"] ** numbers[f"n{col+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col2"] ** numbers[f"n{col+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col3"] ** numbers[f"n{col+i}"]

            + io1[f"target_shape{'half_T' if switcharoo else 'vertical'}"] ** response.latest # half_T isnt already there
            + io1[f"target_shape{'vertical' if switcharoo else 'half_T'}"] ** response.yes # but vertical is

            >>
            + io[f"target_shape{'half_T' if switcharoo else 'vertical'}"] ** response.yes

            + io[f"target_shape{'half_T' if switcharoo else 'vertical'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row-3}"])
            + io[f"target_shape{'half_T' if switcharoo else 'vertical'}_row2"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row-2}"])
            + io[f"target_shape{'half_T' if switcharoo else 'vertical'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row-3}"])
            + io[f"target_shape{'half_T' if switcharoo else 'vertical'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+i}"])
            + io[f"target_shape{'half_T' if switcharoo else 'vertical'}_col2"] ** (numbers[f"n{col+1}"] if switcharoo else numbers[f"n{col+i}"])
            + io[f"target_shape{'half_T' if switcharoo else 'vertical'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+i}"])
            ) 
            for switcharoo in (True, False) for i in range(2) for row in range(4, 6) for col in range(1, 6)
    ]

    half_T_above_vertical_placement_rule_wabstract = [
        (
            + io["above" if switcharoo else "below"] ** response.yes
            + io.input_half_T ** response.yes
            + io.input_vertical ** response.yes

            + io1[f"{'target' if switcharoo else 'input'}_half_T_row1"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_row2"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_row3"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col1"] ** numbers[f"n{col}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col2"] ** numbers[f"n{col+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col3"] ** numbers[f"n{col}"]

            + io1[f"{'input' if switcharoo else 'target'}_vertical_row1"] ** numbers[f"n{row+1}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row2"] ** numbers[f"n{row+2}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row3"] ** numbers[f"n{row+3}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col1"] ** numbers[f"n{col}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col2"] ** numbers[f"n{col}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col3"] ** numbers[f"n{col}"]

            + io1[f"target_shape{'half_T' if switcharoo else 'vertical'}"] ** response.latest # half_T isnt already there
            + io1[f"target_shape{'vertical' if switcharoo else 'half_T'}"] ** response.yes # but vertical is
            >>
            + io[f"target_shape{'half_T' if switcharoo else 'vertical'}"] ** response.yes

            + io[f"target_shape{'half_T' if switcharoo else 'vertical'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+1}"])
            + io[f"target_shape{'half_T' if switcharoo else 'vertical'}_row2"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+2}"])
            + io[f"target_shape{'half_T' if switcharoo else 'vertical'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+3}"])
            + io[f"target_shape{'half_T' if switcharoo else 'vertical'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col}"])
            + io[f"target_shape{'half_T' if switcharoo else 'vertical'}_col2"] ** (numbers[f"n{col+1}"] if switcharoo else numbers[f"n{col}"])
            + io[f"target_shape{'half_T' if switcharoo else 'vertical'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col}"])
            ) 
            for switcharoo in (True, False) for row in range(1, 3) for col in range(1, 6)
    ]

    half_T_left_mirror_L_placement_rule_wabstract = [
        (
            + io["left" if switcharoo else "right"] ** response.yes
            + io.input_half_T ** response.yes
            + io.input_mirror_L ** response.yes

            + io1[f"{'target' if switcharoo else 'input'}_half_T_row1"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_row2"]** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_row3"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col1"] ** numbers[f"n{col}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col2"] ** numbers[f"n{col+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col3"] ** numbers[f"n{col}"]

            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_row1"] ** numbers[f"n{row-i}"]
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_row2"] ** numbers[f"n{row+1-i}"]
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_row3"] ** numbers[f"n{row+1-i}"]
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_col1"] ** numbers[f"n{col+2+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_col2"] ** numbers[f"n{col+1+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_col3"] ** numbers[f"n{col+2+i}"]

            + io1[f"target_shape{'half_T' if switcharoo else 'mirror_L'}"] ** response.latest # half_T isnt already there
            + io1[f"target_shape{'mirror_L' if switcharoo else 'half_T'}"] ** response.yes # but mirror_L is
            >>
            + io[f"target_shape{'half_T' if switcharoo else 'mirror_L'}"] ** response.yes

            + io[f"target_shape{'half_T' if switcharoo else 'mirror_L'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row-i}"])
            + io[f"target_shape{'half_T' if switcharoo else 'mirror_L'}_row2"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+1-i}"])
            + io[f"target_shape{'half_T' if switcharoo else 'mirror_L'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+1-i}"])
            + io[f"target_shape{'half_T' if switcharoo else 'mirror_L'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+2+i}"])
            + io[f"target_shape{'half_T' if switcharoo else 'mirror_L'}_col2"] ** (numbers[f"n{col+1}"] if switcharoo else numbers[f"n{col+1+i}"])
            + io[f"target_shape{'half_T' if switcharoo else 'mirror_L'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+2+i}"])
        )
        for switcharoo in (True, False) for i in range(2) for row in range(1+i, 6) for col in range(1, 5-i)
    ]
    
    half_T_right_mirror_L_placement_rule_wabstract = [
        (
            + io["right" if switcharoo else "left"] ** response.yes
            + io.input_half_T ** response.yes
            + io.input_mirror_L ** response.yes

            + io1[f"{'target' if switcharoo else 'input'}_half_T_row1"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_row2"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_row3"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col1"] ** numbers[f"n{col}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col2"] ** numbers[f"n{col+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col3"] ** numbers[f"n{col}"]

            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_row1"] ** numbers[f"n{row + (-1 if i== 0 else 1)*(i%2 == 0)}"] # 1 up, no up, 1 down.
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_row2"] ** numbers[f"n{row + i}"]
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_row3"] ** numbers[f"n{row+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_col1"] ** numbers[f"n{col-1}"]
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_col2"] ** numbers[f"n{col-2}"]
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_col3"] ** numbers[f"n{col-1}"]

            + io1[f"target_shape{'half_T' if switcharoo else 'mirror_L'}"] ** response.latest # half_T isnt already there
            + io1[f"target_shape{'mirror_L' if switcharoo else 'half_T'}"] ** response.yes # but mirror_L is

            >>
            + io[f"target_shape{'half_T' if switcharoo else 'mirror_L'}"] ** response.yes

            + io[f"target_shape{'half_T' if switcharoo else 'mirror_L'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row + (-1 if i== 0 else 1)*(i%2 == 0)}"])
            + io[f"target_shape{'half_T' if switcharoo else 'mirror_L'}_row2"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row + i}"])
            + io[f"target_shape{'half_T' if switcharoo else 'mirror_L'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+i}"])
            + io[f"target_shape{'half_T' if switcharoo else 'mirror_L'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col-1}"])
            + io[f"target_shape{'half_T' if switcharoo else 'mirror_L'}_col2"] ** (numbers[f"n{col+1}"] if switcharoo else numbers[f"n{col-2}"])
            + io[f"target_shape{'half_T' if switcharoo else 'mirror_L'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col-1}"])
        ) 
        for switcharoo in (True, False) for i in range(3) for row in range(1+(i==0), 6-(i==2)) for col in range(3, 6)
    ]
    
    half_T_below_mirror_L_placement_rule_wabstract = [
        (
            + io["below" if switcharoo else "above"] ** response.yes
            + io.input_half_T ** response.yes
            + io.input_mirror_L ** response.yes

            + io1[f"{'target' if switcharoo else 'input'}_half_T_row1"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_row2"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_row3"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col1"] ** numbers[f"n{col}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col2"] ** numbers[f"n{col+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col3"] ** numbers[f"n{col}"]
            
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_row1"] ** numbers[f"n{row-2}"]
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_row2"] ** numbers[f"n{row-1}"]
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_row3"] ** numbers[f"n{row-1}"]
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_col1"] ** numbers[f"n{col+1+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_col2"] ** numbers[f"n{col+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_col3"] ** numbers[f"n{col+1+i}"]

            + io1[f"target_shape{'half_T' if switcharoo else 'mirror_L'}"] ** response.latest # half_T isnt already there
            + io1[f"target_shape{'mirror_L' if switcharoo else 'half_T'}"] ** response.yes # but mirror_L is
            >>
            + io[f"target_shape{'half_T' if switcharoo else 'mirror_L'}"] ** response.yes

            + io[f"target_shape{'half_T' if switcharoo else 'mirror_L'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row-2}"])
            + io[f"target_shape{'half_T' if switcharoo else 'mirror_L'}_row2"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row-1}"])
            + io[f"target_shape{'half_T' if switcharoo else 'mirror_L'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row-1}"])
            + io[f"target_shape{'half_T' if switcharoo else 'mirror_L'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+1+i}"])
            + io[f"target_shape{'half_T' if switcharoo else 'mirror_L'}_col2"] ** (numbers[f"n{col+1}"] if switcharoo else numbers[f"n{col+i}"])
            + io[f"target_shape{'half_T' if switcharoo else 'mirror_L'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+1+i}"])
        )
        for switcharoo in (True, False) for i in range(2) for row in range(3, 6) for col in range(1, 6-i)
    ]

    half_T_above_mirror_L_placement_rule_wabstract = [
        (
            + io["above" if switcharoo else "below"] ** response.yes
            + io.input_half_T ** response.yes
            + io.input_mirror_L ** response.yes

             + io1[f"{'target' if switcharoo else 'input'}_half_T_row1"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_row2"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_row3"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col1"] ** numbers[f"n{col}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col2"] ** numbers[f"n{col+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_half_T_col3"] ** numbers[f"n{col}"]
             
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_row1"] ** numbers[f"n{row+2}"]
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_row2"] ** numbers[f"n{row+3}"]
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_row3"] ** numbers[f"n{row+3}"]
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_col1"] ** numbers[f"n{col}"]
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_col2"] ** numbers[f"n{col-1}"]
            + io1[f"{'input' if switcharoo else 'target'}_mirror_L_col3"] ** numbers[f"n{col}"]

            + io1[f"target_shape{'half_T' if switcharoo else 'mirror_L'}"] ** response.latest # half_T isnt already there
            + io1[f"target_shape{'mirror_L' if switcharoo else 'half_T'}"] ** response.yes # but mirror_L is
            >>
            + io[f"target_shape{'half_T' if switcharoo else 'mirror_L'}"] ** response.yes

            + io[f"target_shape{'half_T' if switcharoo else 'mirror_L'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+2}"])
            + io[f"target_shape{'half_T' if switcharoo else 'mirror_L'}_row2"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+3}"])
            + io[f"target_shape{'half_T' if switcharoo else 'mirror_L'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+3}"])
            + io[f"target_shape{'half_T' if switcharoo else 'mirror_L'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col}"])
            + io[f"target_shape{'half_T' if switcharoo else 'mirror_L'}_col2"] ** (numbers[f"n{col+1}"] if switcharoo else numbers[f"n{col-1}"])
            + io[f"target_shape{'half_T' if switcharoo else 'mirror_L'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col}"])
        ) 
        for switcharoo in (True, False) for row in range(1, 4) for col in range(2, 6)
    ]

    mirror_L_left_horizontal_placement_rule_wabstract  = [
        (
            + io["left" if switcharoo else "right"] ** response.yes
            + io.input_mirror_L ** response.yes
            + io.input_horizontal ** response.yes

            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row1"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row2"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row3"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col1"] ** numbers[f"n{col}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col2"] ** numbers[f"n{col-1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col3"] ** numbers[f"n{col}"]
            
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_row1"] ** numbers[f"n{row+i}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_row2"] ** numbers[f"n{row+i}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_row3"]** numbers[f"n{row+i}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_col1"] ** numbers[f"n{col+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_col2"] ** numbers[f"n{col+2}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_col3"] ** numbers[f"n{col+3}"]

            + io1[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}"] ** response.latest # mirror_L isnt already there
            + io1[f"target_shape{'horizontal' if switcharoo else 'mirror_L'}"] ** response.yes # but horizontal is

            >>
            + io[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}"] ** response.yes

            + io[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+i}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}_row2"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+i}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+i}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+1}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}_col2"] ** (numbers[f"n{col-1}"] if switcharoo else numbers[f"n{col+2}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+3}"])
            ) 
            for switcharoo in (True, False) for i in range(2) for row in range(1, 6) for col in range(2, 4)
    ]

    mirror_L_right_horizontal_placement_rule_wabstract = [
        (
            + io["right" if switcharoo else "left"] ** response.yes
            + io.input_mirror_L ** response.yes
            + io.input_horizontal ** response.yes

            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row1"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row2"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row3"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col1"] ** numbers[f"n{col}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col2"] ** numbers[f"n{col-1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col3"] ** numbers[f"n{col}"]
            
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_row1"] ** numbers[f"n{row+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_row2"] ** numbers[f"n{row+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_row3"] ** numbers[f"n{row+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_col1"] ** numbers[f"n{col-3-i}"]
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_col2"] ** numbers[f"n{col-2-i}"]
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_col3"] ** numbers[f"n{col-1-i}"]

            + io1[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}"] ** response.latest # mirror_L isnt already there
            + io1[f"target_shape{'horizontal' if switcharoo else 'mirror_L'}"] ** response.yes # but horizontal is
            >>
            + io[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}"] ** response.yes

            + io[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+i}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}_row2"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+i}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+i}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col-3-i}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}_col2"] ** (numbers[f"n{col-1}"] if switcharoo else numbers[f"n{col-2-i}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col-1-i}"])
        ) 
        for switcharoo in (True, False) for i in range(2) for row in range(1, 6) for col in range(4+i, 7)
    ]

    mirror_L_above_horizontal_placement_rul_wabstract = [
        (
            + io["above" if switcharoo else "below"] ** response.yes
            + io.input_mirror_L ** response.yes
            + io.input_horizontal ** response.yes

            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row1"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row2"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row3"]** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col1"] ** numbers[f"n{col}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col2"] ** numbers[f"n{col-1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col3"] ** numbers[f"n{col}"]
            
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_row1"] ** numbers[f"n{row+2}"]
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_row2"] ** numbers[f"n{row+2}"]
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_row3"] ** numbers[f"n{row+2}"]
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_col1"] ** numbers[f"n{col-2+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_col2"] ** numbers[f"n{col-1+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_col3"] ** numbers[f"n{col+i}"]

            + io1[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}"] ** response.latest # mirror_L isnt already there
            + io1[f"target_shape{'horizontal' if switcharoo else 'mirror_L'}"] ** response.yes # but horizontal is

            >>
            + io[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}"] ** response.yes

            + io[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+2}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}_row2"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+2}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+2}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col-2+i}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}_col2"] ** (numbers[f"n{col-1}"] if switcharoo else numbers[f"n{col-1+i}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+i}"])
            )
            for switcharoo in (True, False) for i in range(3) for row in range(1, 5) for col in range(2 + (i == 0), 7-i)
    ]

    mirror_L_below_horizontal_placement_rule_wabstract = [
        (
            +  io["below" if switcharoo else "above"] ** response.yes
            + io.input_mirror_L ** response.yes
            + io.input_horizontal ** response.yes

            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row1"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row2"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row3"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col1"] ** numbers[f"n{col}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col2"] ** numbers[f"n{col-1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col3"] ** numbers[f"n{col}"]

            + io1[f"{'input' if switcharoo else 'target'}_horizontal_row1"] ** numbers[f"n{row-1}"]
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_row2"] ** numbers[f"n{row-1}"]
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_row3"] ** numbers[f"n{row-1}"]
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_col1"] ** numbers[f"n{col-2+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_col2"] ** numbers[f"n{col-1+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_col3"] ** numbers[f"n{col+i}"]

            + io1[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}"] ** response.latest # mirror_L isnt already there
            + io1[f"target_shape{'horizontal' if switcharoo else 'mirror_L'}"] ** response.yes # but horizontal is
            >>
            + io[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}"] ** response.yes

            + io[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row-1}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}_row2"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row-1}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row-1}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col-2+i}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}_col2"] ** (numbers[f"n{col-1}"] if switcharoo else numbers[f"n{col-1+i}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+i}"])
            ) 
            for switcharoo in (True, False) for i in range (3) for row in range(2, 6) for col in range(3-(i!=0), 7-i)
    ]

    mirror_L_left_vertical_placement_rule_wabstract  = [
        (
            + io["left" if switcharoo else "right"] ** response.yes
            + io.input_mirror_L ** response.yes
            + io.input_vertical ** response.yes

            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row1"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row2"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row3"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col1"] ** numbers[f"n{col}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col2"] ** numbers[f"n{col-1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col3"] ** numbers[f"n{col}"]
            
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row1"] ** numbers[f"n{row-1+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row2"] ** numbers[f"n{row+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row3"] ** numbers[f"n{row+1+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col1"] ** numbers[f"n{col+1}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col2"] ** numbers[f"n{col+1}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col3"] ** numbers[f"n{col+1}"]

            + io1[f"target_shape{'mirror_L' if switcharoo else 'vertical'}"] ** response.latest # mirror_L isnt already there
            + io1[f"target_shape{'vertical' if switcharoo else 'mirror_L'}"] ** response.yes # but vertical is
            >>
            + io[f"target_shape{'mirror_L' if switcharoo else 'vertical'}"] ** response.yes

            + io[f"target_shape{'mirror_L' if switcharoo else 'vertical'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row-1+i}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'vertical'}_row2"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+i}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'vertical'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+1+i}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'vertical'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+1}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'vertical'}_col2"] ** (numbers[f"n{col-1}"] if switcharoo else numbers[f"n{col+1}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'vertical'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+1}"])
            ) 
            for switcharoo in (True, False) for i in range(3) for row in range(1+(i==0), 6-i) for col in range(2, 6)
    ]

    mirror_L_right_vertical_placement_rule_wabstract = [
        (
            + io["right" if switcharoo else "left"] ** response.yes
            + io.input_mirror_L ** response.yes
            + io.input_vertical ** response.yes

            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row1"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row2"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row3"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col1"] ** numbers[f"n{col}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col2"] ** numbers[f"n{col-1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col3"] ** numbers[f"n{col}"]
            
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row1"] ** numbers[f"n{row+1-i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row2"] ** numbers[f"n{row+2-i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row3"] ** numbers[f"n{row+3-i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col1"] ** numbers[f"n{col-2 + (i == 3)}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col2"] ** numbers[f"n{col-2 + (i == 3)}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col3"] ** numbers[f"n{col-2 + (i == 3)}"]

            + io1[f"target_shape{'mirror_L' if switcharoo else 'vertical'}"] ** response.latest # mirror_L isnt already there
            + io1[f"target_shape{'vertical' if switcharoo else 'mirror_L'}"] ** response.yes # but vertical is
            >>
            + io[f"target_shape{'mirror_L' if switcharoo else 'vertical'}"] ** response.yes

            + io[f"target_shape{'mirror_L' if switcharoo else 'vertical'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+1-i}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'vertical'}_row2"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+2-i}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'vertical'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+3-i}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'vertical'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col-2 + (i == 3)}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'vertical'}_col2"] ** (numbers[f"n{col-1}"] if switcharoo else numbers[f"n{col-2 + (i == 3)}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'vertical'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col-2 + (i == 3)}"])
            )
            for switcharoo in (True, False) for i in range(4) for row in range(1+max(0, i-1), min(4+i, 6)) for col in range(3 - (i == 3), 7)
    ]

    mirror_L_above_vertical_placement_rule_wabstract = [
        (
            + io["above" if switcharoo else "below"] ** response.yes
            + io.input_mirror_L ** response.yes
            + io.input_vertical ** response.yes

            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row1"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row2"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row3"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col1"] ** numbers[f"n{col}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col2"] ** numbers[f"n{col-1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col3"] ** numbers[f"n{col}"]
            
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row1"]** numbers[f"n{row+2}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row2"] ** numbers[f"n{row+3}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row3"] ** numbers[f"n{row+4}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col1"] ** numbers[f"n{col-1+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col2"] ** numbers[f"n{col-1+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col3"] ** numbers[f"n{col-1+i}"]

            + io1[f"target_shape{'mirror_L' if switcharoo else 'vertical'}"] ** response.latest # mirror_L isnt already there
            + io1[f"target_shape{'vertical' if switcharoo else 'mirror_L'}"] ** response.yes # but vertical is
            >>
            + io[f"target_shape{'mirror_L' if switcharoo else 'vertical'}"] ** response.yes

            + io[f"target_shape{'mirror_L' if switcharoo else 'vertical'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+2}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'vertical'}_row2"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+3}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'vertical'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row+4}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'vertical'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col-1+i}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'vertical'}_col2"] ** (numbers[f"n{col-1}"] if switcharoo else numbers[f"n{col-1+i}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'vertical'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col-1+i}"])
        )
        for switcharoo in (True, False) for i in range(2) for row in range(1, 3) for col in range(2, 7)
    ]

    mirror_L_below_vertical_placement_rule_wabstract = [
        (
            + io["below" if switcharoo else "above"] ** response.yes
            + io.input_mirror_L ** response.yes
            + io.input_vertical ** response.yes

           + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row1"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row2"] ** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_row3"]** numbers[f"n{row+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col1"] ** numbers[f"n{col}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col2"] ** numbers[f"n{col-1}"]
            + io1[f"{'target' if switcharoo else 'input'}_mirror_L_col3"] ** numbers[f"n{col}"]
            
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row1"] ** numbers[f"n{row-3}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row2"] ** numbers[f"n{row-2}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row3"] ** numbers[f"n{row-1}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col1"] ** numbers[f"n{col}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col2"] ** numbers[f"n{col}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col3"] ** numbers[f"n{col}"]

            + io1[f"target_shape{'mirror_L' if switcharoo else 'vertical'}"] ** response.latest # mirror_L isnt already there
            + io1[f"target_shape{'vertical' if switcharoo else 'mirror_L'}"] ** response.yes # but vertical is
            >>
            + io[f"target_shape{'mirror_L' if switcharoo else 'vertical'}"] ** response.yes

            + io[f"target_shape{'mirror_L' if switcharoo else 'vertical'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row-3}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'vertical'}_row2"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row-2}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'vertical'}_row3"] ** (numbers[f"n{row+1}"] if switcharoo else numbers[f"n{row-1}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'vertical'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'vertical'}_col2"] ** (numbers[f"n{col-1}"] if switcharoo else numbers[f"n{col}"])
            + io[f"target_shape{'mirror_L' if switcharoo else 'vertical'}_col3"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col}"])
            )
            for switcharoo in (True, False) for row in range(4, 6) for col in range(2, 7)
    ]

    horizontal_left_vertical_placement_rule_wabstract  = [
        (
            + io["left" if switcharoo else "right"] ** response.yes
            + io.input_vertical ** response.yes
            + io.input_horizontal ** response.yes
            
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_row1"] ** numbers[f"n{row}"]
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_row2"]** numbers[f"n{row}"]
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_row3"] ** numbers[f"n{row}"]
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_col1"] ** numbers[f"n{col}"]
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_col2"] ** numbers[f"n{col+1}"] 
            + io1[f"{'input' if switcharoo else 'target'}_horizontal_col3"] ** numbers[f"n{col+2}"]
            
            
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row1"] ** numbers[f"n{row-2+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row2"] ** numbers[f"n{row-1+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row3"] ** numbers[f"n{row+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col1"] ** numbers[f"n{col+3}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col2"] ** numbers[f"n{col+3}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col3"] ** numbers[f"n{col+3}"]

            + io1[f"target_shape{'horizontal' if switcharoo else 'vertical'}"] ** response.latest # horizontal isnt already there
            + io1[f"target_shape{'vertical' if switcharoo else 'horizontal'}"] ** response.yes # but vertical is
            >>
            + io[f"target_shape{'horizontal' if switcharoo else 'vertical'}"] ** response.yes
            + io[f"target_shape{'horizontal' if switcharoo else 'vertical'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row-2+i}"])
            + io[f"target_shape{'horizontal' if switcharoo else 'vertical'}_row2"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row-1+i}"])
            + io[f"target_shape{'horizontal' if switcharoo else 'vertical'}_row3"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+i}"])
            + io[f"target_shape{'horizontal' if switcharoo else 'vertical'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+3}"])
            + io[f"target_shape{'horizontal' if switcharoo else 'vertical'}_col2"] ** (numbers[f"n{col+1}"] if switcharoo else numbers[f"n{col+3}"])
            + io[f"target_shape{'horizontal' if switcharoo else 'vertical'}_col3"] ** (numbers[f"n{col+2}"] if switcharoo else numbers[f"n{col+3}"])
            ) 
            for switcharoo in (True, False) for i in range(3) for row in range(3-i, 7-i) for col in range(1, 4)
    ]

    horizontal_right_vertical_placement_rule_wabstract = [
        (
            + io["right" if switcharoo else "left"] ** response.yes
            + io.input_vertical ** response.yes
            + io.input_horizontal ** response.yes

            + io1[f"{'target' if switcharoo else 'input'}_horizontal_row1"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_row2"]** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_row3"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_col1"] ** numbers[f"n{col}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_col2"] ** numbers[f"n{col+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_col3"] ** numbers[f"n{col+2}"]
            
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row1"] ** numbers[f"n{row-2+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row2"] ** numbers[f"n{row-1+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row3"] ** numbers[f"n{row+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col1"] ** numbers[f"n{col-1}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col2"] ** numbers[f"n{col-1}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col3"] ** numbers[f"n{col-1}"]

            + io1[f"target_shape{'horizontal' if switcharoo else 'vertical'}"] ** response.latest # horizontal isnt already there
            + io1[f"target_shape{'vertical' if switcharoo else 'horizontal'}"] ** response.yes # but vertical is
            >>
            + io[f"target_shape{'horizontal' if switcharoo else 'vertical'}"] ** response.yes

            + io[f"target_shape{'horizontal' if switcharoo else 'vertical'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row-2+i}"])
            + io[f"target_shape{'horizontal' if switcharoo else 'vertical'}_row2"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row-1+i}"])
            + io[f"target_shape{'horizontal' if switcharoo else 'vertical'}_row3"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+i}"])
            + io[f"target_shape{'horizontal' if switcharoo else 'vertical'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col-1}"])
            + io[f"target_shape{'horizontal' if switcharoo else 'vertical'}_col2"] ** (numbers[f"n{col+1}"] if switcharoo else numbers[f"n{col-1}"])
            + io[f"target_shape{'horizontal' if switcharoo else 'vertical'}_col3"] ** (numbers[f"n{col+2}"] if switcharoo else numbers[f"n{col-1}"])
            ) 
            for switcharoo in (True, False) for i in range(3) for row in range(3-i, 7-i) for col in range(2, 5)
    ]

    horizontal_above_vertical_placement_rule_wabstract = [
        (
            + io["above" if switcharoo else "below"] ** response.yes
            + io.input_vertical ** response.yes
            + io.input_horizontal ** response.yes

            + io1[f"{'target' if switcharoo else 'input'}_horizontal_row1"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_row2"]** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_row3"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_col1"] ** numbers[f"n{col}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_col2"] ** numbers[f"n{col+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_col3"] ** numbers[f"n{col+2}"]

            + io1[f"{'input' if switcharoo else 'target'}_vertical_row1"] ** numbers[f"n{row+1}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row2"] ** numbers[f"n{row+2}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row3"] ** numbers[f"n{row+3}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col1"] ** numbers[f"n{col+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col2"] ** numbers[f"n{col+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col3"] ** numbers[f"n{col+i}"]

            + io1[f"target_shape{'horizontal' if switcharoo else 'vertical'}"] ** response.latest # horizontal isnt already there
            + io1[f"target_shape{'vertical' if switcharoo else 'horizontal'}"] ** response.yes # but vertical is
            >>
            + io[f"target_shape{'horizontal' if switcharoo else 'vertical'}"] ** response.yes

            + io[f"target_shape{'horizontal' if switcharoo else 'vertical'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+1}"])
            + io[f"target_shape{'horizontal' if switcharoo else 'vertical'}_row2"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+2}"])
            + io[f"target_shape{'horizontal' if switcharoo else 'vertical'}_row3"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row+3}"])
            + io[f"target_shape{'horizontal' if switcharoo else 'vertical'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+i}"])
            + io[f"target_shape{'horizontal' if switcharoo else 'vertical'}_col2"] ** (numbers[f"n{col+1}"] if switcharoo else numbers[f"n{col+i}"])
            + io[f"target_shape{'horizontal' if switcharoo else 'vertical'}_col3"] ** (numbers[f"n{col+2}"] if switcharoo else numbers[f"n{col+i}"])
        ) 
        for switcharoo in (True, False) for i in range(3) for row in range(1, 4) for col in range(1, 5)
    ]

    horizontal_below_vertical_placement_rule_wabstract = [
        (
            + io["below" if switcharoo else "above"] ** response.yes
            + io.input_vertical ** response.yes
            + io.input_horizontal ** response.yes

            + io1[f"{'target' if switcharoo else 'input'}_horizontal_row1"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_row2"]** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_row3"] ** numbers[f"n{row}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_col1"] ** numbers[f"n{col}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_col2"] ** numbers[f"n{col+1}"]
            + io1[f"{'target' if switcharoo else 'input'}_horizontal_col3"] ** numbers[f"n{col+2}"]

            + io1[f"{'input' if switcharoo else 'target'}_vertical_row1"] ** numbers[f"n{row-3}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row2"] ** numbers[f"n{row-2}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_row3"] ** numbers[f"n{row-1}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col1"] ** numbers[f"n{col+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col2"] ** numbers[f"n{col+i}"]
            + io1[f"{'input' if switcharoo else 'target'}_vertical_col3"] ** numbers[f"n{col+i}"]

            + io1[f"target_shape{'horizontal' if switcharoo else 'vertical'}"] ** response.latest # horizontal isnt already there
            + io1[f"target_shape{'vertical' if switcharoo else 'horizontal'}"] ** response.yes # but vertical is
            >>
            + io2[f"target_shape{'horizontal' if switcharoo else 'vertical'}"] ** response.latest
            >>
            + io[f"target_shape{'horizontal' if switcharoo else 'vertical'}"] ** response.yes

            + io[f"target_shape{'horizontal' if switcharoo else 'vertical'}_row1"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row-3}"])
            + io[f"target_shape{'horizontal' if switcharoo else 'vertical'}_row2"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row-2}"])
            + io[f"target_shape{'horizontal' if switcharoo else 'vertical'}_row3"] ** (numbers[f"n{row}"] if switcharoo else numbers[f"n{row-1}"])
            + io[f"target_shape{'horizontal' if switcharoo else 'vertical'}_col1"] ** (numbers[f"n{col}"] if switcharoo else numbers[f"n{col+i}"])
            + io[f"target_shape{'horizontal' if switcharoo else 'vertical'}_col2"] ** (numbers[f"n{col+1}"] if switcharoo else numbers[f"n{col+i}"])
            + io[f"target_shape{'horizontal' if switcharoo else 'vertical'}_col3"] ** (numbers[f"n{col+2}"] if switcharoo else numbers[f"n{col+i}"])
            )
            for switcharoo in (True, False) for i in range(3) for row in range(4, 7) for col in range(1, 5)
    ]
    
    participant.search_space_rules.rules.compile(
        *(
            + half_T_first_placement_rule_wabstract + mirror_L_first_placement_rule_wabstract + horizontal_first_placement_rule_wabstract + vertical_first_placement_rule_wabstract
            + half_T_left_of_horizontal_placement_rule_wabstract + half_T_right_of_horizontal_placement_rule_wabstract + half_T_above_horizontal_placement_rule_wabstract + half_T_below_horizontal_placement_rule_wabstract
            + half_T_left_vertical_placement_rule_wabstract + half_T_right_vertical_placement_rule_wabstract + half_T_above_vertical_placement_rule_wabstract + half_T_below_vertical_placement_rule_wabstract
            + half_T_left_mirror_L_placement_rule_wabstract + half_T_right_mirror_L_placement_rule_wabstract + half_T_above_mirror_L_placement_rule_wabstract + half_T_below_mirror_L_placement_rule_wabstract
            + mirror_L_left_horizontal_placement_rule_wabstract + mirror_L_right_horizontal_placement_rule_wabstract + mirror_L_above_horizontal_placement_rule_wabstract + mirror_L_below_horizontal_placement_rule_wabstract
            + mirror_L_left_vertical_placement_rule_wabstract + mirror_L_right_vertical_placement_rule_wabstract + mirror_L_above_vertical_placement_rule_wabstract + mirror_L_below_vertical_placement_rule_wabstract
            + horizontal_left_vertical_placement_rule_wabstract + horizontal_right_vertical_placement_rule_wabstract + horizontal_above_vertical_placement_rule_wabstract + horizontal_below_vertical_placement_rule_wabstract 
        )
    )

def init_abstract_participant_construction_rules(participant):
    global SHAPES

    d1 = participant.abstract_space
    io1 = d1.io
    io2 = d1.io
    response = d1.response

    #FIRST PLACEMENT RULES
    """
    1 1
    1
    """
    half_T_first_placement_rule_abstract = [(
            + io1.input_half_T ** response.yes

            + io1.target_half_T ** response.no
            + io1.target_mirror_L ** response.no
            + io1.target_vertical ** response.no
            + io1.target_horizontal ** response.no

            >>
            + io2.target_half_T ** response.latest
            + io2.stop ** response.no
            + io2.start ** response.yes
            + io2.left ** response.no
            + io2.right ** response.no
            + io2.below ** response.no
            + io2.above ** response.no
         )
    ]

    mirror_L_first_placement_rule_abstract = [
        (   
            + io1.input_mirror_L ** response.yes

            + io1.target_half_T ** response.no
            + io1.target_mirror_L ** response.no
            + io1.target_vertical ** response.no
            + io1.target_horizontal ** response.no
            >>
            + io2.target_mirror_L ** response.latest
            + io2.stop ** response.no
            + io2.start ** response.yes
            + io2.left ** response.no
            + io2.right ** response.no
            + io2.below ** response.no
            + io2.above ** response.no
        )
    ]
    """
      1
    1 1
    """

    horizontal_first_placement_rule_abstract = [
        ( 
                + io1.input_horizontal ** response.yes  

                + io1.target_half_T ** response.no
                + io1.target_mirror_L ** response.no
                + io1.target_vertical ** response.no
                + io1.target_horizontal ** response.no

                >>
                + io2.target_vertical ** response.latest
                + io2.stop ** response.no
                + io2.start ** response.yes
                + io2.left ** response.no
                + io2.right ** response.no
                + io2.below ** response.no
                + io2.above ** response.no  
            )
    ]

    vertical_first_placement_rule_abstract = [
        ( 
                + io1.input_vertical ** response.yes

                + io1.target_half_T ** response.no
                + io1.target_mirror_L ** response.no
                + io1.target_vertical ** response.no
                + io1.target_horizontal ** response.no
                >>
                + io2.target_horizontal ** response.latest
                + io2.stop ** response.no
                + io2.start ** response.yes
                + io2.left ** response.no
                + io2.right ** response.no
                + io2.below ** response.no
                + io2.above ** response.no
            )
    ]

    #SUBSEQUENCE PLACEMENT RULES
    half_T_left_of_horizontal_placement_rule_abstract = [
        (   # switcharoo: i want to place the half_T to the left of the horizontal
            + io1.input_half_T ** response.yes
            + io1.input_horizontal ** response.yes

            + io1[f"target_shape{'half_T' if switcharoo else 'horizontal'}"] ** response.no # half_T isnt already there
            + io1[f"target_shape{'horizontal' if switcharoo else 'half_T'}"] ** response.yes # but horizontal is

            >
            + io2[f"target_shape{'half_T' if switcharoo else 'horizontal'}"] ** response.latest
            + io2.start ** response.no
            + io2.stop ** response.no
            + io2.left ** (response.yes if switcharoo else response.no) # the relation is always in reference to the shape that is already in target
            + io2.right ** (response.no if switcharoo else response.yes)
            + io2.below ** response.no
            + io2.above ** (response.yes if switcharoo else response.no)
        )
        for switcharoo in (True, False)
    ]

    half_T_right_of_horizontal_placement_rule_abstract = [
        (
            +io1.input_half_T ** response.yes
            + io1.input_horizontal ** response.yes

            + io1[f"target_shape{'half_T' if switcharoo else 'horizontal'}"] ** response.no # half_T isnt already there
            + io1[f"target_shape{'horizontal' if switcharoo else 'half_T'}"] ** response.yes # but horizontal is

            >>
            + io2[f"target_shape{'half_T' if switcharoo else 'horizontal'}"] ** response.latest
            + io2.start ** response.no
            + io2.stop ** response.no
            + io2.left ** (response.no if switcharoo else response.yes) # the relation is always in reference to the shape that is already in target
            + io2.right ** (response.yes if switcharoo else response.no)
            + io2.below ** response.no
            + io2.above ** (response.no if switcharoo else response.yes)
        )
        for switcharoo in (True, False)
    ]

    half_T_below_horizontal_placement_rule_abstract = [
        (
            
            + io1.input_half_T ** response.yes
            + io1.input_horizontal ** response.yes

            + io1[f"target_shape{'half_T' if switcharoo else 'horizontal'}"] ** response.no # half_T isnt already there
            + io1[f"target_shape{'horizontal' if switcharoo else 'half_T'}"] ** response.yes # but horizontal is
            >>
            + io2[f"target_shape{'half_T' if switcharoo else 'horizontal'}"] ** response.latest
            + io2.start ** response.no
            + io2.stop ** response.no
            + io2.left ** response.no
            + io2.right ** response.no
            + io2.below ** (response.yes if switcharoo else response.no) # the relation is always in reference to the shape that is already in target
            + io2.above ** (response.no if switcharoo else response.yes)
        ) 
        for switcharoo in (True, False)
    ]

    half_T_above_horizontal_placement_rule_abstract = [
        (

            + io1.input_half_T ** response.yes
            + io1.input_horizontal ** response.yes

            + io1[f"target_shape{'half_T' if switcharoo else 'horizontal'}"] ** response.no # half_T isnt already there
            + io1[f"target_shape{'horizontal' if switcharoo else 'half_T'}"] ** response.yes # but horizontal is

            >>
            + io2[f"target_shape{'half_T' if switcharoo else 'horizontal'}"] ** response.latest
            + io2.start ** response.no
            + io2.stop ** response.no
            + io2.left ** response.no
            + io2.right ** response.no
            + io2.below ** (response.no if switcharoo else response.yes) # the relation is always in reference to the shape that is already in target
            + io2.above ** (response.yes if switcharoo else response.no)
        ) 
        for switcharoo in (True, False)
]

    half_T_left_vertical_placement_rule_abstract = [
        (
             
            + io1.input_half_T ** response.yes
            + io1.input_vertical ** response.yes

            + io1[f"target_shape{'half_T' if switcharoo else 'vertical'}"] ** response.no # half_T isnt already there
            + io1[f"target_shape{'vertical' if switcharoo else 'half_T'}"] ** response.yes # but vertical is
            >>
            + io2[f"target_shape{'half_T' if switcharoo else 'vertical'}"] ** response.latest
            + io2.start ** response.no
            + io2.stop ** response.no
            + io2.left ** (response.yes if switcharoo else response.no) # the relation is always in reference to the shape that is already in target
            + io2.right ** (response.no if switcharoo else response.yes)
            + io2.below ** response.no
            + io2.above ** (response.no if switcharoo else response.yes)
            )
            for switcharoo in (True, False)
    ]
    
    half_T_right_vertical_placement_rule_abstract = [
        (

            + io1.input_half_T ** response.yes
            + io1.input_vertical ** response.yes

            + io1[f"target_shape{'half_T' if switcharoo else 'vertical'}"] ** response.no # half_T isnt already there
            + io1[f"target_shape{'vertical' if switcharoo else 'half_T'}"] ** response.yes # but vertical is
            >>
            + io2[f"target_shape{'half_T' if switcharoo else 'vertical'}"] ** response.latest
            + io2.start ** response.no
            + io2.stop ** response.no
            + io2.left ** (response.no if switcharoo else response.yes) # the relation is always in reference to the shape that is already in target
            + io2.right ** (response.yes if switcharoo else response.no)
            + io2.below ** response.no
            + io2.above ** (response.no if switcharoo else response.yes)
        ) 
        for switcharoo in (True, False)
    ]
    
    half_T_below_vertical_placement_rule_abstract = [
        (
            + io1.input_half_T ** response.yes
            + io1.input_vertical ** response.yes

            + io1[f"target_shape{'half_T' if switcharoo else 'vertical'}"] ** response.no # half_T isnt already there
            + io1[f"target_shape{'vertical' if switcharoo else 'half_T'}"] ** response.yes # but vertical is
            >>
            + io2[f"target_shape{'half_T' if switcharoo else 'vertical'}"] ** response.latest
            + io2.start ** response.no
            + io2.stop ** response.no
            + io2.left ** (response.no if switcharoo else response.yes) # the relation is always in reference to the shape that is already in target
            + io2.right ** (response.yes if switcharoo else response.no)
            + io2.below ** (response.yes if switcharoo else response.no)
            + io2.above ** (response.no if switcharoo else response.yes)
            ) 
            for switcharoo in (True, False)
    ]

    half_T_above_vertical_placement_rule_abstract = [
        (

            + io1.input_half_T ** response.yes
            + io1.input_vertical ** response.yes

            + io1[f"target_shape{'half_T' if switcharoo else 'vertical'}"] ** response.no # half_T isnt already there
            + io1[f"target_shape{'vertical' if switcharoo else 'half_T'}"] ** response.yes # but vertical is
            >>
            + io2[f"target_shape{'half_T' if switcharoo else 'vertical'}"] ** response.latest
            + io2.start ** response.no
            + io2.stop ** response.no
            + io2.left ** (response.no if switcharoo else response.yes) # the relation is always in reference to the shape that is already in target
            + io2.right ** (response.yes if switcharoo else response.no)
            + io2.below ** (response.no if switcharoo else response.yes)
            + io2.above ** (response.yes if switcharoo else response.no)
            ) 
            for switcharoo in (True, False)
    ]

    half_T_left_mirror_L_placement_rule_abstract = [
        (
            
            + io1.input_half_T ** response.yes
            + io1.input_mirror_L ** response.yes

            + io1[f"target_shape{'half_T' if switcharoo else 'mirror_L'}"] ** response.no # half_T isnt already there
            + io1[f"target_shape{'mirror_L' if switcharoo else 'half_T'}"] ** response.yes # but mirror_L is
            >>
            + io2[f"target_shape{'half_T' if switcharoo else 'mirror_L'}"] ** response.latest
            + io2.start ** response.no
            + io2.stop ** response.no
            + io2.left ** (response.yes if switcharoo else response.no) # the relation is always in reference to the shape that is already in target
            + io2.right ** (response.no if switcharoo else response.yes)
            + io2.below ** response.no
            + io2.above ** response.no
        )
        for switcharoo in (True, False)
    ]
    
    half_T_right_mirror_L_placement_rule_abstract = [
        (
           + io1.input_half_T ** response.yes
            + io1.input_mirror_L ** response.yes

            + io1[f"target_shape{'half_T' if switcharoo else 'mirror_L'}"] ** response.no # half_T isnt already there
            + io1[f"target_shape{'mirror_L' if switcharoo else 'half_T'}"] ** response.yes # but mirror_L is
            >>
            + io2[f"target_shape{'half_T' if switcharoo else 'mirror_L'}"] ** response.latest
            + io2.start ** response.no
            + io2.stop ** response.no
            + io2.left ** (response.no if switcharoo else response.yes) # the relation is always in reference to the shape that is already in target
            + io2.right ** (response.yes if switcharoo else response.no)
            + io2.below ** response.no
            + io2.above ** response.no
        ) 
        for switcharoo in (True, False)
    ]
    
    half_T_below_mirror_L_placement_rule_abstract = [
        (
            
            +io1.input_half_T ** response.yes
            + io1.input_mirror_L ** response.yes

            + io1[f"target_shape{'half_T' if switcharoo else 'mirror_L'}"] ** response.no # half_T isnt already there
            + io1[f"target_shape{'mirror_L' if switcharoo else 'half_T'}"] ** response.yes # but mirror_L is
            >>
            + io2[f"target_shape{'half_T' if switcharoo else 'mirror_L'}"] ** response.latest
            + io2.start ** response.no
            + io2.stop ** response.no
            + io2.left ** response.no
            + io2.right ** response.no
            + io2.below ** (response.yes if switcharoo else response.no) # the relation is always in reference to the shape that is already in target
            + io2.above ** (response.no if switcharoo else response.yes)
        )
        for switcharoo in (True, False)
    ]

    half_T_above_mirror_L_placement_rule_abstract = [
        (
            + io1.input_half_T ** response.yes
            + io1.input_mirror_L ** response.yes

            + io1[f"target_shape{'half_T' if switcharoo else 'mirror_L'}"] ** response.no # half_T isnt already there
            + io1[f"target_shape{'mirror_L' if switcharoo else 'half_T'}"] ** response.yes # but mirror_L is
            >>
            + io2[f"target_shape{'half_T' if switcharoo else 'mirror_L'}"] ** response.latest
            + io2.start ** response.no
            + io2.stop ** response.no
            + io2.left ** response.no
            + io2.right ** response.no
            + io2.below ** (response.no if switcharoo else response.yes) # the relation is always in reference to the shape that is already in target
            + io2.above ** (response.yes if switcharoo else response.no)
        ) 
        for switcharoo in (True, False)
    ]

    mirror_L_left_horizontal_placement_rule_abstract  = [
        (
            
            + io1.input_mirror_L ** response.yes
            + io1.input_horizontal ** response.yes

            + io1[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}"] ** response.no # mirror_L isnt already there
            + io1[f"target_shape{'horizontal' if switcharoo else 'mirror_L'}"] ** response.yes # but horizontal is
            >>
            + io2[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}"] ** response.latest
            + io2.start ** response.no
            + io2.stop ** response.no
            + io2.left ** (response.yes if switcharoo else response.no) # the relation is always in reference to the shape that is already in target
            + io2.right ** (response.no if switcharoo else response.yes)
            + io2.below ** response.no
            + io2.above ** response.no
            ) 
            for switcharoo in (True, False)
    ]

    mirror_L_right_horizontal_placement_rule_abstract = [
        (
            + io1.input_mirror_L ** response.yes
            + io1.input_horizontal ** response.yes

            + io1[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}"] ** response.no # mirror_L isnt already there
            + io1[f"target_shape{'horizontal' if switcharoo else 'mirror_L'}"] ** response.yes # but horizontal is
            >>
            + io2[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}"] ** response.latest
            + io2.start ** response.no
            + io2.stop ** response.no
            + io2.left ** (response.no if switcharoo else response.yes) # the relation is always in reference to the shape that is already in target
            + io2.right ** (response.yes if switcharoo else response.no)
            + io2.below ** response.no
            + io2.above ** response.no
        ) 
        for switcharoo in (True, False)
    ]

    mirror_L_above_horizontal_placement_rule_abstract = [
        (
            
            + io1.input_mirror_L ** response.yes
            + io1.input_horizontal ** response.yes

            + io1[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}"] ** response.no # mirror_L isnt already there
            + io1[f"target_shape{'horizontal' if switcharoo else 'mirror_L'}"] ** response.yes # but horizontal is

            >>
            + io2[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}"] ** response.latest
            + io2.start ** response.no
            + io2.stop ** response.no
            + io2.left ** response.no
            + io2.right ** response.no
            + io2.below ** (response.no if switcharoo else response.yes) # the relation is always in reference to the shape that is already in target
            + io2.above ** (response.yes if switcharoo else response.no)
            )
            for switcharoo in (True, False) 
    ]

    mirror_L_below_horizontal_placement_rule_abstract = [
        (
            
            + io1.input_mirror_L ** response.yes
            + io1.input_horizontal ** response.yes

            + io1[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}"] ** response.no # mirror_L isnt already there
            + io1[f"target_shape{'horizontal' if switcharoo else 'mirror_L'}"] ** response.yes # but horizontal is
            >>
            + io2[f"target_shape{'mirror_L' if switcharoo else 'horizontal'}"] ** response.latest
            + io2.start ** response.no
            + io2.stop ** response.no
            + io2.left ** response.no
            + io2.right ** response.no
            + io2.below ** (response.no if switcharoo else response.yes) # the relation is always in reference to the shape that is already in target
            + io2.above ** (response.yes if switcharoo else response.no)
            ) 
            for switcharoo in (True, False)
    ]

    mirror_L_left_vertical_placement_rule_abstract  = [
        (
             
            + io1.input_mirror_L ** response.yes
            + io1.input_vertical ** response.yes

            + io1[f"target_shape{'mirror_L' if switcharoo else 'vertical'}"] ** response.no # mirror_L isnt already there
            + io1[f"target_shape{'vertical' if switcharoo else 'mirror_L'}"] ** response.yes # but vertical is
            >>
            + io2[f"target_shape{'mirror_L' if switcharoo else 'vertical'}"] ** response.latest
            + io2.start ** response.no
            + io2.stop ** response.no
            + io2.left ** (response.yes if switcharoo else response.no) # the relation is always in reference to the shape that is already in target
            + io2.right ** (response.no if switcharoo else response.yes)
            + io2.below ** response.no
            + io2.above ** response.no
            ) 
            for switcharoo in (True, False)
    ]

    mirror_L_right_vertical_placement_rule_abstract = [
        (
            
            + io1.input_mirror_L ** response.yes
            + io1.input_vertical ** response.yes

            + io1[f"target_shape{'mirror_L' if switcharoo else 'vertical'}"] ** response.no # mirror_L isnt already there
            + io1[f"target_shape{'vertical' if switcharoo else 'mirror_L'}"] ** response.yes # but vertical is
            >>
            + io2[f"target_shape{'mirror_L' if switcharoo else 'vertical'}"] ** response.latest
            + io2.start ** response.no
            + io2.stop ** response.no
            + io2.left ** (response.no if switcharoo else response.yes) # the relation is always in reference to the shape that is already in target
            + io2.right ** (response.yes if switcharoo else response.no)
            + io2.below ** response.no
            + io2.above ** response.no
            )
            for switcharoo in (True, False)
    ]

    mirror_L_above_vertical_placement_rule_abstract = [
        (
            
            + io1.input_mirror_L ** response.yes
            + io1.input_vertical ** response.yes

            + io1[f"target_shape{'mirror_L' if switcharoo else 'vertical'}"] ** response.no # mirror_L isnt already there
            + io1[f"target_shape{'vertical' if switcharoo else 'mirror_L'}"] ** response.yes # but vertical is
            >>
            + io1[f"target_shape{'mirror_L' if switcharoo else 'vertical'}"] ** response.latest
            + io2.start ** response.no
            + io2.stop ** response.no
            + io2.left ** response.no
            + io2.right ** response.no
            + io2.below ** (response.no if switcharoo else response.yes) # the relation is always in reference to the shape that is already in target
            + io2.above ** (response.yes if switcharoo else response.no)
        )
        for switcharoo in (True, False)
    ]

    mirror_L_below_vertical_placement_rule_abstract = [
        (
            
            + io1.input_mirror_L ** response.yes
            + io1.input_vertical ** response.yes

            + io1[f"target_shape{'mirror_L' if switcharoo else 'vertical'}"] ** response.no # mirror_L isnt already there
            + io1[f"target_shape{'vertical' if switcharoo else 'mirror_L'}"] ** response.yes # but vertical is
            >>
            + io2[f"target_shape{'mirror_L' if switcharoo else 'vertical'}"] ** response.latest
            + io2.start ** response.no
            + io2.stop ** response.no
            + io2.left ** response.no
            + io2.right ** response.no
            + io2.below ** (response.yes if switcharoo else response.no) # the relation is always in reference to the shape that is already in target
            + io2.above ** (response.no if switcharoo else response.yes)
            )
            for switcharoo in (True, False)
    ]

    horizontal_left_vertical_placement_rule_abstract  = [
        (
           + io1.input_horizontal ** response.yes
            + io1.input_vertical ** response.yes

            + io1[f"target_shape{'horizontal' if switcharoo else 'vertical'}"] ** response.no # horizontal isnt already there
            + io1[f"target_shape{'vertical' if switcharoo else 'horizontal'}"] ** response.yes # but vertical is
            >>
            + io2[f"target_shape{'horizontal' if switcharoo else 'vertical'}"] ** response.latest
            + io2.start ** response.no
            + io2.stop ** response.no
            + io2.left ** (response.yes if switcharoo else response.no) # the relation is always in reference to the shape that is already in target
            + io2.right ** (response.no if switcharoo else response.yes)
            + io2.below ** response.no
            + io2.above ** response.no
            ) 
            for switcharoo in (True, False)
    ]

    horizontal_right_vertical_placement_rule_abstract = [
        (
            + io1.input_horizontal ** response.yes
            + io1.input_vertical ** response.yes

            + io1[f"target_shape{'horizontal' if switcharoo else 'vertical'}"] ** response.no # horizontal isnt already there
            + io1[f"target_shape{'vertical' if switcharoo else 'horizontal'}"] ** response.yes # but vertical is
            >>
            + io2[f"target_shape{'horizontal' if switcharoo else 'vertical'}"] ** response.latest
            + io2.start ** response.no
            + io2.stop ** response.no
            + io2.left ** (response.no if switcharoo else response.yes) # the relation is always in reference to the shape that is already in target
            + io2.right ** (response.yes if switcharoo else response.no)
            + io2.below ** response.no
            + io2.above ** response.no
            ) 
            for switcharoo in (True, False)
    ]

    horizontal_above_vertical_placement_rule_abstract = [
        (
            + io1.input_horizontal ** response.yes
            + io1.input_vertical ** response.yes

            + io1[f"target_shape{'horizontal' if switcharoo else 'vertical'}"] ** response.no # horizontal isnt already there
            + io1[f"target_shape{'vertical' if switcharoo else 'horizontal'}"] ** response.yes # but vertical is
            >>
            + io2[f"target_shape{'horizontal' if switcharoo else 'vertical'}"] ** response.latest
            + io2.start ** response.no
            + io2.stop ** response.no
            + io2.left ** response.no
            + io2.right ** response.no
            + io2.below ** (response.no if switcharoo else response.yes) # the relation is always in reference to the shape that is already in target
            + io2.above ** (response.yes if switcharoo else response.no)
        ) 
        for switcharoo in (True, False)
    ]

    horizontal_below_vertical_placement_rule_abstract = [
        (
           + io1.input_horizontal ** response.yes
            + io1.input_vertical ** response.yes

            + io1[f"target_shape{'horizontal' if switcharoo else 'vertical'}"] ** response.no # horizontal isnt already there
            + io1[f"target_shape{'vertical' if switcharoo else 'horizontal'}"] ** response.yes # but vertical is
            >>
            + io2[f"target_shape{'horizontal' if switcharoo else 'vertical'}"] ** response.latest
            + io2.start ** response.no
            + io2.stop ** response.no
            + io2.left ** response.no
            + io2.right ** response.no
            + io2.below ** (response.yes if switcharoo else response.no) # the relation is always in reference to the shape that is already in target
            + io2.above ** (response.no if switcharoo else response.yes)
        )
            for switcharoo in (True, False)
    ]

    # END PLACEMENT RULES
    stop_construction_rule_all_four_abstract = [
        io1.target_shape_horizontal ** response.yes
        + io1.target_shape_vertical ** response.yes
        + io1.target_shape_half_T ** response.yes
        + io1.target_shape_mirror_L ** response.yes
        >>
        io2.stop ** response.yes
        + io2.start ** response.no

        + io2.left ** response.no
        + io2.right ** response.no
        + io2.below ** response.no
        + io2.above ** response.no
    ]

    stop_construction_rule_one_only_abstract = [
        (
            + io1[f"input_{shape}"] ** response.yes
            + io1[f"input_{(SHAPES[:i] + SHAPES[i+1:])[0]}"] ** response.no
            + io1[f"input_{(SHAPES[:i] + SHAPES[i+1:])[1]}"] ** response.no
            + io1[f"input_{(SHAPES[:i] + SHAPES[i+1:])[2]}"] ** response.no

            + io1[f"target_{shape}"] ** response.yes
            + io1[f"target_{(SHAPES[:i] + SHAPES[i+1:])[0]}"] ** response.no
            + io1[f"target_{(SHAPES[:i] + SHAPES[i+1:])[1]}"] ** response.no
            + io1[f"target_{(SHAPES[:i] + SHAPES[i+1:])[2]}"] ** response.no

            >>
            + io2.stop ** response.yes
            + io2.start ** response.no
            + io2.left ** response.no
            + io2.right ** response.no
            + io2.below ** response.no

        )
        for i, shape in enumerate(SHAPES)
    ]

    stop_construction_rule_two_only_abstract = [
        (
            + io1[f"input_{shape}"] ** response.yes
            + io1[f"input_{other_shape}"] ** response.yes
            + io1[f"input_{[s for s in SHAPES if s not in (shape, other_shape)][0]}"] ** response.no
            + io1[f"input_{[s for s in SHAPES if s not in (shape, other_shape)][1]}"] ** response.no

            + io1[f"target_{shape}"] ** response.yes
            + io1[f"target_{other_shape}"] ** response.yes
            + io1[f"target_{[s for s in SHAPES if s not in (shape, other_shape)][0]}"] ** response.no
            + io1[f"target_{[s for s in SHAPES if s not in (shape, other_shape)][1]}"] ** response.no

            >>
            + io2.stop ** response.yes
            + io2.start ** response.no
            + io2.left ** response.no
            + io2.right ** response.no
            + io2.below ** response.no
        )

        for (shape, other_shape) in itertools.combinations(SHAPES, 2)
    ]

    stop_construction_rule_three_only_abstract = [
        (
            + io1[f"input_{shape}"] ** response.yes
            + io1[f"input_{other_shape}"] ** response.yes
            + io1[f"input_{other_other_shape}"] ** response.yes
            + io1[f"input_{[s for s in SHAPES if s not in (shape, other_shape, other_other_shape)][0]}"] ** response.no

            + io1[f"target_{shape}"] ** response.yes
            + io1[f"target_{other_shape}"] ** response.yes
            + io1[f"target_{other_other_shape}"] ** response.yes
            + io1[f"target_{[s for s in SHAPES if s not in (shape, other_shape, other_other_shape)][0]}"] ** response.no

            >>
            + io2.stop ** response.yes
            + io2.start ** response.no
            + io2.left ** response.no
            + io2.right ** response.no
            + io2.below ** response.no
        )

        for (shape, other_shape, other_other_shape) in itertools.combinations(SHAPES, 3)
    ]

    # combine rules
    participant.construction_abstract_rule.rules.compile(
        *[half_T_first_placement_rule_abstract + mirror_L_first_placement_rule_abstract + vertical_first_placement_rule_abstract + horizontal_first_placement_rule_abstract
            + half_T_left_mirror_L_placement_rule_abstract + half_T_right_mirror_L_placement_rule_abstract + half_T_below_mirror_L_placement_rule_abstract + half_T_above_mirror_L_placement_rule_abstract
            + half_T_left_of_horizontal_placement_rule_abstract + half_T_right_of_horizontal_placement_rule_abstract + half_T_above_horizontal_placement_rule_abstract + half_T_below_horizontal_placement_rule_abstract
            + half_T_left_vertical_placement_rule_abstract + half_T_right_vertical_placement_rule_abstract + half_T_above_vertical_placement_rule_abstract + half_T_below_vertical_placement_rule_abstract
            + mirror_L_left_horizontal_placement_rule_abstract + mirror_L_right_horizontal_placement_rule_abstract + mirror_L_above_horizontal_placement_rule_abstract + mirror_L_below_horizontal_placement_rule_abstract
            + mirror_L_left_vertical_placement_rule_abstract + mirror_L_right_vertical_placement_rule_abstract + mirror_L_above_vertical_placement_rule_abstract + mirror_L_below_vertical_placement_rule_abstract
            + horizontal_left_vertical_placement_rule_abstract + horizontal_right_vertical_placement_rule_abstract + horizontal_above_vertical_placement_rule_abstract + horizontal_below_vertical_placement_rule_abstract
            + stop_construction_rule_all_four_abstract + stop_construction_rule_one_only_abstract + stop_construction_rule_two_only_abstract + stop_construction_rule_three_only_abstract        
        ]
    )

