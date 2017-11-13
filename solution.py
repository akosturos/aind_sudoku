assignments = []


def cross(A, B):
    return [s+t for s in A for t in B]

rows = 'ABCDEFGHI'
cols = '123456789'
rows_reversed = rows[::-1]

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
col_units = [cross(rows, c) for c in cols]
#add in diagonals
diagonal_up = [[r+str(10-int(c)) for (r,c) in zip(rows, cols)]]
diagonal_down = [[r+c for (r,c) in zip(rows, cols)]]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]

unitlist = row_units + col_units + square_units + diagonal_up + diagonal_down
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], []))-set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the values dictionary with the naked twins eliminated from peers.
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers


    no_more_twins = False
    while not no_more_twins:
        board_values = values
        for unit in row_units + col_units + square_units:
            naked_twins_dict = dict()
            for digit in cols:
                # create concatenated list of boxes that have value
                boxes_found = ''.join([box for box in unit if digit in values[box]])
                # check if len == 4, meaning there are two boxes, and if yes insert in dict
                if len(boxes_found) == 4:
                    # check if in dict, if not it is first value
                    if(boxes_found not in naked_twins_dict.keys()):
                        naked_twins_dict[boxes_found] = digit
                    # if in dict, we have found a naked twins (we do not have to worry about
                    #       three values in the naked dict logic, because it is logically
                    #       impossible to two values for three places
                    else:
                        naked_twins_vals = naked_twins_dict[boxes_found] + digit
                        for box in unit:
                            if(box in boxes_found):
                                #naked twins
                                assign_value(values, box, naked_twins_vals)
                            else:
                                #remove naked twins values from same unit
                                assign_value(values, box, values[box].replace(naked_twins_vals[0], ''))
                                assign_value(values, box, values[box].replace(naked_twins_vals[1], ''))
    return values
    """
    no_more_twins = False
    while not no_more_twins:
        board_values = values
        for unit in row_units + col_units + square_units:
            n_t_poss = []
            for box in unit if len(values[box]) == 2:
                n_t_poss.append([[box],[values[box]])
            for item in n_t_poss:
                for comparison in n_t_poss:
                    if n_t_poss[item][1] == n_t_poss[comparison][1]:
                        if item != comparison:
                            n_t_boxes = [n_t_poss[item][0], n_t_poss[comparison][0])
                            n_t_values = n_t_poss[item][1]
                            for comp in unit:
                                if comp in n_t_boxes:
                                    assign_value(values, comp, n_t_values)
                                else:
                                    for digit in n_t_values:
                                        assign_value(values, comp, values[comp].replace(digit, ''))
                                   
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args: grid(string) - A grid in string form.
    Returns: A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a unique value,
    elimintate it from the value of its peers
    Input: Sudoku in dictionary form
    Output: Updated sudoku in dictionary form
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            assign_value(values, peer, values[peer].replace(digit,''))
    return values

def only_choice(values):
    """
    Look to see when there is only one choice available, and if so update values
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
    #see which values are solved
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values = len([box for box in values.keys() if len(values[box]) == 1])
        # eliminate the solved value from peer group
        values = eliminate(values)
        # only choice
        values = only_choice(values)
        # naked twins
        values = naked_twins(values)
        stalled = solved_values == len([box for box in values.keys() if len(values[box]) ==1])
        # check to see if broken
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
   # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
   # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
             return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    return search(values)

    
if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
