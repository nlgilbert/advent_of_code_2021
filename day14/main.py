from errno import ENOENT
from os import name, strerror
from os.path import exists
from typing import Dict, Tuple

import numpy as np

def load_input(path: str) -> Tuple[str, Dict[str, str]]:
    '''Loads the input and returns it as a polymer and a set of rules.'''
    if not exists(path):
        raise FileNotFoundError(ENOENT, strerror(ENOENT), path)
    
    with open(path, 'r') as input_file:
        # Read in the polymer
        polymer = input_file.readline().strip()

        input_file.readline()   # Read the blank line

        # Read in the rules
        rules = {}
        while (line := input_file.readline().strip()) != '':
            rule = line.split(' -> ')
            rules[rule[0]] = rule[1]
        
        return polymer, rules

def polymer_to_pairs(polymer: str) -> Dict[str, int]:
    '''Converts the polymer to a set of counts indicating the number of occurances of each pair of letters.'''
    pairs = {}
    for letter1 in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        for letter2 in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            pair = f'{letter1}{letter2}'
            pairs[pair] = 0
    for idx in range(len(polymer) - 1):
        pair = polymer[idx:idx+2]
        pairs[pair] += 1
    return pairs

def apply_rules(pairs: Dict[str, int], rules: Dict[str, str]) -> Dict[str, int]:
    '''Applies the rules to the polymer described by pairs, returning a new set of pairs.'''
    new_pairs = {}
    for pair in pairs:
        new_pairs[pair] = 0
    
    for pair in pairs:
        letter1 = pair[0]
        letter2 = pair[1]
        if pair in rules:
            middle_letter = rules[pair]
            new_pairs[f'{letter1}{middle_letter}'] += pairs[pair]
            new_pairs[f'{middle_letter}{letter2}'] += pairs[pair]
        else:
            new_pairs[pair] += pairs[pair]
    
    return new_pairs

def get_max_min_diff(pairs: Dict[str, int], last_letter: str) -> int:
    '''Computes the difference between the most common letter and least common letter.'''
    # Count the number of occurences of each letter
    counts = {}
    for pair in pairs:
        letter1 = pair[0]
        if letter1 not in counts:
            counts[letter1] = 0
        counts[letter1] += pairs[pair]
    counts[last_letter] += 1

    # Determine the most and least common letters
    count_values = [counts[k] for k in counts]
    max_count = np.max(count_values)
    min_count = np.max(count_values)
    for count in count_values:
        if count < min_count and count != 0:
            min_count = count
    
    return max_count - min_count


def main():
    # Load in the data
    # polymer, rules = load_input('day14/test_input.txt')
    polymer, rules = load_input('day14/puzzle_input.txt')
    pairs = polymer_to_pairs(polymer)

    print('--- Part 1 ---')
    for _ in range(10):
        pairs = apply_rules(pairs, rules)
    print(f'After 10 steps: {get_max_min_diff(pairs, polymer[-1])}')

    print('')
    # polymer, rules = load_input('day14/test_input.txt')
    polymer, rules = load_input('day14/puzzle_input.txt')
    pairs = polymer_to_pairs(polymer)

    print('--- Part 2 ---')
    for i in range(40):
        pairs = apply_rules(pairs, rules)
    print(f'After 40 steps: {get_max_min_diff(pairs, polymer[-1])}')
    
if __name__ == '__main__':
    main()