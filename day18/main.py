from errno import ENOENT
from os import strerror
from os.path import exists
from typing import List, Union

SFNum = List[Union[str, int]]

def load_input(path: str) -> List[SFNum]:
    '''Loads the input and returns it as a list of snailfish numbers.'''
    if not exists(path):
        raise FileNotFoundError(ENOENT, strerror(ENOENT), path)
    
    with open(path, 'r') as input_file:
        sf_nums = []
        for line in input_file:
            sf_nums.append(str_to_sf_num(line.strip()))
        return sf_nums

def str_to_sf_num(sf_str: str) -> SFNum:
    '''Converts a string to a snailfish number.'''
    sf_num = []
    number_in_progress = ''
    for char in sf_str:
        if char in '[,]':
            if number_in_progress != '':
                sf_num.append(int(number_in_progress))
                number_in_progress = ''
            if char != ',':
                sf_num.append(char)
        else:
            number_in_progress += char
    return sf_num

def get_sf_str(sf_num: SFNum) -> str:
    '''Converts a snailfish number to a string'''
    sf_str = ''
    prev_element = None
    for element in sf_num:
        if prev_element is not None and prev_element != '[' and element != ']':
            sf_str += ','
        sf_str += str(element)
        prev_element = element
    return(sf_str)

def explode(sf_num: SFNum, idx: int) -> SFNum:
    '''Explodes the pair starting at the given index.'''
    left_value = sf_num[idx + 1]
    right_value = sf_num[idx + 2]
    new_sf_num = sf_num[:idx] + [0] + sf_num[idx+4:]
    for left_idx in range(idx - 1, -1, -1):
        if isinstance(new_sf_num[left_idx], int):
            new_sf_num[left_idx] += left_value
            break
    for right_idx in range(idx + 1, len(new_sf_num)):
        if isinstance(new_sf_num[right_idx], int):
            new_sf_num[right_idx] += right_value
            break
    return new_sf_num

def split(sf_num: SFNum, idx: int) -> SFNum:
    '''Splits the regular number at the given index.'''
    left_value = sf_num[idx] // 2
    right_value = sf_num[idx] - left_value
    return sf_num[:idx] + ['[', left_value, right_value, ']'] + sf_num[idx+1:]
    
def reduce(sf_num: SFNum) -> SFNum:
    '''Reduces the give snailfish number.'''
    nesting_level = 0
    for idx in range(len(sf_num)):
        element = sf_num[idx]
        if element == '[':
            nesting_level += 1
            if nesting_level == 5:
                return reduce(explode(sf_num, idx))
        elif element == ']':
            nesting_level -= 1
    for idx in range(len(sf_num)):
        element = sf_num[idx]
        if isinstance(element, int) and element >= 10:
            return reduce(split(sf_num, idx))
    return sf_num

def get_magnitude(sf_num: SFNum) -> int:
    '''Computes the magnitude of the snailfish number.'''
    if len(sf_num) == 1:
        return sf_num[0]
    for idx in range(1, len(sf_num)):
        if isinstance(sf_num[idx-1], int) and isinstance(sf_num[idx], int):
            magnitude = (3 * sf_num[idx-1]) + (2 * sf_num[idx])
            return get_magnitude(sf_num[:idx-2] + [magnitude] + sf_num[idx+2:])

def add_sf_nums(sf_num_1, sf_num_2):
    '''Adds two snailfish number and reduces the sum.'''
    return reduce(['['] + sf_num_1 + sf_num_2 + [']'])
        
def main():
    # Load in the data
    # sf_nums = load_input('day18/test_input.txt')
    sf_nums = load_input('day18/puzzle_input.txt')

    print('--- Part 1 ---')
    sf_sum = sf_nums[0]
    for sf_num in sf_nums[1:]:
        sf_sum = add_sf_nums(sf_sum, sf_num)
    print(f'Magnitude of the final sum: {get_magnitude(sf_sum)}')

    print('')

    print('--- Part 2 ---')
    max_magnitude = 0
    for sf_num_1 in sf_nums:
        for sf_num_2 in sf_nums:
            max_magnitude = max(max_magnitude, get_magnitude(add_sf_nums(sf_num_1, sf_num_2)))
    print(f'Maximum magnitude: {max_magnitude}')
    
if __name__ == '__main__':
    main()