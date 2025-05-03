import math
import itertools

SHAPES = ["half_T", "mirror_L", "vertical", "horizontal"]


def init_participant_response_rules(participant) -> None:
    d = participant.response_space
    io = d.io
    bricks = d.bricks
    numbers = d.numbers
    query_rel = d.query_rel
    response = d.response

    # response rules when given a query and some blocks

    # HALF_T X HORIZONTAL
    # i = 0, horizontal is next to the potruding part of the shape, else it is next to the flat part at the bottom
    half_t_left_of_horizontal = [
        (
            +(
                io.query_block
                ** (bricks.half_T if not switcharoo else bricks.horizontal)
            )
            - io.query_block**bricks.vertical
            - io.query_block**bricks.mirror_L
            - io.query_block ** (bricks.horizontal if not switcharoo else bricks.half_T)
            + io.query_block_reference
            ** (bricks.horizontal if not switcharoo else bricks.half_T)
            - io.query_block_reference**bricks.vertical
            - io.query_block_reference**bricks.mirror_L
            - io.query_block_reference
            ** (bricks.half_T if not switcharoo else bricks.horizontal)
            + 2.0
            * (
                io.query_relation
                ** (query_rel.left if not switcharoo else query_rel.right)
            )
            - 2.0
            * (
                io.query_relation
                ** (query_rel.right if not switcharoo else query_rel.left)
            )
            - 2.0 * (io.query_relation**query_rel.above)
            - 2.0 * (io.query_relation**query_rel.below)
            + io.target_half_T**response.yes
            + io.target_horizontal**response.yes
            + io.target_half_T_row1 ** numbers[f"n{row}"]
            + io.target_half_T_row2 ** numbers[f"n{row}"]
            + io.target_half_T_row3 ** numbers[f"n{row + 1}"]
            + io.target_half_T_col1 ** numbers[f"n{col}"]
            + io.target_half_T_col2 ** numbers[f"n{col + 1}"]
            + io.target_half_T_col3 ** numbers[f"n{col}"]
            + io.target_horizontal_row1 ** numbers[f"n{row + i}"]
            + io.target_horizontal_row2 ** numbers[f"n{row + i}"]
            + io.target_horizontal_row3 ** numbers[f"n{row + i}"]
            + io.target_horizontal_col1 ** numbers[f"n{col + 2 - i}"]
            + io.target_horizontal_col2 ** numbers[f"n{col + 3 - i}"]
            + io.target_horizontal_col3 ** numbers[f"n{col + 4 - i}"]
            >> +(io.output**response.yes)
        )
        for switcharoo in (True, False)
        for i in range(2)
        for row in range(1, 6)
        for col in range(1, 3 + i)
    ]

    half_t_right_of_horizontal = [
        (
            +(
                io.query_block
                ** (bricks.half_T if not switcharoo else bricks.horizontal)
            )
            - io.query_block**bricks.vertical
            - io.query_block**bricks.mirror_L
            - io.query_block ** (bricks.horizontal if not switcharoo else bricks.half_T)
            + io.query_block_reference
            ** (bricks.horizontal if not switcharoo else bricks.half_T)
            - io.query_block_reference**bricks.vertical
            - io.query_block_reference**bricks.mirror_L
            - io.query_block_reference
            ** (bricks.half_T if not switcharoo else bricks.horizontal)
            + 2.0
            * (
                io.query_relation
                ** (query_rel.right if not switcharoo else query_rel.left)
            )
            - 2.0
            * (
                io.query_relation
                ** (query_rel.left if not switcharoo else query_rel.right)
            )
            - 2.0 * (io.query_relation**query_rel.above)
            - 2.0 * (io.query_relation**query_rel.below)
            + io.target_half_T**response.yes
            + io.target_horizontal**response.yes
            + io.target_half_T_row1 ** numbers[f"n{row}"]
            + io.target_half_T_row2 ** numbers[f"n{row}"]
            + io.target_half_T_row3 ** numbers[f"n{row + 1}"]
            + io.target_half_T_col1 ** numbers[f"n{col}"]
            + io.target_half_T_col2 ** numbers[f"n{col + 1}"]
            + io.target_half_T_col3 ** numbers[f"n{col}"]
            + io.target_horizontal_row1 ** numbers[f"n{row + i}"]
            + io.target_horizontal_row2 ** numbers[f"n{row + i}"]
            + io.target_horizontal_row3 ** numbers[f"n{row + i}"]
            + io.target_horizontal_col1 ** numbers[f"n{col - 3}"]
            + io.target_horizontal_col2 ** numbers[f"n{col - 2}"]
            + io.target_horizontal_col3 ** numbers[f"n{col - 1}"]
            >> +(io.output**response.yes)
        )
        for switcharoo in (True, False)
        for i in range(2)
        for row in range(1, 6)
        for col in range(4, 6)
    ]

    half_t_below_horizontal = [
        (
            +(
                io.query_block
                ** (bricks.half_T if not switcharoo else bricks.horizontal)
            )
            - io.query_block**bricks.vertical
            - io.query_block**bricks.mirror_L
            - io.query_block ** (bricks.horizontal if not switcharoo else bricks.half_T)
            + io.query_block_reference
            ** (bricks.horizontal if not switcharoo else bricks.half_T)
            - io.query_block_reference**bricks.vertical
            - io.query_block_reference**bricks.mirror_L
            - io.query_block_reference
            ** (bricks.half_T if not switcharoo else bricks.horizontal)
            + 2.0
            * (
                io.query_relation
                ** (query_rel.below if not switcharoo else query_rel.above)
            )
            - 2.0
            * (
                io.query_relation
                ** (query_rel.above if not switcharoo else query_rel.below)
            )
            - 2.0 * (io.query_relation**query_rel.left)
            - 2.0 * (io.query_relation**query_rel.right)
            + io.target_half_T**response.yes
            + io.target_horizontal**response.yes
            + io.target_half_T_row1 ** numbers[f"n{row}"]
            + io.target_half_T_row2 ** numbers[f"n{row}"]
            + io.target_half_T_row3 ** numbers[f"n{row + 1}"]
            + io.target_half_T_col1 ** numbers[f"n{col}"]
            + io.target_half_T_col2 ** numbers[f"n{col + 1}"]
            + io.target_half_T_col3 ** numbers[f"n{col}"]
            + io.target_horizontal_row1 ** numbers[f"n{row - 1}"]
            + io.target_horizontal_row2 ** numbers[f"n{row - 1}"]
            + io.target_horizontal_row3 ** numbers[f"n{row - 1}"]
            + io.target_horizontal_col1 ** numbers[f"n{col - 2 + i}"]
            + io.target_horizontal_col2 ** numbers[f"n{col - 1 + i}"]
            + io.target_horizontal_col3 ** numbers[f"n{col + i}"]
            >> +(io.output**response.yes)
        )
        for switcharoo in (True, False)
        for i in range(4)
        for row in range(2, 6)
        for col in range(max(3 - i, 1), 6 - max(i - 1, 0))
    ]

    half_t_above_horizontal = [
        (
            +(
                io.query_block
                ** (bricks.half_T if not switcharoo else bricks.horizontal)
            )
            - io.query_block**bricks.vertical
            - io.query_block**bricks.mirror_L
            - io.query_block ** (bricks.horizontal if not switcharoo else bricks.half_T)
            + io.query_block_reference
            ** (bricks.horizontal if not switcharoo else bricks.half_T)
            - io.query_block_reference**bricks.vertical
            - io.query_block_reference**bricks.mirror_L
            - io.query_block_reference
            ** (bricks.half_T if not switcharoo else bricks.horizontal)
            + 2.0
            * (
                io.query_relation
                ** (query_rel.above if not switcharoo else query_rel.below)
            )
            - 2.0
            * (
                io.query_relation
                ** (query_rel.below if not switcharoo else query_rel.above)
            )
            - 2.0 * (io.query_relation**query_rel.left)
            - 2.0 * (io.query_relation**query_rel.right)
            + io.target_half_T**response.yes
            + io.target_horizontal**response.yes
            + io.target_half_T_row1 ** numbers[f"n{row}"]
            + io.target_half_T_row2 ** numbers[f"n{row}"]
            + io.target_half_T_row3 ** numbers[f"n{row + 1}"]
            + io.target_half_T_col1 ** numbers[f"n{col}"]
            + io.target_half_T_col2 ** numbers[f"n{col + 1}"]
            + io.target_half_T_col3 ** numbers[f"n{col}"]
            + io.target_horizontal_row1 ** numbers[f"n{row + 2}"]
            + io.target_horizontal_row2 ** numbers[f"n{row + 2}"]
            + io.target_horizontal_row3 ** numbers[f"n{row + 2}"]
            + io.target_horizontal_col1 ** numbers[f"n{col - 2 + i}"]
            + io.target_horizontal_col2 ** numbers[f"n{col - 1 + i}"]
            + io.target_horizontal_col3 ** numbers[f"n{col + i}"]
            >> +(io.output**response.yes)
        )
        for i in range(3)
        for switcharoo in (True, False)
        for row in range(1, 5)
        for col in range(3 - i, 6 - (i == 2))
    ]

    # HALF_T X VERTICAL

    half_t_left_vertical = [
        (
            +(io.query_block ** (bricks.half_T if not switcharoo else bricks.vertical))
            - io.query_block**bricks.horizontal
            - io.query_block**bricks.mirror_L
            - io.query_block ** (bricks.vertical if not switcharoo else bricks.half_T)
            + io.query_block_reference
            ** (bricks.vertical if not switcharoo else bricks.half_T)
            - io.query_block_reference**bricks.horizontal
            - io.query_block_reference**bricks.mirror_L
            - io.query_block_reference
            ** (bricks.half_T if not switcharoo else bricks.vertical)
            + 2.0
            * (
                io.query_relation
                ** (query_rel.left if not switcharoo else query_rel.right)
            )
            - 2.0
            * (
                io.query_relation
                ** (query_rel.right if not switcharoo else query_rel.left)
            )
            - 2.0 * (io.query_relation**query_rel.above)
            - 2.0 * (io.query_relation**query_rel.below)
            + io.target_half_T**response.yes
            + io.target_vertical**response.yes
            + io.target_half_T_row1 ** numbers[f"n{row}"]
            + io.target_half_T_row2 ** numbers[f"n{row}"]
            + io.target_half_T_row3 ** numbers[f"n{row + 1}"]
            + io.target_half_T_col1 ** numbers[f"n{col}"]
            + io.target_half_T_col2 ** numbers[f"n{col + 1}"]
            + io.target_half_T_col3 ** numbers[f"n{col}"]
            + io.target_vertical_row1 ** numbers[f"n{row + 1 - i}"]
            + io.target_vertical_row2 ** numbers[f"n{row + 2 - i}"]
            + io.target_vertical_row3 ** numbers[f"n{row + 3 - i}"]
            + io.target_vertical_col1 ** numbers[f"n{col + 2 - (i == 0)}"]
            + io.target_vertical_col2 ** numbers[f"n{col + 2 - (i == 0)}"]
            + io.target_vertical_col3 ** numbers[f"n{col + 2 - (i == 0)}"]
            >> +(io.output**response.yes)
        )
        for switcharoo in (True, False)
        for i in range(4)
        for row in range(1 + (i - 1 if i > 1 else 0), 4 + (math.ceil(i / 2)))
        for col in range(1, 6 - (i > 0))
    ]

    half_t_right_vertical = [
        (
            +(io.query_block ** (bricks.half_T if not switcharoo else bricks.vertical))
            - io.query_block**bricks.horizontal
            - io.query_block**bricks.mirror_L
            - io.query_block ** (bricks.vertical if not switcharoo else bricks.half_T)
            + io.query_block_reference
            ** (bricks.vertical if not switcharoo else bricks.half_T)
            - io.query_block_reference**bricks.horizontal
            - io.query_block_reference**bricks.mirror_L
            - io.query_block_reference
            ** (bricks.half_T if not switcharoo else bricks.vertical)
            + 2.0
            * (
                io.query_relation
                ** (query_rel.right if not switcharoo else query_rel.left)
            )
            - 2.0
            * (
                io.query_relation
                ** (query_rel.left if not switcharoo else query_rel.right)
            )
            - 2.0 * (io.query_relation**query_rel.above)
            - 2.0 * (io.query_relation**query_rel.below)
            + io.target_half_T**response.yes
            + io.target_vertical**response.yes
            + io.target_half_T_row1 ** numbers[f"n{row}"]
            + io.target_half_T_row2 ** numbers[f"n{row}"]
            + io.target_half_T_row3 ** numbers[f"n{row + 1}"]
            + io.target_half_T_col1 ** numbers[f"n{col}"]
            + io.target_half_T_col2 ** numbers[f"n{col + 1}"]
            + io.target_half_T_col3 ** numbers[f"n{col}"]
            + io.target_vertical_row1 ** numbers[f"n{row - 2 + i}"]
            + io.target_vertical_row2 ** numbers[f"n{row - 1 + i}"]
            + io.target_vertical_row3 ** numbers[f"n{row + i}"]
            + io.target_vertical_col1 ** numbers[f"n{col - 1}"]
            + io.target_vertical_col2 ** numbers[f"n{col - 1}"]
            + io.target_vertical_col3 ** numbers[f"n{col - 1}"]
            >> +(io.output**response.yes)
        )
        for switcharoo in (True, False)
        for i in range(4)
        for row in range(max(1, 3 - i), 6 - max(0, i - 1))
        for col in range(2, 6)
    ]

    half_t_below_vertical = [
        (
            +(io.query_block ** (bricks.half_T if not switcharoo else bricks.vertical))
            - io.query_block**bricks.horizontal
            - io.query_block**bricks.mirror_L
            - io.query_block ** (bricks.vertical if not switcharoo else bricks.half_T)
            + io.query_block_reference
            ** (bricks.vertical if not switcharoo else bricks.half_T)
            - io.query_block_reference**bricks.horizontal
            - io.query_block_reference**bricks.mirror_L
            - io.query_block_reference
            ** (bricks.half_T if not switcharoo else bricks.vertical)
            + 2.0
            * (
                io.query_relation
                ** (query_rel.below if not switcharoo else query_rel.above)
            )
            - 2.0
            * (
                io.query_relation
                ** (query_rel.above if not switcharoo else query_rel.below)
            )
            - 2.0 * (io.query_relation**query_rel.left)
            - 2.0 * (io.query_relation**query_rel.right)
            + io.target_half_T**response.yes
            + io.target_vertical**response.yes
            + io.target_half_T_row1 ** numbers[f"n{row}"]
            + io.target_half_T_row2 ** numbers[f"n{row}"]
            + io.target_half_T_row3 ** numbers[f"n{row + 1}"]
            + io.target_half_T_col1 ** numbers[f"n{col}"]
            + io.target_half_T_col2 ** numbers[f"n{col + 1}"]
            + io.target_half_T_col3 ** numbers[f"n{col}"]
            + io.target_vertical_row1 ** numbers[f"n{row - 3}"]
            + io.target_vertical_row2 ** numbers[f"n{row - 2}"]
            + io.target_vertical_row3 ** numbers[f"n{row - 3}"]
            + io.target_vertical_col1 ** numbers[f"n{col + i}"]
            + io.target_vertical_col2 ** numbers[f"n{col + i}"]
            + io.target_vertical_col3 ** numbers[f"n{col + i}"]
            >> +(io.output**response.yes)
        )
        for switcharoo in (True, False)
        for i in range(2)
        for row in range(4, 6)
        for col in range(1, 6)
    ]

    half_t_above_vertical = [
        (
            +(io.query_block ** (bricks.half_T if not switcharoo else bricks.vertical))
            - io.query_block**bricks.horizontal
            - io.query_block**bricks.mirror_L
            - io.query_block ** (bricks.vertical if not switcharoo else bricks.half_T)
            + io.query_block_reference
            ** (bricks.vertical if not switcharoo else bricks.half_T)
            - io.query_block_reference**bricks.horizontal
            - io.query_block_reference**bricks.mirror_L
            - io.query_block_reference
            ** (bricks.half_T if not switcharoo else bricks.vertical)
            + 2.0
            * (
                io.query_relation
                ** (query_rel.above if not switcharoo else query_rel.below)
            )
            - 2.0
            * (
                io.query_relation
                ** (query_rel.below if not switcharoo else query_rel.above)
            )
            - 2.0 * (io.query_relation**query_rel.left)
            - 2.0 * (io.query_relation**query_rel.right)
            + io.target_half_T**response.yes
            + io.target_vertical**response.yes
            + io.target_half_T_row1 ** numbers[f"n{row}"]
            + io.target_half_T_row2 ** numbers[f"n{row}"]
            + io.target_half_T_row3 ** numbers[f"n{row + 1}"]
            + io.target_half_T_col1 ** numbers[f"n{col}"]
            + io.target_half_T_col2 ** numbers[f"n{col + 1}"]
            + io.target_half_T_col3 ** numbers[f"n{col}"]
            + io.target_vertical_row1 ** numbers[f"n{row + 1}"]
            + io.target_vertical_row2 ** numbers[f"n{row + 2}"]
            + io.target_vertical_row3 ** numbers[f"n{row + 3}"]
            + io.target_vertical_col1 ** numbers[f"n{col}"]
            + io.target_vertical_col2 ** numbers[f"n{col}"]
            + io.target_vertical_col3 ** numbers[f"n{col}"]
            >> +(io.output**response.yes)
        )
        for switcharoo in (True, False)
        for row in range(1, 3)
        for col in range(1, 6)
    ]

    # HALF_T X MIRROR_L
    half_t_left_mirror_l = [
        (
            +(io.query_block ** (bricks.half_T if not switcharoo else bricks.mirror_L))
            - io.query_block**bricks.horizontal
            - io.query_block**bricks.vertical
            - io.query_block ** (bricks.mirror_L if not switcharoo else bricks.half_T)
            + io.query_block_reference
            ** (bricks.mirror_L if not switcharoo else bricks.half_T)
            - io.query_block_reference**bricks.horizontal
            - io.query_block_reference**bricks.vertical
            - io.query_block_reference
            ** (bricks.half_T if not switcharoo else bricks.mirror_L)
            + 2.0
            * (
                io.query_relation
                ** (query_rel.left if not switcharoo else query_rel.right)
            )
            - 2.0
            * (
                io.query_relation
                ** (query_rel.right if not switcharoo else query_rel.left)
            )
            - 2.0 * (io.query_relation**query_rel.above)
            - 2.0 * (io.query_relation**query_rel.below)
            + io.target_half_T**response.yes
            + io.target_mirror_L**response.yes
            + io.target_half_T_row1 ** numbers[f"n{row}"]
            + io.target_half_T_row2 ** numbers[f"n{row}"]
            + io.target_half_T_row3 ** numbers[f"n{row + 1}"]
            + io.target_half_T_col1 ** numbers[f"n{col}"]
            + io.target_half_T_col2 ** numbers[f"n{col + 1}"]
            + io.target_half_T_col3 ** numbers[f"n{col}"]
            + io.target_mirror_L_row1 ** numbers[f"n{row - i}"]
            + io.target_mirror_L_row2 ** numbers[f"n{row + 1 - i}"]
            + io.target_mirror_L_row3 ** numbers[f"n{row + 1 - i}"]
            + io.target_mirror_L_col1 ** numbers[f"n{col + 2 + i}"]
            + io.target_mirror_L_col2 ** numbers[f"n{col + 1 + i}"]
            + io.target_mirror_L_col3 ** numbers[f"n{col + 2 + i}"]
            >> +(io.output**response.yes)
        )
        for switcharoo in (True, False)
        for i in range(2)
        for row in range(1 + i, 6)
        for col in range(1, 5 - i)
    ]

    """
    # 1 1 2
    # 1 2 2

    #       2
    # 1 1 2 2
    # 1
    """
    half_t_right_mirror_l = [
        (
            +(io.query_block ** (bricks.half_T if not switcharoo else bricks.mirror_L))
            - io.query_block**bricks.horizontal
            - io.query_block**bricks.vertical
            - io.query_block ** (bricks.mirror_L if not switcharoo else bricks.half_T)
            + io.query_block_reference
            ** (bricks.mirror_L if not switcharoo else bricks.half_T)
            - io.query_block_reference**bricks.horizontal
            - io.query_block_reference**bricks.vertical
            - io.query_block_reference
            ** (bricks.half_T if not switcharoo else bricks.mirror_L)
            + 2.0
            * (
                io.query_relation
                ** (query_rel.right if not switcharoo else query_rel.left)
            )
            - 2.0
            * (
                io.query_relation
                ** (query_rel.left if not switcharoo else query_rel.right)
            )
            - 2.0 * (io.query_relation**query_rel.above)
            - 2.0 * (io.query_relation**query_rel.below)
            + io.target_half_T**response.yes
            + io.target_mirror_L**response.yes
            + io.target_half_T_row1 ** numbers[f"n{row}"]
            + io.target_half_T_row2 ** numbers[f"n{row}"]
            + io.target_half_T_row3 ** numbers[f"n{row + 1}"]
            + io.target_half_T_col1 ** numbers[f"n{col}"]
            + io.target_half_T_col2 ** numbers[f"n{col + 1}"]
            + io.target_half_T_col3 ** numbers[f"n{col}"]
            + io.target_mirror_L_row1
            ** numbers[
                f"n{row + (-1 if i == 0 else 1) * (i % 2 == 0)}"
            ]  # 1 up, no up, 1 down.
            + io.target_mirror_L_row2 ** numbers[f"n{row + i}"]
            + io.target_mirror_L_row3 ** numbers[f"n{row + i}"]
            + io.target_mirror_L_col1 ** numbers[f"n{col - 1}"]
            + io.target_mirror_L_col2 ** numbers[f"n{col - 2}"]
            + io.target_mirror_L_col3 ** numbers[f"n{col - 1}"]
            >> +(io.output**response.yes)
        )
        for switcharoo in (True, False)
        for i in range(3)
        for row in range(1 + (i == 0), 6 - (i == 2))
        for col in range(3, 6)
    ]

    half_t_below_mirror_l = [
        (
            +(io.query_block ** (bricks.half_T if not switcharoo else bricks.mirror_L))
            - io.query_block**bricks.horizontal
            - io.query_block**bricks.vertical
            - io.query_block ** (bricks.mirror_L if not switcharoo else bricks.half_T)
            + io.query_block_reference
            ** (bricks.mirror_L if not switcharoo else bricks.half_T)
            - io.query_block_reference**bricks.horizontal
            - io.query_block_reference**bricks.vertical
            - io.query_block_reference
            ** (bricks.half_T if not switcharoo else bricks.mirror_L)
            + 2.0
            * (
                io.query_relation
                ** (query_rel.below if not switcharoo else query_rel.above)
            )
            - 2.0
            * (
                io.query_relation
                ** (query_rel.above if not switcharoo else query_rel.below)
            )
            - 2.0 * (io.query_relation**query_rel.left)
            - 2.0 * (io.query_relation**query_rel.right)
            + io.target_half_T**response.yes
            + io.target_mirror_L**response.yes
            + io.target_half_T_row1 ** numbers[f"n{row}"]
            + io.target_half_T_row2 ** numbers[f"n{row}"]
            + io.target_half_T_row3 ** numbers[f"n{row + 1}"]
            + io.target_half_T_col1 ** numbers[f"n{col}"]
            + io.target_half_T_col2 ** numbers[f"n{col + 1}"]
            + io.target_half_T_col3 ** numbers[f"n{col}"]
            + io.target_mirror_L_row1 ** numbers[f"n{row - 2}"]
            + io.target_mirror_L_row2 ** numbers[f"n{row - 1}"]
            + io.target_mirror_L_row3 ** numbers[f"n{row - 1}"]
            + io.target_mirror_L_col1 ** numbers[f"n{col + i}"]
            + io.target_mirror_L_col2 ** numbers[f"n{col - 1 + i}"]
            + io.target_mirror_L_col3 ** numbers[f"n{col + i}"]
            >> +(io.output**response.yes)
        )
        for switcharoo in (True, False)
        for i in range(3)
        for row in range(3, 6)
        for col in range(1 + (i == 0), 6 - (i == 2))
    ]

    half_t_above_mirror_l = [
        (
            +(io.query_block ** (bricks.half_T if not switcharoo else bricks.mirror_L))
            - io.query_block**bricks.horizontal
            - io.query_block**bricks.vertical
            - io.query_block ** (bricks.mirror_L if not switcharoo else bricks.half_T)
            + io.query_block_reference
            ** (bricks.mirror_L if not switcharoo else bricks.half_T)
            - io.query_block_reference**bricks.horizontal
            - io.query_block_reference**bricks.vertical
            - io.query_block_reference
            ** (bricks.half_T if not switcharoo else bricks.mirror_L)
            + 2.0
            * (
                io.query_relation
                ** (query_rel.above if not switcharoo else query_rel.below)
            )
            - 2.0
            * (
                io.query_relation
                ** (query_rel.below if not switcharoo else query_rel.above)
            )
            - 2.0 * (io.query_relation**query_rel.left)
            - 2.0 * (io.query_relation**query_rel.right)
            + io.target_half_T**response.yes
            + io.target_mirror_L**response.yes
            + io.target_half_T_row1 ** numbers[f"n{row}"]
            + io.target_half_T_row2 ** numbers[f"n{row}"]
            + io.target_half_T_row3 ** numbers[f"n{row + 1}"]
            + io.target_half_T_col1 ** numbers[f"n{col}"]
            + io.target_half_T_col2 ** numbers[f"n{col + 1}"]
            + io.target_half_T_col3 ** numbers[f"n{col}"]
            + io.target_mirror_L_row1 ** numbers[f"n{row + 2}"]
            + io.target_mirror_L_row2 ** numbers[f"n{row + 3}"]
            + io.target_mirror_L_row3 ** numbers[f"n{row + 3}"]
            + io.target_mirror_L_col1 ** numbers[f"n{col}"]
            + io.target_mirror_L_col2 ** numbers[f"n{col - 1}"]
            + io.target_mirror_L_col3 ** numbers[f"n{col}"]
            >> +(io.output**response.yes)
        )
        for switcharoo in (True, False)
        for row in range(1, 4)
        for col in range(2, 6)
    ]

    # MIRROR_L X HORIZONTAL
    mirror_l_left_horizontal = [
        (
            +(
                io.query_block
                ** (bricks.mirror_L if not switcharoo else bricks.horizontal)
            )
            - io.query_block**bricks.half_T
            - io.query_block**bricks.vertical
            - io.query_block
            ** (bricks.horizontal if not switcharoo else bricks.mirror_L)
            + io.query_block_reference
            ** (bricks.horizontal if not switcharoo else bricks.mirror_L)
            - io.query_block_reference**bricks.half_T
            - io.query_block_reference**bricks.vertical
            - io.query_block_reference
            ** (bricks.mirror_L if not switcharoo else bricks.horizontal)
            + 2.0
            * (
                io.query_relation
                ** (query_rel.left if not switcharoo else query_rel.right)
            )
            - 2.0
            * (
                io.query_relation
                ** (query_rel.right if not switcharoo else query_rel.left)
            )
            - 2.0 * (io.query_relation**query_rel.above)
            - 2.0 * (io.query_relation**query_rel.below)
            + io.target_mirror_L**response.yes
            + io.target_horizontal**response.yes
            + io.target_mirror_L_row1 ** numbers[f"n{row}"]
            + io.target_mirror_L_row2 ** numbers[f"n{row + 1}"]
            + io.target_mirror_L_row3 ** numbers[f"n{row + 1}"]
            + io.target_mirror_L_col1 ** numbers[f"n{col}"]
            + io.target_mirror_L_col2 ** numbers[f"n{col - 1}"]
            + io.target_mirror_L_col3 ** numbers[f"n{col}"]
            + io.target_horizontal_row1 ** numbers[f"n{row + i}"]
            + io.target_horizontal_row2 ** numbers[f"n{row + i}"]
            + io.target_horizontal_row3 ** numbers[f"n{row + i}"]
            + io.target_horizontal_col1 ** numbers[f"n{col + 1}"]
            + io.target_horizontal_col2 ** numbers[f"n{col + 2}"]
            + io.target_horizontal_col3 ** numbers[f"n{col + 3}"]
            >> +(io.output**response.yes)
        )
        for switcharoo in (True, False)
        for i in range(2)
        for row in range(1, 6)
        for col in range(2, 4)
    ]

    mirror_l_right_horizontal = [
        (
            +(
                io.query_block
                ** (bricks.mirror_L if not switcharoo else bricks.horizontal)
            )
            - io.query_block**bricks.half_T
            - io.query_block**bricks.vertical
            - io.query_block
            ** (bricks.horizontal if not switcharoo else bricks.mirror_L)
            + io.query_block_reference
            ** (bricks.horizontal if not switcharoo else bricks.mirror_L)
            - io.query_block_reference**bricks.half_T
            - io.query_block_reference**bricks.vertical
            - io.query_block_reference
            ** (bricks.mirror_L if not switcharoo else bricks.horizontal)
            + 2.0
            * (
                io.query_relation
                ** (query_rel.right if not switcharoo else query_rel.left)
            )
            - 2.0
            * (
                io.query_relation
                ** (query_rel.left if not switcharoo else query_rel.right)
            )
            - 2.0 * (io.query_relation**query_rel.above)
            - 2.0 * (io.query_relation**query_rel.below)
            + io.target_mirror_L**response.yes
            + io.target_horizontal**response.yes
            + io.target_mirror_L_row1 ** numbers[f"n{row}"]
            + io.target_mirror_L_row2 ** numbers[f"n{row + 1}"]
            + io.target_mirror_L_row3 ** numbers[f"n{row + 1}"]
            + io.target_mirror_L_col1 ** numbers[f"n{col}"]
            + io.target_mirror_L_col2 ** numbers[f"n{col - 1}"]
            + io.target_mirror_L_col3 ** numbers[f"n{col}"]
            + io.target_horizontal_row1 ** numbers[f"n{row + i}"]
            + io.target_horizontal_row2 ** numbers[f"n{row + i}"]
            + io.target_horizontal_row3 ** numbers[f"n{row + i}"]
            + io.target_horizontal_col1 ** numbers[f"n{col - 3 - i}"]
            + io.target_horizontal_col2 ** numbers[f"n{col - 2 - i}"]
            + io.target_horizontal_col3 ** numbers[f"n{col - 1 - i}"]
            >> +(io.output**response.yes)
        )
        for switcharoo in (True, False)
        for i in range(2)
        for row in range(1, 6)
        for col in range(4 + i, 7)
    ]
    """
    2 2 2 1
        1 1

            1
    2 2 2 1 1
    """

    mirror_l_above_horizontal = [
        (
            +(
                io.query_block
                ** (bricks.mirror_L if not switcharoo else bricks.horizontal)
            )
            - io.query_block**bricks.half_T
            - io.query_block**bricks.vertical
            - io.query_block
            ** (bricks.horizontal if not switcharoo else bricks.mirror_L)
            + io.query_block_reference
            ** (bricks.horizontal if not switcharoo else bricks.mirror_L)
            - io.query_block_reference**bricks.half_T
            - io.query_block_reference**bricks.vertical
            - io.query_block_reference
            ** (bricks.mirror_L if not switcharoo else bricks.horizontal)
            + 2.0
            * (
                io.query_relation
                ** (query_rel.above if not switcharoo else query_rel.below)
            )
            - 2.0
            * (
                io.query_relation
                ** (query_rel.below if not switcharoo else query_rel.above)
            )
            - 2.0 * (io.query_relation**query_rel.left)
            - 2.0 * (io.query_relation**query_rel.right)
            + io.target_mirror_L**response.yes
            + io.target_horizontal**response.yes
            + io.target_mirror_L_row1 ** numbers[f"n{row}"]
            + io.target_mirror_L_row2 ** numbers[f"n{row + 1}"]
            + io.target_mirror_L_row3 ** numbers[f"n{row + 1}"]
            + io.target_mirror_L_col1 ** numbers[f"n{col}"]
            + io.target_mirror_L_col2 ** numbers[f"n{col - 1}"]
            + io.target_mirror_L_col3 ** numbers[f"n{col}"]
            + io.target_horizontal_row1 ** numbers[f"n{row + 2}"]
            + io.target_horizontal_row2 ** numbers[f"n{row + 2}"]
            + io.target_horizontal_row3 ** numbers[f"n{row + 2}"]
            + io.target_horizontal_col1 ** numbers[f"n{col - 3 + i}"]
            + io.target_horizontal_col2 ** numbers[f"n{col - 2 + i}"]
            + io.target_horizontal_col3 ** numbers[f"n{col - 1 + i}"]
            >> +(io.output**response.yes)
        )
        for switcharoo in (True, False)
        for i in range(4)
        for row in range(1, 5)
        for col in range((4 - i if i < 2 else 2), 7 - (i - 1 if i >= 2 else 0))
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

      1
    1 1
      2 2 2
    """

    mirror_l_below_horizontal = [
        (
            +(
                io.query_block
                ** (bricks.mirror_L if not switcharoo else bricks.horizontal)
            )
            - io.query_block**bricks.half_T
            - io.query_block**bricks.vertical
            - io.query_block
            ** (bricks.horizontal if not switcharoo else bricks.mirror_L)
            + io.query_block_reference
            ** (bricks.horizontal if not switcharoo else bricks.mirror_L)
            - io.query_block_reference**bricks.half_T
            - io.query_block_reference**bricks.vertical
            - io.query_block_reference
            ** (bricks.mirror_L if not switcharoo else bricks.horizontal)
            + 2.0
            * (
                io.query_relation
                ** (query_rel.below if not switcharoo else query_rel.above)
            )
            - 2.0
            * (
                io.query_relation
                ** (query_rel.above if not switcharoo else query_rel.below)
            )
            - 2.0 * (io.query_relation**query_rel.left)
            - 2.0 * (io.query_relation**query_rel.right)
            + io.target_mirror_L**response.yes
            + io.target_horizontal**response.yes
            + io.target_mirror_L_row1 ** numbers[f"n{row}"]
            + io.target_mirror_L_row2 ** numbers[f"n{row + 1}"]
            + io.target_mirror_L_row3 ** numbers[f"n{row + 1}"]
            + io.target_mirror_L_col1 ** numbers[f"n{col}"]
            + io.target_mirror_L_col2 ** numbers[f"n{col - 1}"]
            + io.target_mirror_L_col3 ** numbers[f"n{col}"]
            + io.target_horizontal_row1 ** numbers[f"n{row - 1}"]
            + io.target_horizontal_row2 ** numbers[f"n{row - 1}"]
            + io.target_horizontal_row3 ** numbers[f"n{row - 1}"]
            + io.target_horizontal_col1 ** numbers[f"n{col - 2 + i}"]
            + io.target_horizontal_col2 ** numbers[f"n{col - 1 + i}"]
            + io.target_horizontal_col3 ** numbers[f"n{col + i}"]
            >> +(io.output**response.yes)
        )
        for switcharoo in (True, False)
        for i in range(3)
        for row in range(2, 6)
        for col in range(3 - (i != 0), 7 - i)
    ]
    """
    2 2 2
        1
      1 1
    """

    # MIRROR_L X VERTICAL
    mirror_l_left_vertical = [
        (
            +(
                io.query_block
                ** (bricks.mirror_L if not switcharoo else bricks.vertical)
            )
            - io.query_block**bricks.half_T
            - io.query_block**bricks.horizontal
            - io.query_block ** (bricks.vertical if not switcharoo else bricks.mirror_L)
            + io.query_block_reference
            ** (bricks.vertical if not switcharoo else bricks.mirror_L)
            - io.query_block_reference**bricks.half_T
            - io.query_block_reference**bricks.horizontal
            - io.query_block_reference
            ** (bricks.mirror_L if not switcharoo else bricks.vertical)
            + 2.0
            * (
                io.query_relation
                ** (query_rel.left if not switcharoo else query_rel.right)
            )
            - 2.0
            * (
                io.query_relation
                ** (query_rel.right if not switcharoo else query_rel.left)
            )
            - 2.0 * (io.query_relation**query_rel.above)
            - 2.0 * (io.query_relation**query_rel.below)
            + io.target_mirror_L**response.yes
            + io.target_vertical**response.yes
            + io.target_mirror_L_row1 ** numbers[f"n{row}"]
            + io.target_mirror_L_row2 ** numbers[f"n{row + 1}"]
            + io.target_mirror_L_row3 ** numbers[f"n{row + 1}"]
            + io.target_mirror_L_col1 ** numbers[f"n{col}"]
            + io.target_mirror_L_col2 ** numbers[f"n{col - 1}"]
            + io.target_mirror_L_col3 ** numbers[f"n{col}"]
            + io.target_vertical_row1 ** numbers[f"n{row - 2 + i}"]
            + io.target_vertical_row2 ** numbers[f"n{row - 1 + i}"]
            + io.target_vertical_row3 ** numbers[f"n{row + i}"]
            + io.target_vertical_col1 ** numbers[f"n{col + 1}"]
            + io.target_vertical_col2 ** numbers[f"n{col + 1}"]
            + io.target_vertical_col3 ** numbers[f"n{col + 1}"]
            >> +(io.output**response.yes)
        )
        for switcharoo in (True, False)
        for i in range(4)
        for row in range(max(3 - i, 1), 6 - (0 if i < 2 else i - 1))
        for col in range(2, 6)
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

    mirror_l_right_vertical = [
        (
            +(
                io.query_block
                ** (bricks.mirror_L if not switcharoo else bricks.vertical)
            )
            - io.query_block**bricks.half_T
            - io.query_block**bricks.horizontal
            - io.query_block ** (bricks.vertical if not switcharoo else bricks.mirror_L)
            + io.query_block_reference
            ** (bricks.vertical if not switcharoo else bricks.mirror_L)
            - io.query_block_reference**bricks.half_T
            - io.query_block_reference**bricks.horizontal
            - io.query_block_reference
            ** (bricks.mirror_L if not switcharoo else bricks.vertical)
            + 2.0
            * (
                io.query_relation
                ** (query_rel.right if not switcharoo else query_rel.left)
            )
            - 2.0
            * (
                io.query_relation
                ** (query_rel.left if not switcharoo else query_rel.right)
            )
            - 2.0 * (io.query_relation**query_rel.above)
            - 2.0 * (io.query_relation**query_rel.below)
            + io.target_mirror_L**response.yes
            + io.target_vertical**response.yes
            + io.target_mirror_L_row1 ** numbers[f"n{row}"]
            + io.target_mirror_L_row2 ** numbers[f"n{row + 1}"]
            + io.target_mirror_L_row3 ** numbers[f"n{row + 1}"]
            + io.target_mirror_L_col1 ** numbers[f"n{col}"]
            + io.target_mirror_L_col2 ** numbers[f"n{col - 1}"]
            + io.target_mirror_L_col3 ** numbers[f"n{col}"]
            + io.target_vertical_row1 ** numbers[f"n{row + 1 - i}"]
            + io.target_vertical_row2 ** numbers[f"n{row + 2 - i}"]
            + io.target_vertical_row3 ** numbers[f"n{row + 3 - i}"]
            + io.target_vertical_col1 ** numbers[f"n{col - 2 + (i == 3)}"]
            + io.target_vertical_col2 ** numbers[f"n{col - 2 + (i == 3)}"]
            + io.target_vertical_col3 ** numbers[f"n{col - 2 + (i == 3)}"]
            >> +(io.output**response.yes)
        )
        for switcharoo in (True, False)
        for i in range(4)
        for row in range(1 + max(0, i - 1), min(4 + i, 6))
        for col in range(3 - (i == 3), 7)
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

    mirror_l_above_vertical = [
        (
            +(
                io.query_block
                ** (bricks.mirror_L if not switcharoo else bricks.vertical)
            )
            - io.query_block**bricks.half_T
            - io.query_block**bricks.horizontal
            - io.query_block ** (bricks.vertical if not switcharoo else bricks.mirror_L)
            + io.query_block_reference
            ** (bricks.vertical if not switcharoo else bricks.mirror_L)
            - io.query_block_reference**bricks.half_T
            - io.query_block_reference**bricks.horizontal
            - io.query_block_reference
            ** (bricks.mirror_L if not switcharoo else bricks.vertical)
            + 2.0
            * (
                io.query_relation
                ** (query_rel.above if not switcharoo else query_rel.below)
            )
            - 2.0
            * (
                io.query_relation
                ** (query_rel.below if not switcharoo else query_rel.above)
            )
            - 2.0 * (io.query_relation**query_rel.left)
            - 2.0 * (io.query_relation**query_rel.right)
            + io.target_mirror_L**response.yes
            + io.target_vertical**response.yes
            + io.target_mirror_L_row1 ** numbers[f"n{row}"]
            + io.target_mirror_L_row2 ** numbers[f"n{row + 1}"]
            + io.target_mirror_L_row3 ** numbers[f"n{row + 1}"]
            + io.target_mirror_L_col1 ** numbers[f"n{col}"]
            + io.target_mirror_L_col2 ** numbers[f"n{col - 1}"]
            + io.target_mirror_L_col3 ** numbers[f"n{col}"]
            + io.target_vertical_row1 ** numbers[f"n{row + 2}"]
            + io.target_vertical_row2 ** numbers[f"n{row + 3}"]
            + io.target_vertical_row3 ** numbers[f"n{row + 4}"]
            + io.target_vertical_col1 ** numbers[f"n{col - 1 + i}"]
            + io.target_vertical_col2 ** numbers[f"n{col - 1 + i}"]
            + io.target_vertical_col3 ** numbers[f"n{col - 1 + i}"]
            >> +(io.output**response.yes)
        )
        for switcharoo in (True, False)
        for i in range(2)
        for row in range(1, 3)
        for col in range(2, 7)
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

    mirror_l_below_vertical = [
        (
            +(
                io.query_block
                ** (bricks.mirror_L if not switcharoo else bricks.vertical)
            )
            - io.query_block**bricks.half_T
            - io.query_block**bricks.horizontal
            - io.query_block ** (bricks.vertical if not switcharoo else bricks.mirror_L)
            + io.query_block_reference
            ** (bricks.vertical if not switcharoo else bricks.mirror_L)
            - io.query_block_reference**bricks.half_T
            - io.query_block_reference**bricks.horizontal
            - io.query_block_reference
            ** (bricks.mirror_L if not switcharoo else bricks.vertical)
            + 2.0
            * (
                io.query_relation
                ** (query_rel.below if not switcharoo else query_rel.above)
            )
            - 2.0
            * (
                io.query_relation
                ** (query_rel.above if not switcharoo else query_rel.below)
            )
            - 2.0 * (io.query_relation**query_rel.left)
            - 2.0 * (io.query_relation**query_rel.right)
            + io.target_mirror_L**response.yes
            + io.target_vertical**response.yes
            + io.target_mirror_L_row1 ** numbers[f"n{row}"]
            + io.target_mirror_L_row2 ** numbers[f"n{row + 1}"]
            + io.target_mirror_L_row3 ** numbers[f"n{row + 1}"]
            + io.target_mirror_L_col1 ** numbers[f"n{col}"]
            + io.target_mirror_L_col2 ** numbers[f"n{col - 1}"]
            + io.target_mirror_L_col3 ** numbers[f"n{col}"]
            + io.target_vertical_row1 ** numbers[f"n{row - 3}"]
            + io.target_vertical_row2 ** numbers[f"n{row - 2}"]
            + io.target_vertical_row3 ** numbers[f"n{row - 1}"]
            + io.target_vertical_col1 ** numbers[f"n{col}"]
            + io.target_vertical_col2 ** numbers[f"n{col}"]
            + io.target_vertical_col3 ** numbers[f"n{col}"]
            >> +(io.output**response.yes)
        )
        for switcharoo in (True, False)
        for row in range(4, 6)
        for col in range(2, 7)
    ]

    """
      2
      2
      2
      1
    1 1
    """

    # HORIZONTAL X VERTICAL
    horizontal_left_vertical = [
        (
            +(
                io.query_block
                ** (bricks.horizontal if not switcharoo else bricks.vertical)
            )
            - io.query_block**bricks.half_T
            - io.query_block**bricks.mirror_L
            - io.query_block
            ** (bricks.vertical if not switcharoo else bricks.horizontal)
            + io.query_block_reference
            ** (bricks.vertical if not switcharoo else bricks.horizontal)
            - io.query_block_reference**bricks.half_T
            - io.query_block_reference**bricks.mirror_L
            - io.query_block_reference
            ** (bricks.horizontal if not switcharoo else bricks.vertical)
            + 2.0
            * (
                io.query_relation
                ** (query_rel.left if not switcharoo else query_rel.right)
            )
            - 2.0
            * (
                io.query_relation
                ** (query_rel.right if not switcharoo else query_rel.left)
            )
            - 2.0 * (io.query_relation**query_rel.above)
            - 2.0 * (io.query_relation**query_rel.below)
            + io.target_vertical**response.yes
            + io.target_horizontal**response.yes
            + io.target_horizontal_row1 ** numbers[f"n{row}"]
            + io.target_horizontal_row2 ** numbers[f"n{row}"]
            + io.target_horizontal_row3 ** numbers[f"n{row}"]
            + io.target_horizontal_col1 ** numbers[f"n{col}"]
            + io.target_horizontal_col2 ** numbers[f"n{col + 1}"]
            + io.target_horizontal_col3 ** numbers[f"n{col + 2}"]
            + io.target_vertical_row1 ** numbers[f"n{row - 2 + i}"]
            + io.target_vertical_row2 ** numbers[f"n{row - 1 + i}"]
            + io.target_vertical_row3 ** numbers[f"n{row + i}"]
            + io.target_vertical_col1 ** numbers[f"n{col + 3}"]
            + io.target_vertical_col2 ** numbers[f"n{col + 3}"]
            + io.target_vertical_col3 ** numbers[f"n{col + 3}"]
            >> +(io.output**response.yes)
        )
        for switcharoo in (True, False)
        for i in range(3)
        for row in range(3 - i, 7 - i)
        for col in range(1, 4)
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
        (
            +(
                io.query_block
                ** (bricks.horizontal if not switcharoo else bricks.vertical)
            )
            - io.query_block**bricks.half_T
            - io.query_block**bricks.mirror_L
            - io.query_block
            ** (bricks.vertical if not switcharoo else bricks.horizontal)
            + io.query_block_reference
            ** (bricks.vertical if not switcharoo else bricks.horizontal)
            - io.query_block_reference**bricks.half_T
            - io.query_block_reference**bricks.mirror_L
            - io.query_block_reference
            ** (bricks.horizontal if not switcharoo else bricks.vertical)
            + 2.0
            * (
                io.query_relation
                ** (query_rel.right if not switcharoo else query_rel.left)
            )
            - 2.0
            * (
                io.query_relation
                ** (query_rel.left if not switcharoo else query_rel.right)
            )
            - 2.0 * (io.query_relation**query_rel.above)
            - 2.0 * (io.query_relation**query_rel.below)
            + io.target_vertical**response.yes
            + io.target_horizontal**response.yes
            + io.target_horizontal_row1 ** numbers[f"n{row}"]
            + io.target_horizontal_row2 ** numbers[f"n{row}"]
            + io.target_horizontal_row3 ** numbers[f"n{row}"]
            + io.target_horizontal_col1 ** numbers[f"n{col}"]
            + io.target_horizontal_col2 ** numbers[f"n{col + 1}"]
            + io.target_horizontal_col3 ** numbers[f"n{col + 2}"]
            + io.target_vertical_row1 ** numbers[f"n{row - 2 + i}"]
            + io.target_vertical_row2 ** numbers[f"n{row - 1 + i}"]
            + io.target_vertical_row3 ** numbers[f"n{row + i}"]
            + io.target_vertical_col1 ** numbers[f"n{col - 1}"]
            + io.target_vertical_col2 ** numbers[f"n{col - 1}"]
            + io.target_vertical_col3 ** numbers[f"n{col - 1}"]
            >> +(io.output**response.yes)
        )
        for switcharoo in (True, False)
        for i in range(3)
        for row in range(3 - i, 7 - i)
        for col in range(2, 5)
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
        (
            +(
                io.query_block
                ** (bricks.horizontal if not switcharoo else bricks.vertical)
            )
            - io.query_block**bricks.half_T
            - io.query_block**bricks.mirror_L
            - io.query_block
            ** (bricks.vertical if not switcharoo else bricks.horizontal)
            + io.query_block_reference
            ** (bricks.vertical if not switcharoo else bricks.horizontal)
            - io.query_block_reference**bricks.half_T
            - io.query_block_reference**bricks.mirror_L
            - io.query_block_reference
            ** (bricks.horizontal if not switcharoo else bricks.vertical)
            + 2.0
            * (
                io.query_relation
                ** (query_rel.above if not switcharoo else query_rel.below)
            )
            - 2.0
            * (
                io.query_relation
                ** (query_rel.below if not switcharoo else query_rel.above)
            )
            - 2.0 * (io.query_relation**query_rel.left)
            - 2.0 * (io.query_relation**query_rel.right)
            + io.target_vertical**response.yes
            + io.target_horizontal**response.yes
            + io.target_horizontal_row1 ** numbers[f"n{row}"]
            + io.target_horizontal_row2 ** numbers[f"n{row}"]
            + io.target_horizontal_row3 ** numbers[f"n{row}"]
            + io.target_horizontal_col1 ** numbers[f"n{col}"]
            + io.target_horizontal_col2 ** numbers[f"n{col + 1}"]
            + io.target_horizontal_col3 ** numbers[f"n{col + 2}"]
            + io.target_vertical_row1 ** numbers[f"n{row + 1}"]
            + io.target_vertical_row2 ** numbers[f"n{row + 2}"]
            + io.target_vertical_row3 ** numbers[f"n{row + 3}"]
            + io.target_vertical_col1 ** numbers[f"n{col + i}"]
            + io.target_vertical_col2 ** numbers[f"n{col + i}"]
            + io.target_vertical_col3 ** numbers[f"n{col + i}"]
            >> +(io.output**response.yes)
        )
        for switcharoo in (True, False)
        for i in range(3)
        for row in range(1, 4)
        for col in range(1, 5)
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
        (
            +(
                io.query_block
                ** (bricks.horizontal if not switcharoo else bricks.vertical)
            )
            - io.query_block**bricks.half_T
            - io.query_block**bricks.mirror_L
            - io.query_block
            ** (bricks.vertical if not switcharoo else bricks.horizontal)
            + io.query_block_reference
            ** (bricks.vertical if not switcharoo else bricks.horizontal)
            - io.query_block_reference**bricks.half_T
            - io.query_block_reference**bricks.mirror_L
            - io.query_block_reference
            ** (bricks.horizontal if not switcharoo else bricks.vertical)
            + 2.0
            * (
                io.query_relation
                ** (query_rel.below if not switcharoo else query_rel.above)
            )
            - 2.0
            * (
                io.query_relation
                ** (query_rel.above if not switcharoo else query_rel.below)
            )
            - 2.0 * (io.query_relation**query_rel.left)
            - 2.0 * (io.query_relation**query_rel.right)
            + io.target_vertical**response.yes
            + io.target_horizontal**response.yes
            + io.target_horizontal_row1 ** numbers[f"n{row}"]
            + io.target_horizontal_row2 ** numbers[f"n{row}"]
            + io.target_horizontal_row3 ** numbers[f"n{row}"]
            + io.target_horizontal_col1 ** numbers[f"n{col}"]
            + io.target_horizontal_col2 ** numbers[f"n{col + 1}"]
            + io.target_horizontal_col3 ** numbers[f"n{col + 2}"]
            + io.target_vertical_row1 ** numbers[f"n{row - 3}"]
            + io.target_vertical_row2 ** numbers[f"n{row - 2}"]
            + io.target_vertical_row3 ** numbers[f"n{row - 1}"]
            + io.target_vertical_col1 ** numbers[f"n{col + i}"]
            + io.target_vertical_col2 ** numbers[f"n{col + i}"]
            + io.target_vertical_col3 ** numbers[f"n{col + i}"]
            >> +(io.output**response.yes)
        )
        for switcharoo in (True, False)
        for i in range(3)
        for row in range(4, 7)
        for col in range(1, 5)
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

    # no rule
    no_response_rule = [
        (
            +4.0 * (io.query_block**q_block)
            + 4.0 * (io.query_block_reference**q_block_ref)
            + 4.0 * (io.query_relation**rel)
            >> +(io.output**response.no)
        )
        for q_block in (
            bricks.half_T,
            bricks.mirror_L,
            bricks.horizontal,
            bricks.vertical,
        )
        for q_block_ref in (
            bricks.half_T,
            bricks.mirror_L,
            bricks.horizontal,
            bricks.vertical,
        )
        for rel in (query_rel.left, query_rel.right, query_rel.above, query_rel.below)
        if q_block != q_block_ref
    ]

    participant.response_rules.rules.compile(
        *(
            half_t_left_of_horizontal
            + half_t_left_vertical
            + half_t_left_mirror_l
            + half_t_right_of_horizontal
            + half_t_right_vertical
            + half_t_right_mirror_l
            + half_t_below_horizontal
            + half_t_below_vertical
            + half_t_below_mirror_l
            + half_t_above_horizontal
            + half_t_above_vertical
            + half_t_above_mirror_l
            + mirror_l_left_horizontal
            + mirror_l_left_vertical
            + mirror_l_right_horizontal
            + mirror_l_right_vertical
            + mirror_l_below_horizontal
            + mirror_l_below_vertical
            + mirror_l_above_horizontal
            + mirror_l_above_vertical
            + horizontal_left_vertical
            + horizontal_right_vertical
            + horizontal_above_vertical
            + horizontal_below_vertical
            + no_response_rule
        )
    )
    #
    # 50 110 64 40 112 78 88 40 54 88 20 24 40 88 50 118 88 20 112 40 72 72 72 72


def init_participant_construction_rules(participant) -> None:
    d = participant.construction_space
    io = d.io
    con_signal = d.signal_tokens
    numbers = d.numbers
    response = d.response

    # FIRST PLACEMENT RULES
    """
    1 1
    1
    """
    half_t_first_placement_rule = [
        (
            +(io.input_half_T**response.yes)
            + io.input_half_T_row1 ** numbers[f"n{row}"]
            + io.input_half_T_row2 ** numbers[f"n{row}"]
            + io.input_half_T_row3 ** numbers[f"n{row + 1}"]
            + io.input_half_T_col1 ** numbers[f"n{col}"]
            + io.input_half_T_col2 ** numbers[f"n{col + 1}"]
            + io.input_half_T_col3 ** numbers[f"n{col}"]
            + io.target_half_T**response.no
            >> +(io.construction_signal**con_signal.continue_construction)
            + io.target_half_T**response.yes
            + io.target_half_T_row1 ** numbers[f"n{row}"]
            + io.target_half_T_row2 ** numbers[f"n{row}"]
            + io.target_half_T_row3 ** numbers[f"n{row + 1}"]
            + io.target_half_T_col1 ** numbers[f"n{col}"]
            + io.target_half_T_col2 ** numbers[f"n{col + 1}"]
            + io.target_half_T_col3 ** numbers[f"n{col}"]
        )
        for row in range(1, 6)
        for col in range(1, 6)
    ]

    mirror_l_first_placement_rule = [
        (
            +(io.input_mirror_L**response.yes)
            + io.input_mirror_L_row1 ** numbers[f"n{row}"]
            + io.input_mirror_L_row2 ** numbers[f"n{row + 1}"]
            + io.input_mirror_L_row3 ** numbers[f"n{row + 1}"]
            + io.input_mirror_L_col1 ** numbers[f"n{col}"]
            + io.input_mirror_L_col2 ** numbers[f"n{col - 1}"]
            + io.input_mirror_L_col3 ** numbers[f"n{col}"]
            + io.target_mirror_L**response.no
            >> +(io.construction_signal**con_signal.continue_construction)
            + io.target_mirror_L**response.yes
            + io.target_mirror_L_row1 ** numbers[f"n{row}"]
            + io.target_mirror_L_row2 ** numbers[f"n{row + 1}"]
            + io.target_mirror_L_row3 ** numbers[f"n{row + 1}"]
            + io.target_mirror_L_col1 ** numbers[f"n{col}"]
            + io.target_mirror_L_col2 ** numbers[f"n{col - 1}"]
            + io.target_mirror_L_col3 ** numbers[f"n{col}"]
        )
        for row in range(1, 6)
        for col in range(2, 7)
    ]
    """
      1
    1 1
    """

    horizontal_first_placement_rule = [
        (
            +(io.input_horizontal**response.yes)
            + io.input_horizontal_row1 ** numbers[f"n{row}"]
            + io.input_horizontal_row2 ** numbers[f"n{row}"]
            + io.input_horizontal_row3 ** numbers[f"n{row}"]
            + io.input_horizontal_col1 ** numbers[f"n{col}"]
            + io.input_horizontal_col2 ** numbers[f"n{col + 1}"]
            + io.input_horizontal_col3 ** numbers[f"n{col + 2}"]
            + io.target_horizontal**response.no
            >> +(io.construction_signal**con_signal.continue_construction)
            + io.target_horizontal**response.yes
            + io.target_horizontal_row1 ** numbers[f"n{row}"]
            + io.target_horizontal_row2 ** numbers[f"n{row}"]
            + io.target_horizontal_row3 ** numbers[f"n{row}"]
            + io.target_horizontal_col1 ** numbers[f"n{col}"]
            + io.target_horizontal_col2 ** numbers[f"n{col + 1}"]
            + io.target_horizontal_col3 ** numbers[f"n{col + 2}"]
        )
        for row in range(1, 7)
        for col in range(1, 5)
    ]

    vertical_first_placement_rule = [
        (
            +(io.input_vertical**response.yes)
            + io.input_vertical_row1 ** numbers[f"n{row}"]
            + io.input_vertical_row2 ** numbers[f"n{row + 1}"]
            + io.input_vertical_row3 ** numbers[f"n{row + 2}"]
            + io.input_vertical_col1 ** numbers[f"n{col}"]
            + io.input_vertical_col2 ** numbers[f"n{col}"]
            + io.input_vertical_col3 ** numbers[f"n{col}"]
            + io.target_vertical**response.no
            >> +(io.construction_signal**con_signal.continue_construction)
            + io.target_vertical**response.yes
            + io.target_vertical_row1 ** numbers[f"n{row}"]
            + io.target_vertical_row2 ** numbers[f"n{row + 1}"]
            + io.target_vertical_row3 ** numbers[f"n{row + 2}"]
            + io.target_vertical_col1 ** numbers[f"n{col}"]
            + io.target_vertical_col2 ** numbers[f"n{col}"]
            + io.target_vertical_col3 ** numbers[f"n{col}"]
        )
        for row in range(1, 5)
        for col in range(1, 7)
    ]

    # SUBSEQUENCE PLACEMENT RULES
    half_t_left_of_horizontal_placement_rule = [
        (
            +(io.input_half_T**response.yes)
            + io.input_horizontal**response.yes
            + io[f"{'target' if switcharoo else 'input'}_half_T_row1"]
            ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_row2"]
            ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_row3"]
            ** numbers[f"n{row + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col1"]
            ** numbers[f"n{col}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col2"]
            ** numbers[f"n{col + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col3"]
            ** numbers[f"n{col}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_row1"]
            ** numbers[f"n{row + i}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_row2"]
            ** numbers[f"n{row + i}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_row3"]
            ** numbers[f"n{row + i}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_col1"]
            ** numbers[f"n{col + 2 - i}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_col2"]
            ** numbers[f"n{col + 3 - i}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_col3"]
            ** numbers[f"n{col + 4 - i}"]
            + io[f"target_{'half_T' if switcharoo else 'horizontal'}"]
            ** response.yes  # half_T is already there
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}"]
            ** response.no  # but horizontal is not
            >> +(io.construction_signal**con_signal.continue_construction)
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}"] ** response.yes
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + i}"])
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_row2"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + i}"])
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_row3"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + i}"])
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col + 2 - i}"])
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_col2"]
            ** (
                numbers[f"n{col + 1}"] if not switcharoo else numbers[f"n{col + 3 - i}"]
            )
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_col3"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col + 4 - i}"])
        )
        for switcharoo in (True, False)
        for i in range(2)
        for row in range(1, 6)
        for col in range(1, 3 + i)
    ]

    half_t_right_of_horizontal_placement_rule = [
        (
            +(io.input_half_T**response.yes)
            + io.input_horizontal**response.yes
            + io[f"{'target' if switcharoo else 'input'}_half_T_row1"]
            ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_row2"]
            ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_row3"]
            ** numbers[f"n{row + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col1"]
            ** numbers[f"n{col}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col2"]
            ** numbers[f"n{col + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col3"]
            ** numbers[f"n{col}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_row1"]
            ** numbers[f"n{row + i}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_row2"]
            ** numbers[f"n{row + i}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_row3"]
            ** numbers[f"n{row + i}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_col1"]
            ** numbers[f"n{col - 3}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_col2"]
            ** numbers[f"n{col - 2}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_col3"]
            ** numbers[f"n{col - 1}"]
            + io[f"target_{'half_T' if switcharoo else 'horizontal'}"]
            ** response.yes  # half_T is already there
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}"]
            ** response.no  # but horizontal is not
            >> +(io.construction_signal**con_signal.continue_construction)
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}"] ** response.yes
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + i}"])
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_row2"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + i}"])
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_row3"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + i}"])
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col - 3}"])
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_col2"]
            ** (numbers[f"n{col + 1}"] if not switcharoo else numbers[f"n{col - 2}"])
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_col3"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col - 1}"])
        )
        for switcharoo in (True, False)
        for i in range(2)
        for row in range(1, 6)
        for col in range(4, 6)
    ]

    half_t_below_horizontal_placement_rule = [
        (
            +(io.input_half_T**response.yes)
            + io.input_horizontal**response.yes
            + io[f"{'input' if switcharoo else 'target'}_half_T_row1"]
            ** numbers[f"n{row}"]
            + io[f"{'input' if switcharoo else 'target'}_half_T_row2"]
            ** numbers[f"n{row}"]
            + io[f"{'input' if switcharoo else 'target'}_half_T_row3"]
            ** numbers[f"n{row + 1}"]
            + io[f"{'input' if switcharoo else 'target'}_half_T_col1"]
            ** numbers[f"n{col}"]
            + io[f"{'input' if switcharoo else 'target'}_half_T_col2"]
            ** numbers[f"n{col + 1}"]
            + io[f"{'input' if switcharoo else 'target'}_half_T_col3"]
            ** numbers[f"n{col}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_row1"]
            ** numbers[f"n{row - 1}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_row2"]
            ** numbers[f"n{row - 1}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_row3"]
            ** numbers[f"n{row - 1}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_col1"]
            ** numbers[f"n{col - 2 + i}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_col2"]
            ** numbers[f"n{col - 1 + i}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_col3"]
            ** numbers[f"n{col + i}"]
            + io[f"target_{'half_T' if switcharoo else 'horizontal'}"]
            ** response.yes  # half_T is already there
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}"]
            ** response.no  # but horizontal is not
            >> +(io.construction_signal**con_signal.continue_construction)
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}"] ** response.yes
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row - 1}"])
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_row2"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row - 1}"])
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_row3"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row - 1}"])
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col - 2 + i}"])
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_col2"]
            ** (
                numbers[f"n{col + 1}"] if not switcharoo else numbers[f"n{col - 1 + i}"]
            )
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_col3"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col + i}"])
        )
        for switcharoo in (True, False)
        for i in range(4)
        for row in range(2, 6)
        for col in range(max(3 - i, 1), 6 - max(i - 1, 0))
    ]

    half_t_above_horizontal_placement_rule = [
        (
            +(io.input_half_T**response.yes)
            + io.input_horizontal**response.yes
            + io[f"{'input' if switcharoo else 'target'}_half_T_row1"]
            ** numbers[f"n{row}"]
            + io[f"{'input' if switcharoo else 'target'}_half_T_row2"]
            ** numbers[f"n{row}"]
            + io[f"{'input' if switcharoo else 'target'}_half_T_row3"]
            ** numbers[f"n{row + 1}"]
            + io[f"{'input' if switcharoo else 'target'}_half_T_col1"]
            ** numbers[f"n{col}"]
            + io[f"{'input' if switcharoo else 'target'}_half_T_col2"]
            ** numbers[f"n{col + 1}"]
            + io[f"{'input' if switcharoo else 'target'}_half_T_col3"]
            ** numbers[f"n{col}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_row1"]
            ** numbers[f"n{row + 2}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_row2"]
            ** numbers[f"n{row + 2}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_row3"]
            ** numbers[f"n{row + 2}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_col1"]
            ** numbers[f"n{col - 2 + i}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_col2"]
            ** numbers[f"n{col - 1 + i}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_col3"]
            ** numbers[f"n{col + i}"]
            + io[f"target_{'half_T' if switcharoo else 'horizontal'}"]
            ** response.yes  # half_T isnt already there
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}"]
            ** response.no  # but horizontal is
            >> +(io.construction_signal**con_signal.continue_construction)
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}"] ** response.yes
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + 2}"])
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_row2"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + 2}"])
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_row3"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + 2}"])
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col - 2 + i}"])
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_col2"]
            ** (
                numbers[f"n{col + 1}"] if not switcharoo else numbers[f"n{col - 1 + i}"]
            )
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_col3"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col + i}"])
        )
        for switcharoo in (True, False)
        for i in range(3)
        for row in range(1, 5)
        for col in range(3 - i, 6 - (i == 2))
    ]

    half_t_left_vertical_placement_rule = [
        (
            +(io.input_half_T**response.yes)
            + io.input_vertical**response.yes
            + io[f"{'target' if switcharoo else 'input'}_half_T_row1"]
            ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_row2"]
            ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_row3"]
            ** numbers[f"n{row + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col1"]
            ** numbers[f"n{col}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col2"]
            ** numbers[f"n{col + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col3"]
            ** numbers[f"n{col}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_row1"]
            ** numbers[f"n{row + 1 - i}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_row2"]
            ** numbers[f"n{row + 2 - i}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_row3"]
            ** numbers[f"n{row + 3 - i}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_col1"]
            ** numbers[f"n{col + 2 - (i == 0)}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_col2"]
            ** numbers[f"n{col + 2 - (i == 0)}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_col3"]
            ** numbers[f"n{col + 2 - (i == 0)}"]
            + io[f"target_{'half_T' if switcharoo else 'vertical'}"]
            ** response.yes  # half_T isnt already there
            + io[f"target_{'vertical' if switcharoo else 'half_T'}"]
            ** response.no  # but vertical is
            >> +(io.construction_signal**con_signal.continue_construction)
            + io[f"target_{'vertical' if switcharoo else 'half_T'}"] ** response.yes
            + io[f"target_{'vertical' if switcharoo else 'half_T'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + 1 - i}"])
            + io[f"target_{'vertical' if switcharoo else 'half_T'}_row2"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + 2 - i}"])
            + io[f"target_{'vertical' if switcharoo else 'half_T'}_row3"]
            ** (
                numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + 3 - i}"]
            )
            + io[f"target_{'vertical' if switcharoo else 'half_T'}_col1"]
            ** (
                numbers[f"n{col}"]
                if not switcharoo
                else numbers[f"n{col + 2 - (i == 0)}"]
            )
            + io[f"target_{'vertical' if switcharoo else 'half_T'}_col2"]
            ** (
                numbers[f"n{col + 1}"]
                if not switcharoo
                else numbers[f"n{col + 2 - (i == 0)}"]
            )
            + io[f"target_{'vertical' if switcharoo else 'half_T'}_col3"]
            ** (
                numbers[f"n{col}"]
                if not switcharoo
                else numbers[f"n{col + 2 - (i == 0)}"]
            )
        )
        for switcharoo in (True, False)
        for i in range(4)
        for row in range(1 + (i - 1 if i > 1 else 0), 4 + (math.ceil(i / 2)))
        for col in range(1, 6 - (i > 0))
    ]

    half_t_right_vertical_placement_rule = [
        (
            +(io.input_half_T**response.yes)
            + io.input_vertical**response.yes
            + io[f"{'target' if switcharoo else 'input'}_half_T_row1"]
            ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_row2"]
            ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_row3"]
            ** numbers[f"n{row + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col1"]
            ** numbers[f"n{col}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col2"]
            ** numbers[f"n{col + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col3"]
            ** numbers[f"n{col}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_row1"]
            ** numbers[f"n{row - 2 + i}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_row2"]
            ** numbers[f"n{row - 1 + i}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_row3"]
            ** numbers[f"n{row + i}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_col1"]
            ** numbers[f"n{col - 1}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_col2"]
            ** numbers[f"n{col - 1}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_col3"]
            ** numbers[f"n{col - 1}"]
            + io[f"target_{'half_T' if switcharoo else 'vertical'}"]
            ** response.yes  # half_T isnt already there
            + io[f"target_{'vertical' if switcharoo else 'half_T'}"]
            ** response.no  # but vertical is
            >> +(io.construction_signal**con_signal.continue_construction)
            + io[f"target_{'half_T' if switcharoo else 'vertical'}"] ** response.yes
            + io[f"target_{'half_T' if switcharoo else 'vertical'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row - 2 + i}"])
            + io[f"target_{'half_T' if switcharoo else 'vertical'}_row2"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row - 1 + i}"])
            + io[f"target_{'half_T' if switcharoo else 'vertical'}_row3"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + i}"])
            + io[f"target_{'half_T' if switcharoo else 'vertical'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col - 1}"])
            + io[f"target_{'half_T' if switcharoo else 'vertical'}_col2"]
            ** (numbers[f"n{col + 1}"] if not switcharoo else numbers[f"n{col - 1}"])
            + io[f"target_{'half_T' if switcharoo else 'vertical'}_col3"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col - 1}"])
        )
        for switcharoo in (True, False)
        for i in range(4)
        for row in range(max(1, 3 - i), 6 - max(0, i - 1))
        for col in range(2, 6)
    ]

    half_t_below_vertical_placement_rule = [
        (
            +(io.input_half_T**response.yes)
            + io.input_vertical**response.yes
            + io[f"{'target' if switcharoo else 'input'}_half_T_row1"]
            ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_row2"]
            ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_row3"]
            ** numbers[f"n{row + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col1"]
            ** numbers[f"n{col}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col2"]
            ** numbers[f"n{col + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col3"]
            ** numbers[f"n{col}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_row1"]
            ** numbers[f"n{row - 3}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_row2"]
            ** numbers[f"n{row - 2}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_row3"]
            ** numbers[f"n{row - 1}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_col1"]
            ** numbers[f"n{col + i}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_col2"]
            ** numbers[f"n{col + i}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_col3"]
            ** numbers[f"n{col + i}"]
            + io[f"target_{'half_T' if switcharoo else 'vertical'}"]
            ** response.yes  # half_T isnt already there
            + io[f"target_{'vertical' if switcharoo else 'half_T'}"]
            ** response.no  # but vertical is
            >> +(io.construction_signal**con_signal.continue_construction)
            + io[f"target_{'half_T' if switcharoo else 'vertical'}"] ** response.yes
            + io[f"target_{'half_T' if switcharoo else 'vertical'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row - 3}"])
            + io[f"target_{'half_T' if switcharoo else 'vertical'}_row2"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row - 2}"])
            + io[f"target_{'half_T' if switcharoo else 'vertical'}_row3"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row - 1}"])
            + io[f"target_{'half_T' if switcharoo else 'vertical'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col + i}"])
            + io[f"target_{'half_T' if switcharoo else 'vertical'}_col2"]
            ** (numbers[f"n{col + 1}"] if not switcharoo else numbers[f"n{col + i}"])
            + io[f"target_{'half_T' if switcharoo else 'vertical'}_col3"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col + i}"])
        )
        for switcharoo in (True, False)
        for i in range(2)
        for row in range(4, 6)
        for col in range(1, 6)
    ]

    half_t_above_vertical_placement_rule = [
        (
            +(io.input_half_T**response.yes)
            + io.input_vertical**response.yes
            + io[f"{'target' if switcharoo else 'input'}_half_T_row1"]
            ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_row2"]
            ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_row3"]
            ** numbers[f"n{row + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col1"]
            ** numbers[f"n{col}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col2"]
            ** numbers[f"n{col + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col3"]
            ** numbers[f"n{col}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_row1"]
            ** numbers[f"n{row + 1}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_row2"]
            ** numbers[f"n{row + 2}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_row3"]
            ** numbers[f"n{row + 3}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_col1"]
            ** numbers[f"n{col}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_col2"]
            ** numbers[f"n{col}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_col3"]
            ** numbers[f"n{col}"]
            + io[f"target_{'half_T' if switcharoo else 'vertical'}"]
            ** response.yes  # half_T isnt already there
            + io[f"target_{'vertical' if switcharoo else 'half_T'}"]
            ** response.no  # but vertical is
            >> +(io.construction_signal**con_signal.continue_construction)
            + io[f"target_{'vertical' if switcharoo else 'half_T'}"] ** response.yes
            + io[f"target_{'vertical' if switcharoo else 'half_T'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + 1}"])
            + io[f"target_{'vertical' if switcharoo else 'half_T'}_row2"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + 2}"])
            + io[f"target_{'vertical' if switcharoo else 'half_T'}_row3"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + 3}"])
            + io[f"target_{'vertical' if switcharoo else 'half_T'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col}"])
            + io[f"target_{'vertical' if switcharoo else 'half_T'}_col2"]
            ** (numbers[f"n{col + 1}"] if not switcharoo else numbers[f"n{col}"])
            + io[f"target_{'vertical' if switcharoo else 'half_T'}_col3"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col}"])
        )
        for switcharoo in (True, False)
        for row in range(1, 3)
        for col in range(1, 6)
    ]

    half_t_left_mirror_l_placement_rule = [
        (
            +(io.input_half_T**response.yes)
            + io.input_mirror_L**response.yes
            + io[f"{'target' if switcharoo else 'input'}_half_T_row1"]
            ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_row2"]
            ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_row3"]
            ** numbers[f"n{row + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col1"]
            ** numbers[f"n{col}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col2"]
            ** numbers[f"n{col + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col3"]
            ** numbers[f"n{col}"]
            + io[f"{'input' if switcharoo else 'target'}_mirror_L_row1"]
            ** numbers[f"n{row - i}"]
            + io[f"{'input' if switcharoo else 'target'}_mirror_L_row2"]
            ** numbers[f"n{row + 1 - i}"]
            + io[f"{'input' if switcharoo else 'target'}_mirror_L_row3"]
            ** numbers[f"n{row + 1 - i}"]
            + io[f"{'input' if switcharoo else 'target'}_mirror_L_col1"]
            ** numbers[f"n{col + 2 + i}"]
            + io[f"{'input' if switcharoo else 'target'}_mirror_L_col2"]
            ** numbers[f"n{col + 1 + i}"]
            + io[f"{'input' if switcharoo else 'target'}_mirror_L_col3"]
            ** numbers[f"n{col + 2 + i}"]
            + io[f"target_{'half_T' if switcharoo else 'mirror_L'}"]
            ** response.yes  # half_T isnt already there
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}"]
            ** response.no  # but mirror_L is
            >> +(io.construction_signal**con_signal.continue_construction)
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}"] ** response.yes
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row - i}"])
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_row2"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + 1 - i}"])
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_row3"]
            ** (
                numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + 1 - i}"]
            )
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col + 2 + i}"])
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_col2"]
            ** (
                numbers[f"n{col + 1}"] if not switcharoo else numbers[f"n{col + 1 + i}"]
            )
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_col3"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col + 2 + i}"])
        )
        for switcharoo in (True, False)
        for i in range(2)
        for row in range(1 + i, 6)
        for col in range(1, 5 - i)
    ]

    half_t_right_mirror_l_placement_rule = [
        (
            +(io.input_half_T**response.yes)
            + io.input_mirror_L**response.yes
            + io[f"{'target' if switcharoo else 'input'}_half_T_row1"]
            ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_row2"]
            ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_row3"]
            ** numbers[f"n{row + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col1"]
            ** numbers[f"n{col}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col2"]
            ** numbers[f"n{col + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col3"]
            ** numbers[f"n{col}"]
            + io[f"{'input' if switcharoo else 'target'}_mirror_L_row1"]
            ** numbers[
                f"n{row + (-1 if i == 0 else 1) * (i % 2 == 0)}"
            ]  # 1 up, no up, 1 down.
            + io[f"{'input' if switcharoo else 'target'}_mirror_L_row2"]
            ** numbers[f"n{row + i}"]
            + io[f"{'input' if switcharoo else 'target'}_mirror_L_row3"]
            ** numbers[f"n{row + i}"]
            + io[f"{'input' if switcharoo else 'target'}_mirror_L_col1"]
            ** numbers[f"n{col - 1}"]
            + io[f"{'input' if switcharoo else 'target'}_mirror_L_col2"]
            ** numbers[f"n{col - 2}"]
            + io[f"{'input' if switcharoo else 'target'}_mirror_L_col3"]
            ** numbers[f"n{col - 1}"]
            + io[f"target_{'half_T' if switcharoo else 'mirror_L'}"]
            ** response.yes  # half_T isnt already there
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}"]
            ** response.no  # but mirror_L is
            >> +(io.construction_signal**con_signal.continue_construction)
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}"] ** response.yes
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_row1"]
            ** (
                numbers[f"n{row}"]
                if not switcharoo
                else numbers[f"n{row + (-1 if i == 0 else 1) * (i % 2 == 0)}"]
            )
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_row2"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + i}"])
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_row3"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + i}"])
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col - 1}"])
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_col2"]
            ** (numbers[f"n{col + 1}"] if not switcharoo else numbers[f"n{col - 2}"])
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_col3"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col - 1}"])
        )
        for switcharoo in (True, False)
        for i in range(3)
        for row in range(1 + (i == 0), 6 - (i == 2))
        for col in range(3, 6)
    ]

    half_t_below_mirror_l_placement_rule = [
        (
            +(io.input_half_T**response.yes)
            + io.input_mirror_L**response.yes
            + io[f"{'target' if switcharoo else 'input'}_half_T_row1"]
            ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_row2"]
            ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_row3"]
            ** numbers[f"n{row + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col1"]
            ** numbers[f"n{col}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col2"]
            ** numbers[f"n{col + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col3"]
            ** numbers[f"n{col}"]
            + io[f"{'input' if switcharoo else 'target'}_mirror_L_row1"]
            ** numbers[f"n{row - 2}"]
            + io[f"{'input' if switcharoo else 'target'}_mirror_L_row2"]
            ** numbers[f"n{row - 1}"]
            + io[f"{'input' if switcharoo else 'target'}_mirror_L_row3"]
            ** numbers[f"n{row - 1}"]
            + io[f"{'input' if switcharoo else 'target'}_mirror_L_col1"]
            ** numbers[f"n{col + i}"]
            + io[f"{'input' if switcharoo else 'target'}_mirror_L_col2"]
            ** numbers[f"n{col - 1 + i}"]
            + io[f"{'input' if switcharoo else 'target'}_mirror_L_col3"]
            ** numbers[f"n{col + i}"]
            + io[f"target_{'half_T' if switcharoo else 'mirror_L'}"]
            ** response.yes  # half_T isnt already there
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}"]
            ** response.no  # but mirror_L is
            >> +(io.construction_signal**con_signal.continue_construction)
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}"] ** response.yes
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row - 2}"])
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_row2"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row - 1}"])
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_row3"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row - 1}"])
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col + i}"])
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_col2"]
            ** (
                numbers[f"n{col + 1}"] if not switcharoo else numbers[f"n{col - 1 + i}"]
            )
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_col3"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col + i}"])
        )
        for switcharoo in (True, False)
        for i in range(3)
        for row in range(3, 6)
        for col in range(1 + (i == 0), 6 - (i == 2))
    ]

    half_t_above_mirror_l_placement_rule = [
        (
            +(io.input_half_T**response.yes)
            + io.input_mirror_L**response.yes
            + io[f"{'target' if switcharoo else 'input'}_half_T_row1"]
            ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_row2"]
            ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_row3"]
            ** numbers[f"n{row + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col1"]
            ** numbers[f"n{col}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col2"]
            ** numbers[f"n{col + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_half_T_col3"]
            ** numbers[f"n{col}"]
            + io[f"{'input' if switcharoo else 'target'}_mirror_L_row1"]
            ** numbers[f"n{row + 2}"]
            + io[f"{'input' if switcharoo else 'target'}_mirror_L_row2"]
            ** numbers[f"n{row + 3}"]
            + io[f"{'input' if switcharoo else 'target'}_mirror_L_row3"]
            ** numbers[f"n{row + 3}"]
            + io[f"{'input' if switcharoo else 'target'}_mirror_L_col1"]
            ** numbers[f"n{col}"]
            + io[f"{'input' if switcharoo else 'target'}_mirror_L_col2"]
            ** numbers[f"n{col - 1}"]
            + io[f"{'input' if switcharoo else 'target'}_mirror_L_col3"]
            ** numbers[f"n{col}"]
            + io[f"target_{'half_T' if switcharoo else 'mirror_L'}"]
            ** response.yes  # half_T isnt already there
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}"]
            ** response.no  # but mirror_L is
            >> +(io.construction_signal**con_signal.continue_construction)
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}"] ** response.yes
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + 2}"])
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_row2"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + 3}"])
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_row3"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + 3}"])
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col}"])
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_col2"]
            ** (numbers[f"n{col + 1}"] if not switcharoo else numbers[f"n{col - 1}"])
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_col3"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col}"])
        )
        for switcharoo in (True, False)
        for row in range(1, 4)
        for col in range(2, 6)
    ]

    mirror_l_left_horizontal_placement_rule = [
        (
            +(io.input_mirror_L**response.yes)
            + io.input_horizontal**response.yes
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_row1"]
            ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_row2"]
            ** numbers[f"n{row + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_row3"]
            ** numbers[f"n{row + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_col1"]
            ** numbers[f"n{col}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_col2"]
            ** numbers[f"n{col - 1}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_col3"]
            ** numbers[f"n{col}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_row1"]
            ** numbers[f"n{row + i}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_row2"]
            ** numbers[f"n{row + i}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_row3"]
            ** numbers[f"n{row + i}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_col1"]
            ** numbers[f"n{col + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_col2"]
            ** numbers[f"n{col + 2}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_col3"]
            ** numbers[f"n{col + 3}"]
            + io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"]
            ** response.yes  # mirror_L isnt already there
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"]
            ** response.no  # but horizontal is
            >> +(io.construction_signal**con_signal.continue_construction)
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"] ** response.yes
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + i}"])
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_row2"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + i}"])
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_row3"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + i}"])
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col + 1}"])
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_col2"]
            ** (numbers[f"n{col - 1}"] if not switcharoo else numbers[f"n{col + 2}"])
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_col3"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col + 3}"])
        )
        for switcharoo in (True, False)
        for i in range(2)
        for row in range(1, 6)
        for col in range(2, 4)
    ]

    mirror_l_right_horizontal_placement_rule = [
        (
            +(io.input_mirror_L**response.yes)
            + io.input_horizontal**response.yes
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_row1"]
            ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_row2"]
            ** numbers[f"n{row + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_row3"]
            ** numbers[f"n{row + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_col1"]
            ** numbers[f"n{col}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_col2"]
            ** numbers[f"n{col - 1}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_col3"]
            ** numbers[f"n{col}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_row1"]
            ** numbers[f"n{row + i}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_row2"]
            ** numbers[f"n{row + i}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_row3"]
            ** numbers[f"n{row + i}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_col1"]
            ** numbers[f"n{col - 3 - i}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_col2"]
            ** numbers[f"n{col - 2 - i}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_col3"]
            ** numbers[f"n{col - 1 - i}"]
            + io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"]
            ** response.yes  # mirror_L isnt already there
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"]
            ** response.no  # but horizontal is
            >> +(io.construction_signal**con_signal.continue_construction)
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"] ** response.yes
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + i}"])
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_row2"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + i}"])
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_row3"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + i}"])
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col - 3 - i}"])
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_col2"]
            ** (
                numbers[f"n{col - 1}"] if not switcharoo else numbers[f"n{col - 2 - i}"]
            )
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_col3"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col - 1 - i}"])
        )
        for switcharoo in (True, False)
        for i in range(2)
        for row in range(1, 6)
        for col in range(4 + i, 7)
    ]

    mirror_l_above_horizontal_placement_rule = [
        (
            +(io.input_mirror_L**response.yes)
            + io.input_horizontal**response.yes
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_row1"]
            ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_row2"]
            ** numbers[f"n{row + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_row3"]
            ** numbers[f"n{row + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_col1"]
            ** numbers[f"n{col}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_col2"]
            ** numbers[f"n{col - 1}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_col3"]
            ** numbers[f"n{col}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_row1"]
            ** numbers[f"n{row + 2}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_row2"]
            ** numbers[f"n{row + 2}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_row3"]
            ** numbers[f"n{row + 2}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_col1"]
            ** numbers[f"n{col - 3 + i}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_col2"]
            ** numbers[f"n{col - 2 + i}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_col3"]
            ** numbers[f"n{col - 1 + i}"]
            + io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"]
            ** response.yes  # mirror_L isnt already there
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"]
            ** response.no  # but horizontal is
            >> +(io.construction_signal**con_signal.continue_construction)
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"] ** response.yes
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + 2}"])
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_row2"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + 2}"])
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_row3"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + 2}"])
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col - 3 + i}"])
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_col2"]
            ** (
                numbers[f"n{col - 1}"] if not switcharoo else numbers[f"n{col - 2 + i}"]
            )
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_col3"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col - 1 + i}"])
        )
        for switcharoo in (True, False)
        for i in range(4)
        for row in range(1, 5)
        for col in range((4 - i if i < 2 else 2), 7 - (i - 1 if i >= 2 else 0))
    ]

    mirror_l_below_horizontal_placement_rule = [
        (
            +(io.input_mirror_L**response.yes)
            + io.input_horizontal**response.yes
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_row1"]
            ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_row2"]
            ** numbers[f"n{row + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_row3"]
            ** numbers[f"n{row + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_col1"]
            ** numbers[f"n{col}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_col2"]
            ** numbers[f"n{col - 1}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_col3"]
            ** numbers[f"n{col}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_row1"]
            ** numbers[f"n{row - 1}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_row2"]
            ** numbers[f"n{row - 1}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_row3"]
            ** numbers[f"n{row - 1}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_col1"]
            ** numbers[f"n{col - 2 + i}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_col2"]
            ** numbers[f"n{col - 1 + i}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_col3"]
            ** numbers[f"n{col + i}"]
            + io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"]
            ** response.yes  # mirror_L isnt already there
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"]
            ** response.no  # but horizontal is
            >> +(io.construction_signal**con_signal.continue_construction)
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"] ** response.yes
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row - 1}"])
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_row2"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row - 1}"])
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_row3"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row - 1}"])
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col - 2 + i}"])
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_col2"]
            ** (
                numbers[f"n{col - 1}"] if not switcharoo else numbers[f"n{col - 1 + i}"]
            )
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_col3"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col + i}"])
        )
        for switcharoo in (True, False)
        for i in range(3)
        for row in range(2, 6)
        for col in range(3 - (i != 0), 7 - i)
    ]

    mirror_l_left_vertical_placement_rule = [
        (
            +(io.input_mirror_L**response.yes)
            + io.input_vertical**response.yes
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_row1"]
            ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_row2"]
            ** numbers[f"n{row + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_row3"]
            ** numbers[f"n{row + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_col1"]
            ** numbers[f"n{col}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_col2"]
            ** numbers[f"n{col - 1}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_col3"]
            ** numbers[f"n{col}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_row1"]
            ** numbers[f"n{row - 2 + i}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_row2"]
            ** numbers[f"n{row - 1 + i}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_row3"]
            ** numbers[f"n{row + i}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_col1"]
            ** numbers[f"n{col + 1}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_col2"]
            ** numbers[f"n{col + 1}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_col3"]
            ** numbers[f"n{col + 1}"]
            + io[f"target_{'mirror_L' if switcharoo else 'vertical'}"]
            ** response.yes  # mirror_L isnt already there
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}"]
            ** response.no  # but vertical is
            >> +(io.construction_signal**con_signal.continue_construction)
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}"] ** response.yes
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row - 2 + i}"])
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_row2"]
            ** (
                numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row - 1 + i}"]
            )
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_row3"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + i}"])
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col + 1}"])
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_col2"]
            ** (numbers[f"n{col - 1}"] if not switcharoo else numbers[f"n{col + 1}"])
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_col3"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col + 1}"])
        )
        for switcharoo in (True, False)
        for i in range(4)
        for row in range(max(3 - i, 1), 6 - (0 if i < 2 else i - 1))
        for col in range(2, 6)
    ]

    mirror_l_right_vertical_placement_rule = [
        (
            +(io.input_mirror_L**response.yes)
            + io.input_vertical**response.yes
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_row1"]
            ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_row2"]
            ** numbers[f"n{row + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_row3"]
            ** numbers[f"n{row + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_col1"]
            ** numbers[f"n{col}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_col2"]
            ** numbers[f"n{col - 1}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_col3"]
            ** numbers[f"n{col}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_row1"]
            ** numbers[f"n{row + 1 - i}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_row2"]
            ** numbers[f"n{row + 2 - i}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_row3"]
            ** numbers[f"n{row + 3 - i}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_col1"]
            ** numbers[f"n{col - 2 + (i == 3)}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_col2"]
            ** numbers[f"n{col - 2 + (i == 3)}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_col3"]
            ** numbers[f"n{col - 2 + (i == 3)}"]
            + io[f"target_{'mirror_L' if switcharoo else 'vertical'}"]
            ** response.yes  # mirror_L isnt already there
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}"]
            ** response.no  # but vertical is
            >> +(io.construction_signal**con_signal.continue_construction)
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}"] ** response.yes
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + 1 - i}"])
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_row2"]
            ** (
                numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + 2 - i}"]
            )
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_row3"]
            ** (
                numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + 3 - i}"]
            )
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_col1"]
            ** (
                numbers[f"n{col}"]
                if not switcharoo
                else numbers[f"n{col - 2 + (i == 3)}"]
            )
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_col2"]
            ** (
                numbers[f"n{col - 1}"]
                if not switcharoo
                else numbers[f"n{col - 2 + (i == 3)}"]
            )
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_col3"]
            ** (
                numbers[f"n{col}"]
                if not switcharoo
                else numbers[f"n{col - 2 + (i == 3)}"]
            )
        )
        for switcharoo in (True, False)
        for i in range(4)
        for row in range(1 + max(0, i - 1), min(4 + i, 6))
        for col in range(3 - (i == 3), 7)
    ]

    mirror_l_above_vertical_placement_rule = [
        (
            +(io.input_mirror_L**response.yes)
            + io.input_vertical**response.yes
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_row1"]
            ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_row2"]
            ** numbers[f"n{row + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_row3"]
            ** numbers[f"n{row + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_col1"]
            ** numbers[f"n{col}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_col2"]
            ** numbers[f"n{col - 1}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_col3"]
            ** numbers[f"n{col}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_row1"]
            ** numbers[f"n{row + 2}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_row2"]
            ** numbers[f"n{row + 3}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_row3"]
            ** numbers[f"n{row + 4}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_col1"]
            ** numbers[f"n{col - 1 + i}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_col2"]
            ** numbers[f"n{col - 1 + i}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_col3"]
            ** numbers[f"n{col - 1 + i}"]
            + io[f"target_{'mirror_L' if switcharoo else 'vertical'}"]
            ** response.yes  # mirror_L isnt already there
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}"]
            ** response.no  # but vertical is
            >> +(io.construction_signal**con_signal.continue_construction)
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}"] ** response.yes
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + 2}"])
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_row2"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + 3}"])
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_row3"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + 4}"])
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col - 1 + i}"])
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_col2"]
            ** (
                numbers[f"n{col - 1}"] if not switcharoo else numbers[f"n{col - 1 + i}"]
            )
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_col3"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col - 1 + i}"])
        )
        for switcharoo in (True, False)
        for i in range(2)
        for row in range(1, 3)
        for col in range(2, 7)
    ]

    mirror_l_below_vertical_placement_rule = [
        (
            +(io.input_mirror_L**response.yes)
            + io.input_vertical**response.yes
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_row1"]
            ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_row2"]
            ** numbers[f"n{row + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_row3"]
            ** numbers[f"n{row + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_col1"]
            ** numbers[f"n{col}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_col2"]
            ** numbers[f"n{col - 1}"]
            + io[f"{'target' if switcharoo else 'input'}_mirror_L_col3"]
            ** numbers[f"n{col}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_row1"]
            ** numbers[f"n{row - 3}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_row2"]
            ** numbers[f"n{row - 2}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_row3"]
            ** numbers[f"n{row - 1}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_col1"]
            ** numbers[f"n{col}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_col2"]
            ** numbers[f"n{col}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_col3"]
            ** numbers[f"n{col}"]
            + io[f"target_{'mirror_L' if switcharoo else 'vertical'}"]
            ** response.yes  # mirror_L isnt already there
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}"]
            ** response.no  # but vertical is
            >> +(io.construction_signal**con_signal.continue_construction)
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}"] ** response.yes
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row - 3}"])
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_row2"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row - 2}"])
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_row3"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row - 1}"])
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col}"])
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_col2"]
            ** (numbers[f"n{col - 1}"] if not switcharoo else numbers[f"n{col}"])
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_col3"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col}"])
        )
        for switcharoo in (True, False)
        for row in range(4, 6)
        for col in range(2, 7)
    ]

    horizontal_left_vertical_placement_rule = [
        (
            +(io.input_vertical**response.yes)
            + io.input_horizontal**response.yes
            + io[f"{'input' if switcharoo else 'target'}_horizontal_row1"]
            ** numbers[f"n{row}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_row2"]
            ** numbers[f"n{row}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_row3"]
            ** numbers[f"n{row}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_col1"]
            ** numbers[f"n{col}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_col2"]
            ** numbers[f"n{col + 1}"]
            + io[f"{'input' if switcharoo else 'target'}_horizontal_col3"]
            ** numbers[f"n{col + 2}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_row1"]
            ** numbers[f"n{row - 2 + i}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_row2"]
            ** numbers[f"n{row - 1 + i}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_row3"]
            ** numbers[f"n{row + i}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_col1"]
            ** numbers[f"n{col + 3}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_col2"]
            ** numbers[f"n{col + 3}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_col3"]
            ** numbers[f"n{col + 3}"]
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}"]
            ** response.yes  # horizontal isnt already there
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}"]
            ** response.no  # but vertical is
            >> +(io.construction_signal**con_signal.continue_construction)
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}"] ** response.yes
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row - 2 + i}"])
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_row2"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row - 1 + i}"])
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_row3"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + i}"])
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col + 3}"])
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_col2"]
            ** (numbers[f"n{col + 1}"] if not switcharoo else numbers[f"n{col + 3}"])
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_col3"]
            ** (numbers[f"n{col + 2}"] if not switcharoo else numbers[f"n{col + 3}"])
        )
        for switcharoo in (True, False)
        for i in range(3)
        for row in range(3 - i, 7 - i)
        for col in range(1, 4)
    ]

    horizontal_right_vertical_placement_rule = [
        (
            +(io.input_vertical**response.yes)
            + io.input_horizontal**response.yes
            + io[f"{'target' if switcharoo else 'input'}_horizontal_row1"]
            ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_row2"]
            ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_row3"]
            ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_col1"]
            ** numbers[f"n{col}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_col2"]
            ** numbers[f"n{col + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_col3"]
            ** numbers[f"n{col + 2}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_row1"]
            ** numbers[f"n{row - 2 + i}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_row2"]
            ** numbers[f"n{row - 1 + i}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_row3"]
            ** numbers[f"n{row + i}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_col1"]
            ** numbers[f"n{col - 1}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_col2"]
            ** numbers[f"n{col - 1}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_col3"]
            ** numbers[f"n{col - 1}"]
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}"]
            ** response.yes  # horizontal isnt already there
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}"]
            ** response.no  # but vertical is
            >> +(io.construction_signal**con_signal.continue_construction)
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}"] ** response.yes
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row - 2 + i}"])
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_row2"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row - 1 + i}"])
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_row3"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + i}"])
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col - 1}"])
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_col2"]
            ** (numbers[f"n{col + 1}"] if not switcharoo else numbers[f"n{col - 1}"])
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_col3"]
            ** (numbers[f"n{col + 2}"] if not switcharoo else numbers[f"n{col - 1}"])
        )
        for switcharoo in (True, False)
        for i in range(3)
        for row in range(3 - i, 7 - i)
        for col in range(2, 5)
    ]

    horizontal_above_vertical_placement_rule = [
        (
            +(io.input_vertical**response.yes)
            + io.input_horizontal**response.yes
            + io[f"{'target' if switcharoo else 'input'}_horizontal_row1"]
            ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_row2"]
            ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_row3"]
            ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_col1"]
            ** numbers[f"n{col}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_col2"]
            ** numbers[f"n{col + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_col3"]
            ** numbers[f"n{col + 2}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_row1"]
            ** numbers[f"n{row + 1}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_row2"]
            ** numbers[f"n{row + 2}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_row3"]
            ** numbers[f"n{row + 3}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_col1"]
            ** numbers[f"n{col + i}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_col2"]
            ** numbers[f"n{col + i}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_col3"]
            ** numbers[f"n{col + i}"]
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}"]
            ** response.yes  # horizontal isnt already there
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}"]
            ** response.no  # but vertical is
            >> +(io.construction_signal**con_signal.continue_construction)
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}"] ** response.yes
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + 1}"])
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}_row2"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + 2}"])
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}_row3"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + 3}"])
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col + i}"])
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}_col2"]
            ** (numbers[f"n{col + 1}"] if not switcharoo else numbers[f"n{col + i}"])
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}_col3"]
            ** (numbers[f"n{col + 2}"] if not switcharoo else numbers[f"n{col + i}"])
        )
        for switcharoo in (True, False)
        for i in range(3)
        for row in range(1, 4)
        for col in range(1, 5)
    ]

    horizontal_below_vertical_placement_rule = [
        (
            +(io.input_vertical**response.yes)
            + io.input_horizontal**response.yes
            + io[f"{'target' if switcharoo else 'input'}_horizontal_row1"]
            ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_row2"]
            ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_row3"]
            ** numbers[f"n{row}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_col1"]
            ** numbers[f"n{col}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_col2"]
            ** numbers[f"n{col + 1}"]
            + io[f"{'target' if switcharoo else 'input'}_horizontal_col3"]
            ** numbers[f"n{col + 2}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_row1"]
            ** numbers[f"n{row - 3}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_row2"]
            ** numbers[f"n{row - 2}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_row3"]
            ** numbers[f"n{row - 1}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_col1"]
            ** numbers[f"n{col + i}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_col2"]
            ** numbers[f"n{col + i}"]
            + io[f"{'input' if switcharoo else 'target'}_vertical_col3"]
            ** numbers[f"n{col + i}"]
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}"]
            ** response.yes  # horizontal isnt already there
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}"]
            ** response.no  # but vertical is
            >> +(io.construction_signal**con_signal.continue_construction)
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}"] ** response.yes
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row - 3}"])
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_row2"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row - 2}"])
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_row3"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row - 1}"])
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col + i}"])
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_col2"]
            ** (numbers[f"n{col + 1}"] if not switcharoo else numbers[f"n{col + i}"])
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_col3"]
            ** (numbers[f"n{col + 2}"] if not switcharoo else numbers[f"n{col + i}"])
        )
        for switcharoo in (True, False)
        for i in range(3)
        for row in range(4, 7)
        for col in range(1, 5)
    ]

    # END_CONSTRUCTION RULE
    # if all four blocks have been used, then stop construction
    stop_construction_rule_all_four = [
        (
            +(io.target_half_T**response.yes)
            + io.target_mirror_L**response.yes
            + io.target_vertical**response.yes
            + io.target_horizontal**response.yes
            >> +(io.construction_signal**con_signal.stop_construction)
        )
    ]

    stop_construction_input_blocks_used_one = [
        (
            +(io[f"input_{shape}"] ** response.yes)
            + io[f"input_{(SHAPES[:i] + SHAPES[i + 1:])[0]}"] ** response.no
            + io[f"input_{(SHAPES[:i] + SHAPES[i + 1:])[1]}"] ** response.no
            + io[f"input_{(SHAPES[:i] + SHAPES[i + 1:])[2]}"] ** response.no
            + io[f"target_{shape}"] ** response.yes
            + io[f"target_{(SHAPES[:i] + SHAPES[i + 1:])[0]}"] ** response.no
            + io[f"target_{(SHAPES[:i] + SHAPES[i + 1:])[1]}"] ** response.no
            + io[f"target_{(SHAPES[:i] + SHAPES[i + 1:])[2]}"] ** response.no
            >> +(io.construction_signal**con_signal.stop_construction)
        )
        for i, shape in enumerate(SHAPES)
    ]

    stop_construction_input_blocks_used_two = [
        (
            +(io[f"input_{shape}"] ** response.yes)
            + io[f"input_{other_shape}"] ** response.yes
            + io[f"input_{[s for s in SHAPES if s not in (shape, other_shape)][0]}"]
            ** response.no
            + io[f"input_{[s for s in SHAPES if s not in (shape, other_shape)][1]}"]
            ** response.no
            + io[f"target_{shape}"] ** response.yes
            + io[f"target_{other_shape}"] ** response.yes
            + io[f"target_{[s for s in SHAPES if s not in (shape, other_shape)][0]}"]
            ** response.no
            + io[f"target_{[s for s in SHAPES if s not in (shape, other_shape)][1]}"]
            ** response.no
            >> io.construction_signal**con_signal.stop_construction
        )
        for (shape, other_shape) in itertools.combinations(SHAPES, 2)
    ]

    stop_construction_input_blocks_used_three = [
        (
            +(io[f"input_{shape}"] ** response.yes)
            + io[f"input_{other_shape}"] ** response.yes
            + io[f"input_{other_other_shape}"] ** response.yes
            + io[
                f"input_{[s for s in SHAPES if s not in (shape, other_shape, other_other_shape)][0]}"
            ]
            ** response.no
            + io[f"target_{shape}"] ** response.yes
            + io[f"target_{other_shape}"] ** response.yes
            + io[f"target_{other_other_shape}"] ** response.yes
            + io[
                f"target_{[s for s in SHAPES if s not in (shape, other_shape, other_other_shape)][0]}"
            ]
            ** response.no
            >> io.construction_signal**con_signal.stop_construction
        )
        for (shape, other_shape, other_other_shape) in itertools.combinations(SHAPES, 3)
    ]

    # Backtracking rules
    bad_brick_backtracking_rule = [
        (
            +(io[f"input_{shape}"] ** response.no)
            + io[f"target_{shape}"] ** response.yes
            >> io.construction_signal**con_signal.backtrack_construction
        )
        for shape in SHAPES
    ]

    participant.search_space_rules.rules.compile(
        *(
            stop_construction_rule_all_four
            + stop_construction_input_blocks_used_one
            + stop_construction_input_blocks_used_two
            + stop_construction_input_blocks_used_three
            + half_t_first_placement_rule
            + mirror_l_first_placement_rule
            + horizontal_first_placement_rule
            + vertical_first_placement_rule
            + half_t_left_of_horizontal_placement_rule
            + half_t_right_of_horizontal_placement_rule
            + half_t_above_horizontal_placement_rule
            + half_t_below_horizontal_placement_rule
            + half_t_left_vertical_placement_rule
            + half_t_right_vertical_placement_rule
            + half_t_above_vertical_placement_rule
            + half_t_below_vertical_placement_rule
            + half_t_left_mirror_l_placement_rule
            + half_t_right_mirror_l_placement_rule
            + half_t_above_mirror_l_placement_rule
            + half_t_below_mirror_l_placement_rule
            + mirror_l_left_horizontal_placement_rule
            + mirror_l_right_horizontal_placement_rule
            + mirror_l_above_horizontal_placement_rule
            + mirror_l_below_horizontal_placement_rule
            + mirror_l_left_vertical_placement_rule
            + mirror_l_right_vertical_placement_rule
            + mirror_l_above_vertical_placement_rule
            + mirror_l_below_vertical_placement_rule
            + horizontal_left_vertical_placement_rule
            + horizontal_right_vertical_placement_rule
            + horizontal_above_vertical_placement_rule
            + horizontal_below_vertical_placement_rule
            + bad_brick_backtracking_rule
        )
    )


def init_participant_construction_rule_w_abstract(participant):
    d = participant.construction_space
    io = d.io
    numbers = d.numbers
    response = d.response
    con_signal = d.signal_tokens

    # FIRST PLACEMENT RULES
    """
    1 1
    1
    """
    half_t_first_placement_rule = [
        (
            +7.0 * (io.start**response.yes)
            - 7.0 * (io.start**response.no)
            + io.left**response.no
            + io.right**response.no
            + io.above**response.no
            + io.below**response.no
            + io.input_half_T**response.yes
            + io.input_half_T_row1 ** numbers[f"n{row}"]
            + io.input_half_T_row2 ** numbers[f"n{row}"]
            + io.input_half_T_row3 ** numbers[f"n{row + 1}"]
            + io.input_half_T_col1 ** numbers[f"n{col}"]
            + io.input_half_T_col2 ** numbers[f"n{col + 1}"]
            + io.input_half_T_col3 ** numbers[f"n{col}"]
            + 7.0 * (io.target_half_T**response.latest)
            - 7.0 * (io.target_half_T**response.yes)
            - 7.0 * (io.target_half_T**response.no)
            - 7.0 * (io.target_half_T**response.reference)
            >> +(io.target_half_T**response.yes)
            + io.target_half_T_row1 ** numbers[f"n{row}"]
            + io.target_half_T_row2 ** numbers[f"n{row}"]
            + io.target_half_T_row3 ** numbers[f"n{row + 1}"]
            + io.target_half_T_col1 ** numbers[f"n{col}"]
            + io.target_half_T_col2 ** numbers[f"n{col + 1}"]
            + io.target_half_T_col3 ** numbers[f"n{col}"]
            + io.construction_signal**con_signal.continue_construction
        )
        for row in range(1, 6)
        for col in range(1, 6)
    ]

    mirror_l_first_placement_rule = [
        (
            +7.0 * (io.start**response.yes)
            - 7.0 * (io.start**response.no)
            + io.left**response.no
            + io.right**response.no
            + io.above**response.no
            + io.below**response.no
            + io.input_mirror_L**response.yes
            + io.input_mirror_L_row1 ** numbers[f"n{row}"]
            + io.input_mirror_L_row2 ** numbers[f"n{row + 1}"]
            + io.input_mirror_L_row3 ** numbers[f"n{row + 1}"]
            + io.input_mirror_L_col1 ** numbers[f"n{col}"]
            + io.input_mirror_L_col2 ** numbers[f"n{col - 1}"]
            + io.input_mirror_L_col3 ** numbers[f"n{col}"]
            + 7.0 * (io.target_mirror_L**response.latest)
            - 7.0 * (io.target_mirror_L**response.yes)
            - 7.0 * (io.target_mirror_L**response.no)
            - 7.0 * (io.target_mirror_L**response.reference)
            >> +(io.target_mirror_L**response.yes)
            + io.target_mirror_L_row1 ** numbers[f"n{row}"]
            + io.target_mirror_L_row2 ** numbers[f"n{row + 1}"]
            + io.target_mirror_L_row3 ** numbers[f"n{row + 1}"]
            + io.target_mirror_L_col1 ** numbers[f"n{col}"]
            + io.target_mirror_L_col2 ** numbers[f"n{col - 1}"]
            + io.target_mirror_L_col3 ** numbers[f"n{col}"]
            + io.construction_signal**con_signal.continue_construction
        )
        for row in range(1, 6)
        for col in range(2, 7)
    ]
    """
      1
    1 1
    """

    horizontal_first_placement_rule = [
        (
            +7.0 * (io.start**response.yes)
            - 7.0 * (io.start**response.no)
            + io.left**response.no
            + io.right**response.no
            + io.above**response.no
            + io.below**response.no
            + io.input_horizontal**response.yes
            + io.input_horizontal_row1 ** numbers[f"n{row}"]
            + io.input_horizontal_row2 ** numbers[f"n{row}"]
            + io.input_horizontal_row3 ** numbers[f"n{row}"]
            + io.input_horizontal_col1 ** numbers[f"n{col}"]
            + io.input_horizontal_col2 ** numbers[f"n{col + 1}"]
            + io.input_horizontal_col3 ** numbers[f"n{col + 2}"]
            + 7.0 * (io.target_horizontal**response.latest)
            - 7.0 * (io.target_horizontal**response.yes)
            - 7.0 * (io.target_horizontal**response.no)
            - 7.0 * (io.target_horizontal**response.reference)
            >> +(io.target_horizontal**response.yes)
            + io.target_horizontal_row1 ** numbers[f"n{row}"]
            + io.target_horizontal_row2 ** numbers[f"n{row}"]
            + io.target_horizontal_row3 ** numbers[f"n{row}"]
            + io.target_horizontal_col1 ** numbers[f"n{col}"]
            + io.target_horizontal_col2 ** numbers[f"n{col + 1}"]
            + io.target_horizontal_col3 ** numbers[f"n{col + 2}"]
            + io.construction_signal**con_signal.continue_construction
        )
        for row in range(1, 7)
        for col in range(1, 5)
    ]

    vertical_first_placement_rule = [
        (
            +7.0 * (io.start**response.yes)
            - 7.0 * (io.start**response.no)
            + io.left**response.no
            + io.right**response.no
            + io.above**response.no
            + io.below**response.no
            + io.input_vertical**response.yes
            + io.input_vertical_row1 ** numbers[f"n{row}"]
            + io.input_vertical_row2 ** numbers[f"n{row + 1}"]
            + io.input_vertical_row3 ** numbers[f"n{row + 2}"]
            + io.input_vertical_col1 ** numbers[f"n{col}"]
            + io.input_vertical_col2 ** numbers[f"n{col}"]
            + io.input_vertical_col3 ** numbers[f"n{col}"]
            + 7.0 * (io.target_vertical**response.latest)
            - 7.0 * (io.target_vertical**response.yes)
            - 7.0 * (io.target_vertical**response.no)
            - 7.0 * (io.target_vertical**response.reference)
            >> +(io.target_vertical**response.yes)
            + io.target_vertical_row1 ** numbers[f"n{row}"]
            + io.target_vertical_row2 ** numbers[f"n{row + 1}"]
            + io.target_vertical_row3 ** numbers[f"n{row + 2}"]
            + io.target_vertical_col1 ** numbers[f"n{col}"]
            + io.target_vertical_col2 ** numbers[f"n{col}"]
            + io.target_vertical_col3 ** numbers[f"n{col}"]
            + io.construction_signal**con_signal.continue_construction
        )
        for row in range(1, 5)
        for col in range(1, 7)
    ]

    # SUBSEQUENCE PLACEMENT RULES
    half_t_left_of_horizontal_placement_rule = [
        (
            +(io.input_half_T**response.yes)
            + io.input_horizontal**response.yes
            + io.start**response.no
            + (7.0 if r_switcharoo else 1.0)
            * (io.left ** (response.yes if r_switcharoo else response.no))
            - (7.0 if r_switcharoo else 1.0)
            * (io.left ** (response.no if r_switcharoo else response.yes))
            + (1.0 if r_switcharoo else 7.0)
            * (io.right ** (response.no if r_switcharoo else response.yes))
            - (1.0 if r_switcharoo else 7.0)
            * (io.right ** (response.yes if r_switcharoo else response.no))
            + io.above**response.no
            + io.below**response.no
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_row1"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_row2"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_row3"]
            ** numbers[f"n{row + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_col1"]
            ** numbers[f"n{col}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_col2"]
            ** numbers[f"n{col + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_col3"]
            ** numbers[f"n{col}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_row1"]
            ** numbers[f"n{row + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_row2"]
            ** numbers[f"n{row + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_row3"]
            ** numbers[f"n{row + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_col1"]
            ** numbers[f"n{col + 2 - i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_col2"]
            ** numbers[f"n{col + 3 - i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_col3"]
            ** numbers[f"n{col + 4 - i}"]
            + 2.0
            * (
                io[f"target_{'half_T' if switcharoo else 'horizontal'}"]
                ** response.reference
            )  # half_T is already there
            + 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'half_T'}"]
                ** response.latest
            )  # but horizontal is not
            - 2.0
            * (io[f"target_{'half_T' if switcharoo else 'horizontal'}"] ** response.yes)
            - 2.0
            * (
                io[f"target_{'half_T' if switcharoo else 'horizontal'}"]
                ** response.latest
            )
            - 2.0
            * (io[f"target_{'half_T' if switcharoo else 'horizontal'}"] ** response.no)
            - 2.0
            * (io[f"target_{'horizontal' if switcharoo else 'half_T'}"] ** response.yes)
            - 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'half_T'}"]
                ** response.reference
            )
            - 2.0
            * (io[f"target_{'horizontal' if switcharoo else 'half_T'}"] ** response.no)
            >> +(
                io[f"target_{'horizontal' if switcharoo else 'half_T'}"] ** response.yes
            )
            + io[f"target_{'half_T' if switcharoo else 'horizontal'}"] ** response.yes
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + i}"])
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_row2"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + i}"])
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_row3"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + i}"])
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col + 2 - i}"])
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_col2"]
            ** (
                numbers[f"n{col + 1}"] if not switcharoo else numbers[f"n{col + 3 - i}"]
            )
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_col3"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col + 4 - i}"])
            + io.construction_signal**con_signal.continue_construction
        )
        for r_switcharoo in (True, False)
        for switcharoo in (True, False)
        for i in range(2)
        for row in range(1, 6)
        for col in range(1, 3 + i)
    ]

    half_t_right_of_horizontal_placement_rule = [
        (
            +(io.input_half_T**response.yes)
            + io.input_horizontal**response.yes
            + io.start**response.no
            + (1.0 if r_switcharoo else 7.0)
            * (io.left ** (response.no if r_switcharoo else response.yes))
            - (1.0 if r_switcharoo else 7.0)
            * (io.left ** (response.yes if r_switcharoo else response.no))
            + (7.0 if r_switcharoo else 1.0)
            * (io.right ** (response.yes if r_switcharoo else response.no))
            - (7.0 if r_switcharoo else 1.0)
            * (io.right ** (response.no if r_switcharoo else response.yes))
            + io.above**response.no
            + io.below**response.no
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_row1"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_row2"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_row3"]
            ** numbers[f"n{row + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_col1"]
            ** numbers[f"n{col}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_col2"]
            ** numbers[f"n{col + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_col3"]
            ** numbers[f"n{col}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_row1"]
            ** numbers[f"n{row + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_row2"]
            ** numbers[f"n{row + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_row3"]
            ** numbers[f"n{row + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_col1"]
            ** numbers[f"n{col - 3}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_col2"]
            ** numbers[f"n{col - 2}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_col3"]
            ** numbers[f"n{col - 1}"]
            + 2.0
            * (
                io[f"target_{'half_T' if switcharoo else 'horizontal'}"]
                ** response.reference
            )  # half_T is already there
            + 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'half_T'}"]
                ** response.latest
            )  # but horizontal is not
            - 2.0
            * (io[f"target_{'half_T' if switcharoo else 'horizontal'}"] ** response.yes)
            - 2.0
            * (
                io[f"target_{'half_T' if switcharoo else 'horizontal'}"]
                ** response.latest
            )
            - 2.0
            * (io[f"target_{'half_T' if switcharoo else 'horizontal'}"] ** response.no)
            - 2.0
            * (io[f"target_{'horizontal' if switcharoo else 'half_T'}"] ** response.yes)
            - 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'half_T'}"]
                ** response.reference
            )
            - 2.0
            * (io[f"target_{'horizontal' if switcharoo else 'half_T'}"] ** response.no)
            >> +(
                io[f"target_{'horizontal' if switcharoo else 'half_T'}"] ** response.yes
            )
            + io[f"target_{'half_T' if switcharoo else 'horizontal'}"] ** response.yes
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + i}"])
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_row2"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + i}"])
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_row3"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + i}"])
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col - 3}"])
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_col2"]
            ** (numbers[f"n{col + 1}"] if not switcharoo else numbers[f"n{col - 2}"])
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_col3"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col - 1}"])
            + io.construction_signal**con_signal.continue_construction
        )
        for r_switcharoo in (True, False)
        for switcharoo in (True, False)
        for i in range(2)
        for row in range(1, 6)
        for col in range(4, 6)
    ]

    half_t_below_horizontal_placement_rule = [
        (
            +(io.input_half_T**response.yes)
            + io.input_horizontal**response.yes
            + io.start**response.no
            + io.left**response.no
            + io.right**response.no
            + (1.0 if r_switcharoo else 7.0)
            * (io.above ** (response.no if r_switcharoo else response.yes))
            - (1.0 if r_switcharoo else 7.0)
            * (io.above ** (response.yes if r_switcharoo else response.no))
            + (7.0 if r_switcharoo else 1.0)
            * (io.below ** (response.yes if r_switcharoo else response.no))
            - (7.0 if r_switcharoo else 1.0)
            * (io.below ** (response.no if r_switcharoo else response.yes))
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_row1"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_row2"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_row3"]
            ** numbers[f"n{row + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_col1"]
            ** numbers[f"n{col}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_col2"]
            ** numbers[f"n{col + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_col3"]
            ** numbers[f"n{col}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_row1"]
            ** numbers[f"n{row - 1}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_row2"]
            ** numbers[f"n{row - 1}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_row3"]
            ** numbers[f"n{row - 1}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_col1"]
            ** numbers[f"n{col - 2 + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_col2"]
            ** numbers[f"n{col - 1 + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_col3"]
            ** numbers[f"n{col + i}"]
            + 2.0
            * (
                io[f"target_{'half_T' if switcharoo else 'horizontal'}"]
                ** response.reference
            )  # half_T is already there
            + 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'half_T'}"]
                ** response.latest
            )  # but horizontal is not
            - 2.0
            * (io[f"target_{'half_T' if switcharoo else 'horizontal'}"] ** response.yes)
            - 2.0
            * (
                io[f"target_{'half_T' if switcharoo else 'horizontal'}"]
                ** response.latest
            )
            - 2.0
            * (io[f"target_{'half_T' if switcharoo else 'horizontal'}"] ** response.no)
            - 2.0
            * (io[f"target_{'horizontal' if switcharoo else 'half_T'}"] ** response.yes)
            - 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'half_T'}"]
                ** response.reference
            )
            - 2.0
            * (io[f"target_{'horizontal' if switcharoo else 'half_T'}"] ** response.no)
            >> +(
                io[f"target_{'horizontal' if switcharoo else 'half_T'}"] ** response.yes
            )
            + io[f"target_{'half_T' if switcharoo else 'horizontal'}"] ** response.yes
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row - 1}"])
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_row2"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row - 1}"])
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_row3"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row - 1}"])
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col - 2 + i}"])
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_col2"]
            ** (
                numbers[f"n{col + 1}"] if not switcharoo else numbers[f"n{col - 1 + i}"]
            )
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_col3"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col + i}"])
            + io.construction_signal**con_signal.continue_construction
        )
        for r_switcharoo in (True, False)
        for switcharoo in (True, False)
        for i in range(4)
        for row in range(2, 6)
        for col in range(max(3 - i, 1), 6 - max(i - 1, 0))
    ]

    half_t_above_horizontal_placement_rule = [
        (
            +(io.input_half_T**response.yes)
            + io.input_horizontal**response.yes
            + io.start**response.no
            + io.left**response.no
            + io.right**response.no
            + (7.0 if r_switcharoo else 1.0)
            * (io.above ** (response.yes if r_switcharoo else response.no))
            - (7.0 if r_switcharoo else 1.0)
            * (io.above ** (response.no if r_switcharoo else response.yes))
            + (1.0 if r_switcharoo else 7.0)
            * (io.below ** (response.no if r_switcharoo else response.yes))
            - (1.0 if r_switcharoo else 7.0)
            * (io.below ** (response.yes if r_switcharoo else response.no))
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_row1"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_row2"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_row3"]
            ** numbers[f"n{row + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_col1"]
            ** numbers[f"n{col}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_col2"]
            ** numbers[f"n{col + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_col3"]
            ** numbers[f"n{col}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_row1"]
            ** numbers[f"n{row + 2}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_row2"]
            ** numbers[f"n{row + 2}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_row3"]
            ** numbers[f"n{row + 2}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_col1"]
            ** numbers[f"n{col - 2 + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_col2"]
            ** numbers[f"n{col - 1 + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_col3"]
            ** numbers[f"n{col + i}"]
            + 2.0
            * (
                io[f"target_{'half_T' if switcharoo else 'horizontal'}"]
                ** response.reference
            )  # half_T isnt already there
            + 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'half_T'}"]
                ** response.latest
            )  # but horizontal is
            - 2.0
            * (io[f"target_{'half_T' if switcharoo else 'horizontal'}"] ** response.yes)
            - 2.0
            * (
                io[f"target_{'half_T' if switcharoo else 'horizontal'}"]
                ** response.latest
            )
            - 2.0
            * (io[f"target_{'half_T' if switcharoo else 'horizontal'}"] ** response.no)
            - 2.0
            * (io[f"target_{'horizontal' if switcharoo else 'half_T'}"] ** response.yes)
            - 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'half_T'}"]
                ** response.reference
            )
            - 2.0
            * (io[f"target_{'horizontal' if switcharoo else 'half_T'}"] ** response.no)
            >> +(
                io[f"target_{'horizontal' if switcharoo else 'half_T'}"] ** response.yes
            )
            + io[f"target_{'half_T' if switcharoo else 'horizontal'}"] ** response.yes
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + 2}"])
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_row2"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + 2}"])
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_row3"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + 2}"])
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col - 2 + i}"])
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_col2"]
            ** (
                numbers[f"n{col + 1}"] if not switcharoo else numbers[f"n{col - 1 + i}"]
            )
            + io[f"target_{'horizontal' if switcharoo else 'half_T'}_col3"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col + i}"])
            + io.construction_signal**con_signal.continue_construction
        )
        for r_switcharoo in (True, False)
        for switcharoo in (True, False)
        for i in range(3)
        for row in range(1, 5)
        for col in range(3 - i, 6 - (i == 2))
    ]

    half_t_left_vertical_placement_rule = [
        (
            +(io.input_half_T**response.yes)
            + io.input_vertical**response.yes
            + io.start**response.no
            + (7.0 if r_switcharoo else 1.0)
            * (io.left ** (response.yes if r_switcharoo else response.no))
            - (7.0 if r_switcharoo else 1.0)
            * (io.left ** (response.no if r_switcharoo else response.yes))
            + (1.0 if r_switcharoo else 7.0)
            * (io.right ** (response.no if r_switcharoo else response.yes))
            - (1.0 if r_switcharoo else 7.0)
            * (io.right ** (response.yes if r_switcharoo else response.no))
            + io.above**response.no
            + io.below**response.no
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_row1"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_row2"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_row3"]
            ** numbers[f"n{row + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_col1"]
            ** numbers[f"n{col}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_col2"]
            ** numbers[f"n{col + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_col3"]
            ** numbers[f"n{col}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_row1"]
            ** numbers[f"n{row + 1 - i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_row2"]
            ** numbers[f"n{row + 2 - i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_row3"]
            ** numbers[f"n{row + 3 - i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_col1"]
            ** numbers[f"n{col + 2 - (i == 0)}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_col2"]
            ** numbers[f"n{col + 2 - (i == 0)}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_col3"]
            ** numbers[f"n{col + 2 - (i == 0)}"]
            + 2.0
            * (
                io[f"target_{'half_T' if switcharoo else 'vertical'}"]
                ** response.reference
            )  # half_T isnt already there
            + 2.0
            * (
                io[f"target_{'vertical' if switcharoo else 'half_T'}"]
                ** response.latest
            )  # but vertical is
            - 2.0
            * (io[f"target_{'half_T' if switcharoo else 'vertical'}"] ** response.yes)
            - 2.0
            * (
                io[f"target_{'half_T' if switcharoo else 'vertical'}"]
                ** response.latest
            )
            - 2.0
            * (io[f"target_{'half_T' if switcharoo else 'vertical'}"] ** response.no)
            - 2.0
            * (io[f"target_{'vertical' if switcharoo else 'half_T'}"] ** response.yes)
            - 2.0
            * (
                io[f"target_{'vertical' if switcharoo else 'half_T'}"]
                ** response.reference
            )
            - 2.0
            * (io[f"target_{'vertical' if switcharoo else 'half_T'}"] ** response.no)
            >> +(io[f"target_{'vertical' if switcharoo else 'half_T'}"] ** response.yes)
            + io[f"target_{'half_T' if switcharoo else 'vertical'}"] ** response.yes
            + io[f"target_{'vertical' if switcharoo else 'half_T'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + 1 - i}"])
            + io[f"target_{'vertical' if switcharoo else 'half_T'}_row2"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + 2 - i}"])
            + io[f"target_{'vertical' if switcharoo else 'half_T'}_row3"]
            ** (
                numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + 3 - i}"]
            )
            + io[f"target_{'vertical' if switcharoo else 'half_T'}_col1"]
            ** (
                numbers[f"n{col}"]
                if not switcharoo
                else numbers[f"n{col + 2 - (i == 0)}"]
            )
            + io[f"target_{'vertical' if switcharoo else 'half_T'}_col2"]
            ** (
                numbers[f"n{col + 1}"]
                if not switcharoo
                else numbers[f"n{col + 2 - (i == 0)}"]
            )
            + io[f"target_{'vertical' if switcharoo else 'half_T'}_col3"]
            ** (
                numbers[f"n{col}"]
                if not switcharoo
                else numbers[f"n{col + 2 - (i == 0)}"]
            )
            + io.construction_signal**con_signal.continue_construction
        )
        for r_switcharoo in (True, False)
        for switcharoo in (True, False)
        for i in range(4)
        for row in range(1 + (i - 1 if i > 1 else 0), 4 + (math.ceil(i / 2)))
        for col in range(1, 6 - (i > 0))
    ]

    half_t_right_vertical_placement_rule = [
        (
            +(io.input_half_T**response.yes)
            + io.input_vertical**response.yes
            + io.start**response.no
            + (1.0 if r_switcharoo else 7.0)
            * (io.left ** (response.no if r_switcharoo else response.yes))
            - (1.0 if r_switcharoo else 7.0)
            * (io.left ** (response.yes if r_switcharoo else response.no))
            + (7.0 if r_switcharoo else 1.0)
            * (io.right ** (response.yes if r_switcharoo else response.no))
            - (7.0 if r_switcharoo else 1.0)
            * (io.right ** (response.no if r_switcharoo else response.yes))
            + io.above**response.no
            + io.below**response.no
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_row1"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_row2"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_row3"]
            ** numbers[f"n{row + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_col1"]
            ** numbers[f"n{col}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_col2"]
            ** numbers[f"n{col + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_col3"]
            ** numbers[f"n{col}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_row1"]
            ** numbers[f"n{row - 2 + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_row2"]
            ** numbers[f"n{row - 1 + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_row3"]
            ** numbers[f"n{row + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_col1"]
            ** numbers[f"n{col - 1}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_col2"]
            ** numbers[f"n{col - 1}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_col3"]
            ** numbers[f"n{col - 1}"]
            + 2.0
            * (
                io[f"target_{'half_T' if switcharoo else 'vertical'}"]
                ** response.reference
            )  # half_T isnt already there
            + 2.0
            * (
                io[f"target_{'vertical' if switcharoo else 'half_T'}"]
                ** response.latest
            )  # but vertical is
            - 2.0
            * (io[f"target_{'half_T' if switcharoo else 'vertical'}"] ** response.yes)
            - 2.0
            * (
                io[f"target_{'half_T' if switcharoo else 'vertical'}"]
                ** response.latest
            )
            - 2.0
            * (io[f"target_{'half_T' if switcharoo else 'vertical'}"] ** response.no)
            - 2.0
            * (io[f"target_{'vertical' if switcharoo else 'half_T'}"] ** response.yes)
            - 2.0
            * (
                io[f"target_{'vertical' if switcharoo else 'half_T'}"]
                ** response.reference
            )
            - 2.0
            * (io[f"target_{'vertical' if switcharoo else 'half_T'}"] ** response.no)
            >> +(io[f"target_{'half_T' if switcharoo else 'vertical'}"] ** response.yes)
            + io[f"target_{'vertical' if switcharoo else 'half_T'}"] ** response.yes
            + io[f"target_{'vertical' if switcharoo else 'half_T'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row - 2 + i}"])
            + io[f"target_{'vertical' if switcharoo else 'half_T'}_row2"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row - 1 + i}"])
            + io[f"target_{'vertical' if switcharoo else 'half_T'}_row3"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + i}"])
            + io[f"target_{'vertical' if switcharoo else 'half_T'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col - 1}"])
            + io[f"target_{'vertical' if switcharoo else 'half_T'}_col2"]
            ** (numbers[f"n{col + 1}"] if not switcharoo else numbers[f"n{col - 1}"])
            + io[f"target_{'vertical' if switcharoo else 'half_T'}_col3"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col - 1}"])
            + io.construction_signal**con_signal.continue_construction
        )
        for r_switcharoo in (True, False)
        for switcharoo in (True, False)
        for i in range(4)
        for row in range(max(1, 3 - i), 6 - max(0, i - 1))
        for col in range(2, 6)
    ]

    half_t_below_vertical_placement_rule = [
        (
            +(io.input_half_T**response.yes)
            + io.input_vertical**response.yes
            + io.start**response.no
            + io.left**response.no
            + io.right**response.no
            + (1.0 if r_switcharoo else 7.0)
            * (io.above ** (response.no if r_switcharoo else response.yes))
            - (1.0 if r_switcharoo else 7.0)
            * (io.above ** (response.yes if r_switcharoo else response.no))
            + (7.0 if r_switcharoo else 1.0)
            * (io.below ** (response.yes if r_switcharoo else response.no))
            - (7.0 if r_switcharoo else 1.0)
            * (io.below ** (response.no if r_switcharoo else response.yes))
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_row1"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_row2"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_row3"]
            ** numbers[f"n{row + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_col1"]
            ** numbers[f"n{col}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_col2"]
            ** numbers[f"n{col + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_col3"]
            ** numbers[f"n{col}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_row1"]
            ** numbers[f"n{row - 3}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_row2"]
            ** numbers[f"n{row - 2}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_row3"]
            ** numbers[f"n{row - 1}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_col1"]
            ** numbers[f"n{col + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_col2"]
            ** numbers[f"n{col + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_col3"]
            ** numbers[f"n{col + i}"]
            + 2.0
            * (
                io[f"target_{'half_T' if switcharoo else 'vertical'}"]
                ** response.reference
            )  # half_T isnt already there
            + 2.0
            * (
                io[f"target_{'vertical' if switcharoo else 'half_T'}"]
                ** response.latest
            )  # but vertical is
            - 2.0
            * (io[f"target_{'half_T' if switcharoo else 'vertical'}"] ** response.yes)
            - 2.0
            * (
                io[f"target_{'half_T' if switcharoo else 'vertical'}"]
                ** response.latest
            )
            - 2.0
            * (io[f"target_{'half_T' if switcharoo else 'vertical'}"] ** response.no)
            - 2.0
            * (io[f"target_{'vertical' if switcharoo else 'half_T'}"] ** response.yes)
            - 2.0
            * (
                io[f"target_{'vertical' if switcharoo else 'half_T'}"]
                ** response.reference
            )
            - 2.0
            * (io[f"target_{'vertical' if switcharoo else 'half_T'}"] ** response.no)
            >> +(io[f"target_{'half_T' if switcharoo else 'vertical'}"] ** response.yes)
            + io[f"target_{'vertical' if switcharoo else 'half_T'}"] ** response.yes
            + io[f"target_{'vertical' if switcharoo else 'half_T'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row - 3}"])
            + io[f"target_{'vertical' if switcharoo else 'half_T'}_row2"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row - 2}"])
            + io[f"target_{'vertical' if switcharoo else 'half_T'}_row3"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row - 1}"])
            + io[f"target_{'vertical' if switcharoo else 'half_T'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col + i}"])
            + io[f"target_{'vertical' if switcharoo else 'half_T'}_col2"]
            ** (numbers[f"n{col + 1}"] if not switcharoo else numbers[f"n{col + i}"])
            + io[f"target_{'vertical' if switcharoo else 'half_T'}_col3"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col + i}"])
            + io.construction_signal**con_signal.continue_construction
        )
        for r_switcharoo in (True, False)
        for switcharoo in (True, False)
        for i in range(2)
        for row in range(4, 6)
        for col in range(1, 6)
    ]

    half_t_above_vertical_placement_rule = [
        (
            +(io.input_half_T**response.yes)
            + io.input_vertical**response.yes
            + io.start**response.no
            + io.left**response.no
            + io.right**response.no
            + (7.0 if r_switcharoo else 1.0)
            * (io.above ** (response.yes if r_switcharoo else response.no))
            - (7.0 if r_switcharoo else 1.0)
            * (io.above ** (response.no if r_switcharoo else response.yes))
            + (1.0 if r_switcharoo else 7.0)
            * (io.below ** (response.no if r_switcharoo else response.yes))
            - (1.0 if r_switcharoo else 7.0)
            * (io.below ** (response.yes if r_switcharoo else response.no))
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_row1"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_row2"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_row3"]
            ** numbers[f"n{row + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_col1"]
            ** numbers[f"n{col}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_col2"]
            ** numbers[f"n{col + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_col3"]
            ** numbers[f"n{col}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_row1"]
            ** numbers[f"n{row + 1}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_row2"]
            ** numbers[f"n{row + 2}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_row3"]
            ** numbers[f"n{row + 3}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_col1"]
            ** numbers[f"n{col}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_col2"]
            ** numbers[f"n{col}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_col3"]
            ** numbers[f"n{col}"]
            + 2.0
            * (
                io[f"target_{'half_T' if switcharoo else 'vertical'}"]
                ** response.reference
            )  # half_T isnt already there
            + 2.0
            * (
                io[f"target_{'vertical' if switcharoo else 'half_T'}"]
                ** response.latest
            )  # but vertical is
            - 2.0
            * (io[f"target_{'half_T' if switcharoo else 'vertical'}"] ** response.yes)
            - 2.0
            * (
                io[f"target_{'half_T' if switcharoo else 'vertical'}"]
                ** response.latest
            )
            - 2.0
            * (io[f"target_{'half_T' if switcharoo else 'vertical'}"] ** response.no)
            - 2.0
            * (io[f"target_{'vertical' if switcharoo else 'half_T'}"] ** response.yes)
            - 2.0
            * (
                io[f"target_{'vertical' if switcharoo else 'half_T'}"]
                ** response.reference
            )
            - 2.0
            * (io[f"target_{'vertical' if switcharoo else 'half_T'}"] ** response.no)
            >> +(io[f"target_{'vertical' if switcharoo else 'half_T'}"] ** response.yes)
            + io[f"target_{'half_T' if switcharoo else 'vertical'}"] ** response.yes
            + io[f"target_{'vertical' if switcharoo else 'half_T'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + 1}"])
            + io[f"target_{'vertical' if switcharoo else 'half_T'}_row2"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + 2}"])
            + io[f"target_{'vertical' if switcharoo else 'half_T'}_row3"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + 3}"])
            + io[f"target_{'vertical' if switcharoo else 'half_T'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col}"])
            + io[f"target_{'vertical' if switcharoo else 'half_T'}_col2"]
            ** (numbers[f"n{col + 1}"] if not switcharoo else numbers[f"n{col}"])
            + io[f"target_{'vertical' if switcharoo else 'half_T'}_col3"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col}"])
            + io.construction_signal**con_signal.continue_construction
        )
        for r_switcharoo in (True, False)
        for switcharoo in (True, False)
        for row in range(1, 3)
        for col in range(1, 6)
    ]

    half_t_left_mirror_l_placement_rule = [
        (
            +(io.input_half_T**response.yes)
            + io.input_mirror_L**response.yes
            + io.start**response.no
            + (7.0 if r_switcharoo else 1.0)
            * (io.left ** (response.yes if r_switcharoo else response.no))
            - (7.0 if r_switcharoo else 1.0)
            * (io.left ** (response.no if r_switcharoo else response.yes))
            + (1.0 if r_switcharoo else 7.0)
            * (io.right ** (response.no if r_switcharoo else response.yes))
            - (1.0 if r_switcharoo else 7.0)
            * (io.right ** (response.yes if r_switcharoo else response.no))
            + io.above**response.no
            + io.below**response.no
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_row1"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_row2"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_row3"]
            ** numbers[f"n{row + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_col1"]
            ** numbers[f"n{col}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_col2"]
            ** numbers[f"n{col + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_col3"]
            ** numbers[f"n{col}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_mirror_L_row1"]
            ** numbers[f"n{row - i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_mirror_L_row2"]
            ** numbers[f"n{row + 1 - i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_mirror_L_row3"]
            ** numbers[f"n{row + 1 - i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_mirror_L_col1"]
            ** numbers[f"n{col + 2 + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_mirror_L_col2"]
            ** numbers[f"n{col + 1 + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_mirror_L_col3"]
            ** numbers[f"n{col + 2 + i}"]
            + 2.0
            * (
                io[f"target_{'half_T' if switcharoo else 'mirror_L'}"]
                ** response.reference
            )  # half_T isnt already there
            + 2.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'half_T'}"]
                ** response.latest
            )  # but mirror_L is
            - 2.0
            * (io[f"target_{'half_T' if switcharoo else 'mirror_L'}"] ** response.yes)
            - 2.0
            * (
                io[f"target_{'half_T' if switcharoo else 'mirror_L'}"]
                ** response.latest
            )
            - 2.0
            * (io[f"target_{'half_T' if switcharoo else 'mirror_L'}"] ** response.no)
            - 2.0
            * (io[f"target_{'mirror_L' if switcharoo else 'half_T'}"] ** response.yes)
            - 2.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'half_T'}"]
                ** response.reference
            )
            - 2.0
            * (io[f"target_{'mirror_L' if switcharoo else 'half_T'}"] ** response.no)
            >> +(io[f"target_{'mirror_L' if switcharoo else 'half_T'}"] ** response.yes)
            + io[f"target_{'half_T' if switcharoo else 'mirror_L'}"] ** response.yes
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row - i}"])
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_row2"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + 1 - i}"])
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_row3"]
            ** (
                numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + 1 - i}"]
            )
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col + 2 + i}"])
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_col2"]
            ** (
                numbers[f"n{col + 1}"] if not switcharoo else numbers[f"n{col + 1 + i}"]
            )
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_col3"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col + 2 + i}"])
            + io.construction_signal**con_signal.continue_construction
        )
        for r_switcharoo in (True, False)
        for switcharoo in (True, False)
        for i in range(2)
        for row in range(1 + i, 6)
        for col in range(1, 5 - i)
    ]

    half_t_right_mirror_l_placement_rule = [
        (
            +(io.input_half_T**response.yes)
            + io.input_mirror_L**response.yes
            + io.start**response.no
            + (1.0 if r_switcharoo else 7.0)
            * (io.left ** (response.no if r_switcharoo else response.yes))
            - (1.0 if r_switcharoo else 7.0)
            * (io.left ** (response.yes if r_switcharoo else response.no))
            + (7.0 if r_switcharoo else 1.0)
            * (io.right ** (response.yes if r_switcharoo else response.no))
            - (7.0 if r_switcharoo else 1.0)
            * (io.right ** (response.no if r_switcharoo else response.yes))
            + io.above**response.no
            + io.below**response.no
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_row1"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_row2"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_row3"]
            ** numbers[f"n{row + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_col1"]
            ** numbers[f"n{col}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_col2"]
            ** numbers[f"n{col + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_col3"]
            ** numbers[f"n{col}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_mirror_L_row1"]
            ** numbers[
                f"n{row + (-1 if i == 0 else 1) * (i % 2 == 0)}"
            ]  # 1 up, no up, 1 down.
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_mirror_L_row2"]
            ** numbers[f"n{row + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_mirror_L_row3"]
            ** numbers[f"n{row + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_mirror_L_col1"]
            ** numbers[f"n{col - 1}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_mirror_L_col2"]
            ** numbers[f"n{col - 2}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_mirror_L_col3"]
            ** numbers[f"n{col - 1}"]
            + 2.0
            * (
                io[f"target_{'half_T' if switcharoo else 'mirror_L'}"]
                ** response.reference
            )  # half_T isnt already there
            + 2.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'half_T'}"]
                ** response.latest
            )  # but mirror_L is
            - 2.0
            * (io[f"target_{'half_T' if switcharoo else 'mirror_L'}"] ** response.yes)
            - 2.0
            * (
                io[f"target_{'half_T' if switcharoo else 'mirror_L'}"]
                ** response.latest
            )
            - 2.0
            * (io[f"target_{'half_T' if switcharoo else 'mirror_L'}"] ** response.no)
            - 2.0
            * (io[f"target_{'mirror_L' if switcharoo else 'half_T'}"] ** response.yes)
            - 2.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'half_T'}"]
                ** response.reference
            )
            - 2.0
            * (io[f"target_{'mirror_L' if switcharoo else 'half_T'}"] ** response.no)
            >> +(io[f"target_{'mirror_L' if switcharoo else 'half_T'}"] ** response.yes)
            + io[f"target_{'half_T' if switcharoo else 'mirror_L'}"] ** response.yes
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_row1"]
            ** (
                numbers[f"n{row}"]
                if not switcharoo
                else numbers[f"n{row + (-1 if i == 0 else 1) * (i % 2 == 0)}"]
            )
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_row2"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + i}"])
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_row3"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + i}"])
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col - 1}"])
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_col2"]
            ** (numbers[f"n{col + 1}"] if not switcharoo else numbers[f"n{col - 2}"])
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_col3"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col - 1}"])
            + io.construction_signal**con_signal.continue_construction
        )
        for r_switcharoo in (True, False)
        for switcharoo in (True, False)
        for i in range(3)
        for row in range(1 + (i == 0), 6 - (i == 2))
        for col in range(3, 6)
    ]

    half_t_below_mirror_l_placement_rule = [
        (
            +(io.input_half_T**response.yes)
            + io.input_mirror_L**response.yes
            + io.start**response.no
            + io.left**response.no
            + io.right**response.no
            + (1.0 if r_switcharoo else 7.0)
            * (io.above ** (response.no if r_switcharoo else response.yes))
            - (1.0 if r_switcharoo else 7.0)
            * (io.above ** (response.yes if r_switcharoo else response.no))
            + (7.0 if r_switcharoo else 1.0)
            * (io.below ** (response.yes if r_switcharoo else response.no))
            - (7.0 if r_switcharoo else 1.0)
            * (io.below ** (response.no if r_switcharoo else response.yes))
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_row1"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_row2"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_row3"]
            ** numbers[f"n{row + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_col1"]
            ** numbers[f"n{col}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_col2"]
            ** numbers[f"n{col + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_col3"]
            ** numbers[f"n{col}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_mirror_L_row1"]
            ** numbers[f"n{row - 2}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_mirror_L_row2"]
            ** numbers[f"n{row - 1}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_mirror_L_row3"]
            ** numbers[f"n{row - 1}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_mirror_L_col1"]
            ** numbers[f"n{col + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_mirror_L_col2"]
            ** numbers[f"n{col - 1 + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_mirror_L_col3"]
            ** numbers[f"n{col + i}"]
            + 2.0
            * (
                io[f"target_{'half_T' if switcharoo else 'mirror_L'}"]
                ** response.reference
            )  # half_T isnt already there
            + 2.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'half_T'}"]
                ** response.latest
            )  # but mirror_L is
            - 2.0
            * (io[f"target_{'half_T' if switcharoo else 'mirror_L'}"] ** response.yes)
            - 2.0
            * (
                io[f"target_{'half_T' if switcharoo else 'mirror_L'}"]
                ** response.latest
            )
            - 2.0
            * (io[f"target_{'half_T' if switcharoo else 'mirror_L'}"] ** response.no)
            - 2.0
            * (io[f"target_{'mirror_L' if switcharoo else 'half_T'}"] ** response.yes)
            - 2.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'half_T'}"]
                ** response.reference
            )
            - 2.0
            * (io[f"target_{'mirror_L' if switcharoo else 'half_T'}"] ** response.no)
            >> +(io[f"target_{'mirror_L' if switcharoo else 'half_T'}"] ** response.yes)
            + io[f"target_{'half_T' if switcharoo else 'mirror_L'}"] ** response.yes
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row - 2}"])
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_row2"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row - 1}"])
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_row3"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row - 1}"])
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col + i}"])
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_col2"]
            ** (
                numbers[f"n{col + 1}"] if not switcharoo else numbers[f"n{col - 1 + i}"]
            )
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_col3"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col + i}"])
            + io.construction_signal**con_signal.continue_construction
        )
        for r_switcharoo in (True, False)
        for switcharoo in (True, False)
        for i in range(3)
        for row in range(3, 6)
        for col in range(1 + (i == 0), 6 - (i == 2))
    ]

    half_t_above_mirror_l_placement_rule = [
        (
            +(io.input_half_T**response.yes)
            + io.input_mirror_L**response.yes
            + io.start**response.no
            + io.left**response.no
            + io.right**response.no
            + (7.0 if r_switcharoo else 1.0)
            * (io.above ** (response.yes if r_switcharoo else response.no))
            - (7.0 if r_switcharoo else 1.0)
            * (io.above ** (response.no if r_switcharoo else response.yes))
            + (1.0 if r_switcharoo else 7.0)
            * (io.below ** (response.no if r_switcharoo else response.yes))
            - (1.0 if r_switcharoo else 7.0)
            * (io.below ** (response.yes if r_switcharoo else response.no))
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_row1"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_row2"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_row3"]
            ** numbers[f"n{row + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_col1"]
            ** numbers[f"n{col}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_col2"]
            ** numbers[f"n{col + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_half_T_col3"]
            ** numbers[f"n{col}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_mirror_L_row1"]
            ** numbers[f"n{row + 2}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_mirror_L_row2"]
            ** numbers[f"n{row + 3}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_mirror_L_row3"]
            ** numbers[f"n{row + 3}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_mirror_L_col1"]
            ** numbers[f"n{col}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_mirror_L_col2"]
            ** numbers[f"n{col - 1}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_mirror_L_col3"]
            ** numbers[f"n{col}"]
            + 2.0
            * (
                io[f"target_{'half_T' if switcharoo else 'mirror_L'}"]
                ** response.reference
            )  # half_T isnt already there
            + 2.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'half_T'}"]
                ** response.latest
            )  # but mirror_L is
            - 2.0
            * (io[f"target_{'half_T' if switcharoo else 'mirror_L'}"] ** response.yes)
            - 2.0
            * (
                io[f"target_{'half_T' if switcharoo else 'mirror_L'}"]
                ** response.latest
            )
            - 2.0
            * (io[f"target_{'half_T' if switcharoo else 'mirror_L'}"] ** response.no)
            - 2.0
            * (io[f"target_{'mirror_L' if switcharoo else 'half_T'}"] ** response.yes)
            - 2.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'half_T'}"]
                ** response.reference
            )
            - 2.0
            * (io[f"target_{'mirror_L' if switcharoo else 'half_T'}"] ** response.no)
            >> +(io[f"target_{'mirror_L' if switcharoo else 'half_T'}"] ** response.yes)
            + io[f"target_{'half_T' if switcharoo else 'mirror_L'}"] ** response.yes
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + 2}"])
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_row2"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + 3}"])
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_row3"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + 3}"])
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col}"])
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_col2"]
            ** (numbers[f"n{col + 1}"] if not switcharoo else numbers[f"n{col - 1}"])
            + io[f"target_{'mirror_L' if switcharoo else 'half_T'}_col3"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col}"])
            + io.construction_signal**con_signal.continue_construction
        )
        for r_switcharoo in (True, False)
        for switcharoo in (True, False)
        for row in range(1, 4)
        for col in range(2, 6)
    ]

    mirror_l_left_horizontal_placement_rule = [
        (
            +(io.input_mirror_L**response.yes)
            + io.input_horizontal**response.yes
            + io.start**response.no
            + (7.0 if r_switcharoo else 1.0)
            * (io.left ** (response.yes if r_switcharoo else response.no))
            - (7.0 if r_switcharoo else 1.0)
            * (io.left ** (response.no if r_switcharoo else response.yes))
            + (1.0 if r_switcharoo else 7.0)
            * (io.right ** (response.no if r_switcharoo else response.yes))
            - (1.0 if r_switcharoo else 7.0)
            * (io.right ** (response.yes if r_switcharoo else response.no))
            + io.above**response.no
            + io.below**response.no
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_row1"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_row2"]
            ** numbers[f"n{row + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_row3"]
            ** numbers[f"n{row + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_col1"]
            ** numbers[f"n{col}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_col2"]
            ** numbers[f"n{col - 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_col3"]
            ** numbers[f"n{col}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_row1"]
            ** numbers[f"n{row + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_row2"]
            ** numbers[f"n{row + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_row3"]
            ** numbers[f"n{row + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_col1"]
            ** numbers[f"n{col + 1}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_col2"]
            ** numbers[f"n{col + 2}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_col3"]
            ** numbers[f"n{col + 3}"]
            + 2.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"]
                ** response.reference
            )  # mirror_L isnt already there
            + 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"]
                ** response.latest
            )  # but horizontal is
            - 2.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"]
                ** response.yes
            )
            - 2.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"]
                ** response.latest
            )
            - 2.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"]
                ** response.no
            )
            - 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"]
                ** response.yes
            )
            - 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"]
                ** response.reference
            )
            - 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"]
                ** response.no
            )
            >> +(
                io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"]
                ** response.yes
            )
            + io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"] ** response.yes
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + i}"])
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_row2"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + i}"])
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_row3"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + i}"])
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col + 1}"])
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_col2"]
            ** (numbers[f"n{col - 1}"] if not switcharoo else numbers[f"n{col + 2}"])
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_col3"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col + 3}"])
            + io.construction_signal**con_signal.continue_construction
        )
        for r_switcharoo in (True, False)
        for switcharoo in (True, False)
        for i in range(2)
        for row in range(1, 6)
        for col in range(2, 4)
    ]

    mirror_l_right_horizontal_placement_rule = [
        (
            +(io.input_mirror_L**response.yes)
            + io.input_horizontal**response.yes
            + io.start**response.no
            + (1.0 if r_switcharoo else 7.0)
            * (io.left ** (response.no if r_switcharoo else response.yes))
            - (1.0 if r_switcharoo else 7.0)
            * (io.left ** (response.yes if r_switcharoo else response.no))
            + (7.0 if r_switcharoo else 1.0)
            * (io.right ** (response.yes if r_switcharoo else response.no))
            - (7.0 if r_switcharoo else 1.0)
            * (io.right ** (response.no if r_switcharoo else response.yes))
            + io.above**response.no
            + io.below**response.no
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_row1"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_row2"]
            ** numbers[f"n{row + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_row3"]
            ** numbers[f"n{row + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_col1"]
            ** numbers[f"n{col}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_col2"]
            ** numbers[f"n{col - 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_col3"]
            ** numbers[f"n{col}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_row1"]
            ** numbers[f"n{row + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_row2"]
            ** numbers[f"n{row + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_row3"]
            ** numbers[f"n{row + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_col1"]
            ** numbers[f"n{col - 3 - i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_col2"]
            ** numbers[f"n{col - 2 - i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_col3"]
            ** numbers[f"n{col - 1 - i}"]
            + 2.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"]
                ** response.reference
            )  # mirror_L isnt already there
            + 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"]
                ** response.latest
            )  # but horizontal is
            - 2.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"]
                ** response.yes
            )
            - 2.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"]
                ** response.latest
            )
            - 2.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"]
                ** response.no
            )
            - 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"]
                ** response.yes
            )
            - 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"]
                ** response.reference
            )
            - 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"]
                ** response.no
            )
            >> +(
                io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"]
                ** response.yes
            )
            + io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"] ** response.yes
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + i}"])
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_row2"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + i}"])
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_row3"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + i}"])
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col - 3 - i}"])
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_col2"]
            ** (
                numbers[f"n{col - 1}"] if not switcharoo else numbers[f"n{col - 2 - i}"]
            )
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_col3"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col - 1 - i}"])
            + io.construction_signal**con_signal.continue_construction
        )
        for r_switcharoo in (True, False)
        for switcharoo in (True, False)
        for i in range(2)
        for row in range(1, 6)
        for col in range(4 + i, 7)
    ]

    mirror_l_above_horizontal_placement_rule = [
        (
            +(io.input_mirror_L**response.yes)
            + io.input_horizontal**response.yes
            + io.start**response.no
            + io.left**response.no
            + io.right**response.no
            + (7.0 if r_switcharoo else 1.0)
            * (io.above ** (response.yes if r_switcharoo else response.no))
            - (7.0 if r_switcharoo else 1.0)
            * (io.above ** (response.no if r_switcharoo else response.yes))
            + (1.0 if r_switcharoo else 7.0)
            * (io.below ** (response.no if r_switcharoo else response.yes))
            - (1.0 if r_switcharoo else 7.0)
            * (io.below ** (response.yes if r_switcharoo else response.no))
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_row1"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_row2"]
            ** numbers[f"n{row + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_row3"]
            ** numbers[f"n{row + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_col1"]
            ** numbers[f"n{col}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_col2"]
            ** numbers[f"n{col - 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_col3"]
            ** numbers[f"n{col}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_row1"]
            ** numbers[f"n{row + 2}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_row2"]
            ** numbers[f"n{row + 2}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_row3"]
            ** numbers[f"n{row + 2}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_col1"]
            ** numbers[f"n{col - 3 + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_col2"]
            ** numbers[f"n{col - 2 + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_col3"]
            ** numbers[f"n{col - 1 + i}"]
            + 2.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"]
                ** response.reference
            )  # mirror_L isnt already there
            + 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"]
                ** response.latest
            )  # but horizontal is
            - 2.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"]
                ** response.yes
            )
            - 2.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"]
                ** response.latest
            )
            - 2.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"]
                ** response.no
            )
            - 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"]
                ** response.yes
            )
            - 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"]
                ** response.reference
            )
            - 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"]
                ** response.no
            )
            >> +(
                io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"]
                ** response.yes
            )
            + io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"] ** response.yes
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + 2}"])
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_row2"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + 2}"])
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_row3"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + 2}"])
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col - 3 + i}"])
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_col2"]
            ** (
                numbers[f"n{col - 1}"] if not switcharoo else numbers[f"n{col - 2 + i}"]
            )
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_col3"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col - 1 + i}"])
            + io.construction_signal**con_signal.continue_construction
        )
        for r_switcharoo in (True, False)
        for switcharoo in (True, False)
        for i in range(4)
        for row in range(1, 5)
        for col in range((4 - i if i < 2 else 2), 7 - (i - 1 if i >= 2 else 0))
    ]

    mirror_l_below_horizontal_placement_rule = [
        (
            +(io.input_mirror_L**response.yes)
            + io.input_horizontal**response.yes
            + io.start**response.no
            + io.left**response.no
            + io.right**response.no
            + (1.0 if r_switcharoo else 7.0)
            * (io.above ** (response.no if r_switcharoo else response.yes))
            - (1.0 if r_switcharoo else 7.0)
            * (io.above ** (response.yes if r_switcharoo else response.no))
            + (7.0 if r_switcharoo else 1.0)
            * (io.below ** (response.yes if r_switcharoo else response.no))
            - (7.0 if r_switcharoo else 1.0)
            * (io.below ** (response.no if r_switcharoo else response.yes))
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_row1"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_row2"]
            ** numbers[f"n{row + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_row3"]
            ** numbers[f"n{row + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_col1"]
            ** numbers[f"n{col}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_col2"]
            ** numbers[f"n{col - 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_col3"]
            ** numbers[f"n{col}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_row1"]
            ** numbers[f"n{row - 1}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_row2"]
            ** numbers[f"n{row - 1}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_row3"]
            ** numbers[f"n{row - 1}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_col1"]
            ** numbers[f"n{col - 2 + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_col2"]
            ** numbers[f"n{col - 1 + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_horizontal_col3"]
            ** numbers[f"n{col + i}"]
            + 2.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"]
                ** response.reference
            )  # mirror_L isnt already there
            + 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"]
                ** response.latest
            )  # but horizontal is
            - 2.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"]
                ** response.yes
            )
            - 2.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"]
                ** response.latest
            )
            - 2.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"]
                ** response.no
            )
            - 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"]
                ** response.yes
            )
            - 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"]
                ** response.reference
            )
            - 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"]
                ** response.no
            )
            >> +(
                io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"]
                ** response.yes
            )
            + io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"] ** response.yes
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row - 1}"])
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_row2"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row - 1}"])
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_row3"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row - 1}"])
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col - 2 + i}"])
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_col2"]
            ** (
                numbers[f"n{col - 1}"] if not switcharoo else numbers[f"n{col - 1 + i}"]
            )
            + io[f"target_{'horizontal' if switcharoo else 'mirror_L'}_col3"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col + i}"])
            + io.construction_signal**con_signal.continue_construction
        )
        for r_switcharoo in (True, False)
        for switcharoo in (True, False)
        for i in range(3)
        for row in range(2, 6)
        for col in range(3 - (i != 0), 7 - i)
    ]

    mirror_l_left_vertical_placement_rule = [
        (
            +(io.input_mirror_L**response.yes)
            + io.input_vertical**response.yes
            + io.start**response.no
            + (7.0 if r_switcharoo else 1.0)
            * (io.left ** (response.yes if r_switcharoo else response.no))
            - (7.0 if r_switcharoo else 1.0)
            * (io.left ** (response.no if r_switcharoo else response.yes))
            + (1.0 if r_switcharoo else 7.0)
            * (io.right ** (response.no if r_switcharoo else response.yes))
            - (1.0 if r_switcharoo else 7.0)
            * (io.right ** (response.yes if r_switcharoo else response.no))
            + io.above**response.no
            + io.below**response.no
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_row1"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_row2"]
            ** numbers[f"n{row + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_row3"]
            ** numbers[f"n{row + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_col1"]
            ** numbers[f"n{col}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_col2"]
            ** numbers[f"n{col - 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_col3"]
            ** numbers[f"n{col}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_row1"]
            ** numbers[f"n{row - 2 + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_row2"]
            ** numbers[f"n{row - 1 + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_row3"]
            ** numbers[f"n{row + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_col1"]
            ** numbers[f"n{col + 1}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_col2"]
            ** numbers[f"n{col + 1}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_col3"]
            ** numbers[f"n{col + 1}"]
            + 2.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'vertical'}"]
                ** response.reference
            )  # mirror_L isnt already there
            + 2.0
            * (
                io[f"target_{'vertical' if switcharoo else 'mirror_L'}"]
                ** response.latest
            )  # but vertical is
            - 2.0
            * (io[f"target_{'mirror_L' if switcharoo else 'vertical'}"] ** response.yes)
            - 2.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'vertical'}"]
                ** response.latest
            )
            - 2.0
            * (io[f"target_{'mirror_L' if switcharoo else 'vertical'}"] ** response.no)
            - 2.0
            * (io[f"target_{'vertical' if switcharoo else 'mirror_L'}"] ** response.yes)
            - 2.0
            * (
                io[f"target_{'vertical' if switcharoo else 'mirror_L'}"]
                ** response.reference
            )
            - 2.0
            * (io[f"target_{'vertical' if switcharoo else 'mirror_L'}"] ** response.no)
            >> +(
                io[f"target_{'vertical' if switcharoo else 'mirror_L'}"] ** response.yes
            )
            + io[f"target_{'mirror_L' if switcharoo else 'vertical'}"] ** response.yes
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row - 2 + i}"])
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_row2"]
            ** (
                numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row - 1 + i}"]
            )
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_row3"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + i}"])
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col + 1}"])
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_col2"]
            ** (numbers[f"n{col - 1}"] if not switcharoo else numbers[f"n{col + 1}"])
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_col3"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col + 1}"])
            + io.construction_signal**con_signal.continue_construction
        )
        for r_switcharoo in (True, False)
        for switcharoo in (True, False)
        for i in range(4)
        for row in range(max(3 - i, 1), 6 - (0 if i < 2 else i - 1))
        for col in range(2, 6)
    ]

    mirror_l_right_vertical_placement_rule = [
        (
            +(io.input_mirror_L**response.yes)
            + io.input_vertical**response.yes
            + io.start**response.no
            + (1.0 if r_switcharoo else 7.0)
            * (io.left ** (response.no if r_switcharoo else response.yes))
            - (1.0 if r_switcharoo else 7.0)
            * (io.left ** (response.yes if r_switcharoo else response.no))
            + (7.0 if r_switcharoo else 1.0)
            * (io.right ** (response.yes if r_switcharoo else response.no))
            - (7.0 if r_switcharoo else 1.0)
            * (io.right ** (response.no if r_switcharoo else response.yes))
            + io.above**response.no
            + io.below**response.no
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_row1"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_row2"]
            ** numbers[f"n{row + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_row3"]
            ** numbers[f"n{row + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_col1"]
            ** numbers[f"n{col}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_col2"]
            ** numbers[f"n{col - 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_col3"]
            ** numbers[f"n{col}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_row1"]
            ** numbers[f"n{row + 1 - i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_row2"]
            ** numbers[f"n{row + 2 - i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_row3"]
            ** numbers[f"n{row + 3 - i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_col1"]
            ** numbers[f"n{col - 2 + (i == 3)}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_col2"]
            ** numbers[f"n{col - 2 + (i == 3)}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_col3"]
            ** numbers[f"n{col - 2 + (i == 3)}"]
            + 2.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'vertical'}"]
                ** response.reference
            )  # mirror_L isnt already there
            + 2.0
            * (
                io[f"target_{'vertical' if switcharoo else 'mirror_L'}"]
                ** response.latest
            )  # but vertical is
            - 2.0
            * (io[f"target_{'mirror_L' if switcharoo else 'vertical'}"] ** response.yes)
            - 2.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'vertical'}"]
                ** response.latest
            )
            - 2.0
            * (io[f"target_{'mirror_L' if switcharoo else 'vertical'}"] ** response.no)
            - 2.0
            * (io[f"target_{'vertical' if switcharoo else 'mirror_L'}"] ** response.yes)
            - 2.0
            * (
                io[f"target_{'vertical' if switcharoo else 'mirror_L'}"]
                ** response.reference
            )
            - 2.0
            * (io[f"target_{'vertical' if switcharoo else 'mirror_L'}"] ** response.no)
            >> +(
                io[f"target_{'vertical' if switcharoo else 'mirror_L'}"] ** response.yes
            )
            + io[f"target_{'mirror_L' if switcharoo else 'vertical'}"] ** response.yes
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + 1 - i}"])
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_row2"]
            ** (
                numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + 2 - i}"]
            )
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_row3"]
            ** (
                numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + 3 - i}"]
            )
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_col1"]
            ** (
                numbers[f"n{col}"]
                if not switcharoo
                else numbers[f"n{col - 2 + (i == 3)}"]
            )
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_col2"]
            ** (
                numbers[f"n{col - 1}"]
                if not switcharoo
                else numbers[f"n{col - 2 + (i == 3)}"]
            )
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_col3"]
            ** (
                numbers[f"n{col}"]
                if not switcharoo
                else numbers[f"n{col - 2 + (i == 3)}"]
            )
            + io.construction_signal**con_signal.continue_construction
        )
        for r_switcharoo in (True, False)
        for switcharoo in (True, False)
        for i in range(4)
        for row in range(1 + max(0, i - 1), min(4 + i, 6))
        for col in range(3 - (i == 3), 7)
    ]

    mirror_l_above_vertical_placement_rule = [
        (
            +(io.input_mirror_L**response.yes)
            + io.input_vertical**response.yes
            + io.start**response.no
            + io.left**response.no
            + io.right**response.no
            + (7.0 if r_switcharoo else 1.0)
            * (io.above ** (response.yes if r_switcharoo else response.no))
            - (7.0 if r_switcharoo else 1.0)
            * (io.above ** (response.no if r_switcharoo else response.yes))
            + (1.0 if r_switcharoo else 7.0)
            * (io.below ** (response.no if r_switcharoo else response.yes))
            - (1.0 if r_switcharoo else 7.0)
            * (io.below ** (response.yes if r_switcharoo else response.no))
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_row1"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_row2"]
            ** numbers[f"n{row + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_row3"]
            ** numbers[f"n{row + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_col1"]
            ** numbers[f"n{col}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_col2"]
            ** numbers[f"n{col - 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_col3"]
            ** numbers[f"n{col}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_row1"]
            ** numbers[f"n{row + 2}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_row2"]
            ** numbers[f"n{row + 3}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_row3"]
            ** numbers[f"n{row + 4}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_col1"]
            ** numbers[f"n{col - 1 + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_col2"]
            ** numbers[f"n{col - 1 + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_col3"]
            ** numbers[f"n{col - 1 + i}"]
            + 2.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'vertical'}"]
                ** response.reference
            )  # mirror_L isnt already there
            + 2.0
            * (
                io[f"target_{'vertical' if switcharoo else 'mirror_L'}"]
                ** response.latest
            )  # but vertical is
            - 2.0
            * (io[f"target_{'mirror_L' if switcharoo else 'vertical'}"] ** response.yes)
            - 2.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'vertical'}"]
                ** response.latest
            )
            - 2.0
            * (io[f"target_{'mirror_L' if switcharoo else 'vertical'}"] ** response.no)
            - 2.0
            * (io[f"target_{'vertical' if switcharoo else 'mirror_L'}"] ** response.yes)
            - 2.0
            * (
                io[f"target_{'vertical' if switcharoo else 'mirror_L'}"]
                ** response.reference
            )
            - 2.0
            * (io[f"target_{'vertical' if switcharoo else 'mirror_L'}"] ** response.no)
            >> +(
                io[f"target_{'vertical' if switcharoo else 'mirror_L'}"] ** response.yes
            )
            + io[f"target_{'mirror_L' if switcharoo else 'vertical'}"] ** response.yes
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + 2}"])
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_row2"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + 3}"])
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_row3"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row + 4}"])
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col - 1 + i}"])
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_col2"]
            ** (
                numbers[f"n{col - 1}"] if not switcharoo else numbers[f"n{col - 1 + i}"]
            )
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_col3"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col - 1 + i}"])
            + io.construction_signal**con_signal.continue_construction
        )
        for r_switcharoo in (True, False)
        for switcharoo in (True, False)
        for i in range(2)
        for row in range(1, 3)
        for col in range(2, 7)
    ]

    mirror_l_below_vertical_placement_rule = [
        (
            +(io.input_mirror_L**response.yes)
            + io.input_vertical**response.yes
            + io.start**response.no
            + io.left**response.no
            + io.right**response.no
            + (1.0 if r_switcharoo else 7.0)
            * (io.above ** (response.no if r_switcharoo else response.yes))
            - (1.0 if r_switcharoo else 7.0)
            * (io.above ** (response.yes if r_switcharoo else response.no))
            + (7.0 if r_switcharoo else 1.0)
            * (io.below ** (response.yes if r_switcharoo else response.no))
            - (7.0 if r_switcharoo else 1.0)
            * (io.below ** (response.no if r_switcharoo else response.yes))
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_row1"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_row2"]
            ** numbers[f"n{row + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_row3"]
            ** numbers[f"n{row + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_col1"]
            ** numbers[f"n{col}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_col2"]
            ** numbers[f"n{col - 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_mirror_L_col3"]
            ** numbers[f"n{col}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_row1"]
            ** numbers[f"n{row - 3}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_row2"]
            ** numbers[f"n{row - 2}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_row3"]
            ** numbers[f"n{row - 1}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_col1"]
            ** numbers[f"n{col}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_col2"]
            ** numbers[f"n{col}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_col3"]
            ** numbers[f"n{col}"]
            + 2.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'vertical'}"]
                ** response.reference
            )  # mirror_L isnt already there
            + 2.0
            * (
                io[f"target_{'vertical' if switcharoo else 'mirror_L'}"]
                ** response.latest
            )  # but vertical is
            - 2.0
            * (io[f"target_{'mirror_L' if switcharoo else 'vertical'}"] ** response.yes)
            - 2.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'vertical'}"]
                ** response.latest
            )
            - 2.0
            * (io[f"target_{'mirror_L' if switcharoo else 'vertical'}"] ** response.no)
            - 2.0
            * (io[f"target_{'vertical' if switcharoo else 'mirror_L'}"] ** response.yes)
            - 2.0
            * (
                io[f"target_{'vertical' if switcharoo else 'mirror_L'}"]
                ** response.reference
            )
            - 2.0
            * (io[f"target_{'vertical' if switcharoo else 'mirror_L'}"] ** response.no)
            >> +(
                io[f"target_{'vertical' if switcharoo else 'mirror_L'}"] ** response.yes
            )
            + io[f"target_{'mirror_L' if switcharoo else 'vertical'}"] ** response.yes
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row - 3}"])
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_row2"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row - 2}"])
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_row3"]
            ** (numbers[f"n{row + 1}"] if not switcharoo else numbers[f"n{row - 1}"])
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col}"])
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_col2"]
            ** (numbers[f"n{col - 1}"] if not switcharoo else numbers[f"n{col}"])
            + io[f"target_{'vertical' if switcharoo else 'mirror_L'}_col3"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col}"])
            + io.construction_signal**con_signal.continue_construction
        )
        for r_switcharoo in (True, False)
        for switcharoo in (True, False)
        for row in range(4, 6)
        for col in range(2, 7)
    ]

    horizontal_left_vertical_placement_rule = [
        (
            +(io.input_vertical**response.yes)
            + io.input_horizontal**response.yes
            + io.start**response.no
            + (7.0 if r_switcharoo else 1.0)
            * (io.left ** (response.yes if r_switcharoo else response.no))
            - (7.0 if r_switcharoo else 1.0)
            * (io.left ** (response.no if r_switcharoo else response.yes))
            + (1.0 if r_switcharoo else 7.0)
            * (io.right ** (response.no if r_switcharoo else response.yes))
            - (1.0 if r_switcharoo else 7.0)
            * (io.right ** (response.yes if r_switcharoo else response.no))
            + io.above**response.no
            + io.below**response.no
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_horizontal_row1"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_horizontal_row2"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_horizontal_row3"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_horizontal_col1"]
            ** numbers[f"n{col}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_horizontal_col2"]
            ** numbers[f"n{col + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_horizontal_col3"]
            ** numbers[f"n{col + 2}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_row1"]
            ** numbers[f"n{row - 2 + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_row2"]
            ** numbers[f"n{row - 1 + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_row3"]
            ** numbers[f"n{row + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_col1"]
            ** numbers[f"n{col + 3}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_col2"]
            ** numbers[f"n{col + 3}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_col3"]
            ** numbers[f"n{col + 3}"]
            + 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'vertical'}"]
                ** response.reference
            )  # horizontal isnt already there
            + 2.0
            * (
                io[f"target_{'vertical' if switcharoo else 'horizontal'}"]
                ** response.latest
            )  # but vertical is
            - 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'vertical'}"]
                ** response.yes
            )
            - 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'vertical'}"]
                ** response.latest
            )
            - 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'vertical'}"]
                ** response.no
            )
            - 2.0
            * (
                io[f"target_{'vertical' if switcharoo else 'horizontal'}"]
                ** response.yes
            )
            - 2.0
            * (
                io[f"target_{'vertical' if switcharoo else 'horizontal'}"]
                ** response.reference
            )
            - 2.0
            * (
                io[f"target_{'vertical' if switcharoo else 'horizontal'}"]
                ** response.no
            )
            >> +(
                io[f"target_{'vertical' if switcharoo else 'horizontal'}"]
                ** response.yes
            )
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}"] ** response.yes
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row - 2 + i}"])
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_row2"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row - 1 + i}"])
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_row3"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + i}"])
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col + 3}"])
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_col2"]
            ** (numbers[f"n{col + 1}"] if not switcharoo else numbers[f"n{col + 3}"])
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_col3"]
            ** (numbers[f"n{col + 2}"] if not switcharoo else numbers[f"n{col + 3}"])
            + io.construction_signal**con_signal.continue_construction
        )
        for r_switcharoo in (True, False)
        for switcharoo in (True, False)
        for i in range(3)
        for row in range(3 - i, 7 - i)
        for col in range(1, 4)
    ]

    horizontal_right_vertical_placement_rule = [
        (
            +(io.input_vertical**response.yes)
            + io.input_horizontal**response.yes
            + io.start**response.no
            + (1.0 if r_switcharoo else 7.0)
            * (io.left ** (response.no if r_switcharoo else response.yes))
            - (1.0 if r_switcharoo else 7.0)
            * (io.left ** (response.yes if r_switcharoo else response.no))
            + (7.0 if r_switcharoo else 1.0)
            * (io.right ** (response.yes if r_switcharoo else response.no))
            - (7.0 if r_switcharoo else 1.0)
            * (io.right ** (response.no if r_switcharoo else response.yes))
            + io.above**response.no
            + io.below**response.no
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_horizontal_row1"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_horizontal_row2"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_horizontal_row3"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_horizontal_col1"]
            ** numbers[f"n{col}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_horizontal_col2"]
            ** numbers[f"n{col + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_horizontal_col3"]
            ** numbers[f"n{col + 2}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_row1"]
            ** numbers[f"n{row - 2 + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_row2"]
            ** numbers[f"n{row - 1 + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_row3"]
            ** numbers[f"n{row + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_col1"]
            ** numbers[f"n{col - 1}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_col2"]
            ** numbers[f"n{col - 1}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_col3"]
            ** numbers[f"n{col - 1}"]
            + 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'vertical'}"]
                ** response.reference
            )  # horizontal isnt already there
            + 2.0
            * (
                io[f"target_{'vertical' if switcharoo else 'horizontal'}"]
                ** response.latest
            )  # but vertical is
            - 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'vertical'}"]
                ** response.yes
            )
            - 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'vertical'}"]
                ** response.latest
            )
            - 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'vertical'}"]
                ** response.no
            )
            - 2.0
            * (
                io[f"target_{'vertical' if switcharoo else 'horizontal'}"]
                ** response.yes
            )
            - 2.0
            * (
                io[f"target_{'vertical' if switcharoo else 'horizontal'}"]
                ** response.reference
            )
            - 2.0
            * (
                io[f"target_{'vertical' if switcharoo else 'horizontal'}"]
                ** response.no
            )
            >> +(
                io[f"target_{'vertical' if switcharoo else 'horizontal'}"]
                ** response.yes
            )
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}"] ** response.yes
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row - 2 + i}"])
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_row2"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row - 1 + i}"])
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_row3"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + i}"])
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col - 1}"])
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_col2"]
            ** (numbers[f"n{col + 1}"] if not switcharoo else numbers[f"n{col - 1}"])
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_col3"]
            ** (numbers[f"n{col + 2}"] if not switcharoo else numbers[f"n{col - 1}"])
            + io.construction_signal**con_signal.continue_construction
        )
        for r_switcharoo in (True, False)
        for switcharoo in (True, False)
        for i in range(3)
        for row in range(3 - i, 7 - i)
        for col in range(2, 5)
    ]

    horizontal_above_vertical_placement_rule = [
        (
            +(io.input_vertical**response.yes)
            + io.input_horizontal**response.yes
            + io.start**response.no
            + io.left**response.no
            + io.right**response.no
            + (7.0 if r_switcharoo else 1.0)
            * (io.above ** (response.yes if r_switcharoo else response.no))
            - (7.0 if r_switcharoo else 1.0)
            * (io.above ** (response.no if r_switcharoo else response.yes))
            + (1.0 if r_switcharoo else 7.0)
            * (io.below ** (response.no if r_switcharoo else response.yes))
            - (1.0 if r_switcharoo else 7.0)
            * (io.below ** (response.yes if r_switcharoo else response.no))
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_horizontal_row1"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_horizontal_row2"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_horizontal_row3"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_horizontal_col1"]
            ** numbers[f"n{col}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_horizontal_col2"]
            ** numbers[f"n{col + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_horizontal_col3"]
            ** numbers[f"n{col + 2}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_row1"]
            ** numbers[f"n{row + 1}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_row2"]
            ** numbers[f"n{row + 2}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_row3"]
            ** numbers[f"n{row + 3}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_col1"]
            ** numbers[f"n{col + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_col2"]
            ** numbers[f"n{col + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_col3"]
            ** numbers[f"n{col + i}"]
            + 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'vertical'}"]
                ** response.reference
            )  # horizontal isnt already there
            + 2.0
            * (
                io[f"target_{'vertical' if switcharoo else 'horizontal'}"]
                ** response.latest
            )  # but vertical is
            - 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'vertical'}"]
                ** response.yes
            )
            - 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'vertical'}"]
                ** response.latest
            )
            - 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'vertical'}"]
                ** response.no
            )
            - 2.0
            * (
                io[f"target_{'vertical' if switcharoo else 'horizontal'}"]
                ** response.yes
            )
            - 2.0
            * (
                io[f"target_{'vertical' if switcharoo else 'horizontal'}"]
                ** response.reference
            )
            - 2.0
            * (
                io[f"target_{'vertical' if switcharoo else 'horizontal'}"]
                ** response.no
            )
            >> +(
                io[f"target_{'vertical' if switcharoo else 'horizontal'}"]
                ** response.yes
            )
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}"] ** response.yes
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + 1}"])
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_row2"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + 2}"])
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_row3"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row + 3}"])
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col + i}"])
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_col2"]
            ** (numbers[f"n{col + 1}"] if not switcharoo else numbers[f"n{col + i}"])
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_col3"]
            ** (numbers[f"n{col + 2}"] if not switcharoo else numbers[f"n{col + i}"])
            + io.construction_signal**con_signal.continue_construction
        )
        for r_switcharoo in (True, False)
        for switcharoo in (True, False)
        for i in range(3)
        for row in range(1, 4)
        for col in range(1, 5)
    ]

    horizontal_below_vertical_placement_rule = [
        (
            +(io.input_vertical**response.yes)
            + io.input_horizontal**response.yes
            + io.start**response.no
            + io.left**response.no
            + io.right**response.no
            + (1.0 if r_switcharoo else 7.0)
            * (io.above ** (response.no if r_switcharoo else response.yes))
            - (1.0 if r_switcharoo else 7.0)
            * (io.above ** (response.yes if r_switcharoo else response.no))
            + (7.0 if r_switcharoo else 1.0)
            * (io.below ** (response.yes if r_switcharoo else response.no))
            - (7.0 if r_switcharoo else 1.0)
            * (io.below ** (response.no if r_switcharoo else response.yes))
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_horizontal_row1"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_horizontal_row2"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_horizontal_row3"]
            ** numbers[f"n{row}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_horizontal_col1"]
            ** numbers[f"n{col}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_horizontal_col2"]
            ** numbers[f"n{col + 1}"]
            + (2.0 if switcharoo else 1.0)
            * io[f"{'target' if switcharoo else 'input'}_horizontal_col3"]
            ** numbers[f"n{col + 2}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_row1"]
            ** numbers[f"n{row - 3}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_row2"]
            ** numbers[f"n{row - 2}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_row3"]
            ** numbers[f"n{row - 1}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_col1"]
            ** numbers[f"n{col + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_col2"]
            ** numbers[f"n{col + i}"]
            + (1.0 if switcharoo else 2.0)
            * io[f"{'input' if switcharoo else 'target'}_vertical_col3"]
            ** numbers[f"n{col + i}"]
            + 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'vertical'}"]
                ** response.reference
            )  # horizontal isnt already there
            + 2.0
            * (
                io[f"target_{'vertical' if switcharoo else 'horizontal'}"]
                ** response.latest
            )  # but vertical is
            - 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'vertical'}"]
                ** response.latest
            )
            - 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'vertical'}"]
                ** response.yes
            )
            - 2.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'vertical'}"]
                ** response.no
            )
            - 2.0
            * (
                io[f"target_{'vertical' if switcharoo else 'horizontal'}"]
                ** response.reference
            )
            - 2.0
            * (
                io[f"target_{'vertical' if switcharoo else 'horizontal'}"]
                ** response.yes
            )
            - 2.0
            * (
                io[f"target_{'vertical' if switcharoo else 'horizontal'}"]
                ** response.no
            )
            >> +(
                io[f"target_{'vertical' if switcharoo else 'horizontal'}"]
                ** response.yes
            )
            + io[f"target_{'horizontal' if switcharoo else 'vertical'}"] ** response.yes
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_row1"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row - 3}"])
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_row2"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row - 2}"])
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_row3"]
            ** (numbers[f"n{row}"] if not switcharoo else numbers[f"n{row - 1}"])
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_col1"]
            ** (numbers[f"n{col}"] if not switcharoo else numbers[f"n{col + i}"])
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_col2"]
            ** (numbers[f"n{col + 1}"] if not switcharoo else numbers[f"n{col + i}"])
            + io[f"target_{'vertical' if switcharoo else 'horizontal'}_col3"]
            ** (numbers[f"n{col + 2}"] if not switcharoo else numbers[f"n{col + i}"])
            + io.construction_signal**con_signal.continue_construction
        )
        for r_switcharoo in (True, False)
        for switcharoo in (True, False)
        for i in range(3)
        for row in range(4, 7)
        for col in range(1, 5)
    ]

    # Backtracking rules
    bad_brick_backtracking_rule = [
        (
            +(io[f"input_{shape}"] ** response.no)
            + io[f"target_{shape}"] ** response.yes
            >> io.construction_signal**con_signal.backtrack_construction
        )
        for shape in SHAPES
    ]

    passive_backtracking_rule_one = [
        (
            +(io[f"input_{shape}"] ** response.yes)
            + io[f"input_{(SHAPES[:i] + SHAPES[i + 1:])[0]}"] ** response.no
            + io[f"input_{(SHAPES[:i] + SHAPES[i + 1:])[1]}"] ** response.no
            + io[f"input_{(SHAPES[:i] + SHAPES[i + 1:])[2]}"] ** response.no
            >> +(io.construction_signal**con_signal.backtrack_construction)
        )
        for i, shape in enumerate(SHAPES)
    ]

    passive_backtracking_rule_two = [
        (
            +(io[f"input_{shape}"] ** response.yes)
            + io[f"input_{other_shape}"] ** response.yes
            + io[f"input_{[s for s in SHAPES if s not in (shape, other_shape)][0]}"]
            ** response.no
            + io[f"input_{[s for s in SHAPES if s not in (shape, other_shape)][1]}"]
            ** response.no
            >> io.construction_signal**con_signal.backtrack_construction
        )
        for (shape, other_shape) in itertools.combinations(SHAPES, 2)
    ]

    passive_backtracking_rule_three = [
        (
            +(io[f"input_{shape}"] ** response.yes)
            + io[f"input_{other_shape}"] ** response.yes
            + io[f"input_{other_other_shape}"] ** response.yes
            + io[
                f"input_{[s for s in SHAPES if s not in (shape, other_shape, other_other_shape)][0]}"
            ]
            ** response.no
            >> io.construction_signal**con_signal.backtrack_construction
        )
        for (shape, other_shape, other_other_shape) in itertools.combinations(SHAPES, 3)
    ]

    passive_backtracking_rule_four = [
        (
            +(io["input_half_T"] ** response.yes)
            + io["input_mirror_L"] ** response.yes
            + io["input_horizontal"] ** response.yes
            + io["input_vertical"] ** response.yes
            >> io.construction_signal**con_signal.backtrack_construction
        )
    ]

    # END_CONSTRUCTION RULE
    # if all four blocks have been used, then stop construction
    stop_construction_rule_all_four = [
        (
            +(io.target_half_T**response.yes)
            + io.target_mirror_L**response.yes
            + io.target_vertical**response.yes
            + io.target_horizontal**response.yes
            >> +(io.construction_signal**con_signal.stop_construction)
        )
    ]

    stop_construction_rule_all_four_reference = [
        (
            +(2.0 if i != 0 else 1.0)
            * (io.target_half_T ** (response.yes if i != 0 else response.reference))
            + (2.0 if i != 1 else 1.0)
            * (io.target_mirror_L ** (response.yes if i != 1 else response.reference))
            + (2.0 if i != 2 else 1.0)
            * (io.target_vertical ** (response.yes if i != 2 else response.reference))
            + (2.0 if i != 3 else 1.0)
            * (io.target_horizontal ** (response.yes if i != 3 else response.reference))
            # - if no
            - (2.0 if i != 0 else 1.0) * (io.target_half_T**response.no)
            - (2.0 if i != 1 else 1.0) * (io.target_mirror_L**response.no)
            - (2.0 if i != 2 else 1.0) * (io.target_vertical**response.no)
            - (2.0 if i != 3 else 1.0) * (io.target_horizontal**response.no)
            >> +(io.construction_signal**con_signal.stop_construction)
        )
        for i in range(4)
    ]

    stop_construction_input_blocks_used_one = [
        (
            +(io[f"input_{shape}"] ** response.yes)
            + io[f"input_{(SHAPES[:i] + SHAPES[i + 1:])[0]}"] ** response.no
            + io[f"input_{(SHAPES[:i] + SHAPES[i + 1:])[1]}"] ** response.no
            + io[f"input_{(SHAPES[:i] + SHAPES[i + 1:])[2]}"] ** response.no
            + io[f"target_{shape}"] ** response.yes
            + io[f"target_{(SHAPES[:i] + SHAPES[i + 1:])[0]}"] ** response.no
            + io[f"target_{(SHAPES[:i] + SHAPES[i + 1:])[1]}"] ** response.no
            + io[f"target_{(SHAPES[:i] + SHAPES[i + 1:])[2]}"] ** response.no
            >> +(io.construction_signal**con_signal.stop_construction)
        )
        for i, shape in enumerate(SHAPES)
    ]

    stop_construction_input_blocks_used_two = [
        (
            +(io[f"input_{shape}"] ** response.yes)
            + io[f"input_{other_shape}"] ** response.yes
            + io[f"input_{[s for s in SHAPES if s not in (shape, other_shape)][0]}"]
            ** response.no
            + io[f"input_{[s for s in SHAPES if s not in (shape, other_shape)][1]}"]
            ** response.no
            + io[f"target_{shape}"] ** response.yes
            + io[f"target_{other_shape}"] ** response.yes
            + io[f"target_{[s for s in SHAPES if s not in (shape, other_shape)][0]}"]
            ** response.no
            + io[f"target_{[s for s in SHAPES if s not in (shape, other_shape)][1]}"]
            ** response.no
            >> io.construction_signal**con_signal.stop_construction
        )
        for (shape, other_shape) in itertools.combinations(SHAPES, 2)
    ]

    stop_construction_input_blocks_used_three = [
        (
            +(io[f"input_{shape}"] ** response.yes)
            + io[f"input_{other_shape}"] ** response.yes
            + io[f"input_{other_other_shape}"] ** response.yes
            + io[
                f"input_{[s for s in SHAPES if s not in (shape, other_shape, other_other_shape)][0]}"
            ]
            ** response.no
            + io[f"target_{shape}"] ** response.yes
            + io[f"target_{other_shape}"] ** response.yes
            + io[f"target_{other_other_shape}"] ** response.yes
            + io[
                f"target_{[s for s in SHAPES if s not in (shape, other_shape, other_other_shape)][0]}"
            ]
            ** response.no
            >> io.construction_signal**con_signal.stop_construction
        )
        for (shape, other_shape, other_other_shape) in itertools.combinations(SHAPES, 3)
    ]

    participant.search_space_rules.rules.compile(
        *(
            half_t_first_placement_rule
            + mirror_l_first_placement_rule
            + horizontal_first_placement_rule
            + vertical_first_placement_rule
            + half_t_left_of_horizontal_placement_rule
            + half_t_right_of_horizontal_placement_rule
            + half_t_above_horizontal_placement_rule
            + half_t_below_horizontal_placement_rule
            + half_t_left_vertical_placement_rule
            + half_t_right_vertical_placement_rule
            + half_t_above_vertical_placement_rule
            + half_t_below_vertical_placement_rule
            + half_t_left_mirror_l_placement_rule
            + half_t_right_mirror_l_placement_rule
            + half_t_above_mirror_l_placement_rule
            + half_t_below_mirror_l_placement_rule
            + mirror_l_left_horizontal_placement_rule
            + mirror_l_right_horizontal_placement_rule
            + mirror_l_above_horizontal_placement_rule
            + mirror_l_below_horizontal_placement_rule
            + mirror_l_left_vertical_placement_rule
            + mirror_l_right_vertical_placement_rule
            + mirror_l_above_vertical_placement_rule
            + mirror_l_below_vertical_placement_rule
            + horizontal_left_vertical_placement_rule
            + horizontal_right_vertical_placement_rule
            + horizontal_above_vertical_placement_rule
            + horizontal_below_vertical_placement_rule
            + stop_construction_input_blocks_used_one
            + stop_construction_input_blocks_used_two
            + stop_construction_input_blocks_used_three
            + stop_construction_rule_all_four
            + stop_construction_rule_all_four_reference
            + bad_brick_backtracking_rule
            + passive_backtracking_rule_one
            + passive_backtracking_rule_two
            + passive_backtracking_rule_three
            + passive_backtracking_rule_four
        )
    )
