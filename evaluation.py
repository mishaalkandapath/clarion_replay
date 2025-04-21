import numpy as np
import re
from utils import filter_keys_by_rule_chunk

from pyClarion import Key

SHAPE_MAP = {"half_T": 1, "mirror_L": 2, "vertical": 3, "horizontal": 4}
REVERSE_SHAPE_MAP = {v: k for k, v in SHAPE_MAP.items()}

def mk_ontopness(REQUIRED_FORM):
    """
    Check if there is ontopness in pattern.
    """
    ontopness = False
    count_ontop = 0
    ontop = 0
    below = 0
    
    if REQUIRED_FORM.size > 0:  # Check if not empty
        for i in range(1, REQUIRED_FORM.shape[0]):
            row_current = REQUIRED_FORM.shape[0] - i
            row_above = REQUIRED_FORM.shape[0] - (i + 1)
            
            if np.any(REQUIRED_FORM[row_current, :] - REQUIRED_FORM[row_above, :] != 0):
                index = np.where((REQUIRED_FORM[row_current, :] - REQUIRED_FORM[row_above, :]) != 0)[0]
                
                if np.any((REQUIRED_FORM[row_current, index] * REQUIRED_FORM[row_above, index]) != 0):
                    ontopness = True
                    count_ontop = count_ontop + 1
                    
                    elements_form = np.unique(REQUIRED_FORM)
                    elements_form = elements_form[elements_form != 0]
                    
                    row1 = np.where(REQUIRED_FORM == elements_form[0])[0]
                    row2 = np.where(REQUIRED_FORM == elements_form[1])[0]
                    
                    if np.min(row1) < np.min(row2):
                        ontop = elements_form[0]
                        below = elements_form[1]
                    elif np.min(row1) > np.min(row2):
                        ontop = elements_form[1]
                        below = elements_form[0]
    
    return ontopness, count_ontop, ontop, below

def mk_besideness(REQUIRED_FORM):
    """
    Check if there is besideness in pattern.
    """
    besideness = False
    count_beside = 0
    left = 0
    right = 0
    
    if REQUIRED_FORM.size > 0:  # Check if not empty
        REQUIRED_FORM = REQUIRED_FORM.T
        
        for i in range(1, REQUIRED_FORM.shape[0]):
            row_current = REQUIRED_FORM.shape[0] - i
            row_above = REQUIRED_FORM.shape[0] - (i + 1)
            
            if np.any(REQUIRED_FORM[row_current, :] - REQUIRED_FORM[row_above, :] != 0):
                index = np.where((REQUIRED_FORM[row_current, :] - REQUIRED_FORM[row_above, :]) != 0)[0]
                
                if np.any((REQUIRED_FORM[row_current, index] * REQUIRED_FORM[row_above, index]) != 0):
                    besideness = True
                    count_beside = count_beside + 1
                    
                    elements_form = np.unique(REQUIRED_FORM)
                    elements_form = elements_form[elements_form != 0]
                    
                    row1 = np.where(REQUIRED_FORM == elements_form[0])[0]
                    row2 = np.where(REQUIRED_FORM == elements_form[1])[0]
                    
                    if np.min(row1) < np.min(row2):
                        left = elements_form[0]
                        right = elements_form[1]
                    elif np.min(row1) > np.min(row2):
                        left = elements_form[1]
                        right = elements_form[0]
    
    return besideness, count_beside, left, right

def brick_connectedness(stim_grid):
    bricks_conn_trial = [0, 0, 0] #Element connected to middle via besideness | middle Element | Element connected to middle via ontopness
    bricks_rel_trial = [0, 0, 0, 0] # left element | ontop element | right element | below element

    bricks = np.unique(stim_grid)[1:] # dont need 0 
    
    part1 = np.copy(stim_grid); part1[part1==bricks[0]] = 0;
    part2 = np.copy(stim_grid); part2[part1==bricks[1]] = 0;
    part3 = np.copy(stim_grid); part3[part1==bricks[2]] = 0;

    bricks_order = np.array([[mk_ontopness(part3)[0]+mk_ontopness(part2)[0], mk_ontopness(part1)[0]+mk_ontopness(part3)[0], mk_ontopness(part1)[0]+mk_ontopness(part2)[0]], [mk_besideness(part3)[0]+mk_besideness(part2)[0], mk_besideness(part1)[0]+mk_besideness(part3)[0], mk_besideness(part1)[0]+mk_besideness(part2)[0]]])
    bricks_order = ([np.where(~bricks_order[0, :] & bricks_order[1,:])[0],
                     np.where(bricks_order[0,:] & bricks_order[1,:])[0],
                       np.where(bricks_order[0,:] & ~bricks_order[1,:])[0]])
    try:
        bricks_conn_trial = bricks[bricks_order].T
    except:
        print("somethign happened here")

    if mk_ontopness(part1)[0]:
        _, _, bricks_rel_trial[1], bricks_rel_trial[3] = mk_ontopness(part1)
    elif mk_ontopness(part2)[0]:
        _, _, bricks_rel_trial[1], bricks_rel_trial[3] = mk_ontopness(part2)
    elif mk_ontopness(part3)[0]:
        _, _, bricks_rel_trial[1], bricks_rel_trial[3] = mk_ontopness(part3)
    
    if mk_besideness(part1)[0]:
        _, _, bricks_rel_trial[0], bricks_rel_trial[2] = mk_besideness(part1)
    elif mk_besideness(part2)[0]:
        _, _, bricks_rel_trial[0], bricks_rel_trial[2] = mk_besideness(part2)
    elif mk_besideness(part3)[0]:
        _, _, bricks_rel_trial[0], bricks_rel_trial[2] = mk_besideness(part3)

    assert 0 not in bricks_conn_trial, "0 in bricks_conn_trial"
    assert 0 not in bricks_rel_trial, "0 in bricks_rel_trial"
    
    return bricks_conn_trial.flatten(), bricks_rel_trial

def calculate_delayed_effects(rule_choices, grids, participant):
    """
    bascially one - zero vectors of categorie of rules, plot em to get a plot like the one in the paper. 
    """
    max_len = max([len(g) for g in grids])
    stable_to_present = np.zeros((len(rule_choices), max_len))
    present_to_stable = np.zeros((len(rule_choices), max_len)) # backtracking
    distant_to_stable = np.zeros((len(rule_choices), max_len)) 
    stable_to_distant = np.zeros((len(rule_choices), max_len)) 
    present_to_present = np.zeros((len(rule_choices), max_len)) 

    pass

def simple_sequenceness(rule_choices, rule_lhs_information, grids, participant):
    
    max_len = max([len(g) for g in grids])-1
    stable_to_present = np.zeros((len(rule_choices), max_len))
    present_to_stable = np.zeros((len(rule_choices), max_len)) # backtracking
    distant_to_stable = np.zeros((len(rule_choices), max_len)) 
    stable_to_distant = np.zeros((len(rule_choices), max_len)) 
    present_to_present = np.zeros((len(rule_choices), max_len)) 

    for i, choices_in_trial in enumerate(rule_choices):
        stable_block = [k[-1] for k in choices_in_trial[0] if re.match(r"target_{mirror_L|half_T|horizontal|vertical}", str(k[-1][0]))][0][0]
        stable_block = str(stable_block)[len('target_'):]
        
        #now is it a present, present typa situation or a present, distant present typa situation. 
        _, brick_rel = brick_connectedness(grids[i])
        only_presents = brick_rel.tolist().count(SHAPE_MAP[stable_block]) == 2
        present = brick_rel((t := brick_rel.tolist().index(SHAPE_MAP[stable_block])) - 2 if t > 2 else t + 2)
        present2 = (t := np.unique(grids))[t not in (present, SHAPE_MAP[stable_block], 0)]
        present_block = REVERSE_SHAPE_MAP[present]
        present2_block = REVERSE_SHAPE_MAP[present2]

        for j, _ in enumerate(choices_in_trial[1:]):
            other_blocks = [k[-1] for k in rule_lhs_information[j+1] if re.match(r"(target_{mirror_L|half_T|horizontal|vertical})", str(k[-1][0]))]
            
            if only_presents:
                if stable_block in [k[0][len("target_"):] for k in other_blocks]\
                and "yes" in [k[1] for k in other_blocks if k[0][len("target_"):] == stable_block]:
                    stable_to_present[i, j] = 1
                elif stable_block in [k[0][len("target_"):] for k in other_blocks]:
                    present_to_stable[i, j] = 1 # this prolly will never happen -- but curious to see
                else:
                    present_to_present[i, j] = 1
            else:
                if stable_block in [k[0][len("target_"):] for k in other_blocks]\
                and "yes" in [k[1] for k in other_blocks if k[0][len("target_"):] == stable_block]\
                    and present_block in [k[0][len("target_"):] for k in other_blocks]:
                    stable_to_present[i, j] = 1
                elif stable_block in [k[0][len("target_"):] for k in other_blocks]\
                    and "yes" in [k[1] for k in other_blocks if k[0][len("target_"):] == stable_block]\
                        and present2_block in [k[0][len("target_"):] for k in other_blocks]:
                    stable_to_distant[i, j] = 1
                elif stable_block in [k[0][len("target_"):] for k in other_blocks]\
                    and present_block in [k[0][len("target_"):] for k in other_blocks]:
                    present_to_stable[i, j] = 1
                elif stable_block in [k[0][len("target_"):] for k in other_blocks]\
                    and present2_block in [k[0][len("target_"):] for k in other_blocks]:
                    distant_to_stable[i, j] = 1
                else:
                    present_to_present[i, j] = 1

    return stable_to_present, present_to_stable, distant_to_stable, stable_to_distant, present_to_present