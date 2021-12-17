from errno import ENOENT
from os import strerror
from os.path import exists
from typing import List, Tuple

from heapq import heappop, heappush
import numpy as np
from node import Node

def load_input(path: str) -> np.ndarray:
    '''Loads the input and returns it as a grid of risks.'''
    if not exists(path):
        raise FileNotFoundError(ENOENT, strerror(ENOENT), path)
    
    with open(path, 'r') as input_file:
        return np.array([[int(char) for char in line.strip()] for line in input_file])
        
def convert_to_risk_map(risks: np.ndarray) -> List[List[Node]]:
    '''Converts a grid of risks into a risk map of Nodes.'''
    risk_map = []
    for row in range(risks.shape[0]):
        map_row = []
        for col in range(risks.shape[1]):
            map_row.append(Node((row, col), risks[row, col]))
        risk_map.append(map_row)
    return risk_map

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

def get_min_risk_path(risk_map: List[List[Node]]) -> int:
    '''Uses Dijkstra's algorithm to compute the risk of the minimum risk path through the risk map.'''
    start = risk_map[0][0]
    end = risk_map[-1][-1]
    height = len(risk_map)
    width = len(risk_map[0])
    start.visited = True
    start.dist = 0
    queue = [start]
    while True:
        node = heappop(queue)
        if node == end:
            return node.dist
        for coords in get_adjacent_coords(node.coords, (height, width)):
            row, col = coords
            adj_node = risk_map[row][col]
            if adj_node.visited:
                continue
            adj_node.visited = True
            adj_node.dist = node.dist + adj_node.risk
            heappush(queue, adj_node)

def expand_risks(risks: np.ndarray) -> np.ndarray:
    '''Expands the grid by a factor of 5 as needed for Part 2.'''
    expanded_risk_map = []
    for tile_row in range(5):
        for i in range(risks.shape[0]):
            row = []
            for tile_col in range(5):
                for j in range(risks.shape[1]):
                    risk = ((risks[i, j] + tile_row + tile_col - 1) % 9) + 1
                    row.append(risk)
            expanded_risk_map.append(row)
    return np.array(expanded_risk_map)

def main():
    # Load in the data
    # risk_map = load_input('day15/test_input.txt')
    risks = load_input('day15/puzzle_input.txt')

    print('--- Part 1 ---')
    risk_map = convert_to_risk_map(risks)
    print(f'The minimum path of the original risk_map has risk {get_min_risk_path(risk_map)}')

    print('')

    print('--- Part 2 ---')
    risk_map = convert_to_risk_map(expand_risks(risks))
    print(f'The minimum path of the extended risk_map has risk {get_min_risk_path(risk_map)}')
    
if __name__ == '__main__':
    main()