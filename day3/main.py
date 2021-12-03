from errno import ENOENT
from os import strerror
from os.path import exists
from typing import List, Tuple

import numpy as np

def load_input(path: str) -> np.ndarray:
    '''Loads the input and returns it as a 2D NumPy array of 1s and 0s.'''
    if not exists(path):
        raise FileNotFoundError(ENOENT, strerror(ENOENT), path)
    
    with open(path, 'r') as input_file:
        data = []
        for line in input_file.readlines():
            row = []
            for bit in line.strip():
                row.append(int(bit))
            data.append(row)
        return np.array(data)

def bits_to_decimal(bits: np.ndarray) -> int:
    '''Given an array of 1s and 0s, returns the decimal value of the bits.'''
    value = 0
    for bit in bits:
        value = (value << 1) + bit
    return value

def get_most_common(data: np.ndarray) -> np.ndarray:
    '''Returns the most common bit in each postion.'''
    bits = []
    for pos in range(data.shape[1]):
        bits.append(np.bincount(data[:, pos]).argmax())
    return np.array(bits)

def get_least_common(data: np.ndarray) -> np.ndarray:
    '''Returns the least common bit in each postion.'''
    bits = []
    for pos in range(data.shape[1]):
        bits.append(np.bincount(data[:, pos]).argmin())
    return np.array(bits)

def keep_most_common(data: np.ndarray, pos: int) -> np.ndarray:
    '''Keeps only the data points where the given position contains the most common value.'''
    # If most common and least common are equal, keep 1s
    most_common = get_most_common(data)
    least_common = get_least_common(data)
    if most_common[pos] == least_common[pos]:
        filter = data[:, pos] == 1
    else:
        filter = data[:, pos] == most_common[pos]
    return data[filter]

def keep_least_common(data: np.ndarray, pos: int) -> np.ndarray:
    '''Keeps only the data points where the given position contains the least common value.'''
    # If most common and least common are equal, keep 0s
    most_common = get_most_common(data)
    least_common = get_least_common(data)
    if most_common[pos] == least_common[pos]:
        filter = data[:, pos] == 0
    else:
        filter = data[:, pos] == least_common[pos]
    return data[filter]

def main():
    # # Load in the data
    data = load_input('day3/puzzle_input.txt')

    get_most_common(data)
    
    print('--- Part 1 ---')
    gamma_rate = bits_to_decimal(get_most_common(data))
    epsilon_rate = bits_to_decimal(get_least_common(data))
    print(f'Gamma rate: {gamma_rate}')
    print(f'Epsilon rate: {epsilon_rate}')
    print(f'Power consumption: {gamma_rate * epsilon_rate}')
    print('')

    print('--- Part 2 ---')
    oxygen_list = data
    for pos in range(data.shape[1]):
        oxygen_list = keep_most_common(oxygen_list, pos)
        if len(oxygen_list) == 1:
            break
    oxygen_rating = bits_to_decimal(oxygen_list[0])
    print(f'Oxygen generator rating: {oxygen_rating}')

    co2_list = data
    for pos in range(data.shape[1]):
        co2_list = keep_least_common(co2_list, pos)
        if len(co2_list) == 1:
            break
    co2_rating = bits_to_decimal(co2_list[0])
    print(f'CO2 scrubber rating: {co2_rating}')
    print(f'Life support rating: {oxygen_rating * co2_rating}')

if __name__ == '__main__':
    main()