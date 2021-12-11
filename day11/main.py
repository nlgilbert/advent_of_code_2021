from errno import ENOENT
from os import strerror
from os.path import exists
from typing import List, Tuple

import numpy as np

def load_input(path: str) -> np.ndarray:
    '''Loads the input and returns it as an np.ndarray of ints.'''
    if not exists(path):
        raise FileNotFoundError(ENOENT, strerror(ENOENT), path)
    
    with open(path, 'r') as input_file:
        lines = [line.strip() for line in input_file]
        return np.array([[int(char) for char in line] for line in lines])

def get_adjacent_coords(coords: Tuple[int, int]) -> List[Tuple[int, int]]:
    '''Returns a list of all coordinates adjacent to the given coordinate (including diagonals).'''
    adj_coords = []
    row, col = coords

    for i in range(row-1, row+2):
        for j in range(col-1, col+2):
            if i < 0 or i > 9:
                continue
            if j < 0 or j > 9:
                continue
            adj_coords.append((i, j))
    return adj_coords

def flash(grid: np.ndarray, coords: Tuple[int, int], flashed: List[Tuple[int, int]]) -> None:
    '''Flashes the octopus at the given coordinate, flashing its neighbors if necessary.'''
    if coords in flashed:
        return
    flashed.append(coords)
    for adj_coords in get_adjacent_coords(coords):
        grid[adj_coords] += 1
        if grid[adj_coords] > 9:
            flash(grid, adj_coords, flashed)

def do_step(grid: np.ndarray) -> int:
    '''Performs a single step in the grid, returning the number of flashes.'''
    for i in range(10):
        for j in range(10):
            grid[i, j] += 1
    
    flashed = []
    for i in range(10):
        for j in range(10):
            if grid[i, j] > 9:
                flash(grid, (i, j), flashed)
    
    for coord in flashed:
        grid[coord] = 0
    
    return len(flashed)

def main():
    # Load in the data
    # grid = load_input('day11/test_input.txt')
    grid = load_input('day11/puzzle_input.txt')

    print('--- Part 1 ---')
    num_flashes = 0
    for i in range(100):
        num_flashes += do_step(grid)
    print(f'Number of flashes after 100 steps: {num_flashes}')
    
    print('')
    # grid = load_input('day11/test_input.txt')
    grid = load_input('day11/puzzle_input.txt')

    print('--- Part 2 ---')
    step = 1
    while do_step(grid) < 100:
        step += 1
    print(f'All octopuses flash together at step {step}')
    
if __name__ == '__main__':
    main()