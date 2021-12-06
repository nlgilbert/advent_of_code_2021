from errno import ENOENT
from os import strerror
from os.path import exists
from typing import List

def load_input(path: str) -> List[int]:
    '''Loads the input and returns it as a list of the number of lanternfish on each day count.'''
    if not exists(path):
        raise FileNotFoundError(ENOENT, strerror(ENOENT), path)
    
    with open(path, 'r') as input_file:
        lanternfish = [int(days) for days in input_file.readline().strip().split(',')]
        fish_count = [0] * 9
        for fish in lanternfish:
            fish_count[fish] += 1
        return fish_count

def simulate_day(fish_count: List[int]) -> List[int]:
    '''Simulate a day for the lanternfish.'''
    next_day = [0] * 9
    for day in range(8):
        next_day[day] = fish_count[day + 1]
    next_day[8] = fish_count[0]
    next_day[6] += fish_count[0]
    return next_day

def main():
    # Load in the data
    fish_count = load_input('day6/puzzle_input.txt')

    print('--- Part 1 ---')
    for day in range(80):
        fish_count = simulate_day(fish_count)
    print(f'After 80 days there are {sum(fish_count)} lanternfish.')
    
    print('')
    fish_count = load_input('day6/puzzle_input.txt')

    print('--- Part 2 ---')
    for day in range(256):
        fish_count = simulate_day(fish_count)
    print(f'After 256 days there are {sum(fish_count)} lanternfish.')

    
if __name__ == '__main__':
    main()