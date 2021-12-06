from errno import ENOENT
from os import strerror
from os.path import exists
from typing import List, Tuple
from vent import Vent

def load_input(path: str) -> List[Vent]:
    '''Loads the input and returns it as a list of Vents.'''
    if not exists(path):
        raise FileNotFoundError(ENOENT, strerror(ENOENT), path)
    
    with open(path, 'r') as input_file:
        vents = []
        for line in input_file:
            points = line.strip().split(' -> ')
            p1 = points[0].split(',')
            p2 = points[1].split(',')
            vents.append(Vent(
                x1=int(p1[0]),
                y1=int(p1[1]),
                x2=int(p2[0]),
                y2=int(p2[1])
            ))
        return vents

def mark_vent(grid: List[List[int]], vent: Vent) -> List[List[int]]:
    '''Marks the given vent on a grid.'''
    for point in vent.get_covered_points():
        grid[point[0]][point[1]] += 1
    return grid

def count_at_least(grid: List[List[int]], at_least: int) -> int:
    '''Counts the number of grid locations covered by at least the given number of vents.'''
    count = 0
    for row in grid:
        for value in row:
            if value >= at_least:
                count += 1
    return count

def main():
    # Load in the data
    vents = load_input('day5/puzzle_input.txt')
    grid = [([0] * 1000) for _ in range(1000)]

    print('--- Part 1 ---')
    for vent in vents:
        if vent.is_horizontal() or vent.is_vertical():
            grid = mark_vent(grid, vent)
    print(f'Considering only horizontal and vertical vents, there are {count_at_least(grid, 2)} spots that are at least 2.')
            
    print('')
    grid = [([0] * 1000) for _ in range(1000)]

    print('--- Part 2 ---')
    for vent in vents:
        grid = mark_vent(grid, vent)
    print(f'Including all vents, there are {count_at_least(grid, 2)} spots that are at least 2.')

    
if __name__ == '__main__':
    main()