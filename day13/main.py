from errno import ENOENT
from os import name, strerror
from os.path import exists
from typing import List, Tuple

import numpy as np

def load_input(path: str) -> Tuple[np.ndarray, List[str, int]]:
    '''Loads the input and returns it as a grid and a list of folds.'''
    if not exists(path):
        raise FileNotFoundError(ENOENT, strerror(ENOENT), path)
    
    with open(path, 'r') as input_file:
        dots = []
        while (line := input_file.readline().strip()) != '':
            coords = line.split(',')
            dots.append((int(coords[1]), int(coords[0])))
        folds = []
        while (line := input_file.readline().strip()) != '':
            axis = line.split()[-1].split('=')
            folds.append((axis[0], int(axis[1])))
    
    # Create a grid
    y_max = np.max([dot[0] for dot in dots])
    x_max = np.max([dot[1] for dot in dots])
    grid = []
    for y in range(y_max + 1):
        row = []
        for x in range(x_max + 1):
            row.append(False)
        grid.append(row)
    
    # Add the dots to the grid
    grid = np.array(grid)
    for dot in dots:
        grid[dot] = True
    return grid, folds

def do_fold(grid: np.ndarray, fold: Tuple[str, int]) -> np.ndarray:
    '''Performs a fold on the grid, returning the folded grid.'''
    dir = fold[0]
    value = fold[1]

    # Get the size of the folded grid
    y_size = grid.shape[0]
    x_size = grid.shape[1]
    if dir == 'x':
        x_size = value
    else:
        y_size = value

    # Populate the folded grid
    folded_grid = []
    for y in range(y_size):
        row = []
        for x in range(x_size):
            if dir == 'x':
                offset = value - x
                is_dot = grid[y, x] or grid[y, value + offset]
            else:
                offset = value - y
                is_dot = grid[y, x] or grid[value + offset, x]
            row.append(is_dot)
        folded_grid.append(row)
    return np.array(folded_grid)

def count_dots(grid: np.ndarray) -> int:
    '''Counts the number of dots in the grid.'''
    return np.count_nonzero(grid)

def print_grid(grid: np.ndarray) -> None:
    '''Prints the grid.'''
    for y in range(grid.shape[0]):
        row = ''
        for x in range(grid.shape[1]):
            if grid[y, x]:
                row += '#'
            else:
                row += ' '
        print(row)

def main():
    # Load in the data
    # grid, folds = load_input('day13/test_input.txt')
    grid, folds = load_input('day13/puzzle_input.txt')

    print('--- Part 1 ---')
    grid = do_fold(grid, folds[0])
    print(f'After 1 fold there are {count_dots(grid)} dots.')
    
    print('')
    # grid, folds = load_input('day13/test_input.txt')
    grid, folds = load_input('day13/puzzle_input.txt')

    print('--- Part 2 ---')
    for fold in folds:
        grid = do_fold(grid, fold)
    print_grid(grid)
    
if __name__ == '__main__':
    main()