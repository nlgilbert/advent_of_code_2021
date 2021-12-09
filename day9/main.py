from errno import ENOENT
from os import strerror
from os.path import exists
from typing import List, Tuple

import numpy as np

def load_input(path: str) -> np.ndarray:
    '''Loads the input and returns it as a list (digits, value) tuples.'''
    if not exists(path):
        raise FileNotFoundError(ENOENT, strerror(ENOENT), path)
    
    with open(path, 'r') as input_file:
        height_map = []
        for line in input_file:
            height_map.append([int(digit) for digit in line.strip()])
        return np.array(height_map)
    
def get_adjacent_coords(coords: Tuple[int, int], shape: Tuple[int, int]) -> List[Tuple[int, int]]:
    '''Returns a list of all coordinates adjacent to the given coordinate.'''
    adj_coords = []
    row, col = coords
    num_rows, num_cols = shape

    if row > 0:
        adj_coords.append((row - 1, col))
    if row < num_rows - 1:
        adj_coords.append((row + 1, col))
    if col > 0:
        adj_coords.append((row, col - 1))
    if col < num_cols - 1:
        adj_coords.append((row, col + 1))
    
    return adj_coords

def is_local_min(coords: Tuple[int, int], height_map: np.ndarray) -> bool:
    '''Checks if the given coordinates describe a local minimum in the height map.'''
    for adj_coords in get_adjacent_coords(coords, height_map.shape):
        if height_map[adj_coords] <= height_map[coords]:
            return False
    return True

def get_local_mins(height_map: np.ndarray) -> List[Tuple[int, int]]:
    '''Returns a list of the coordinates of all local minima in the height map.'''
    local_mins = []
    for row in range(height_map.shape[0]):
        for col in range(height_map.shape[1]):
            if is_local_min((row, col), height_map):
                local_mins.append((row, col))
    return local_mins

def get_basin(local_min: Tuple[int, int], height_map: np.ndarray) -> List[Tuple[int, int]]:
    '''Gets a list of all coordinates in the basin containing the given local minimum.'''
    basin_coords = [local_min]
    to_search = get_adjacent_coords(local_min, height_map.shape)
    while len(to_search) > 0:
        coords = to_search.pop()
        if height_map[coords] == 9:
            continue
        basin_coords.append(coords)
        for adj_coords in get_adjacent_coords(coords, height_map.shape):
            if adj_coords not in basin_coords and adj_coords not in to_search:
                to_search.append(adj_coords)
    return basin_coords


def main():
    # Load in the data
    height_map = load_input('day9/puzzle_input.txt')

    print('--- Part 1 ---')
    total_risk_level = 0
    for local_min in get_local_mins(height_map):
        total_risk_level += height_map[local_min] + 1
    print(f'The total risk level is {total_risk_level}.')
    
    print('')

    print('--- Part 2 ---')
    local_mins = get_local_mins(height_map)
    basin_sizes = sorted([len(get_basin(local_min, height_map)) for local_min in local_mins])
    print(f'The product of the three largest basin sizes is {basin_sizes[-1] * basin_sizes[-2] * basin_sizes[-3]}.')

    
if __name__ == '__main__':
    main()