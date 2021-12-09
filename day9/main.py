from errno import ENOENT
from os import strerror
from os.path import exists
from typing import List, Tuple

import numpy as np

def load_input(path: str) -> List[Tuple[List[str], List[str]]]:
    '''Loads the input and returns it as a list (digits, value) tuples.'''
    if not exists(path):
        raise FileNotFoundError(ENOENT, strerror(ENOENT), path)
    
    with open(path, 'r') as input_file:
        height_map = []
        for line in input_file:
            height_map.append([int(digit) for digit in line.strip()])
        return np.array(height_map)
    
def get_adjacent_coords(coords, shape):
    adjacent_coords = []
    row, col = coords
    num_rows, num_cols = shape

    if row > 0:
        adjacent_coords.append((row - 1, col))
    if row < num_rows - 1:
        adjacent_coords.append((row + 1, col))
    if col > 0:
        adjacent_coords.append((row, col - 1))
    if col < num_cols - 1:
        adjacent_coords.append((row, col + 1))
    
    return adjacent_coords

def is_local_min(coords, height_map):
    row, col = coords
    for adjacent_coord in get_adjacent_coords(coords, height_map.shape):
        adj_row, adj_col = adjacent_coord
        if height_map[adj_row, adj_col] < height_map[row, col]:
            return False
    return True

def get_total_risk_level(height_map):
    total_risk_level = 0
    for row in range(height_map.shape[0]):
        for col in range(height_map.shape[1]):
            if is_local_min((row, col), height_map):
                total_risk_level += height_map[row, col] + 1
    return total_risk_level

def main():
    # Load in the data
    height_map = load_input('day9/puzzle_input.txt')

    print('--- Part 1 ---')
    print(f'The total risk level is {get_total_risk_level(height_map)}.')
    
    print('')

    print('--- Part 2 ---')
    
if __name__ == '__main__':
    main()