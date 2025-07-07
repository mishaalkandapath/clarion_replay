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
            + 7.0 * (io.start**response.yes)
            - 7.0 * (io.start**response.no)
            - 1.0 * (io.target_mirror_L ** response.yes)
            - 1.0 * (io.target_horizontal ** response.yes)
            - 1.0 * (io.target_vertical ** response.yes)
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
            - 1.0 * (io.target_half_T ** response.yes)
            - 1.0 * (io.target_horizontal ** response.yes)
            - 1.0 * (io.target_vertical ** response.yes)
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
            - 1.0 * (io.target_mirror_L ** response.yes)
            - 1.0 * (io.target_half_T ** response.yes)
            - 1.0 * (io.target_vertical ** response.yes)
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
            - 1.0 * (io.target_mirror_L ** response.yes)
            - 1.0 * (io.target_horizontal ** response.yes)
            - 1.0 * (io.target_half_T ** response.yes)
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
            + 5.0
            * (
                io[f"target_{'half_T' if switcharoo else 'horizontal'}"]
                ** response.reference
            )  # half_T is already there
            + 5.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'half_T'}"]
                ** response.latest
            )  # but horizontal is not
            - 5.0
            * (io[f"target_{'half_T' if switcharoo else 'horizontal'}"] ** response.yes)
            - 5.0
            * (
                io[f"target_{'half_T' if switcharoo else 'horizontal'}"]
                ** response.latest
            )
            - 5.0
            * (io[f"target_{'half_T' if switcharoo else 'horizontal'}"] ** response.no)
            - 5.0
            * (io[f"target_{'horizontal' if switcharoo else 'half_T'}"] ** response.yes)
            - 5.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'half_T'}"]
                ** response.reference
            )
            - 5.0
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
            + 5.0
            * (
                io[f"target_{'half_T' if switcharoo else 'horizontal'}"]
                ** response.reference
            )  # half_T is already there
            + 5.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'half_T'}"]
                ** response.latest
            )  # but horizontal is not
            - 5.0
            * (io[f"target_{'half_T' if switcharoo else 'horizontal'}"] ** response.yes)
            - 5.0
            * (
                io[f"target_{'half_T' if switcharoo else 'horizontal'}"]
                ** response.latest
            )
            - 5.0
            * (io[f"target_{'half_T' if switcharoo else 'horizontal'}"] ** response.no)
            - 5.0
            * (io[f"target_{'horizontal' if switcharoo else 'half_T'}"] ** response.yes)
            - 5.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'half_T'}"]
                ** response.reference
            )
            - 5.0
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
            + 5.0
            * (
                io[f"target_{'half_T' if switcharoo else 'horizontal'}"]
                ** response.reference
            )  # half_T is already there
            + 5.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'half_T'}"]
                ** response.latest
            )  # but horizontal is not
            - 5.0
            * (io[f"target_{'half_T' if switcharoo else 'horizontal'}"] ** response.yes)
            - 5.0
            * (
                io[f"target_{'half_T' if switcharoo else 'horizontal'}"]
                ** response.latest
            )
            - 5.0
            * (io[f"target_{'half_T' if switcharoo else 'horizontal'}"] ** response.no)
            - 5.0
            * (io[f"target_{'horizontal' if switcharoo else 'half_T'}"] ** response.yes)
            - 5.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'half_T'}"]
                ** response.reference
            )
            - 5.0
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
            + 5.0
            * (
                io[f"target_{'half_T' if switcharoo else 'horizontal'}"]
                ** response.reference
            )  # half_T isnt already there
            + 5.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'half_T'}"]
                ** response.latest
            )  # but horizontal is
            - 5.0
            * (io[f"target_{'half_T' if switcharoo else 'horizontal'}"] ** response.yes)
            - 5.0
            * (
                io[f"target_{'half_T' if switcharoo else 'horizontal'}"]
                ** response.latest
            )
            - 5.0
            * (io[f"target_{'half_T' if switcharoo else 'horizontal'}"] ** response.no)
            - 5.0
            * (io[f"target_{'horizontal' if switcharoo else 'half_T'}"] ** response.yes)
            - 5.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'half_T'}"]
                ** response.reference
            )
            - 5.0
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
            + 5.0
            * (
                io[f"target_{'half_T' if switcharoo else 'vertical'}"]
                ** response.reference
            )  # half_T isnt already there
            + 5.0
            * (
                io[f"target_{'vertical' if switcharoo else 'half_T'}"]
                ** response.latest
            )  # but vertical is
            - 5.0
            * (io[f"target_{'half_T' if switcharoo else 'vertical'}"] ** response.yes)
            - 5.0
            * (
                io[f"target_{'half_T' if switcharoo else 'vertical'}"]
                ** response.latest
            )
            - 5.0
            * (io[f"target_{'half_T' if switcharoo else 'vertical'}"] ** response.no)
            - 5.0
            * (io[f"target_{'vertical' if switcharoo else 'half_T'}"] ** response.yes)
            - 5.0
            * (
                io[f"target_{'vertical' if switcharoo else 'half_T'}"]
                ** response.reference
            )
            - 5.0
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
            + 5.0
            * (
                io[f"target_{'half_T' if switcharoo else 'vertical'}"]
                ** response.reference
            )  # half_T isnt already there
            + 5.0
            * (
                io[f"target_{'vertical' if switcharoo else 'half_T'}"]
                ** response.latest
            )  # but vertical is
            - 5.0
            * (io[f"target_{'half_T' if switcharoo else 'vertical'}"] ** response.yes)
            - 5.0
            * (
                io[f"target_{'half_T' if switcharoo else 'vertical'}"]
                ** response.latest
            )
            - 5.0
            * (io[f"target_{'half_T' if switcharoo else 'vertical'}"] ** response.no)
            - 5.0
            * (io[f"target_{'vertical' if switcharoo else 'half_T'}"] ** response.yes)
            - 5.0
            * (
                io[f"target_{'vertical' if switcharoo else 'half_T'}"]
                ** response.reference
            )
            - 5.0
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
            + 5.0
            * (
                io[f"target_{'half_T' if switcharoo else 'vertical'}"]
                ** response.reference
            )  # half_T isnt already there
            + 5.0
            * (
                io[f"target_{'vertical' if switcharoo else 'half_T'}"]
                ** response.latest
            )  # but vertical is
            - 5.0
            * (io[f"target_{'half_T' if switcharoo else 'vertical'}"] ** response.yes)
            - 5.0
            * (
                io[f"target_{'half_T' if switcharoo else 'vertical'}"]
                ** response.latest
            )
            - 5.0
            * (io[f"target_{'half_T' if switcharoo else 'vertical'}"] ** response.no)
            - 5.0
            * (io[f"target_{'vertical' if switcharoo else 'half_T'}"] ** response.yes)
            - 5.0
            * (
                io[f"target_{'vertical' if switcharoo else 'half_T'}"]
                ** response.reference
            )
            - 5.0
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
            + 5.0
            * (
                io[f"target_{'half_T' if switcharoo else 'vertical'}"]
                ** response.reference
            )  # half_T isnt already there
            + 5.0
            * (
                io[f"target_{'vertical' if switcharoo else 'half_T'}"]
                ** response.latest
            )  # but vertical is
            - 5.0
            * (io[f"target_{'half_T' if switcharoo else 'vertical'}"] ** response.yes)
            - 5.0
            * (
                io[f"target_{'half_T' if switcharoo else 'vertical'}"]
                ** response.latest
            )
            - 5.0
            * (io[f"target_{'half_T' if switcharoo else 'vertical'}"] ** response.no)
            - 5.0
            * (io[f"target_{'vertical' if switcharoo else 'half_T'}"] ** response.yes)
            - 5.0
            * (
                io[f"target_{'vertical' if switcharoo else 'half_T'}"]
                ** response.reference
            )
            - 5.0
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
            + 5.0
            * (
                io[f"target_{'half_T' if switcharoo else 'mirror_L'}"]
                ** response.reference
            )  # half_T isnt already there
            + 5.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'half_T'}"]
                ** response.latest
            )  # but mirror_L is
            - 5.0
            * (io[f"target_{'half_T' if switcharoo else 'mirror_L'}"] ** response.yes)
            - 5.0
            * (
                io[f"target_{'half_T' if switcharoo else 'mirror_L'}"]
                ** response.latest
            )
            - 5.0
            * (io[f"target_{'half_T' if switcharoo else 'mirror_L'}"] ** response.no)
            - 5.0
            * (io[f"target_{'mirror_L' if switcharoo else 'half_T'}"] ** response.yes)
            - 5.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'half_T'}"]
                ** response.reference
            )
            - 5.0
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
            + 5.0
            * (
                io[f"target_{'half_T' if switcharoo else 'mirror_L'}"]
                ** response.reference
            )  # half_T isnt already there
            + 5.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'half_T'}"]
                ** response.latest
            )  # but mirror_L is
            - 5.0
            * (io[f"target_{'half_T' if switcharoo else 'mirror_L'}"] ** response.yes)
            - 5.0
            * (
                io[f"target_{'half_T' if switcharoo else 'mirror_L'}"]
                ** response.latest
            )
            - 5.0
            * (io[f"target_{'half_T' if switcharoo else 'mirror_L'}"] ** response.no)
            - 5.0
            * (io[f"target_{'mirror_L' if switcharoo else 'half_T'}"] ** response.yes)
            - 5.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'half_T'}"]
                ** response.reference
            )
            - 5.0
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
            + 5.0
            * (
                io[f"target_{'half_T' if switcharoo else 'mirror_L'}"]
                ** response.reference
            )  # half_T isnt already there
            + 5.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'half_T'}"]
                ** response.latest
            )  # but mirror_L is
            - 5.0
            * (io[f"target_{'half_T' if switcharoo else 'mirror_L'}"] ** response.yes)
            - 5.0
            * (
                io[f"target_{'half_T' if switcharoo else 'mirror_L'}"]
                ** response.latest
            )
            - 5.0
            * (io[f"target_{'half_T' if switcharoo else 'mirror_L'}"] ** response.no)
            - 5.0
            * (io[f"target_{'mirror_L' if switcharoo else 'half_T'}"] ** response.yes)
            - 5.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'half_T'}"]
                ** response.reference
            )
            - 5.0
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
            + 5.0
            * (
                io[f"target_{'half_T' if switcharoo else 'mirror_L'}"]
                ** response.reference
            )  # half_T isnt already there
            + 5.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'half_T'}"]
                ** response.latest
            )  # but mirror_L is
            - 5.0
            * (io[f"target_{'half_T' if switcharoo else 'mirror_L'}"] ** response.yes)
            - 5.0
            * (
                io[f"target_{'half_T' if switcharoo else 'mirror_L'}"]
                ** response.latest
            )
            - 5.0
            * (io[f"target_{'half_T' if switcharoo else 'mirror_L'}"] ** response.no)
            - 5.0
            * (io[f"target_{'mirror_L' if switcharoo else 'half_T'}"] ** response.yes)
            - 5.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'half_T'}"]
                ** response.reference
            )
            - 5.0
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
            + 5.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"]
                ** response.reference
            )  # mirror_L isnt already there
            + 5.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"]
                ** response.latest
            )  # but horizontal is
            - 5.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"]
                ** response.yes
            )
            - 5.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"]
                ** response.latest
            )
            - 5.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"]
                ** response.no
            )
            - 5.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"]
                ** response.yes
            )
            - 5.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"]
                ** response.reference
            )
            - 5.0
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
            + 5.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"]
                ** response.reference
            )  # mirror_L isnt already there
            + 5.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"]
                ** response.latest
            )  # but horizontal is
            - 5.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"]
                ** response.yes
            )
            - 5.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"]
                ** response.latest
            )
            - 5.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"]
                ** response.no
            )
            - 5.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"]
                ** response.yes
            )
            - 5.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"]
                ** response.reference
            )
            - 5.0
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
            + 5.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"]
                ** response.reference
            )  # mirror_L isnt already there
            + 5.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"]
                ** response.latest
            )  # but horizontal is
            - 5.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"]
                ** response.yes
            )
            - 5.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"]
                ** response.latest
            )
            - 5.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"]
                ** response.no
            )
            - 5.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"]
                ** response.yes
            )
            - 5.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"]
                ** response.reference
            )
            - 5.0
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
            + 5.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"]
                ** response.reference
            )  # mirror_L isnt already there
            + 5.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"]
                ** response.latest
            )  # but horizontal is
            - 5.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"]
                ** response.yes
            )
            - 5.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"]
                ** response.latest
            )
            - 5.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'horizontal'}"]
                ** response.no
            )
            - 5.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"]
                ** response.yes
            )
            - 5.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'mirror_L'}"]
                ** response.reference
            )
            - 5.0
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
            + 5.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'vertical'}"]
                ** response.reference
            )  # mirror_L isnt already there
            + 5.0
            * (
                io[f"target_{'vertical' if switcharoo else 'mirror_L'}"]
                ** response.latest
            )  # but vertical is
            - 5.0
            * (io[f"target_{'mirror_L' if switcharoo else 'vertical'}"] ** response.yes)
            - 5.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'vertical'}"]
                ** response.latest
            )
            - 5.0
            * (io[f"target_{'mirror_L' if switcharoo else 'vertical'}"] ** response.no)
            - 5.0
            * (io[f"target_{'vertical' if switcharoo else 'mirror_L'}"] ** response.yes)
            - 5.0
            * (
                io[f"target_{'vertical' if switcharoo else 'mirror_L'}"]
                ** response.reference
            )
            - 5.0
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
            + 5.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'vertical'}"]
                ** response.reference
            )  # mirror_L isnt already there
            + 5.0
            * (
                io[f"target_{'vertical' if switcharoo else 'mirror_L'}"]
                ** response.latest
            )  # but vertical is
            - 5.0
            * (io[f"target_{'mirror_L' if switcharoo else 'vertical'}"] ** response.yes)
            - 5.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'vertical'}"]
                ** response.latest
            )
            - 5.0
            * (io[f"target_{'mirror_L' if switcharoo else 'vertical'}"] ** response.no)
            - 5.0
            * (io[f"target_{'vertical' if switcharoo else 'mirror_L'}"] ** response.yes)
            - 5.0
            * (
                io[f"target_{'vertical' if switcharoo else 'mirror_L'}"]
                ** response.reference
            )
            - 5.0
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
            + 5.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'vertical'}"]
                ** response.reference
            )  # mirror_L isnt already there
            + 5.0
            * (
                io[f"target_{'vertical' if switcharoo else 'mirror_L'}"]
                ** response.latest
            )  # but vertical is
            - 5.0
            * (io[f"target_{'mirror_L' if switcharoo else 'vertical'}"] ** response.yes)
            - 5.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'vertical'}"]
                ** response.latest
            )
            - 5.0
            * (io[f"target_{'mirror_L' if switcharoo else 'vertical'}"] ** response.no)
            - 5.0
            * (io[f"target_{'vertical' if switcharoo else 'mirror_L'}"] ** response.yes)
            - 5.0
            * (
                io[f"target_{'vertical' if switcharoo else 'mirror_L'}"]
                ** response.reference
            )
            - 5.0
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
            + 5.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'vertical'}"]
                ** response.reference
            )  # mirror_L isnt already there
            + 5.0
            * (
                io[f"target_{'vertical' if switcharoo else 'mirror_L'}"]
                ** response.latest
            )  # but vertical is
            - 5.0
            * (io[f"target_{'mirror_L' if switcharoo else 'vertical'}"] ** response.yes)
            - 5.0
            * (
                io[f"target_{'mirror_L' if switcharoo else 'vertical'}"]
                ** response.latest
            )
            - 5.0
            * (io[f"target_{'mirror_L' if switcharoo else 'vertical'}"] ** response.no)
            - 5.0
            * (io[f"target_{'vertical' if switcharoo else 'mirror_L'}"] ** response.yes)
            - 5.0
            * (
                io[f"target_{'vertical' if switcharoo else 'mirror_L'}"]
                ** response.reference
            )
            - 5.0
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
            + 5.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'vertical'}"]
                ** response.reference
            )  # horizontal isnt already there
            + 5.0
            * (
                io[f"target_{'vertical' if switcharoo else 'horizontal'}"]
                ** response.latest
            )  # but vertical is
            - 5.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'vertical'}"]
                ** response.yes
            )
            - 5.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'vertical'}"]
                ** response.latest
            )
            - 5.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'vertical'}"]
                ** response.no
            )
            - 5.0
            * (
                io[f"target_{'vertical' if switcharoo else 'horizontal'}"]
                ** response.yes
            )
            - 5.0
            * (
                io[f"target_{'vertical' if switcharoo else 'horizontal'}"]
                ** response.reference
            )
            - 5.0
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
            + 5.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'vertical'}"]
                ** response.reference
            )  # horizontal isnt already there
            + 5.0
            * (
                io[f"target_{'vertical' if switcharoo else 'horizontal'}"]
                ** response.latest
            )  # but vertical is
            - 5.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'vertical'}"]
                ** response.yes
            )
            - 5.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'vertical'}"]
                ** response.latest
            )
            - 5.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'vertical'}"]
                ** response.no
            )
            - 5.0
            * (
                io[f"target_{'vertical' if switcharoo else 'horizontal'}"]
                ** response.yes
            )
            - 5.0
            * (
                io[f"target_{'vertical' if switcharoo else 'horizontal'}"]
                ** response.reference
            )
            - 5.0
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
            + 5.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'vertical'}"]
                ** response.reference
            )  # horizontal isnt already there
            + 5.0
            * (
                io[f"target_{'vertical' if switcharoo else 'horizontal'}"]
                ** response.latest
            )  # but vertical is
            - 5.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'vertical'}"]
                ** response.yes
            )
            - 5.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'vertical'}"]
                ** response.latest
            )
            - 5.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'vertical'}"]
                ** response.no
            )
            - 5.0
            * (
                io[f"target_{'vertical' if switcharoo else 'horizontal'}"]
                ** response.yes
            )
            - 5.0
            * (
                io[f"target_{'vertical' if switcharoo else 'horizontal'}"]
                ** response.reference
            )
            - 5.0
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
            + 5.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'vertical'}"]
                ** response.reference
            )  # horizontal isnt already there
            + 5.0
            * (
                io[f"target_{'vertical' if switcharoo else 'horizontal'}"]
                ** response.latest
            )  # but vertical is
            - 5.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'vertical'}"]
                ** response.latest
            )
            - 5.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'vertical'}"]
                ** response.yes
            )
            - 5.0
            * (
                io[f"target_{'horizontal' if switcharoo else 'vertical'}"]
                ** response.no
            )
            - 5.0
            * (
                io[f"target_{'vertical' if switcharoo else 'horizontal'}"]
                ** response.reference
            )
            - 5.0
            * (
                io[f"target_{'vertical' if switcharoo else 'horizontal'}"]
                ** response.yes
            )
            - 5.0
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
