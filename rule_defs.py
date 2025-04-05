from pyClarion import (Agent, Input, Choice, ChunkStore, FixedRules, 
    Family, Atoms, Atom, BaseLevel, Pool, NumDict, Event, Priority)

from typing import *
import math

def init_participant_response_rules(participant) -> None:
    d = participant.response_space
    io = d.io
    bricks = d.bricks
    grid_rows = d.grid_rows
    grid_cols = d.grid_cols
    query_rel = d.query_rel
    response = d.response

    #response rules when given a query and some blocks
    
    # HALF_T X HORIZONTAL
    #i = 0, horizontal is next to the potruding part of the shape, else it is next to the flat part at the bottom
    half_T_left_of_horizontal = [
        (+ io.query_block ** (bricks.half_T if not switcharoo else bricks.horizontal)
        + io.query_block_reference ** (bricks.horizontal if not switcharoo else bricks.half_T)
        + io.query_relation ** (query_rel.left if not switcharoo else query_rel.right)
        + io.target_shape1 ** bricks.half_T
        + io.target_shape4 ** bricks.horizontal
        + io.target_shape1_row1 ** grid_rows[f"r{row}"]
        + io.target_shape1_row2 ** grid_rows[f"r{row}"]
        + io.target_shape1_row3 ** grid_rows[f"r{row+1}"]
        + io.target_shape1_col1 ** grid_cols[f"c{col}"]
        + io.target_shape1_col2 ** grid_cols[f"c{col+1}"]
        + io.target_shape1_col3 ** grid_cols[f"c{col}"]
        + io.target_shape4_row1 ** grid_rows[f"r{row+i}"]
        + io.target_shape4_row2 ** grid_rows[f"r{row+i}"]
        + io.target_shape4_row3 ** grid_rows[f"r{row+i}"]
        + io.target_shape4_col1 ** grid_cols[f"c{col+2-i}"]
        + io.target_shape4_col2 ** grid_cols[f"c{col+3-i}"]
        + io.target_shape4_col3 ** grid_cols[f"c{col+4-i}"]
        >>
        + io.output ** response.yes) for switcharoo in (True, False) for i in range(2) for row in range(1, 6) for col in range(1, 3 + i)
    ]

    half_T_right_of_horizontal = [
        (+ io.query_block ** (bricks.half_T if not switcharoo else bricks.horizontal)
        + io.query_block_reference ** (bricks.horizontal if not switcharoo else bricks.half_T)
        + io.query_relation ** (query_rel.right if not switcharoo else query_rel.left)
        + io.target_shape1 ** bricks.half_T
        + io.target_shape4 ** bricks.horizontal
        + io.target_shape1_row1 ** grid_rows[f"r{row}"]
        + io.target_shape1_row2 ** grid_rows[f"r{row}"]
        + io.target_shape1_row3 ** grid_rows[f"r{row+1}"]
        + io.target_shape1_col1 ** grid_cols[f"c{col}"]
        + io.target_shape1_col2 ** grid_cols[f"c{col+1}"]
        + io.target_shape1_col3 ** grid_cols[f"c{col}"]
        + io.target_shape4_row1 ** grid_rows[f"r{row+i}"]
        + io.target_shape4_row2 ** grid_rows[f"r{row+i}"]
        + io.target_shape4_row3 ** grid_rows[f"r{row+i}"]
        + io.target_shape4_col1 ** grid_cols[f"c{col-3}"]
        + io.target_shape4_col2 ** grid_cols[f"c{col-2}"]
        + io.target_shape4_col3 ** grid_cols[f"c{col-1}"]
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
        + io.target_shape1 ** bricks.half_T
        + io.target_shape4 ** bricks.horizontal
        + io.target_shape1_row1 ** grid_rows[f"r{row}"]
        + io.target_shape1_row2 ** grid_rows[f"r{row}"]
        + io.target_shape1_row3 ** grid_rows[f"r{row+1}"]
        + io.target_shape1_col1 ** grid_cols[f"c{col}"]
        + io.target_shape1_col2 ** grid_cols[f"c{col+1}"]
        + io.target_shape1_col3 ** grid_cols[f"c{col}"]
        + io.target_shape4_row1 ** grid_rows[f"r{row-1}"]
        + io.target_shape4_row2 ** grid_rows[f"r{row-1}"]
        + io.target_shape4_row3 ** grid_rows[f"r{row-1}"]
        + io.target_shape4_col1 ** grid_cols[f"c{col-1+i}"]
        + io.target_shape4_col2 ** grid_cols[f"c{col+i}"]
        + io.target_shape4_col3 ** grid_cols[f"c{col+1+i}"]
        >>
        + io.output ** response.yes) for switcharoo in (True, False) for i in range(3) for row in range(2, 6) for col in range(1 + (i == 0), 6-i)
    ]

    half_T_above_horizontal = [
        (+ io.query_block ** (bricks.half_T if not switcharoo else bricks.horizontal)
        + io.query_block_reference ** (bricks.horizontal if not switcharoo else bricks.half_T)
        + io.query_relation ** (query_rel.above if not switcharoo else query_rel.below)
        + io.target_shape1 ** bricks.half_T
        + io.target_shape4 ** bricks.horizontal
        + io.target_shape1_row1 ** grid_rows[f"r{row}"]
        + io.target_shape1_row2 ** grid_rows[f"r{row}"]
        + io.target_shape1_row3 ** grid_rows[f"r{row+1}"]
        + io.target_shape1_col1 ** grid_cols[f"c{col}"]
        + io.target_shape1_col2 ** grid_cols[f"c{col+1}"]
        + io.target_shape1_col3 ** grid_cols[f"c{col}"]
        + io.target_shape4_row1 ** grid_rows[f"r{row+2}"]
        + io.target_shape4_row2 ** grid_rows[f"r{row+2}"]
        + io.target_shape4_row3 ** grid_rows[f"r{row+2}"]
        + io.target_shape4_col1 ** grid_cols[f"c{col-2+i}"]
        + io.target_shape4_col2 ** grid_cols[f"c{col-1+i}"]
        + io.target_shape4_col3 ** grid_cols[f"c{col+i}"]
        >>
        + io.output ** response.yes) for i in range(3) for switcharoo in (True, False) for row in range(1, 5) for col in range(3-i, 6-(i==2))
]

    #HALF_T X VERTICAL

    half_T_left_vertical = [
        (+ io.query_block ** (bricks.half_T if not switcharoo else bricks.vertical)
        + io.query_block_reference ** (bricks.vertical if not switcharoo else bricks.half_T)
        + io.query_relation ** (query_rel.left if not switcharoo else query_rel.right)
        + io.target_shape1 ** bricks.half_T
        + io.target_shape3 ** bricks.vertical
        + io.target_shape1_row1 ** grid_rows[f"r{row}"]
        + io.target_shape1_row2 ** grid_rows[f"r{row}"]
        + io.target_shape1_row3 ** grid_rows[f"r{row+1}"]
        + io.target_shape1_col1 ** grid_cols[f"c{col}"]
        + io.target_shape1_col2 ** grid_cols[f"c{col+1}"]
        + io.target_shape1_col3 ** grid_cols[f"c{col}"]
        + io.target_shape3_row1 ** grid_rows[f"r{row+1-i}"]
        + io.target_shape3_row2 ** grid_rows[f"r{row+2-i}"]
        + io.target_shape3_row3 ** grid_rows[f"r{row+3-i}"]
        + io.target_shape3_col1 ** grid_cols[f"c{col+2- (i == 0)}"]
        + io.target_shape3_col2 ** grid_cols[f"c{col+2 - (i == 0)}"]
        + io.target_shape3_col3 ** grid_cols[f"c{col+2 - (i == 0)}"]
        >>
        + io.output ** response.yes) for switcharoo in (True, False) for i in range(4) for row in range(1+(i-1 if i > 1 else 0), 4 + (math.ceil(i/2))) for col in range(1, 6-(i > 0))
    ]

    half_T_right_vertical = [
        (+ io.query_block ** (bricks.half_T if not switcharoo else bricks.vertical)
        + io.query_block_reference ** (bricks.vertical if not switcharoo else bricks.half_T)
        + io.query_relation ** (query_rel.right if not switcharoo else query_rel.left)
        + io.target_shape1 ** bricks.half_T
        + io.target_shape3 ** bricks.vertical
        + io.target_shape1_row1 ** grid_rows[f"r{row}"]
        + io.target_shape1_row2 ** grid_rows[f"r{row}"]
        + io.target_shape1_row3 ** grid_rows[f"r{row+1}"]
        + io.target_shape1_col1 ** grid_cols[f"c{col}"]
        + io.target_shape1_col2 ** grid_cols[f"c{col+1}"]
        + io.target_shape1_col3 ** grid_cols[f"c{col}"]
        + io.target_shape3_row1 ** grid_rows[f"r{row-2+i}"]
        + io.target_shape3_row2 ** grid_rows[f"r{row-1+i}"]
        + io.target_shape3_row3 ** grid_rows[f"r{row+i}"]
        + io.target_shape3_col1 ** grid_cols[f"c{col-1}"]
        + io.target_shape3_col2 ** grid_cols[f"c{col-1}"]
        + io.target_shape3_col3 ** grid_cols[f"c{col-1}"]
        >>
        + io.output ** response.yes) for switcharoo in (True, False) for i in range(4) for row in range(max(1, 3-i), 6-max(0, i-1)) for col in range(2, 6)
    ]

    half_T_below_vertical = [
        (+ io.query_block ** (bricks.half_T if not switcharoo else bricks.vertical)
        + io.query_block_reference ** (bricks.vertical if not switcharoo else bricks.half_T)
        + io.query_relation ** (query_rel.below if not switcharoo else query_rel.above)
        + io.target_shape1 ** bricks.half_T
        + io.target_shape3 ** bricks.vertical
        + io.target_shape1_row1 ** grid_rows[f"r{row}"]
        + io.target_shape1_row2 ** grid_rows[f"r{row}"]
        + io.target_shape1_row3 ** grid_rows[f"r{row+1}"]
        + io.target_shape1_col1 ** grid_cols[f"c{col}"]
        + io.target_shape1_col2 ** grid_cols[f"c{col+1}"]
        + io.target_shape1_col3 ** grid_cols[f"c{col}"]
        + io.target_shape3_row1 ** grid_rows[f"r{row-3}"]
        + io.target_shape3_row2 ** grid_rows[f"r{row-2}"]
        + io.target_shape3_row3 ** grid_rows[f"r{row-3}"]
        + io.target_shape3_col1 ** grid_cols[f"c{col+i}"]
        + io.target_shape3_col2 ** grid_cols[f"c{col+i}"]
        + io.target_shape3_col3 ** grid_cols[f"c{col+i}"]
        >>
        + io.output ** response.yes) for switcharoo in (True, False) for i in range(2) for row in range(4, 6) for col in range(1, 6)
    ]

    half_T_above_vertical = [
        (+ io.query_block ** (bricks.half_T if not switcharoo else bricks.vertical)
        + io.query_block_reference ** (bricks.vertical if not switcharoo else bricks.half_T)
        + io.query_relation ** (query_rel.above if not switcharoo else query_rel.below)
        + io.target_shape1 ** bricks.half_T
        + io.target_shape3 ** bricks.vertical
        + io.target_shape1_row1 ** grid_rows[f"r{row}"]
        + io.target_shape1_row2 ** grid_rows[f"r{row}"]
        + io.target_shape1_row3 ** grid_rows[f"r{row+1}"]
        + io.target_shape1_col1 ** grid_cols[f"c{col}"]
        + io.target_shape1_col2 ** grid_cols[f"c{col+1}"]
        + io.target_shape1_col3 ** grid_cols[f"c{col}"]
        + io.target_shape3_row1 ** grid_rows[f"r{row+1}"]
        + io.target_shape3_row2 ** grid_rows[f"r{row+2}"]
        + io.target_shape3_row3 ** grid_rows[f"r{row+3}"]
        + io.target_shape3_col1 ** grid_cols[f"c{col}"]
        + io.target_shape3_col2 ** grid_cols[f"c{col}"]
        + io.target_shape3_col3 ** grid_cols[f"c{col}"]
        >>
        + io.output ** response.yes) for switcharoo in (True, False) for row in range(1, 3) for col in range(1, 6)
    ]

    #HALF_T X MIRROR_L
    half_T_left_mirror_L = [
        (+ io.query_block ** (bricks.half_T if not switcharoo else bricks.mirror_L)
        + io.query_block_reference ** (bricks.mirror_L if not switcharoo else bricks.half_T)
        + io.query_relation ** (query_rel.left if not switcharoo else query_rel.right)
        + io.target_shape1 ** bricks.half_T
        + io.target_shape2 ** bricks.mirror_L
        + io.target_shape1_row1 ** grid_rows[f"r{row}"]
        + io.target_shape1_row2 ** grid_rows[f"r{row}"]
        + io.target_shape1_row3 ** grid_rows[f"r{row+1}"]
        + io.target_shape1_col1 ** grid_cols[f"c{col}"]
        + io.target_shape1_col2 ** grid_cols[f"c{col+1}"]
        + io.target_shape1_col3 ** grid_cols[f"c{col}"]
        + io.target_shape2_row1 ** grid_rows[f"r{row-i}"]
        + io.target_shape2_row2 ** grid_rows[f"r{row+1-i}"]
        + io.target_shape2_row3 ** grid_rows[f"r{row+1-i}"]
        + io.target_shape2_col1 ** grid_cols[f"c{col+2+i}"]
        + io.target_shape2_col2 ** grid_cols[f"c{col+1+i}"]
        + io.target_shape2_col3 ** grid_cols[f"c{col+2+i}"]
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
        + io.target_shape1 ** bricks.half_T
        + io.target_shape2 ** bricks.mirror_L
        + io.target_shape1_row1 ** grid_rows[f"r{row}"]
        + io.target_shape1_row2 ** grid_rows[f"r{row}"]
        + io.target_shape1_row3 ** grid_rows[f"r{row+1}"]
        + io.target_shape1_col1 ** grid_cols[f"c{col}"]
        + io.target_shape1_col2 ** grid_cols[f"c{col+1}"]
        + io.target_shape1_col3 ** grid_cols[f"c{col}"]
        + io.target_shape2_row1 ** grid_rows[f"r{row + (-1 if i== 0 else 1)*(i%2 == 0)}"] # 1 up, no up, 1 down.
        + io.target_shape2_row2 ** grid_rows[f"r{row + i}"]
        + io.target_shape2_row3 ** grid_rows[f"r{row+i}"]
        + io.target_shape2_col1 ** grid_cols[f"c{col-1}"]
        + io.target_shape2_col2 ** grid_cols[f"c{col-2}"]
        + io.target_shape2_col3 ** grid_cols[f"c{col-1}"]
        >>
        + io.output ** response.yes) for switcharoo in (True, False) for i in range(3) for row in range(1+(i==0), 6-(i==2)) for col in range(3, 6)
    ]

    half_T_below_mirror_L = [
        (+ io.query_block ** (bricks.half_T if not switcharoo else bricks.mirror_L)
        + io.query_block_reference ** (bricks.mirror_L if not switcharoo else bricks.half_T)
        + io.query_relation ** (query_rel.below if not switcharoo else query_rel.above)
        + io.target_shape1 ** bricks.half_T
        + io.target_shape2 ** bricks.mirror_L
        + io.target_shape1_row1 ** grid_rows[f"r{row}"]
        + io.target_shape1_row2 ** grid_rows[f"r{row}"]
        + io.target_shape1_row3 ** grid_rows[f"r{row+1}"]
        + io.target_shape1_col1 ** grid_cols[f"c{col}"]
        + io.target_shape1_col2 ** grid_cols[f"c{col+1}"]
        + io.target_shape1_col3 ** grid_cols[f"c{col}"]
        + io.target_shape2_row1 ** grid_rows[f"r{row-2}"]
        + io.target_shape2_row2 ** grid_rows[f"r{row-1}"]
        + io.target_shape2_row3 ** grid_rows[f"r{row-1}"]
        + io.target_shape2_col1 ** grid_cols[f"c{col+1+i}"]
        + io.target_shape2_col2 ** grid_cols[f"c{col+i}"]
        + io.target_shape2_col3 ** grid_cols[f"c{col+1+i}"]
        >>
        + io.output ** response.yes) for i in range(2) for switcharoo in (True, False) for row in range(3, 6) for col in range(1, 6-i)
    ]

    half_T_above_mirror_L = [
        (+ io.query_block ** (bricks.half_T if not switcharoo else bricks.mirror_L)
        + io.query_block_reference ** (bricks.mirror_L if not switcharoo else bricks.half_T)
        + io.query_relation ** (query_rel.above if not switcharoo else query_rel.below)
        + io.target_shape1 ** bricks.half_T
        + io.target_shape2 ** bricks.mirror_L
        + io.target_shape1_row1 ** grid_rows[f"r{row}"]
        + io.target_shape1_row2 ** grid_rows[f"r{row}"]
        + io.target_shape1_row3 ** grid_rows[f"r{row+1}"]
        + io.target_shape1_col1 ** grid_cols[f"c{col}"]
        + io.target_shape1_col2 ** grid_cols[f"c{col+1}"]
        + io.target_shape1_col3 ** grid_cols[f"c{col}"]
        + io.target_shape2_row1 ** grid_rows[f"r{row+2}"]
        + io.target_shape2_row2 ** grid_rows[f"r{row+3}"]
        + io.target_shape2_row3 ** grid_rows[f"r{row+3}"]
        + io.target_shape2_col1 ** grid_cols[f"c{col}"]
        + io.target_shape2_col2 ** grid_cols[f"c{col-1}"]
        + io.target_shape2_col3 ** grid_cols[f"c{col}"]
        >>
        + io.output ** response.yes) for switcharoo in (True, False) for row in range(1, 4) for col in range(2, 6)
    ]

    #MIRROR_L X HORIZONTAL
    mirror_L_left_horizontal  = [
        (+ io.query_block ** (bricks.mirror_L if not switcharoo else bricks.horizontal)
        + io.query_block_reference ** (bricks.horizontal if not switcharoo else bricks.mirror_L)
        + io.query_relation ** (query_rel.left if not switcharoo else query_rel.right)
        + io.target_shape2 ** bricks.mirror_L
        + io.target_shape4 ** bricks.horizontal
        + io.target_shape2_row1 ** grid_rows[f"r{row}"]
        + io.target_shape2_row2 ** grid_rows[f"r{row+1}"]
        + io.target_shape2_row3 ** grid_rows[f"r{row+1}"]
        + io.target_shape2_col1 ** grid_cols[f"c{col}"]
        + io.target_shape2_col2 ** grid_cols[f"c{col-1}"]
        + io.target_shape2_col3 ** grid_cols[f"c{col}"]
        + io.target_shape4_row1 ** grid_rows[f"r{row+i}"]
        + io.target_shape4_row2 ** grid_rows[f"r{row+i}"]
        + io.target_shape4_row3 ** grid_rows[f"r{row+i}"]
        + io.target_shape4_col1 ** grid_cols[f"c{col+1}"]
        + io.target_shape4_col2 ** grid_cols[f"c{col+2}"]
        + io.target_shape4_col3 ** grid_cols[f"c{col+3}"]
        >>
        + io.output ** response.yes) for switcharoo in (True, False) for i in range(2) for row in range(1, 6) for col in range(2, 4)
    ]

    mirror_L_right_horizontal = [
        (+ io.query_block ** (bricks.mirror_L if not switcharoo else bricks.horizontal)
        + io.query_block_reference ** (bricks.horizontal if not switcharoo else bricks.mirror_L)
        + io.query_relation ** (query_rel.right if not switcharoo else query_rel.left)
        + io.target_shape2 ** bricks.mirror_L
        + io.target_shape4 ** bricks.horizontal
        + io.target_shape2_row1 ** grid_rows[f"r{row}"]
        + io.target_shape2_row2 ** grid_rows[f"r{row+1}"]
        + io.target_shape2_row3 ** grid_rows[f"r{row+1}"]
        + io.target_shape2_col1 ** grid_cols[f"c{col}"]
        + io.target_shape2_col2 ** grid_cols[f"c{col-1}"]
        + io.target_shape2_col3 ** grid_cols[f"c{col}"]
        + io.target_shape4_row1 ** grid_rows[f"r{row+i}"]
        + io.target_shape4_row2 ** grid_rows[f"r{row+i}"]
        + io.target_shape4_row3 ** grid_rows[f"r{row+i}"]
        + io.target_shape4_col1 ** grid_cols[f"c{col-3-i}"]
        + io.target_shape4_col2 ** grid_cols[f"c{col-2-i}"]
        + io.target_shape4_col3 ** grid_cols[f"c{col-1-i}"]
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
        + io.target_shape2 ** bricks.mirror_L
        + io.target_shape4 ** bricks.horizontal
        + io.target_shape2_row1 ** grid_rows[f"r{row}"]
        + io.target_shape2_row2 ** grid_rows[f"r{row+1}"]
        + io.target_shape2_row3 ** grid_rows[f"r{row+1}"]
        + io.target_shape2_col1 ** grid_cols[f"c{col}"]
        + io.target_shape2_col2 ** grid_cols[f"c{col-1}"]
        + io.target_shape2_col3 ** grid_cols[f"c{col}"]
        + io.target_shape4_row1 ** grid_rows[f"r{row+2}"]
        + io.target_shape4_row2 ** grid_rows[f"r{row+2}"]
        + io.target_shape4_row3 ** grid_rows[f"r{row+2}"]
        + io.target_shape4_col1 ** grid_cols[f"c{col-2+i}"]
        + io.target_shape4_col2 ** grid_cols[f"c{col-1+i}"]
        + io.target_shape4_col3 ** grid_cols[f"c{col+i}"]
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
        + io.target_shape2 ** bricks.mirror_L
        + io.target_shape4 ** bricks.horizontal
        + io.target_shape2_row1 ** grid_rows[f"r{row}"]
        + io.target_shape2_row2 ** grid_rows[f"r{row+1}"]
        + io.target_shape2_row3 ** grid_rows[f"r{row+1}"]
        + io.target_shape2_col1 ** grid_cols[f"c{col}"]
        + io.target_shape2_col2 ** grid_cols[f"c{col-1}"]
        + io.target_shape2_col3 ** grid_cols[f"c{col}"]
        + io.target_shape4_row1 ** grid_rows[f"r{row-1}"]
        + io.target_shape4_row2 ** grid_rows[f"r{row-1}"]
        + io.target_shape4_row3 ** grid_rows[f"r{row-1}"]
        + io.target_shape4_col1 ** grid_cols[f"c{col-2+i}"]
        + io.target_shape4_col2 ** grid_cols[f"c{col-1+i}"]
        + io.target_shape4_col3 ** grid_cols[f"c{col+i}"]
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
        + io.target_shape2 ** bricks.mirror_L
        + io.target_shape3 ** bricks.vertical
        + io.target_shape2_row1 ** grid_rows[f"r{row}"]
        + io.target_shape2_row2 ** grid_rows[f"r{row+1}"]
        + io.target_shape2_row3 ** grid_rows[f"r{row+1}"]
        + io.target_shape2_col1 ** grid_cols[f"c{col}"]
        + io.target_shape2_col2 ** grid_cols[f"c{col-1}"]
        + io.target_shape2_col3 ** grid_cols[f"c{col}"]
        + io.target_shape3_row1 ** grid_rows[f"r{row-1+i}"]
        + io.target_shape3_row2 ** grid_rows[f"r{row+i}"]
        + io.target_shape3_row3 ** grid_rows[f"r{row+1+i}"]
        + io.target_shape3_col1 ** grid_cols[f"c{col+1}"]
        + io.target_shape3_col2 ** grid_cols[f"c{col+1}"]
        + io.target_shape3_col3 ** grid_cols[f"c{col+1}"]
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
        + io.target_shape2 ** bricks.mirror_L
        + io.target_shape3 ** bricks.vertical
        + io.target_shape2_row1 ** grid_rows[f"r{row}"]
        + io.target_shape2_row2 ** grid_rows[f"r{row+1}"]
        + io.target_shape2_row3 ** grid_rows[f"r{row+1}"]
        + io.target_shape2_col1 ** grid_cols[f"c{col}"]
        + io.target_shape2_col2 ** grid_cols[f"c{col-1}"]
        + io.target_shape2_col3 ** grid_cols[f"c{col}"]
        + io.target_shape3_row1 ** grid_rows[f"r{row+1-i}"]
        + io.target_shape3_row2 ** grid_rows[f"r{row+2-i}"]
        + io.target_shape3_row3 ** grid_rows[f"r{row+3-i}"]
        + io.target_shape3_col1 ** grid_cols[f"c{col-2 + (i == 3)}"]
        + io.target_shape3_col2 ** grid_cols[f"c{col-2 + (i == 3)}"]
        + io.target_shape3_col3 ** grid_cols[f"c{col-2 + (i == 3)}"]
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
        + io.target_shape2 ** bricks.mirror_L
        + io.target_shape3 ** bricks.vertical
        + io.target_shape2_row1 ** grid_rows[f"r{row}"]
        + io.target_shape2_row2 ** grid_rows[f"r{row+1}"]
        + io.target_shape2_row3 ** grid_rows[f"r{row+1}"]
        + io.target_shape2_col1 ** grid_cols[f"c{col}"]
        + io.target_shape2_col2 ** grid_cols[f"c{col-1}"]
        + io.target_shape2_col3 ** grid_cols[f"c{col}"]
        + io.target_shape3_row1 ** grid_rows[f"r{row+2}"]
        + io.target_shape3_row2 ** grid_rows[f"r{row+3}"]
        + io.target_shape3_row3 ** grid_rows[f"r{row+4}"]
        + io.target_shape3_col1 ** grid_cols[f"c{col-1+i}"]
        + io.target_shape3_col2 ** grid_cols[f"c{col-1+i}"]
        + io.target_shape3_col3 ** grid_cols[f"c{col-1+i}"]
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
        + io.target_shape2 ** bricks.mirror_L
        + io.target_shape3 ** bricks.vertical
        + io.target_shape2_row1 ** grid_rows[f"r{row}"]
        + io.target_shape2_row2 ** grid_rows[f"r{row+1}"]
        + io.target_shape2_row3 ** grid_rows[f"r{row+1}"]
        + io.target_shape2_col1 ** grid_cols[f"c{col}"]
        + io.target_shape2_col2 ** grid_cols[f"c{col-1}"]
        + io.target_shape2_col3 ** grid_cols[f"c{col}"]
        + io.target_shape3_row1 ** grid_rows[f"r{row-3}"]
        + io.target_shape3_row2 ** grid_rows[f"r{row-2}"]
        + io.target_shape3_row3 ** grid_rows[f"r{row-1}"]
        + io.target_shape3_col1 ** grid_cols[f"c{col}"]
        + io.target_shape3_col2 ** grid_cols[f"c{col}"]
        + io.target_shape3_col3 ** grid_cols[f"c{col}"]
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
        + io.target_shape3 ** bricks.horizontal
        + io.target_shape4 ** bricks.vertical
        + io.target_shape3_row1 ** grid_rows[f"r{row}"]
        + io.target_shape3_row2 ** grid_rows[f"r{row}"]
        + io.target_shape3_row3 ** grid_rows[f"r{row}"]
        + io.target_shape3_col1 ** grid_cols[f"c{col}"]
        + io.target_shape3_col2 ** grid_cols[f"c{col+1}"] 
        + io.target_shape3_col3 ** grid_cols[f"c{col+2}"]
        + io.target_shape4_row1 ** grid_rows[f"r{row-2+i}"]
        + io.target_shape4_row2 ** grid_rows[f"r{row-1+i}"]
        + io.target_shape4_row3 ** grid_rows[f"r{row+i}"]
        + io.target_shape4_col1 ** grid_cols[f"c{col+3}"]
        + io.target_shape4_col2 ** grid_cols[f"c{col+3}"]
        + io.target_shape4_col3 ** grid_cols[f"c{col+3}"]
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
        + io.target_shape3 ** bricks.horizontal
        + io.target_shape4 ** bricks.vertical
        + io.target_shape3_row1 ** grid_rows[f"r{row}"]
        + io.target_shape3_row2 ** grid_rows[f"r{row}"]
        + io.target_shape3_row3 ** grid_rows[f"r{row}"]
        + io.target_shape3_col1 ** grid_cols[f"c{col}"]
        + io.target_shape3_col2 ** grid_cols[f"c{col+1}"] 
        + io.target_shape3_col3 ** grid_cols[f"c{col+2}"]
        + io.target_shape4_row1 ** grid_rows[f"r{row-2+i}"]
        + io.target_shape4_row2 ** grid_rows[f"r{row-1+i}"]
        + io.target_shape4_row3 ** grid_rows[f"r{row+i}"]
        + io.target_shape4_col1 ** grid_cols[f"c{col-1}"]
        + io.target_shape4_col2 ** grid_cols[f"c{col-1}"]
        + io.target_shape4_col3 ** grid_cols[f"c{col-1}"]
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
        + io.target_shape3 ** bricks.horizontal
        + io.target_shape4 ** bricks.vertical
        + io.target_shape3_row1 ** grid_rows[f"r{row}"]
        + io.target_shape3_row2 ** grid_rows[f"r{row}"]
        + io.target_shape3_row3 ** grid_rows[f"r{row}"]
        + io.target_shape3_col1 ** grid_cols[f"c{col}"]
        + io.target_shape3_col2 ** grid_cols[f"c{col+1}"] 
        + io.target_shape3_col3 ** grid_cols[f"c{col+2}"]
        + io.target_shape4_row1 ** grid_rows[f"r{row+1}"]
        + io.target_shape4_row2 ** grid_rows[f"r{row+2}"]
        + io.target_shape4_row3 ** grid_rows[f"r{row+3}"]
        + io.target_shape4_col1 ** grid_cols[f"c{col+i}"]
        + io.target_shape4_col2 ** grid_cols[f"c{col+i}"]
        + io.target_shape4_col3 ** grid_cols[f"c{col+i}"]
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
        + io.target_shape3 ** bricks.horizontal
        + io.target_shape4 ** bricks.vertical
        + io.target_shape3_row1 ** grid_rows[f"r{row}"]
        + io.target_shape3_row2 ** grid_rows[f"r{row}"]
        + io.target_shape3_row3 ** grid_rows[f"r{row}"]
        + io.target_shape3_col1 ** grid_cols[f"c{col}"]
        + io.target_shape3_col2 ** grid_cols[f"c{col+1}"] 
        + io.target_shape3_col3 ** grid_cols[f"c{col+2}"]
        + io.target_shape4_row1 ** grid_rows[f"r{row-3}"]
        + io.target_shape4_row2 ** grid_rows[f"r{row-2}"]
        + io.target_shape4_row3 ** grid_rows[f"r{row-1}"]
        + io.target_shape4_col1 ** grid_cols[f"c{col+i}"]
        + io.target_shape4_col2 ** grid_cols[f"c{col+i}"]
        + io.target_shape4_col3 ** grid_cols[f"c{col+i}"]
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
    
    d = participant.construction_space
    io = d.io
    bricks = d.bricks
    brick_nos = d.brick_nos
    con_signal = d.signal_tokens
    grid_rows = d.grid_rows
    grid_cols = d.grid_cols

    #FIRST PLACEMENT RULES
    """
    1 1
    1
    """
    half_T_first_placement_rule = [
        (   + io.input_shape1 ** bricks.half_T
            + io.input_shape1_row1 ** grid_rows[f"r{row}"]
            + io.input_shape1_row2 ** grid_rows[f"r{row}"]
            + io.input_shape1_row3 ** grid_rows[f"r{row+1}"]
            + io.input_shape1_col1 ** grid_cols[f"c{col}"]
            + io.input_shape1_col2 ** grid_cols[f"c{col+1}"]
            + io.input_shape1_col3 ** grid_cols[f"c{col}"]

            >>
            + io.target_shape1 ** bricks.half_T
            + io.target_shape1_row1 ** grid_rows[f"r{row}"]
            + io.target_shape1_row2 ** grid_rows[f"r{row}"]
            + io.target_shape1_row3 ** grid_rows[f"r{row+1}"]
            + io.target_shape1_col1 ** grid_cols[f"c{col}"]
            + io.target_shape1_col2 ** grid_cols[f"c{col+1}"]
            + io.target_shape1_col3 ** grid_cols[f"c{col}"]
         )
         for row in range(1, 6) for col in range(1, 6)
    ]

    mirror_L_first_placement_rule = [
        ( + io.input_shape2 ** bricks.mirror_L
          + io.input_shape2_row1 ** grid_rows[f"r{row}"]
            + io.input_shape2_row2 ** grid_rows[f"r{row+1}"]
            + io.input_shape2_row3 ** grid_rows[f"r{row+1}"]
            + io.input_shape2_col1 ** grid_cols[f"c{col}"]
            + io.input_shape2_col2 ** grid_cols[f"c{col-1}"]
            + io.input_shape2_col3 ** grid_cols[f"c{col}"]
            >>
            + io.target_shape2 ** bricks.mirror_L

            + io.target_shape2_row1 ** grid_rows[f"r{row}"]
            + io.target_shape2_row2 ** grid_rows[f"r{row+1}"]
            + io.target_shape2_row3 ** grid_rows[f"r{row+1}"]
            + io.target_shape2_col1 ** grid_cols[f"c{col}"]
            + io.target_shape2_col2 ** grid_cols[f"c{col-1}"]
            + io.target_shape2_col3 ** grid_cols[f"c{col}"]  
        )
        for row in range(1, 6) for col in range(2, 7)
    ]
    """
      1
    1 1
    """

    horizontal_first_placement_rule = [
        ( + io.input_shape3 ** bricks.horizontal
            + io.input_shape3_row1 ** grid_rows[f"r{row}"]
                + io.input_shape3_row2 ** grid_rows[f"r{row}"]
                + io.input_shape3_row3 ** grid_rows[f"r{row}"]
                + io.input_shape3_col1 ** grid_cols[f"c{col}"]
                + io.input_shape3_col2 ** grid_cols[f"c{col+1}"]
                + io.input_shape3_col3 ** grid_cols[f"c{col+2}"]
                >>
                + io.target_shape3 ** bricks.horizontal
    
                + io.target_shape3_row1 ** grid_rows[f"r{row}"]
                + io.target_shape3_row2 ** grid_rows[f"r{row}"]
                + io.target_shape3_row3 ** grid_rows[f"r{row}"]
                + io.target_shape3_col1 ** grid_cols[f"c{col}"]
                + io.target_shape3_col2 ** grid_cols[f"c{col+1}"]
                + io.target_shape3_col3 ** grid_cols[f"c{col+2}"]  
            )
        for row in range(1, 7) for col in range(1, 5)
    ]

    vertical_first_placement_rule = [
        ( + io.input_shape4 ** bricks.vertical
            + io.input_shape4_row1 ** grid_rows[f"r{row}"]
                + io.input_shape4_row2 ** grid_rows[f"r{row+1}"]
                + io.input_shape4_row3 ** grid_rows[f"r{row+2}"]
                + io.input_shape4_col1 ** grid_cols[f"c{col}"]
                + io.input_shape4_col2 ** grid_cols[f"c{col}"]
                + io.input_shape4_col3 ** grid_cols[f"c{col}"]
                >>
                + io.target_shape4 ** bricks.vertical

                + io.target_shape4_row1 ** grid_rows[f"r{row}"]
                + io.target_shape4_row2 ** grid_rows[f"r{row+1}"]
                + io.target_shape4_row3 ** grid_rows[f"r{row+2}"]
                + io.target_shape4_col1 ** grid_cols[f"c{col}"]
                + io.target_shape4_col2 ** grid_cols[f"c{col}"]
                + io.target_shape4_col3 ** grid_cols[f"c{col}"]  
            )
        for row in range(1, 5) for col in range(1, 7)
    ]

    #SUBSEQUENCE PLACEMENT RULES
    half_T_left_of_horizontal_placement_rule = [
        (
            + io.input_shape1 ** bricks.half_T
            + io.input_shape4 ** bricks.horizontal
            + io.input_shape1_row1 ** grid_rows[f"r{row}"]
            + io.input_shape1_row2 ** grid_rows[f"r{row}"]
            + io.input_shape1_row3 ** grid_rows[f"r{row+1}"]
            + io.input_shape1_col1 ** grid_cols[f"c{col}"]
            + io.input_shape1_col2 ** grid_cols[f"c{col+1}"]
            + io.input_shape1_col3 ** grid_cols[f"c{col}"]
            + io.input_shape4_row1 ** grid_rows[f"r{row+i}"]
            + io.input_shape4_row2 ** grid_rows[f"r{row+i}"]
            + io.input_shape4_row3 ** grid_rows[f"r{row+i}"]
            + io.input_shape4_col1 ** grid_cols[f"c{col+2-i}"]
            + io.input_shape4_col2 ** grid_cols[f"c{col+3-i}"]
            + io.input_shape4_col3 ** grid_cols[f"c{col+4-i}"]

            >>
            + io.target_shape1 ** bricks.half_T
            + io.target_shape4 ** bricks.horizontal
            + io.target_shape1_row1 ** grid_rows[f"r{row}"]
            + io.target_shape1_row2 ** grid_rows[f"r{row}"]
            + io.target_shape1_row3 ** grid_rows[f"r{row+1}"]
            + io.target_shape1_col1 ** grid_cols[f"c{col}"]
            + io.target_shape1_col2 ** grid_cols[f"c{col+1}"]
            + io.target_shape1_col3 ** grid_cols[f"c{col}"]
            + io.target_shape4_row1 ** grid_rows[f"r{row+i}"]
            + io.target_shape4_row2 ** grid_rows[f"r{row+i}"]
            + io.target_shape4_row3 ** grid_rows[f"r{row+i}"]
            + io.target_shape4_col1 ** grid_cols[f"c{col+2-i}"]
            + io.target_shape4_col2 ** grid_cols[f"c{col+3-i}"]
            + io.target_shape4_col3 ** grid_cols[f"c{col+4-i}"]
        )
        for i in range(2) for row in range(1, 6) for col in range(1, 3 + i)
    ]

    half_T_right_of_horizontal_placement_rule = [
        (
            + io.input_shape1 ** bricks.half_T
            + io.input_shape4 ** bricks.horizontal
            + io.input_shape1_row1 ** grid_rows[f"r{row}"]
            + io.input_shape1_row2 ** grid_rows[f"r{row}"]
            + io.input_shape1_row3 ** grid_rows[f"r{row+1}"]
            + io.input_shape1_col1 ** grid_cols[f"c{col}"]
            + io.input_shape1_col2 ** grid_cols[f"c{col+1}"]
            + io.input_shape1_col3 ** grid_cols[f"c{col}"]
            + io.input_shape4_row1 ** grid_rows[f"r{row+i}"]
            + io.input_shape4_row2 ** grid_rows[f"r{row+i}"]
            + io.input_shape4_row3 ** grid_rows[f"r{row+i}"]
            + io.input_shape4_col1 ** grid_cols[f"c{col-3}"]
            + io.input_shape4_col2 ** grid_cols[f"c{col-2}"]
            + io.input_shape4_col3 ** grid_cols[f"c{col-1}"]
            >>
            + io.target_shape1 ** bricks.half_T
            + io.target_shape4 ** bricks.horizontal
            + io.target_shape1_row1 ** grid_rows[f"r{row}"]
            + io.target_shape1_row2 ** grid_rows[f"r{row}"]
            + io.target_shape1_row3 ** grid_rows[f"r{row+1}"]
            + io.target_shape1_col1 ** grid_cols[f"c{col}"]
            + io.target_shape1_col2 ** grid_cols[f"c{col+1}"]
            + io.target_shape1_col3 ** grid_cols[f"c{col}"]
            + io.target_shape4_row1 ** grid_rows[f"r{row+i}"]
            + io.target_shape4_row2 ** grid_rows[f"r{row+i}"]
            + io.target_shape4_row3 ** grid_rows[f"r{row+i}"]
            + io.target_shape4_col1 ** grid_cols[f"c{col-3}"]
            + io.target_shape4_col2 ** grid_cols[f"c{col-2}"]
            + io.target_shape4_col3 ** grid_cols[f"c{col-1}"]
        )
        for i in range(2) for row in range(1, 6) for col in range(4, 6)
    ]

    half_T_below_horizontal_placement_rule = [
        (
            + io.input_shape1 ** bricks.half_T
            + io.input_shape4 ** bricks.horizontal
            + io.input_shape1_row1 ** grid_rows[f"r{row}"]
            + io.input_shape1_row2 ** grid_rows[f"r{row}"]
            + io.input_shape1_row3 ** grid_rows[f"r{row+1}"]
            + io.input_shape1_col1 ** grid_cols[f"c{col}"]
            + io.input_shape1_col2 ** grid_cols[f"c{col+1}"]
            + io.input_shape1_col3 ** grid_cols[f"c{col}"]
            + io.input_shape4_row1 ** grid_rows[f"r{row-1}"]
            + io.input_shape4_row2 ** grid_rows[f"r{row-1}"]
            + io.input_shape4_row3 ** grid_rows[f"r{row-1}"]
            + io.input_shape4_col1 ** grid_cols[f"c{col-1+i}"]
            + io.input_shape4_col2 ** grid_cols[f"c{col+i}"]
            + io.input_shape4_col3 ** grid_cols[f"c{col+1+i}"]
            >>
            + io.target_shape1 ** bricks.half_T
            + io.target_shape4 ** bricks.horizontal
            + io.target_shape1_row1 ** grid_rows[f"r{row}"]
            + io.target_shape1_row2 ** grid_rows[f"r{row}"]
            + io.target_shape1_row3 ** grid_rows[f"r{row+1}"]
            + io.target_shape1_col1 ** grid_cols[f"c{col}"]
            + io.target_shape1_col2 ** grid_cols[f"c{col+1}"]
            + io.target_shape1_col3 ** grid_cols[f"c{col}"]
            + io.target_shape4_row1 ** grid_rows[f"r{row-1}"]
            + io.target_shape4_row2 ** grid_rows[f"r{row-1}"]
            + io.target_shape4_row3 ** grid_rows[f"r{row-1}"]
            + io.target_shape4_col1 ** grid_cols[f"c{col-1+i}"]
            + io.target_shape4_col2 ** grid_cols[f"c{col+i}"]
            + io.target_shape4_col3 ** grid_cols[f"c{col+1+i}"]
        ) 
        for i in range(3) for row in range(2, 6) for col in range(1 + (i == 0), 6-i)
    ]

    half_T_above_horizontal_placement_rule = [
        (
            + io.input_shape1 ** bricks.half_T
            + io.input_shape4 ** bricks.horizontal
            + io.input_shape1_row1 ** grid_rows[f"r{row}"]
            + io.input_shape1_row2 ** grid_rows[f"r{row}"]
            + io.input_shape1_row3 ** grid_rows[f"r{row+1}"]
            + io.input_shape1_col1 ** grid_cols[f"c{col}"]
            + io.input_shape1_col2 ** grid_cols[f"c{col+1}"]
            + io.input_shape1_col3 ** grid_cols[f"c{col}"]
            + io.input_shape4_row1 ** grid_rows[f"r{row+2}"]
            + io.input_shape4_row2 ** grid_rows[f"r{row+2}"]
            + io.input_shape4_row3 ** grid_rows[f"r{row+2}"]
            + io.input_shape4_col1 ** grid_cols[f"c{col-2+i}"]
            + io.input_shape4_col2 ** grid_cols[f"c{col-1+i}"]
            + io.input_shape4_col3 ** grid_cols[f"c{col+i}"]
            >>
            + io.target_shape1 ** bricks.half_T
            + io.target_shape4 ** bricks.horizontal
            + io.target_shape1_row1 ** grid_rows[f"r{row}"]
            + io.target_shape1_row2 ** grid_rows[f"r{row}"]
            + io.target_shape1_row3 ** grid_rows[f"r{row+1}"]
            + io.target_shape1_col1 ** grid_cols[f"c{col}"]
            + io.target_shape1_col2 ** grid_cols[f"c{col+1}"]
            + io.target_shape1_col3 ** grid_cols[f"c{col}"]
            + io.target_shape4_row1 ** grid_rows[f"r{row+2}"]
            + io.target_shape4_row2 ** grid_rows[f"r{row+2}"]
            + io.target_shape4_row3 ** grid_rows[f"r{row+2}"]
            + io.target_shape4_col1 ** grid_cols[f"c{col-2+i}"]
            + io.target_shape4_col2 ** grid_cols[f"c{col-1+i}"]
            + io.target_shape4_col3 ** grid_cols[f"c{col+i}"]
        ) 
        for i in range(3) for row in range(1, 5) for col in range(3-i, 6-(i==2))
]

    half_T_left_vertical_placement_rule = [
        (
            + io.input_shape1 ** bricks.half_T
            + io.input_shape3 ** bricks.vertical
            + io.input_shape1_row1 ** grid_rows[f"r{row}"]
            + io.input_shape1_row2 ** grid_rows[f"r{row}"]
            + io.input_shape1_row3 ** grid_rows[f"r{row+1}"]
            + io.input_shape1_col1 ** grid_cols[f"c{col}"]
            + io.input_shape1_col2 ** grid_cols[f"c{col+1}"]
            + io.input_shape1_col3 ** grid_cols[f"c{col}"]
            + io.input_shape3_row1 ** grid_rows[f"r{row+1-i}"]
            + io.input_shape3_row2 ** grid_rows[f"r{row+2-i}"]
            + io.input_shape3_row3 ** grid_rows[f"r{row+3-i}"]
            + io.input_shape3_col1 ** grid_cols[f"c{col+2- (i == 0)}"]
            + io.input_shape3_col2 ** grid_cols[f"c{col+2- (i == 0)}"]
            + io.input_shape3_col3 ** grid_cols[f"c{col+2- (i == 0)}"]
            >>
            + io.target_shape1 ** bricks.half_T
            + io.target_shape3 ** bricks.vertical
            + io.target_shape1_row1 ** grid_rows[f"r{row}"]
            + io.target_shape1_row2 ** grid_rows[f"r{row}"]
            + io.target_shape1_row3 ** grid_rows[f"r{row+1}"]
            + io.target_shape1_col1 ** grid_cols[f"c{col}"]
            + io.target_shape1_col2 ** grid_cols[f"c{col+1}"]
            + io.target_shape1_col3 ** grid_cols[f"c{col}"]
            + io.target_shape3_row1 ** grid_rows[f"r{row+1-i}"]
            + io.target_shape3_row2 ** grid_rows[f"r{row+2-i}"]
            + io.target_shape3_row3 ** grid_rows[f"r{row+3-i}"]
            + io.target_shape3_col1 ** grid_cols[f"c{col+2- (i == 0)}"]
            + io.target_shape3_col2 ** grid_cols[f"c{col+2 - (i == 0)}"]
            + io.target_shape3_col3 ** grid_cols[f"c{col+2 - (i == 0)}"]
            )
            for i in range(4) for row in range(1+(i-1 if i > 1 else 0), 4 + (math.ceil(i/2))) for col in range(1, 6-(i > 0))
    ]
    
    half_T_right_vertical_placement_rule = [
        (
            + io.input_shape1 ** bricks.half_T
            + io.input_shape3 ** bricks.vertical
            + io.input_shape1_row1 ** grid_rows[f"r{row}"]
            + io.input_shape1_row2 ** grid_rows[f"r{row}"]
            + io.input_shape1_row3 ** grid_rows[f"r{row+1}"]
            + io.input_shape1_col1 ** grid_cols[f"c{col}"]
            + io.input_shape1_col2 ** grid_cols[f"c{col+1}"]
            + io.input_shape1_col3 ** grid_cols[f"c{col}"]
            + io.input_shape3_row1 ** grid_rows[f"r{row-2+i}"]
            + io.input_shape3_row2 ** grid_rows[f"r{row-1+i}"]
            + io.input_shape3_row3 ** grid_rows[f"r{row+i}"]
            + io.input_shape3_col1 ** grid_cols[f"c{col-1}"]
            + io.input_shape3_col2 ** grid_cols[f"c{col-1}"]
            + io.input_shape3_col3 ** grid_cols[f"c{col-1}"]
            >>
            + io.target_shape1 ** bricks.half_T
            + io.target_shape3 ** bricks.vertical
            + io.target_shape1_row1 ** grid_rows[f"r{row}"]
            + io.target_shape1_row2 ** grid_rows[f"r{row}"]
            + io.target_shape1_row3 ** grid_rows[f"r{row+1}"]
            + io.target_shape1_col1 ** grid_cols[f"c{col}"]
            + io.target_shape1_col2 ** grid_cols[f"c{col+1}"]
            + io.target_shape1_col3 ** grid_cols[f"c{col}"]
            + io.target_shape3_row1 ** grid_rows[f"r{row-2+i}"]
            + io.target_shape3_row2 ** grid_rows[f"r{row-1+i}"]
            + io.target_shape3_row3 ** grid_rows[f"r{row+i}"]
            + io.target_shape3_col1 ** grid_cols[f"c{col-1}"]
            + io.target_shape3_col2 ** grid_cols[f"c{col-1}"]
            + io.target_shape3_col3 ** grid_cols[f"c{col-1}"]
        ) 
        for i in range(4) for row in range(max(1, 3-i), 6-max(0, i-1)) for col in range(2, 6)
    ]
    
    half_T_below_vertical_placement_rule = [
        (
            + io.input_shape1 ** bricks.half_T
            + io.input_shape3 ** bricks.vertical
            + io.input_shape1_row1 ** grid_rows[f"r{row}"]
            + io.input_shape1_row2 ** grid_rows[f"r{row}"]
            + io.input_shape1_row3 ** grid_rows[f"r{row+1}"]
            + io.input_shape1_col1 ** grid_cols[f"c{col}"]
            + io.input_shape1_col2 ** grid_cols[f"c{col+1}"]
            + io.input_shape1_col3 ** grid_cols[f"c{col}"]
            + io.input_shape3_row1 ** grid_rows[f"r{row-3}"]
            + io.input_shape3_row2 ** grid_rows[f"r{row-2}"]
            + io.input_shape3_row3 ** grid_rows[f"r{row-3}"]
            + io.input_shape3_col1 ** grid_cols[f"c{col+i}"]
            + io.input_shape3_col2 ** grid_cols[f"c{col+i}"]
            + io.input_shape3_col3 ** grid_cols[f"c{col+i}"]
            >>
            + io.target_shape1 ** bricks.half_T
            + io.target_shape3 ** bricks.vertical
            + io.target_shape1_row1 ** grid_rows[f"r{row}"]
            + io.target_shape1_row2 ** grid_rows[f"r{row}"]
            + io.target_shape1_row3 ** grid_rows[f"r{row+1}"]
            + io.target_shape1_col1 ** grid_cols[f"c{col}"]
            + io.target_shape1_col2 ** grid_cols[f"c{col+1}"]
            + io.target_shape1_col3 ** grid_cols[f"c{col}"]
            + io.target_shape3_row1 ** grid_rows[f"r{row-3}"]
            + io.target_shape3_row2 ** grid_rows[f"r{row-2}"]
            + io.target_shape3_row3 ** grid_rows[f"r{row-3}"]
            + io.target_shape3_col1 ** grid_cols[f"c{col+i}"]
            + io.target_shape3_col2 ** grid_cols[f"c{col+i}"]
            + io.target_shape3_col3 ** grid_cols[f"c{col+i}"]
            ) 
            for i in range(2) for row in range(4, 6) for col in range(1, 6)
    ]

    half_T_above_vertical_placement_rule = [
        (
            + io.input_shape1 ** bricks.half_T
            + io.input_shape3 ** bricks.vertical
            + io.input_shape1_row1 ** grid_rows[f"r{row}"]
            + io.input_shape1_row2 ** grid_rows[f"r{row}"]
            + io.input_shape1_row3 ** grid_rows[f"r{row+1}"]
            + io.input_shape1_col1 ** grid_cols[f"c{col}"]
            + io.input_shape1_col2 ** grid_cols[f"c{col+1}"]
            + io.input_shape1_col3 ** grid_cols[f"c{col}"]
            + io.input_shape3_row1 ** grid_rows[f"r{row+1}"]
            + io.input_shape3_row2 ** grid_rows[f"r{row+2}"]
            + io.input_shape3_row3 ** grid_rows[f"r{row+3}"]
            + io.input_shape3_col1 ** grid_cols[f"c{col}"]
            + io.input_shape3_col2 ** grid_cols[f"c{col}"]
            + io.input_shape3_col3 ** grid_cols[f"c{col}"]
            >>
            + io.target_shape1 ** bricks.half_T
            + io.target_shape3 ** bricks.vertical
            + io.target_shape1_row1 ** grid_rows[f"r{row}"]
            + io.target_shape1_row2 ** grid_rows[f"r{row}"]
            + io.target_shape1_row3 ** grid_rows[f"r{row+1}"]
            + io.target_shape1_col1 ** grid_cols[f"c{col}"]
            + io.target_shape1_col2 ** grid_cols[f"c{col+1}"]
            + io.target_shape1_col3 ** grid_cols[f"c{col}"]
            + io.target_shape3_row1 ** grid_rows[f"r{row+1}"]
            + io.target_shape3_row2 ** grid_rows[f"r{row+2}"]
            + io.target_shape3_row3 ** grid_rows[f"r{row+3}"]
            + io.target_shape3_col1 ** grid_cols[f"c{col}"]
            + io.target_shape3_col2 ** grid_cols[f"c{col}"]
            + io.target_shape3_col3 ** grid_cols[f"c{col}"]
            ) 
            for row in range(1, 3) for col in range(1, 6)
    ]

    half_T_left_mirror_L_placement_rule = [
        (
            + io.input_shape1 ** bricks.half_T
            + io.input_shape2 ** bricks.mirror_L
            + io.input_shape1_row1 ** grid_rows[f"r{row}"]
            + io.input_shape1_row2 ** grid_rows[f"r{row}"]
            + io.input_shape1_row3 ** grid_rows[f"r{row+1}"]
            + io.input_shape1_col1 ** grid_cols[f"c{col}"]
            + io.input_shape1_col2 ** grid_cols[f"c{col+1}"]
            + io.input_shape1_col3 ** grid_cols[f"c{col}"]
            + io.input_shape2_row1 ** grid_rows[f"r{row-i}"]
            + io.input_shape2_row2 ** grid_rows[f"r{row+1-i}"]
            + io.input_shape2_row3 ** grid_rows[f"r{row+1-i}"]
            + io.input_shape2_col1 ** grid_cols[f"c{col+2+i}"]
            + io.input_shape2_col2 ** grid_cols[f"c{col+1+i}"]
            + io.input_shape2_col3 ** grid_cols[f"c{col+2+i}"]
            >>
            + io.target_shape1 ** bricks.half_T
            + io.target_shape2 ** bricks.mirror_L
            + io.target_shape1_row1 ** grid_rows[f"r{row}"]
            + io.target_shape1_row2 ** grid_rows[f"r{row}"]
            + io.target_shape1_row3 ** grid_rows[f"r{row+1}"]
            + io.target_shape1_col1 ** grid_cols[f"c{col}"]
            + io.target_shape1_col2 ** grid_cols[f"c{col+1}"]
            + io.target_shape1_col3 ** grid_cols[f"c{col}"]
            + io.target_shape2_row1 ** grid_rows[f"r{row-i}"]
            + io.target_shape2_row2 ** grid_rows[f"r{row+1-i}"]
            + io.target_shape2_row3 ** grid_rows[f"r{row+1-i}"]
            + io.target_shape2_col1 ** grid_cols[f"c{col+2+i}"]
            + io.target_shape2_col2 ** grid_cols[f"c{col+1+i}"]
            + io.target_shape2_col3 ** grid_cols[f"c{col+2+i}"]
        )
        for i in range(2) for row in range(1+i, 6) for col in range(1, 5-i)
    ]
    
    half_T_right_mirror_L_placement_rule = [
        (
            + io.input_shape1 ** bricks.half_T
            + io.input_shape2 ** bricks.mirror_L
            + io.input_shape1_row1 ** grid_rows[f"r{row}"]
            + io.input_shape1_row2 ** grid_rows[f"r{row}"]
            + io.input_shape1_row3 ** grid_rows[f"r{row+1}"]
            + io.input_shape1_col1 ** grid_cols[f"c{col}"]
            + io.input_shape1_col2 ** grid_cols[f"c{col+1}"]
            + io.input_shape1_col3 ** grid_cols[f"c{col}"]
            + io.input_shape2_row1 ** grid_rows[f"r{row + (-1 if i== 0 else 1)*(i%2 == 0)}"] # 1 up, no up, 1 down.
            + io.input_shape2_row2 ** grid_rows[f"r{row + i}"]
            + io.input_shape2_row3 ** grid_rows[f"r{row+i}"]
            + io.input_shape2_col1 ** grid_cols[f"c{col-1}"]
            + io.input_shape2_col2 ** grid_cols[f"c{col-2}"]
            + io.input_shape2_col3 ** grid_cols[f"c{col-1}"]
            >>
            + io.target_shape1 ** bricks.half_T
            + io.target_shape2 ** bricks.mirror_L
            + io.target_shape1_row1 ** grid_rows[f"r{row}"]
            + io.target_shape1_row2 ** grid_rows[f"r{row}"]
            + io.target_shape1_row3 ** grid_rows[f"r{row+1}"]
            + io.target_shape1_col1 ** grid_cols[f"c{col}"]
            + io.target_shape1_col2 ** grid_cols[f"c{col+1}"]
            + io.target_shape1_col3 ** grid_cols[f"c{col}"]
            + io.target_shape2_row1 ** grid_rows[f"r{row + (-1 if i== 0 else 1)*(i%2 == 0)}"] # 1 up, no up, 1 down.
            + io.target_shape2_row2 ** grid_rows[f"r{row + i}"]
            + io.target_shape2_row3 ** grid_rows[f"r{row+i}"]
            + io.target_shape2_col1 ** grid_cols[f"c{col-1}"]
            + io.target_shape2_col2 ** grid_cols[f"c{col-2}"]
            + io.target_shape2_col3 ** grid_cols[f"c{col-1}"]
        ) 
        for i in range(3) for row in range(1+(i==0), 6-(i==2)) for col in range(3, 6)
    ]
    
    half_T_below_mirror_L_placement_rule = [
        (
            + io.input_shape1 ** bricks.half_T
            + io.input_shape2 ** bricks.mirror_L
            + io.input_shape1_row1 ** grid_rows[f"r{row}"]
            + io.input_shape1_row2 ** grid_rows[f"r{row}"]
            + io.input_shape1_row3 ** grid_rows[f"r{row+1}"]
            + io.input_shape1_col1 ** grid_cols[f"c{col}"]
            + io.input_shape1_col2 ** grid_cols[f"c{col+1}"]
            + io.input_shape1_col3 ** grid_cols[f"c{col}"]
            + io.input_shape2_row1 ** grid_rows[f"r{row-2}"]
            + io.input_shape2_row2 ** grid_rows[f"r{row-1}"]
            + io.input_shape2_row3 ** grid_rows[f"r{row-1}"]
            + io.input_shape2_col1 ** grid_cols[f"c{col+1+i}"]
            + io.input_shape2_col2 ** grid_cols[f"c{col+i}"]
            + io.input_shape2_col3 ** grid_cols[f"c{col+1+i}"]
            >>
            + io.target_shape1 ** bricks.half_T
            + io.target_shape2 ** bricks.mirror_L
            + io.target_shape1_row1 ** grid_rows[f"r{row}"]
            + io.target_shape1_row2 ** grid_rows[f"r{row}"]
            + io.target_shape1_row3 ** grid_rows[f"r{row+1}"]
            + io.target_shape1_col1 ** grid_cols[f"c{col}"]
            + io.target_shape1_col2 ** grid_cols[f"c{col+1}"]
            + io.target_shape1_col3 ** grid_cols[f"c{col}"]
            + io.target_shape2_row1 ** grid_rows[f"r{row-2}"]
            + io.target_shape2_row2 ** grid_rows[f"r{row-1}"]
            + io.target_shape2_row3 ** grid_rows[f"r{row-1}"]
            + io.target_shape2_col1 ** grid_cols[f"c{col+1+i}"]
            + io.target_shape2_col2 ** grid_cols[f"c{col+i}"]
            + io.target_shape2_col3 ** grid_cols[f"c{col+1+i}"]
        )
        for i in range(2) for row in range(3, 6) for col in range(1, 6-i)
    ]

    half_T_above_mirror_L_placement_rule = [
        (
            + io.input_shape1 ** bricks.half_T
            + io.input_shape2 ** bricks.mirror_L
            + io.input_shape1_row1 ** grid_rows[f"r{row}"]
            + io.input_shape1_row2 ** grid_rows[f"r{row}"]
            + io.input_shape1_row3 ** grid_rows[f"r{row+1}"]
            + io.input_shape1_col1 ** grid_cols[f"c{col}"]
            + io.input_shape1_col2 ** grid_cols[f"c{col+1}"]
            + io.input_shape1_col3 ** grid_cols[f"c{col}"]
            + io.input_shape2_row1 ** grid_rows[f"r{row+2}"]
            + io.input_shape2_row2 ** grid_rows[f"r{row+3}"]
            + io.input_shape2_row3 ** grid_rows[f"r{row+3}"]
            + io.input_shape2_col1 ** grid_cols[f"c{col}"]
            + io.input_shape2_col2 ** grid_cols[f"c{col-1}"]
            + io.input_shape2_col3 ** grid_cols[f"c{col}"]
            >>
            + io.target_shape1 ** bricks.half_T
            + io.target_shape2 ** bricks.mirror_L
            + io.target_shape1_row1 ** grid_rows[f"r{row}"]
            + io.target_shape1_row2 ** grid_rows[f"r{row}"]
            + io.target_shape1_row3 ** grid_rows[f"r{row+1}"]
            + io.target_shape1_col1 ** grid_cols[f"c{col}"]
            + io.target_shape1_col2 ** grid_cols[f"c{col+1}"]
            + io.target_shape1_col3 ** grid_cols[f"c{col}"]
            + io.target_shape2_row1 ** grid_rows[f"r{row+2}"]
            + io.target_shape2_row2 ** grid_rows[f"r{row+3}"]
            + io.target_shape2_row3 ** grid_rows[f"r{row+3}"]
            + io.target_shape2_col1 ** grid_cols[f"c{col}"]
            + io.target_shape2_col2 ** grid_cols[f"c{col-1}"]
            + io.target_shape2_col3 ** grid_cols[f"c{col}"]
        ) 
        for row in range(1, 4) for col in range(2, 6)
    ]

    mirror_L_left_horizontal_placement_rule  = [
        (
            + io.input_shape2 ** bricks.mirror_L
            + io.input_shape4 ** bricks.horizontal
            + io.input_shape2_row1 ** grid_rows[f"r{row}"]
            + io.input_shape2_row2 ** grid_rows[f"r{row+1}"]
            + io.input_shape2_row3 ** grid_rows[f"r{row+1}"]
            + io.input_shape2_col1 ** grid_cols[f"c{col}"]
            + io.input_shape2_col2 ** grid_cols[f"c{col-1}"]
            + io.input_shape2_col3 ** grid_cols[f"c{col}"]
            + io.input_shape4_row1 ** grid_rows[f"r{row+i}"]
            + io.input_shape4_row2 ** grid_rows[f"r{row+i}"]
            + io.input_shape4_row3 ** grid_rows[f"r{row+i}"]
            + io.input_shape4_col1 ** grid_cols[f"c{col+1}"]
            + io.input_shape4_col2 ** grid_cols[f"c{col+2}"]
            + io.input_shape4_col3 ** grid_cols[f"c{col+3}"]
            >>
            + io.target_shape2 ** bricks.mirror_L
            + io.target_shape4 ** bricks.horizontal
            + io.target_shape2_row1 ** grid_rows[f"r{row}"]
            + io.target_shape2_row2 ** grid_rows[f"r{row+1}"]
            + io.target_shape2_row3 ** grid_rows[f"r{row+1}"]
            + io.target_shape2_col1 ** grid_cols[f"c{col}"]
            + io.target_shape2_col2 ** grid_cols[f"c{col-1}"]
            + io.target_shape2_col3 ** grid_cols[f"c{col}"]
            + io.target_shape4_row1 ** grid_rows[f"r{row+i}"]
            + io.target_shape4_row2 ** grid_rows[f"r{row+i}"]
            + io.target_shape4_row3 ** grid_rows[f"r{row+i}"]
            + io.target_shape4_col1 ** grid_cols[f"c{col+1}"]
            + io.target_shape4_col2 ** grid_cols[f"c{col+2}"]
            + io.target_shape4_col3 ** grid_cols[f"c{col+3}"]
            ) 
            for i in range(2) for row in range(1, 6) for col in range(2, 4)
    ]

    mirror_L_right_horizontal_placement_rule = [
        (
            + io.input_shape2 ** bricks.mirror_L
            + io.input_shape4 ** bricks.horizontal
            + io.input_shape2_row1 ** grid_rows[f"r{row}"]
            + io.input_shape2_row2 ** grid_rows[f"r{row+1}"]
            + io.input_shape2_row3 ** grid_rows[f"r{row+1}"]
            + io.input_shape2_col1 ** grid_cols[f"c{col}"]
            + io.input_shape2_col2 ** grid_cols[f"c{col-1}"]
            + io.input_shape2_col3 ** grid_cols[f"c{col}"]
            + io.input_shape4_row1 ** grid_rows[f"r{row+i}"]
            + io.input_shape4_row2 ** grid_rows[f"r{row+i}"]
            + io.input_shape4_row3 ** grid_rows[f"r{row+i}"]
            + io.input_shape4_col1 ** grid_cols[f"c{col-3-i}"]
            + io.input_shape4_col2 ** grid_cols[f"c{col-2-i}"]
            + io.input_shape4_col3 ** grid_cols[f"c{col-1-i}"]
            >>
            + io.target_shape2 ** bricks.mirror_L
            + io.target_shape4 ** bricks.horizontal
            + io.target_shape2_row1 ** grid_rows[f"r{row}"]
            + io.target_shape2_row2 ** grid_rows[f"r{row+1}"]
            + io.target_shape2_row3 ** grid_rows[f"r{row+1}"]
            + io.target_shape2_col1 ** grid_cols[f"c{col}"]
            + io.target_shape2_col2 ** grid_cols[f"c{col-1}"]
            + io.target_shape2_col3 ** grid_cols[f"c{col}"]
            + io.target_shape4_row1 ** grid_rows[f"r{row+i}"]
            + io.target_shape4_row2 ** grid_rows[f"r{row+i}"]
            + io.target_shape4_row3 ** grid_rows[f"r{row+i}"]
            + io.target_shape4_col1 ** grid_cols[f"c{col-3-i}"]
            + io.target_shape4_col2 ** grid_cols[f"c{col-2-i}"]
            + io.target_shape4_col3 ** grid_cols[f"c{col-1-i}"]
        ) 
        for i in range(2) for row in range(1, 6) for col in range(4+i, 7)
    ]

    mirror_L_above_horizontal_placement_rule = [
        (
            + io.input_shape2 ** bricks.mirror_L
            + io.input_shape4 ** bricks.horizontal
            + io.input_shape2_row1 ** grid_rows[f"r{row}"]
            + io.input_shape2_row2 ** grid_rows[f"r{row+1}"]
            + io.input_shape2_row3 ** grid_rows[f"r{row+1}"]
            + io.input_shape2_col1 ** grid_cols[f"c{col}"]
            + io.input_shape2_col2 ** grid_cols[f"c{col-1}"]
            + io.input_shape2_col3 ** grid_cols[f"c{col}"]
            + io.input_shape4_row1 ** grid_rows[f"r{row+2}"]
            + io.input_shape4_row2 ** grid_rows[f"r{row+2}"]
            + io.input_shape4_row3 ** grid_rows[f"r{row+2}"]
            + io.input_shape4_col1 ** grid_cols[f"c{col-2+i}"]
            + io.input_shape4_col2 ** grid_cols[f"c{col-1+i}"]
            + io.input_shape4_col3 ** grid_cols[f"c{col+i}"]
            >>
            + io.target_shape2 ** bricks.mirror_L
            + io.target_shape4 ** bricks.horizontal
            + io.target_shape2_row1 ** grid_rows[f"r{row}"]
            + io.target_shape2_row2 ** grid_rows[f"r{row+1}"]
            + io.target_shape2_row3 ** grid_rows[f"r{row+1}"]
            + io.target_shape2_col1 ** grid_cols[f"c{col}"]
            + io.target_shape2_col2 ** grid_cols[f"c{col-1}"]
            + io.target_shape2_col3 ** grid_cols[f"c{col}"]
            + io.target_shape4_row1 ** grid_rows[f"r{row+2}"]
            + io.target_shape4_row2 ** grid_rows[f"r{row+2}"]
            + io.target_shape4_row3 ** grid_rows[f"r{row+2}"]
            + io.target_shape4_col1 ** grid_cols[f"c{col-2+i}"]
            + io.target_shape4_col2 ** grid_cols[f"c{col-1+i}"]
            + io.target_shape4_col3 ** grid_cols[f"c{col+i}"]
            )
            for i in range(3) for row in range(1, 5) for col in range(2 + (i == 0), 7-i)
    ]

    mirror_L_below_horizontal_placement_rule = [
        (
            + io.input_shape2 ** bricks.mirror_L
            + io.input_shape4 ** bricks.horizontal
            + io.input_shape2_row1 ** grid_rows[f"r{row}"]
            + io.input_shape2_row2 ** grid_rows[f"r{row+1}"]
            + io.input_shape2_row3 ** grid_rows[f"r{row+1}"]
            + io.input_shape2_col1 ** grid_cols[f"c{col}"]
            + io.input_shape2_col2 ** grid_cols[f"c{col-1}"]
            + io.input_shape2_col3 ** grid_cols[f"c{col}"]
            + io.input_shape4_row1 ** grid_rows[f"r{row-1}"]
            + io.input_shape4_row2 ** grid_rows[f"r{row-1}"]
            + io.input_shape4_row3 ** grid_rows[f"r{row-1}"]
            + io.input_shape4_col1 ** grid_cols[f"c{col-2+i}"]
            + io.input_shape4_col2 ** grid_cols[f"c{col-1+i}"]
            + io.input_shape4_col3 ** grid_cols[f"c{col+i}"]
            >>
            + io.target_shape2 ** bricks.mirror_L
            + io.target_shape4 ** bricks.horizontal
            + io.target_shape2_row1 ** grid_rows[f"r{row}"]
            + io.target_shape2_row2 ** grid_rows[f"r{row+1}"]
            + io.target_shape2_row3 ** grid_rows[f"r{row+1}"]
            + io.target_shape2_col1 ** grid_cols[f"c{col}"]
            + io.target_shape2_col2 ** grid_cols[f"c{col-1}"]
            + io.target_shape2_col3 ** grid_cols[f"c{col}"]
            + io.target_shape4_row1 ** grid_rows[f"r{row-1}"]
            + io.target_shape4_row2 ** grid_rows[f"r{row-1}"]
            + io.target_shape4_row3 ** grid_rows[f"r{row-1}"]
            + io.target_shape4_col1 ** grid_cols[f"c{col-2+i}"]
            + io.target_shape4_col2 ** grid_cols[f"c{col-1+i}"]
            + io.target_shape4_col3 ** grid_cols[f"c{col+i}"]
            ) 
            for i in range (3) for row in range(2, 6) for col in range(3-(i!=0), 7-i)
    ]

    mirror_L_left_vertical_placement_rule  = [
        (
            + io.input_shape2 ** bricks.mirror_L
            + io.input_shape3 ** bricks.vertical
            + io.input_shape2_row1 ** grid_rows[f"r{row}"]
            + io.input_shape2_row2 ** grid_rows[f"r{row+1}"]
            + io.input_shape2_row3 ** grid_rows[f"r{row+1}"]
            + io.input_shape2_col1 ** grid_cols[f"c{col}"]
            + io.input_shape2_col2 ** grid_cols[f"c{col-1}"]
            + io.input_shape2_col3 ** grid_cols[f"c{col}"]
            + io.input_shape3_row1 ** grid_rows[f"r{row-1+i}"]
            + io.input_shape3_row2 ** grid_rows[f"r{row+i}"]
            + io.input_shape3_row3 ** grid_rows[f"r{row+1+i}"]
            + io.input_shape3_col1 ** grid_cols[f"c{col+1}"]
            + io.input_shape3_col2 ** grid_cols[f"c{col+1}"]
            + io.input_shape3_col3 ** grid_cols[f"c{col+1}"]
            >>
            + io.target_shape2 ** bricks.mirror_L
            + io.target_shape3 ** bricks.vertical
            + io.target_shape2_row1 ** grid_rows[f"r{row}"]
            + io.target_shape2_row2 ** grid_rows[f"r{row+1}"]
            + io.target_shape2_row3 ** grid_rows[f"r{row+1}"]
            + io.target_shape2_col1 ** grid_cols[f"c{col}"]
            + io.target_shape2_col2 ** grid_cols[f"c{col-1}"]
            + io.target_shape2_col3 ** grid_cols[f"c{col}"]
            + io.target_shape3_row1 ** grid_rows[f"r{row-1+i}"]
            + io.target_shape3_row2 ** grid_rows[f"r{row+i}"]
            + io.target_shape3_row3 ** grid_rows[f"r{row+1+i}"]
            + io.target_shape3_col1 ** grid_cols[f"c{col+1}"]
            + io.target_shape3_col2 ** grid_cols[f"c{col+1}"]
            + io.target_shape3_col3 ** grid_cols[f"c{col+1}"]
            ) 
            for i in range(3) for row in range(1+(i==0), 6-i) for col in range(2, 6)
    ]

    mirror_L_right_vertical_placement_rule = [
        (
            + io.input_shape2 ** bricks.mirror_L
            + io.input_shape3 ** bricks.vertical
            + io.input_shape2_row1 ** grid_rows[f"r{row}"]
            + io.input_shape2_row2 ** grid_rows[f"r{row+1}"]
            + io.input_shape2_row3 ** grid_rows[f"r{row+1}"]
            + io.input_shape2_col1 ** grid_cols[f"c{col}"]
            + io.input_shape2_col2 ** grid_cols[f"c{col-1}"]
            + io.input_shape2_col3 ** grid_cols[f"c{col}"]
            + io.input_shape3_row1 ** grid_rows[f"r{row+1-i}"]
            + io.input_shape3_row2 ** grid_rows[f"r{row+2-i}"]
            + io.input_shape3_row3 ** grid_rows[f"r{row+3-i}"]
            + io.input_shape3_col1 ** grid_cols[f"c{col-2 + (i == 3)}"]
            + io.input_shape3_col2 ** grid_cols[f"c{col-2 + (i == 3)}"]
            + io.input_shape3_col3 ** grid_cols[f"c{col-2 + (i == 3)}"]
            >>
            + io.target_shape2 ** bricks.mirror_L
            + io.target_shape3 ** bricks.vertical
            + io.target_shape2_row1 ** grid_rows[f"r{row}"]
            + io.target_shape2_row2 ** grid_rows[f"r{row+1}"]
            + io.target_shape2_row3 ** grid_rows[f"r{row+1}"]
            + io.target_shape2_col1 ** grid_cols[f"c{col}"]
            + io.target_shape2_col2 ** grid_cols[f"c{col-1}"]
            + io.target_shape2_col3 ** grid_cols[f"c{col}"]
            + io.target_shape3_row1 ** grid_rows[f"r{row+1-i}"]
            + io.target_shape3_row2 ** grid_rows[f"r{row+2-i}"]
            + io.target_shape3_row3 ** grid_rows[f"r{row+3-i}"]
            + io.target_shape3_col1 ** grid_cols[f"c{col-2 + (i == 3)}"]
            + io.target_shape3_col2 ** grid_cols[f"c{col-2 + (i == 3)}"]
            + io.target_shape3_col3 ** grid_cols[f"c{col-2 + (i == 3)}"]
            )
            for i in range(4) for row in range(1+max(0, i-1), min(4+i, 6)) for col in range(3 - (i == 3), 7)
    ]

    mirror_L_above_vertical_placement_rule = [
        (
            + io.input_shape2 ** bricks.mirror_L
            + io.input_shape3 ** bricks.vertical
            + io.input_shape2_row1 ** grid_rows[f"r{row}"]
            + io.input_shape2_row2 ** grid_rows[f"r{row+1}"]
            + io.input_shape2_row3 ** grid_rows[f"r{row+1}"]
            + io.input_shape2_col1 ** grid_cols[f"c{col}"]
            + io.input_shape2_col2 ** grid_cols[f"c{col-1}"]
            + io.input_shape2_col3 ** grid_cols[f"c{col}"]
            + io.input_shape3_row1 ** grid_rows[f"r{row+2}"]
            + io.input_shape3_row2 ** grid_rows[f"r{row+3}"]
            + io.input_shape3_row3 ** grid_rows[f"r{row+4}"]
            + io.input_shape3_col1 ** grid_cols[f"c{col-1+i}"]
            + io.input_shape3_col2 ** grid_cols[f"c{col-1+i}"]
            + io.input_shape3_col3 ** grid_cols[f"c{col-1+i}"]
            >>
            + io.target_shape2 ** bricks.mirror_L
            + io.target_shape3 ** bricks.vertical
            + io.target_shape2_row1 ** grid_rows[f"r{row}"]
            + io.target_shape2_row2 ** grid_rows[f"r{row+1}"]
            + io.target_shape2_row3 ** grid_rows[f"r{row+1}"]
            + io.target_shape2_col1 ** grid_cols[f"c{col}"]
            + io.target_shape2_col2 ** grid_cols[f"c{col-1}"]
            + io.target_shape2_col3 ** grid_cols[f"c{col}"]
            + io.target_shape3_row1 ** grid_rows[f"r{row+2}"]
            + io.target_shape3_row2 ** grid_rows[f"r{row+3}"]
            + io.target_shape3_row3 ** grid_rows[f"r{row+4}"]
            + io.target_shape3_col1 ** grid_cols[f"c{col-1+i}"]
            + io.target_shape3_col2 ** grid_cols[f"c{col-1+i}"]
            + io.target_shape3_col3 ** grid_cols[f"c{col-1+i}"]
        )
        for i in range(2) for row in range(1, 3) for col in range(2, 7)
    ]

    mirror_L_below_vertical_placement_rule = [
        (
            + io.input_shape2 ** bricks.mirror_L
            + io.input_shape3 ** bricks.vertical
            + io.input_shape2_row1 ** grid_rows[f"r{row}"]
            + io.input_shape2_row2 ** grid_rows[f"r{row+1}"]
            + io.input_shape2_row3 ** grid_rows[f"r{row+1}"]
            + io.input_shape2_col1 ** grid_cols[f"c{col}"]
            + io.input_shape2_col2 ** grid_cols[f"c{col-1}"]
            + io.input_shape2_col3 ** grid_cols[f"c{col}"]
            + io.input_shape3_row1 ** grid_rows[f"r{row-3}"]
            + io.input_shape3_row2 ** grid_rows[f"r{row-2}"]
            + io.input_shape3_row3 ** grid_rows[f"r{row-1}"]
            + io.input_shape3_col1 ** grid_cols[f"c{col}"]
            + io.input_shape3_col2 ** grid_cols[f"c{col}"]
            + io.input_shape3_col3 ** grid_cols[f"c{col}"]
            >>
            + io.target_shape2 ** bricks.mirror_L
            + io.target_shape3 ** bricks.vertical
            + io.target_shape2_row1 ** grid_rows[f"r{row}"]
            + io.target_shape2_row2 ** grid_rows[f"r{row+1}"]
            + io.target_shape2_row3 ** grid_rows[f"r{row+1}"]
            + io.target_shape2_col1 ** grid_cols[f"c{col}"]
            + io.target_shape2_col2 ** grid_cols[f"c{col-1}"]
            + io.target_shape2_col3 ** grid_cols[f"c{col}"]
            + io.target_shape3_row1 ** grid_rows[f"r{row-3}"]
            + io.target_shape3_row2 ** grid_rows[f"r{row-2}"]
            + io.target_shape3_row3 ** grid_rows[f"r{row-1}"]
            + io.target_shape3_col1 ** grid_cols[f"c{col}"]
            + io.target_shape3_col2 ** grid_cols[f"c{col}"]
            + io.target_shape3_col3 ** grid_cols[f"c{col}"]
            )
            for row in range(4, 6) for col in range(2, 7)
    ]

    horizontal_left_vertical_placement_rule  = [
        (
            + io.input_shape3 ** bricks.horizontal
            + io.input_shape4 ** bricks.vertical
            + io.input_shape3_row1 ** grid_rows[f"r{row}"]
            + io.input_shape3_row2 ** grid_rows[f"r{row}"]
            + io.input_shape3_row3 ** grid_rows[f"r{row}"]
            + io.input_shape3_col1 ** grid_cols[f"c{col}"]
            + io.input_shape3_col2 ** grid_cols[f"c{col+1}"] 
            + io.input_shape3_col3 ** grid_cols[f"c{col+2}"]
            + io.input_shape4_row1 ** grid_rows[f"r{row-2+i}"]
            + io.input_shape4_row2 ** grid_rows[f"r{row-1+i}"]
            + io.input_shape4_row3 ** grid_rows[f"r{row+i}"]
            + io.input_shape4_col1 ** grid_cols[f"c{col+3}"]
            + io.input_shape4_col2 ** grid_cols[f"c{col+3}"]
            + io.input_shape4_col3 ** grid_cols[f"c{col+3}"]
            >>
            + io.target_shape3 ** bricks.horizontal
            + io.target_shape4 ** bricks.vertical
            + io.target_shape3_row1 ** grid_rows[f"r{row}"]
            + io.target_shape3_row2 ** grid_rows[f"r{row}"]
            + io.target_shape3_row3 ** grid_rows[f"r{row}"]
            + io.target_shape3_col1 ** grid_cols[f"c{col}"]
            + io.target_shape3_col2 ** grid_cols[f"c{col+1}"] 
            + io.target_shape3_col3 ** grid_cols[f"c{col+2}"]
            + io.target_shape4_row1 ** grid_rows[f"r{row-2+i}"]
            + io.target_shape4_row2 ** grid_rows[f"r{row-1+i}"]
            + io.target_shape4_row3 ** grid_rows[f"r{row+i}"]
            + io.target_shape4_col1 ** grid_cols[f"c{col+3}"]
            + io.target_shape4_col2 ** grid_cols[f"c{col+3}"]
            + io.target_shape4_col3 ** grid_cols[f"c{col+3}"]
            ) 
            for i in range(3) for row in range(3-i, 7-i) for col in range(1, 4)
    ]

    horizontal_right_vertical_placement_rule = [
        (
            + io.input_shape3 ** bricks.horizontal
            + io.input_shape4 ** bricks.vertical
            + io.input_shape3_row1 ** grid_rows[f"r{row}"]
            + io.input_shape3_row2 ** grid_rows[f"r{row}"]
            + io.input_shape3_row3 ** grid_rows[f"r{row}"]
            + io.input_shape3_col1 ** grid_cols[f"c{col}"]
            + io.input_shape3_col2 ** grid_cols[f"c{col+1}"] 
            + io.input_shape3_col3 ** grid_cols[f"c{col+2}"]
            + io.input_shape4_row1 ** grid_rows[f"r{row-2+i}"]
            + io.input_shape4_row2 ** grid_rows[f"r{row-1+i}"]
            + io.input_shape4_row3 ** grid_rows[f"r{row+i}"]
            + io.input_shape4_col1 ** grid_cols[f"c{col-1}"]
            + io.input_shape4_col2 ** grid_cols[f"c{col-1}"]
            + io.input_shape4_col3 ** grid_cols[f"c{col-1}"]
            >>
            + io.target_shape3 ** bricks.horizontal
            + io.target_shape4 ** bricks.vertical
            + io.target_shape3_row1 ** grid_rows[f"r{row}"]
            + io.target_shape3_row2 ** grid_rows[f"r{row}"]
            + io.target_shape3_row3 ** grid_rows[f"r{row}"]
            + io.target_shape3_col1 ** grid_cols[f"c{col}"]
            + io.target_shape3_col2 ** grid_cols[f"c{col+1}"] 
            + io.target_shape3_col3 ** grid_cols[f"c{col+2}"]
            + io.target_shape4_row1 ** grid_rows[f"r{row-2+i}"]
            + io.target_shape4_row2 ** grid_rows[f"r{row-1+i}"]
            + io.target_shape4_row3 ** grid_rows[f"r{row+i}"]
            + io.target_shape4_col1 ** grid_cols[f"c{col-1}"]
            + io.target_shape4_col2 ** grid_cols[f"c{col-1}"]
            + io.target_shape4_col3 ** grid_cols[f"c{col-1}"]
            ) 
            for i in range(3) for row in range(3-i, 7-i) for col in range(2, 5)
    ]

    horizontal_above_vertical_placement_rule = [
        (
            + io.input_shape3 ** bricks.horizontal
            + io.input_shape4 ** bricks.vertical
            + io.input_shape3_row1 ** grid_rows[f"r{row}"]
            + io.input_shape3_row2 ** grid_rows[f"r{row}"]
            + io.input_shape3_row3 ** grid_rows[f"r{row}"]
            + io.input_shape3_col1 ** grid_cols[f"c{col}"]
            + io.input_shape3_col2 ** grid_cols[f"c{col+1}"] 
            + io.input_shape3_col3 ** grid_cols[f"c{col+2}"]
            + io.input_shape4_row1 ** grid_rows[f"r{row+1}"]
            + io.input_shape4_row2 ** grid_rows[f"r{row+2}"]
            + io.input_shape4_row3 ** grid_rows[f"r{row+3}"]
            + io.input_shape4_col1 ** grid_cols[f"c{col+i}"]
            + io.input_shape4_col2 ** grid_cols[f"c{col+i}"]
            + io.input_shape4_col3 ** grid_cols[f"c{col+i}"]
            >>
            + io.target_shape3 ** bricks.horizontal
            + io.target_shape4 ** bricks.vertical
            + io.target_shape3_row1 ** grid_rows[f"r{row}"]
            + io.target_shape3_row2 ** grid_rows[f"r{row}"]
            + io.target_shape3_row3 ** grid_rows[f"r{row}"]
            + io.target_shape3_col1 ** grid_cols[f"c{col}"]
            + io.target_shape3_col2 ** grid_cols[f"c{col+1}"] 
            + io.target_shape3_col3 ** grid_cols[f"c{col+2}"]
            + io.target_shape4_row1 ** grid_rows[f"r{row+1}"]
            + io.target_shape4_row2 ** grid_rows[f"r{row+2}"]
            + io.target_shape4_row3 ** grid_rows[f"r{row+3}"]
            + io.target_shape4_col1 ** grid_cols[f"c{col+i}"]
            + io.target_shape4_col2 ** grid_cols[f"c{col+i}"]
            + io.target_shape4_col3 ** grid_cols[f"c{col+i}"]
        ) 
        for i in range(3) for row in range(1, 4) for col in range(1, 5)
    ]

    horizontal_below_vertical_placement_rule = [
        (
            + io.input_shape3 ** bricks.horizontal
            + io.input_shape4 ** bricks.vertical
            + io.input_shape3_row1 ** grid_rows[f"r{row}"]
            + io.input_shape3_row2 ** grid_rows[f"r{row}"]
            + io.input_shape3_row3 ** grid_rows[f"r{row}"]
            + io.input_shape3_col1 ** grid_cols[f"c{col}"]
            + io.input_shape3_col2 ** grid_cols[f"c{col+1}"] 
            + io.input_shape3_col3 ** grid_cols[f"c{col+2}"]
            + io.input_shape4_row1 ** grid_rows[f"r{row-3}"]
            + io.input_shape4_row2 ** grid_rows[f"r{row-2}"]
            + io.input_shape4_row3 ** grid_rows[f"r{row-1}"]
            + io.input_shape4_col1 ** grid_cols[f"c{col+i}"]
            + io.input_shape4_col2 ** grid_cols[f"c{col+i}"]
            + io.input_shape4_col3 ** grid_cols[f"c{col+i}"]
            >>
            + io.target_shape3 ** bricks.horizontal
            + io.target_shape4 ** bricks.vertical
            + io.target_shape3_row1 ** grid_rows[f"r{row}"]
            + io.target_shape3_row2 ** grid_rows[f"r{row}"]
            + io.target_shape3_row3 ** grid_rows[f"r{row}"]
            + io.target_shape3_col1 ** grid_cols[f"c{col}"]
            + io.target_shape3_col2 ** grid_cols[f"c{col+1}"] 
            + io.target_shape3_col3 ** grid_cols[f"c{col+2}"]
            + io.target_shape4_row1 ** grid_rows[f"r{row-3}"]
            + io.target_shape4_row2 ** grid_rows[f"r{row-2}"]
            + io.target_shape4_row3 ** grid_rows[f"r{row-1}"]
            + io.target_shape4_col1 ** grid_cols[f"c{col+i}"]
            + io.target_shape4_col2 ** grid_cols[f"c{col+i}"]
            + io.target_shape4_col3 ** grid_cols[f"c{col+i}"]
            )
            for i in range(3) for row in range(4, 7) for col in range(1, 5)
    ]

    # END_CONSTRUCTION RULE
    # if all four blocks have been used, then stop construction
    #TODO: is it possible for a dimension to not be bound with anything? that is the empty state yes? -- 0.0 activation value yea?
    stop_construction_rule_all_four = [(
        + io.target_shape1 ** bricks.half_T
        + io.target_shape2 ** bricks.mirror_L
        + io.target_shape3 ** bricks.vertical
        + io.target_shape4 ** bricks.horizontal

        >>
        + io.construction_signal ** con_signal.stop_construction)
    ]

    brick_map = {1: d.bricks.half_T, 2: d.bricks.mirror_L, 3: d.bricks.vertical, 4: d.bricks.horizontal}
    stop_construction_input_blocks_used_one = [(
        io.brick_nos ** brick_nos[f"n1"]
        + io[f"input_shape{shape_no}"] ** brick_map[shape_no]
        + io[f"target_shape{shape_no}"] ** brick_map[shape_no]
        >>
        io.construction_signal ** con_signal.stop_construction
        )
        for shape_no in range(1, 5)
    ]

    stop_construction_input_blocks_used_two = [
        (
            io.brick_nos ** brick_nos[f"n2"]
            + io[f"input_shape{shape_no1}"] ** brick_map[shape_no1]
            + io[f"input_shape{shape_no2}"] ** brick_map[shape_no2]
            + io[f"target_shape{shape_no1}"] ** brick_map[shape_no1]
            + io[f"target_shape{shape_no2}"] ** brick_map[shape_no2]
            >>
            io.construction_signal ** con_signal.stop_construction
        )
        for shape_no1 in range(1, 5) for shape_no2 in range(1, 5) if shape_no1 != shape_no2
    ]

    stop_construction_input_blocks_used_three = [
        (
            io.brick_nos ** brick_nos[f"n3"]
            + io[f"input_shape{shape_no1}"] ** brick_map[shape_no1]
            + io[f"input_shape{shape_no2}"] ** brick_map[shape_no2]
            + io[f"input_shape{shape_no3}"] ** brick_map[shape_no3]
            + io[f"target_shape{shape_no1}"] ** brick_map[shape_no1]
            + io[f"target_shape{shape_no2}"] ** brick_map[shape_no2]
            + io[f"target_shape{shape_no3}"] ** brick_map[shape_no3]
            >>
            io.construction_signal ** con_signal.stop_construction
        )
        for shape_no1 in range(1, 5) for shape_no2 in range(1, 5) for shape_no3 in range(1, 5) 
        if shape_no1 != shape_no2 and shape_no1 != shape_no3 and shape_no2 != shape_no3
    ]
    
    # participant.search_space_rules.rules.compile(
    #     *(
    #         stop_construction_rule_all_four + stop_construction_input_blocks_used_one + stop_construction_input_blocks_used_two + stop_construction_input_blocks_used_three
    #         + half_T_first_placement_rule + mirror_L_first_placement_rule + horizontal_first_placement_rule + vertical_first_placement_rule
    #         + half_T_left_of_horizontal_placement_rule + half_T_right_of_horizontal_placement_rule + half_T_above_horizontal_placement_rule + half_T_below_horizontal_placement_rule
    #         + half_T_left_vertical_placement_rule + half_T_right_vertical_placement_rule + half_T_above_vertical_placement_rule + half_T_below_vertical_placement_rule
    #         + half_T_left_mirror_L_placement_rule + half_T_right_mirror_L_placement_rule + half_T_above_mirror_L_placement_rule + half_T_below_mirror_L_placement_rule
    #         + mirror_L_left_horizontal_placement_rule + mirror_L_right_horizontal_placement_rule + mirror_L_above_horizontal_placement_rule + mirror_L_below_horizontal_placement_rule
    #         + mirror_L_left_vertical_placement_rule + mirror_L_right_vertical_placement_rule + mirror_L_above_vertical_placement_rule + mirror_L_below_vertical_placement_rule
    #         + horizontal_left_vertical_placement_rule + horizontal_right_vertical_placement_rule + horizontal_above_vertical_placement_rule + horizontal_below_vertical_placement_rule 
    #     )
    # )

    # temporary: to evaluate the functioning of response rules
    dummy_stop_construction_rule = [(
        #TODO: empty condition?
        + io[f"input_shape{shape_no}"] ** bricks[brick_name]
        >>
        io.construction_signal ** con_signal.stop_construction 
    )
     for (shape_no, brick_name) in zip(range(1, 5), ["half_T", "mirror_L", "vertical", "horizontal"])
    ]

    participant.search_space_rules.rules.compile(
        *dummy_stop_construction_rule
    )