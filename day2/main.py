from errno import ENOENT
from os import strerror
from os.path import exists
from typing import List, Tuple

def load_input(path: str) -> List[str]:
    '''Loads the input and returns it as a list of instructions.'''
    if not exists(path):
        raise FileNotFoundError(ENOENT, strerror(ENOENT), path)
    
    with open(path, 'r') as input_file:
        return [line.strip() for line in input_file.readlines()]

def apply_steps_naive(steps: List[str]) -> Tuple[int, int]:
    '''Applies the list of steps consecutively, returning the final position.'''
    pos_h = 0
    pos_d = 0
    for step in steps:
        tokens = step.split(' ')
        direction = tokens[0]
        magnitude = int(tokens[1])
        if direction == 'forward':
            pos_h += magnitude
        elif direction == 'up':
            pos_d -= magnitude
        elif direction == 'down':
            pos_d += magnitude
    return (pos_h, pos_d)

def apply_steps_with_aim(steps: List[str]) -> Tuple[int, int]:
    '''Applies the list of steps consecutively, returning the final position.'''
    pos_h = 0
    pos_d = 0
    aim = 0
    for step in steps:
        tokens = step.split(' ')
        direction = tokens[0]
        magnitude = int(tokens[1])
        if direction == 'forward':
            pos_h += magnitude
            pos_d += aim * magnitude
        elif direction == 'up':
            aim -= magnitude
        elif direction == 'down':
            aim += magnitude
    return (pos_h, pos_d)


def main():
    # Load in the data
    data = load_input('day2/puzzle_input.txt')
    
    print('--- Part 1 ---')
    pos_h, pos_d = apply_steps_naive(data)
    print(f'Final position is horizontal: {pos_h}, depth: {pos_d}')
    print(f'The product of our position components is {pos_h * pos_d}')
    print('')

    print('--- Part 2 ---')
    pos_h, pos_d = apply_steps_with_aim(data)
    print(f'Final position is horizontal: {pos_h}, depth: {pos_d}')
    print(f'The product of our position components is {pos_h * pos_d}')
    


if __name__ == '__main__':
    main()