from errno import ENOENT
from os import strerror
from os.path import exists
from typing import List

def load_input(path: str) -> List[int]:
    '''Loads the input and returns it as a list of integers.'''
    if not exists(path):
        raise FileNotFoundError(ENOENT, strerror(ENOENT), path)
    
    with open(path, 'r') as input_file:
        str_data = input_file.readlines()
        int_data = [int(line.strip()) for line in str_data]
        return int_data

def count_increases(data: List[int], span: int = 1) -> int:
    '''Counts the number of times a value in the data is greater than the preceding value.'''
    num_increases = 0
    for first, second in zip(data[:-span], data[span:]):
        if second > first:
            num_increases += 1
    return num_increases

def main():
    # Load in the data
    data = load_input('day1/puzzle_input.txt')
    
    print('--- Part 1 ---')
    print(f'The depth increases {count_increases(data)} times.')
    print('')

    print('--- Part 2 ---')
    print(f'The three-sized sliding window increases {count_increases(data, 3)} times.')


if __name__ == '__main__':
    main()