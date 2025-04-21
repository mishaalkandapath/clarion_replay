import numpy as np

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

def calculate_delayed_effects(rule_choices):
    pass