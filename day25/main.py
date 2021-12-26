from errno import ENOENT
from os import strerror
from os.path import exists
from typing import List

FloorMap = List[List[str]]

def load_input(path: str) -> FloorMap:
    '''Loads the input and returns it as a grid of characters.'''
    if not exists(path):
        raise FileNotFoundError(ENOENT, strerror(ENOENT), path)
    
    with open(path, 'r') as input_file:
        return [[char for char in line.strip()] for line in input_file]

def floor_maps_equal(fm_1: FloorMap, fm_2: FloorMap) -> bool:
    '''Checks for equality between two floor maps.'''
    if fm_1 is None and fm_2 is None:
        return True
    if fm_1 is None or fm_2 is None:
        return False
    for line_1, line_2 in zip(fm_1, fm_2):
        for char_1, char_2 in zip(line_1, line_2):
            if char_1 != char_2:
                return False
    return True

def copy_floor_map(floor_map: FloorMap) -> FloorMap:
    '''Returns a copy of the floor map.'''
    return [[char for char in line] for line in floor_map]

def move_east_herd(floor_map: FloorMap) -> FloorMap:
    '''Moves all east-moving sea cucumbers.'''
    next_floor_map = copy_floor_map(floor_map)
    height = len(floor_map)
    width = len(floor_map[0])
    for row in range(height):
        for col in range(width):
            # Only consider east-moving sea cucumbers
            if floor_map[row][col] != '>':
                continue
            # Check for empty space in front
            if floor_map[row][(col+1) % width] == '.':
                # Move the sea cucumber
                next_floor_map[row][col] = '.'
                next_floor_map[row][(col+1) % width] = '>'
    return next_floor_map

def move_south_herd(floor_map: FloorMap) -> FloorMap:
    '''Moves all south-moving sea cucumbers.'''
    next_floor_map = copy_floor_map(floor_map)
    height = len(floor_map)
    width = len(floor_map[0])
    for row in range(height):
        for col in range(width):
            # Only consider east-moving sea cucumbers
            if floor_map[row][col] != 'v':
                continue
            # Check for empty space in front
            if floor_map[(row+1) % height][col] == '.':
                # Move the sea cucumber
                next_floor_map[row][col] = '.'
                next_floor_map[(row+1) % height][col] = 'v'
    return next_floor_map

def perform_step(floor_map: FloorMap) -> FloorMap:
    '''Performs a single step, moving both herds of sea cucumbers.'''
    after_east_herd = move_east_herd(floor_map)
    after_south_herd = move_south_herd(after_east_herd)
    return after_south_herd

def main():
    # Load in the data
    # floor_map = load_input('day25/test_input.txt')
    floor_map = load_input('day25/puzzle_input.txt')

    print('--- Part 1 ---')
    prev_floor_map = None
    current_floor_map = copy_floor_map(floor_map)
    step = 0
    while not floor_maps_equal(current_floor_map, prev_floor_map):
        prev_floor_map = current_floor_map
        current_floor_map = perform_step(current_floor_map)
        step += 1
    print(f'The sea cucumbers did not move during step {step}')
    
if __name__ == '__main__':
    main()