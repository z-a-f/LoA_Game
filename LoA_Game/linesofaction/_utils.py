# StrEnum was introduced in Python 3.11
# We create our own if version is lower than 3.11
import sys
import numpy as np

if sys.version_info < (3, 11):
    from enum import Enum
    class StrEnum(str, Enum):
        @staticmethod
        def _generate_next_value_(name, start, count, last_values):
            return name.lower()
        def __str__(self):
            return str(self.value)
else:
    from enum import StrEnum

# === Pretty Printers ===
def to_lines(
        board,
        highlight=None,   # Positions to highlight
        active=None,      # Active position
        char_map=None,
    ):
    '''Converts the board to a list of lists with each element being a string / char
    
    Args:
        board (np.ndarray): Board to convert to lines.
        with_header (bool): Whether to include the header.
        with_index (bool): Whether to include the row index.
        highlights (list): List of positions to highlight.
        active (tuple): Active position to highlight.
        char_map (dict): Dictionary mapping values to characters.
            If 'active' is present, it could be either a character or a mapping dict
            If 'highlight' is present, it could be either a character or a mapping dict
    '''
    highlight = set(highlight) if highlight is not None else set()

    if char_map is None:
        char_map = {}
    char_map.setdefault('highlight', {})
    char_map.setdefault('active', {})
    highlight_default = 'X'
    active_default = 'O'

    lines = []
    header = [chr(c) for c in range(ord('A'), ord('A') + board.shape[1])]
    index = list(range(1, board.shape[0]+1))

    for idx, row in enumerate(board):
        line = []
        for col_idx, value in enumerate(row):
            if (idx, col_idx) == active:
                line.append(char_map['active'].get(value, active_default))
            elif (idx, col_idx) in highlight:
                line.append(char_map['highlight'].get(value, highlight_default))
            else:
                line.append(char_map.get(value, str(value)))
        lines.append(line)
    return header, index, lines



# === Coordinate Generators ===
def line_coords(shape, pivot_position, orientation):
    '''Creates coordinates for the given direction and pivot position.
    
    Args:
        pivot_position (tuple): Pivot position for the mask.
        orientation (str): Orientation of the line in the mask
            One of 'horizontal', 'vertical', 'diagonal', 'antidiagonal'.
            Or shorthand 'h', 'v', 'd', 'a'.
    '''
    row, col = pivot_position
    if row >= shape[0] or col >= shape[1]:
        raise ValueError(f'Pivot position {pivot_position} is out of bounds for shape {shape}')
    row = row % shape[0]
    col = col % shape[1]
    assert orientation in ['horizontal', 'vertical', 'diagonal', 'antidiagonal', 'h', 'v', 'd', 'a'], f'Invalid orientation: {orientation}'

    coords = None

    if orientation in ['h', 'horizontal']:
        coords = ((row, i) for i in range(shape[1]))
    elif orientation in ['v', 'vertical']:
        coords = ((i, col) for i in range(shape[0]))
    elif orientation in ['d', 'diagonal']:
        offset = min(row, col)  # Move to the top-left corner
        row -= offset
        col -= offset
        min_range = range(min(shape[0]-row, shape[1]-col))
        coords = ((row+i, col+i) for i in min_range)
    elif orientation in ['a', 'antidiagonal']:
        offset = min(row, shape[1]-col-1)  # Move to the top-right corner
        row -= offset
        col += offset
        min_range = range(min(shape[0]-row, col+1))
        coords = ((row+i, col-i) for i in min_range)
    return set(coords)

def line_of_sight_coords(shape, pivot_position,
                         obstacle_coords,
                         orientation,
                         include_obstacles=False):
    '''Creates coordinates of the lines of sight for the given direction and pivot position.

    Args:
        shape (tuple): Shape of the environment
        pivot_position (tuple): Pivot position for the line of sight.
        obstacle_coords (np.ndarray): coordinates of the obstacles
        orientation (str): Orientation of the line
            One of 'horizontal', 'vertical', 'diagonal', 'antidiagonal'.
            Or shorthand 'h', 'v', 'd', 'a'.
        include_obstacles (bool): Whether to include the obstacles in the line of sight.
    
    Returns:
        set: Coordinates of the line of sight.
    
    Note: The pivot position is included in the line of sight.
    '''
    # Convert coordinates to list of tuples
    obstacle_coords = set(map(tuple, obstacle_coords))
    # Check if pivot position is an obstacle
    if pivot_position in obstacle_coords:
        return set([pivot_position]) if include_obstacles else set()
    # Get the coordinates of the line
    coords = line_coords(shape, pivot_position, orientation)
    # Get the coordinates of the obstacles that lay on the line
    obstacle_coords = set(map(tuple, obstacle_coords)).intersection(coords)
    if len(obstacle_coords) == 0:
        # No obstructions
        return coords
    # Find the obstacles that are closest to the pivot position
    delta = [0, 0]
    if orientation.startswith('h'):
        delta[1] = 1
    elif orientation.startswith('v'):
        delta[0] = 1
    elif orientation.startswith('d'):
        delta = [1, 1]
    elif orientation.startswith('a'):
        delta = [1, -1]
    else:
        raise ValueError(f'Invalid orientation: {orientation}')
    
    result = set([pivot_position])
    row, col = pivot_position
    while row < shape[0] and col < shape[1]:
        if (row, col) in obstacle_coords:
            if include_obstacles:
                result.add((row, col))
            break
        result.add((row, col))
        row += delta[0]
        col += delta[1]
    row, col = pivot_position
    while row >= 0 and col >= 0:
        if (row, col) in obstacle_coords:
            if include_obstacles:
                result.add((row, col))
            break
        result.add((row, col))
        row -= delta[0]
        col -= delta[1]
    return result

def _split_around_pivot(coords, pivot_position, orientation):
    '''Splits the coordinates around the pivot into two parts.
    
    Note: This excludes the pivot itself.

    The split is done on the sorted coordinates, and follow the rules on sorting:
        * Horizontal: West -> Pivot -> East
        * Vertical: North -> Pivot -> South
        * Diagonal: North-West -> Pivot -> South-East
        * Antidiagonal: North-East -> Pivot -> South-West
    '''
    result = {}
    coords = sorted(coords)
    pivot_idx = coords.index(pivot_position)

    if orientation.startswith('h'):
        result['w'] = set(coords[:pivot_idx])
        result['e'] = set(coords[pivot_idx+1:])
    elif orientation.startswith('v'):
        result['n'] = set(coords[:pivot_idx])
        result['s'] = set(coords[pivot_idx+1:])
    elif orientation.startswith('d'):
        result['nw'] = set(coords[:pivot_idx])
        result['se'] = set(coords[pivot_idx+1:])
    elif orientation.startswith('a'):
        result['ne'] = set(coords[:pivot_idx])
        result['sw'] = set(coords[pivot_idx+1:])
    else:
        raise ValueError(f'Invalid orientation: {orientation}')
    return result

def orientation2direction(coords, pivot_position, orientation=None):
    '''Converts orientation coordinates to direction coordinates.
    
    Args:
        coords (set): Coordinates of the line of sight.
        pivot_position (tuple): Pivot position for the line of sight.
        orientation (str): Orientation of the line
            One of 'horizontal', 'vertical', 'diagonal', 'antidiagonal'.
            Or shorthand 'h', 'v', 'd', 'a'.
        
    Note:
        * orientation cannot be None if coords is a set
        * if coords is a dict, the key is assumed to be the orientation
    '''
    if not isinstance(coords, dict):
        assert orientation is not None, 'Orientation cannot be None if coords is a set.'
        coords = {orientation: coords}
    result = {}
    for key, value in coords.items():
        result.update(_split_around_pivot(value, pivot_position, key))
    return result

def all_line_of_sight_coords(shape, pivot_position, obstacle_coords, include_obstacles=True):
    '''Creates all line of sight coordinates for the given pivot position.

    The line of sight is blocked by obstacles in the obstacle mask.

    Args:
        shape (tuple): Shape of the environment
        pivot_position (tuple): Pivot position for the mask.
        obstacle_coords (np.ndarray): coordinates of the obstacles
    
    Returns:
        dict: Dictionary of coordinates for all directions.
    '''
    pivot_position = tuple([
        pivot_position[0] % shape[0],
        pivot_position[1] % shape[1],
    ])
    coords = {}
    # Add orientations
    for orientation in 'hvda':
        coords[orientation] = line_of_sight_coords(
            shape, pivot_position, obstacle_coords, orientation,
            include_obstacles=include_obstacles)
    # Add directions as well
    coords.update(orientation2direction(coords, pivot_position))  # These don't include the pivot
    return coords

# === Mask Generators ===
def line_mask(shape, pivot_position, orientation):
    '''Creates a mask for the given direction and pivot position.

    Args:
        pivot_position (tuple): Pivot position for the mask.
        orientation (str): Orientation of the line in the mask
            One of 'horizontal', 'vertical', 'diagonal', 'antidiagonal'.
            Or shorthand 'h', 'v', 'd', 'a'.
    
    Returns:
        np.ndarray: Mask for the given direction and pivot position.
    '''
    mask = np.zeros(shape, dtype=bool)
    coords = line_coords(shape, pivot_position, orientation)
    mask[tuple(zip(*coords))] = True
    return mask


def line_of_sight_mask(obstacle_mask, pivot_position, orientation, include_obstacles=False):
    '''Creates a line of sight mask for the given direction and pivot position.

    The line of sight is blocked by obstacles in the obstacle mask.

    Args:
        obstacle_mask (np.ndarray): Mask of obstacles.
        pivot_position (tuple): Pivot position for the mask.
        orientation (str): Orientation of the line in the mask
            One of 'horizontal', 'vertical', 'diagonal', 'antidiagonal'.
            Or shorthand 'h', 'v', 'd', 'a'.
    
    Returns:
        np.ndarray: Mask for the given direction and pivot position.
    '''   
    mask = np.zeros_like(obstacle_mask, dtype=bool)
    if obstacle_mask[pivot_position]:
        if include_obstacles:
            mask[pivot_position] = True
        return mask
    # Find the coordinates
    obstacle_coords = np.argwhere(obstacle_mask)
    obstacle_coords = sorted(map(tuple, obstacle_coords.tolist()))
    coords = line_of_sight_coords(obstacle_mask.shape,
                                  pivot_position,
                                  obstacle_coords,
                                  orientation,
                                  include_obstacles=include_obstacles)
    # print(f'===> DEBUG: {pivot_position=}, {coords=}, {obstacle_coords=}')
    mask[tuple(zip(*coords))] = True
    return mask

def all_lines_of_sight_mask(obstacle_mask, pivot_position, include_obstacles=False):
    '''Creates all line of sight masks for the given pivot position.

    The line of sight is blocked by obstacles in the obstacle mask.

    Args:
        obstacle_mask (np.ndarray): Mask of obstacles.
        pivot_position (tuple): Pivot position for the mask.
    
    Returns:
        dict: Dictionary of masks for all directions.
    '''
    mask = np.zeros_like(obstacle_mask, dtype=bool)
    if obstacle_mask[pivot_position]:
        if include_obstacles:
            mask[pivot_position] = True
        return mask
    obstacle_coords = np.argwhere(obstacle_mask)
    obstacle_coords = sorted(map(tuple, obstacle_coords.tolist()))

    coords = all_line_of_sight_coords(obstacle_mask.shape,
                                      pivot_position,
                                      obstacle_coords,
                                      include_obstacles=include_obstacles)
    for key in 'hvda':
        crd = coords[key]
        mask[tuple(zip(*crd))] = True
    return mask

def print_mask(mask, highlight=None):
    '''Prints the mask in a human-readable format.'''
    # for row in mask:
    #     print(''.join(['#' if x else '.' for x in row]))
    for row_idx in range(mask.shape[0]):
        row = mask[row_idx]
        row_str = ''
        for col_idx in range(mask.shape[1]):
            if highlight is not None and (row_idx, col_idx) == highlight:
                row_str += ' O'
            else:
                row_str += ' #' if row[col_idx] else ' .'
        print(row_str)
