from errno import ENOENT
from os import strerror
from os.path import exists
from typing import Dict, List, Tuple
import heapq as hq

import numpy as np

def load_input(path: str) -> np.ndarray:
    '''Loads the input and returns it as a grid of risks.'''
    if not exists(path):
        raise FileNotFoundError(ENOENT, strerror(ENOENT), path)
    
    with open(path, 'r') as input_file:
        return np.array([[int(char) for char in line.strip()] for line in input_file])     
        
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

def search(m):
    h,w = np.shape(m)
    q = [(0,(0,0))]     # risk, starting point
    while q:
        risk, (x,y) = hq.heappop(q)
        if (x,y) == (w-1,h-1):
            return risk
        for x,y in [(x,y+1),(x+1,y),(x,y-1),(x-1,y)]:
            if x >= 0 and x < w and y >= 0 and y < h and m[y][x] >= 0:
                hq.heappush(q, (risk+(m[y][x] % 9)+1, (x,y)))
                m[y][x] = -1    # mark as seen

def get_cost_map(grid):
    cost_map = np.zeros_like(grid)
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if i == 0 and j == 0:
                cost_map[i, j] = 0
            elif i == 0:
                cost_map[i, j] = cost_map[i, j-1] + grid[i, j]
            elif j == 0:
                cost_map[i, j] = cost_map[i-1, j] + grid[i, j]
            else:
                cost_map[i, j] = min(cost_map[i-1, j], cost_map[i, j-1]) + grid[i, j]

    changed = True
    num_changed = 0
    while changed:
        print(f'num_changed = {num_changed}')
        changed = False

        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                adj_coords = get_adjacent_coords((i, j), cost_map.shape)
                for coords in adj_coords:
                    new_risk = cost_map[coords] + grid[i, j]
                    if new_risk < cost_map[i, j]:
                        cost_map[i, j] = new_risk
                        changed = True

        num_changed += 1
    
    return cost_map

def expand_grid(grid):
    expanded_grid = []
    for tile_row in range(5):
        for i in range(grid.shape[0]):
            row = []
            for tile_col in range(5):
                for j in range(grid.shape[1]):
                    risk = ((grid[i, j] + tile_row + tile_col - 1) % 9) + 1
                    row.append(risk)
            expanded_grid.append(row)
    return np.array(expanded_grid)


def main():
    # Load in the data
    # grid = load_input('day15/test_input.txt')
    grid = load_input('day15/puzzle_input.txt')

    print('--- Part 1 ---')
    # cost_map = get_cost_map(grid)
    print(f'The minimum path of the original grid has risk {search(grid - 1)}')

    print('')

    print('--- Part 2 ---')
    expanded_grid = expand_grid(grid)
    # for row in expanded_nodes:
    #     print(row)
    # cost_map = get_cost_map(expanded_nodes)
    print(f'The minimum path of the extended grid has risk {search(expanded_nodes - 1)}')
    
if __name__ == '__main__':
    main()