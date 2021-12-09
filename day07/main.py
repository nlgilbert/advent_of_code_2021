from errno import ENOENT
from os import strerror
from os.path import exists
from typing import List

import numpy as np

def load_input(path: str) -> List[int]:
    '''Loads the input and returns it as a list of the position of each crab.'''
    if not exists(path):
        raise FileNotFoundError(ENOENT, strerror(ENOENT), path)
    
    with open(path, 'r') as input_file:
        return [int(value) for value in input_file.readline().strip().split(',')]

def get_fuel_for_position(crab_positions, position):
    '''Gets the amount of fuel needed to align all the crabs at the given position
    using the naive fuel consumption model.'''
    total_fuel = 0
    for crab_pos in crab_positions:
        total_fuel += abs(crab_pos - position)
    return total_fuel

def get_fuel_for_position_increasing(crab_positions, position):
    '''Gets the amount of fuel needed to align all the crabs at the given position
    using the increasing fuel consumption model.'''
    total_fuel = 0
    for crab_pos in crab_positions:
        total_fuel += triangle_number(abs(crab_pos - position))
    return total_fuel

def triangle_number(n: int) -> int:
    '''Returns the nth triangle number.'''
    return sum(range(n+1))

def main():
    # Load in the data
    crab_positions = load_input('day07/puzzle_input.txt')

    print('--- Part 1 ---')
    min_fuel = None
    min_fuel_position = None
    for position in range(np.min(crab_positions), np.max(crab_positions) + 1):
        fuel_for_pos = get_fuel_for_position(crab_positions, position)
        if min_fuel is None or fuel_for_pos < min_fuel:
            min_fuel = fuel_for_pos
            min_fuel_position = position
    print(f'The minimum fuel used is {min_fuel} for position {min_fuel_position}.')
    
    print('')

    print('--- Part 2 ---')
    min_fuel = None
    min_fuel_position = None
    for position in range(np.min(crab_positions), np.max(crab_positions) + 1):
        fuel_for_pos = get_fuel_for_position_increasing(crab_positions, position)
        if min_fuel is None or fuel_for_pos < min_fuel:
            min_fuel = fuel_for_pos
            min_fuel_position = position
    print(f'The minimum fuel used is {min_fuel} for position {min_fuel_position}.')
    
if __name__ == '__main__':
    main()