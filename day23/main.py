from errno import ENOENT
from os import strerror
from os.path import exists
from typing import List
from heapq import heappop, heappush, heapify

from node import Node

ENERGY_PER_STEP = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000
}

TEST_BURROW = [
    '#############',
    '#AA.D.....AD#',
    '###B#.#C#.###',
    '  #D#B#C#.#',
    '  #D#B#C#.#',
    '  #A#B#C#.#',
    '  #########'
]

def load_input(path: str) -> List[None]:
    '''Loads the input and returns it as a list of reboot steps.'''
    if not exists(path):
        raise FileNotFoundError(ENOENT, strerror(ENOENT), path)
    
    with open(path, 'r') as input_file:
        burrow = []
        for line in input_file:
            if line[-1] == '\n':
                burrow.append(line[:-1])
            else:
                burrow.append(line)
        return burrow
        
def get_adj_coords(coords, burrow, require_vacant=True):
    row, col = coords
    adj_coords = []
    for adj_coord in [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]:
        adj_row, adj_col = adj_coord
        if burrow[adj_row][adj_col] != '#':
            if burrow[adj_row][adj_col] == '.' or not require_vacant:
                adj_coords.append(adj_coord)
    return adj_coords

def get_wrong_letter_coords_in_room(burrow, col, desired_letter):
    wrong_coords = []
    wrong_below = False
    for row in range(len(burrow) - 2, 1, -1):
        letter = burrow[row][col]
        if letter != desired_letter or wrong_below:
            wrong_below = True
            if letter in 'ABCD':
                wrong_coords.append(((row, col), letter))
    return wrong_coords


def get_wrong_letter_coords(burrow):
    wrong_coords = []
    # Check hallway
    for col in range(1, 12):
        if burrow[1][col] != '.':
            wrong_coords.append(((1, col), burrow[1][col]))
    # Check room 1
    wrong_coords += get_wrong_letter_coords_in_room(burrow, 3, 'A')
    # Check room 2
    wrong_coords += get_wrong_letter_coords_in_room(burrow, 5, 'B')
    # Check room 3
    wrong_coords += get_wrong_letter_coords_in_room(burrow, 7, 'C')
    # Check room 4
    wrong_coords += get_wrong_letter_coords_in_room(burrow, 9, 'D')

    return wrong_coords

def can_move_into_room(burrow, col, letter, desired_letter):
    if letter != desired_letter:
        return False
    hit_empty_space = False
    for row in range(len(burrow) - 2, 1, -1):
        if hit_empty_space:
            if burrow[row][col] != '.':
                return False
        else:
            if burrow[row][col] == '.':
                hit_empty_space = True
            elif burrow[row][col] != desired_letter:
                return False
    return True

def can_move_through_coords(burrow, target, start):
    start_row, start_col = start
    letter = burrow[start_row][start_col]
    assert letter in 'ABCD'
    row, col = target

    # Can't move there if it's already occupied
    if burrow[row][col] != '.':
        return False
    # All letters can move through the hallway
    if row == 1:
        return True
    # We can move out of any room
    if row > 1 and start_row > row and col == start_col:
        return True
    # Don't move into a room unless you are the proper letter and it only contains the proper letter
    if row > 1:
        if col == 3:
            return can_move_into_room(burrow, 3, letter, 'A')
        if col == 5:
            return can_move_into_room(burrow, 5, letter, 'B')
        if col == 7:
            return can_move_into_room(burrow, 7, letter, 'C')
        if col == 9:
            return can_move_into_room(burrow, 9, letter, 'D')
    # We should have caught all cases by now
    assert False    


def can_stop_on_coords(burrow, target, start):
    start_row, start_col = start
    letter = burrow[start_row][start_col]
    assert letter in 'ABCD'
    row, col = target

    # If we can't move through it, we can't stop on it
    if not can_move_through_coords(burrow, target, start):
        return False
    # If the target is in the hallway, don't stop in front of a room
    if row == 1 and burrow[row+1][col] != '#':
        return False
    # If we started in the hallway, we have to move into a room
    if start_row == 1 and row == 1:
        return False
    # If the target is in a room, don't stop on our way out
    if row > 1 and start_row > row and col == start_col:
        return False
    # If the target is in a room, don't stop on our way in
    if row > 1 and burrow[row + 1][col] == '.':
        return False
    return True

def get_valid_next_coords(burrow, start):
    row, col = start
    letter = burrow[row][col]
    assert letter in 'ABCD'

    valid_coords = []
    visited = []
    coords_to_try = [(start, 0)]
    while len(coords_to_try) > 0:
        coords, steps = coords_to_try.pop()
        visited.append(coords)
        for adj_coords in get_adj_coords(coords, burrow):
            if adj_coords in visited:
                continue
            if not can_move_through_coords(burrow, adj_coords, start):
                continue
            coords_to_try.append((adj_coords, steps + 1))
            if can_stop_on_coords(burrow, adj_coords, start):
                valid_coords.append((adj_coords, steps + 1))
    return valid_coords

def get_burrow_after_move(burrow, start, end):
    start_row, start_col = start
    letter = burrow[start_row][start_col]
    assert letter in 'ABCD'
    end_row, end_col = end
    assert burrow[end_row][end_col] == '.'

    burrow_after_move = []
    for row in range(len(burrow)):
        line = burrow[row]
        if row == start_row and row == end_row:
            after_clear = line[:start_col] + '.' + line[start_col+1:]
            burrow_after_move.append(after_clear[:end_col] + letter + after_clear[end_col+1:])
        elif row == start_row:
            burrow_after_move.append(line[:start_col] + '.' + line[start_col+1:])
        elif row == end_row:
            burrow_after_move.append(line[:end_col] + letter + line[end_col+1:])
        else:
            burrow_after_move.append(line)
    return burrow_after_move

def get_possible_next_burrows(burrow):
    next_burrows = []
    for start_coords, letter in get_wrong_letter_coords(burrow):
        for end_coords, steps in get_valid_next_coords(burrow, start_coords):
            burrow_after_move = get_burrow_after_move(burrow, start_coords, end_coords)
            energy = ENERGY_PER_STEP[letter] * steps
            next_burrows.append((burrow_after_move, energy))
    return next_burrows

def burrow_equals(burrow_1, burrow_2):
    for burrow_1_line, burrow_2_line in zip(burrow_1, burrow_2):
        if burrow_1_line != burrow_2_line:
            return False
    return True

def burrow_as_string(burrow):
    burrow_str = burrow[0]
    for line in burrow[1:]:
        burrow_str += f'\n{line}'
    return burrow_str

def get_min_energy(burrow):
    burrow_costs = {burrow_as_string(burrow): 0}
    to_visit = [Node(burrow, 0)]

    # Construct the organized burrow
    organized_burrow = [
        '#############',
        '#...........#',
        '###A#B#C#D###',
        '  #########'
    ]
    while len(organized_burrow) < len(burrow):
        organized_burrow.insert(3, '  #A#B#C#D#')

    # Use Dijkstra's to find the minimum energy
    burrow_history = {burrow_as_string(burrow): [to_visit[0]]}
    while len(to_visit) > 0:
        node = heappop(to_visit)
        burrow_str = burrow_as_string(node.burrow)
        # if burrow_str in burrow_costs:
        #     continue
        # burrow_costs[burrow_str] = node.energy
        if burrow_equals(node.burrow, organized_burrow):
            print('Found minimum energy to organize:')
            for node_step in burrow_history[burrow_str]:
                print(f'Energy: {node_step.energy}')
                print_burrow(node_step.burrow)
            return node.energy
        for next_burrow, energy in get_possible_next_burrows(node.burrow):
            adj_node = Node(next_burrow, node.energy + energy)
            burrow_str = burrow_as_string(node.burrow)
            adj_burrow_str = burrow_as_string(adj_node.burrow)
            assert burrow_str in burrow_history
            history = burrow_history[burrow_str]
            adj_history = history[:]
            adj_history.append(adj_node)
            if adj_burrow_str in burrow_costs and burrow_costs[adj_burrow_str] <= adj_node.energy:
                continue
            burrow_costs[adj_burrow_str] = adj_node.energy
            burrow_history[adj_burrow_str] = adj_history
            heappush(to_visit, adj_node)

def print_burrow(burrow):
    for line in burrow:
        print(line)
    print('')
    
def main():
    # Load in the data
    # burrow = load_input('day23/test_input.txt')
    burrow = load_input('day23/puzzle_input.txt')

    print('--- Part 1 ---')
    print(f'Minimum energy to organize original: {get_min_energy(burrow)}')

    print('')
    burrow.insert(3, '  #D#C#B#A#')
    burrow.insert(4, '  #D#B#A#C#')

    print('--- Part 2 ---')
    # print_burrow(burrow)
    print(f'Minimum energy to organize unfolded: {get_min_energy(burrow)}')
    print(f'')
    
if __name__ == '__main__':
    main()