assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

import sys
def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    ## Find all instances of naked twins
    # Find all boxes with only 2 possible values
    two_values = [box for box in values.keys() if len(values[box]) == 2]

	# Find naked twins
	# Create lists of twins if:
	# a) Both box and twin are really twins (same values with box =/= twin);
	# b) Twin is really a peer of box ;
	# c) Tuple (box,twin) is not duplicated (Mirrored)
    previous_twins = set() # Store previous twins to avoid mirror duplicates
    naked_twins = [[box,twin] for box in two_values for twin in two_values \
                   if (values[box] == values[twin]) and (box != twin)      \
				   and (twin in peers[box])                                \
				   and tuple([box,twin]) not in previous_twins and         \
				   not previous_twins.add(tuple([twin,box]))               ]

	## Eliminate the naked twins as possibilities for their peers
    for twins in range(len(naked_twins)):
		# Find the units containing the naked twins
        twins_units = [list for list in unitlist if all(x in list for x in naked_twins[twins])]
        for box in naked_twins[twins]:
            two_digit = values[box]
            for digit in two_digit:
                for units in twins_units:
                    for peer in units:
                        if peer not in naked_twins[twins]:
							# Remove digit from peers in unit
                            values = assign_value(values, peer, values[peer].replace(digit,''))	
    return values
	

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]

# Define rows
rows = 'ABCDEFGHI'
# Define columns
cols = '123456789'

# Create boxes elements    
boxes = cross(rows, cols)

## Create Units
# Create row units
row_units = [cross(r, cols) for r in rows]
# Create column units
column_units = [cross(rows, c) for c in cols]
# Create square units
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
# Create diagonal units (principal and secundary)
diagonal_units = [[rd+cd for rd,cd in zip(rows,cols[::i])] for i in (1,-1)]

# Create unit list with all units
unitlist = row_units + column_units + square_units + diagonal_units

# Create a dictionary with key = boxes and values = units that each boxe belongs to
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)

# Create a dictionary with key = boxes and values = all peers of each box
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
	(Copied from solution code from class 10 from Lecture 3)		
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
	(Copied from solution code from class 10 from Lecture 3)
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
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
	(Modified from solution code from class 10 from Lecture 3)
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values = assign_value(values, peer, values[peer].replace(digit,''))
    return values

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
	(Modified from solution code from class 10 from Lecture 3)
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values = assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
	"""
	Reduce puzzle using eliminate, naked twins and only choice strategies
	Input: A sudoku in dictionary form.
	Output: The resulting sudoku in dictionary form. False if no solution exists.
	(Modified from solution code from class 10 from Lecture 3)
	"""
	solved_values = [box for box in values.keys() if len(values[box]) == 1]
	stalled = False
	while not stalled:
        # Check how many boxes have a determined value before reducing
		solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        
        ## Constraint propagation techniques		
        # Use the Eliminate Strategy
		values = eliminate(values)
		# Use the Naked Twins Strategy
		values = naked_twins(values)
        # Use the Only Choice Strategy
		values = only_choice(values)
		
        # Check how many boxes have a determined value after reducing
		solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
		
        # If no new values were added, stop the loop.
		stalled = solved_values_before == solved_values_after
		
        # Sanity check, return False if there is a box with zero available values:
		if len([box for box in values.keys() if len(values[box]) == 0]):
			return False
	return values

def search(values):
    '''
	Depth-first search
	Input: A sudoku in dictionary form.
	Output: The resulting sudoku in dictionary form. False if no solution exists.
	(Modified from solution code from class 10 from Lecture 3)
	'''
	# Reduce puzzle with constraint propagation and naked twins
    values = reduce_puzzle(values)
	
    if values is False:
        return False ## Failed earlier
		
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
		
    # Chose one of the unfilled square s with the fewest possibilities
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
    Input: grid - string representing a sudoku grid.
    Output: The dictionary representation of the final sudoku grid. False if no solution exists.
    """
	# Encode grid in dict values
    values = grid_values(grid)
	
	# Solve sudoku with search, constraint propagation and naked twins
    values = search(values)
	
    if values:
        return values
    else:
        return False

if __name__ == '__main__':
	# hard diagonal sudoku test: diag_sudoku_grid = '.23.....................5915............4.......3........9.....9......1....7....6'
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
