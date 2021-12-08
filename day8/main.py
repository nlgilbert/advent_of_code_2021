from errno import ENOENT
from os import strerror
from os.path import exists
from typing import Dict, List, Tuple

SEVEN_SEG_MAPPING = {
    'abcefg': 0,
    'cf': 1,
    'acdeg': 2,
    'acdfg': 3,
    'bcdf': 4,
    'abdfg': 5,
    'abdefg': 6,
    'acf': 7,
    'abcdefg': 8,
    'abcdfg': 9,
}

def load_input(path: str) -> List[Tuple[List[str], List[str]]]:
    '''Loads the input and returns it as a list (digits, value) tuples.'''
    if not exists(path):
        raise FileNotFoundError(ENOENT, strerror(ENOENT), path)
    
    with open(path, 'r') as input_file:
        sequences = []
        for line in input_file:
            split_line = line.strip().split(' | ')
            digits = split_line[0].split(' ')
            value = split_line[1].split(' ')
            sequences.append((digits, value))
        return sequences

def count_1478(sequences: List[Tuple[List[str], List[str]]]) -> int:
    '''Counts the number of occurances of 1, 4, 7, and 8 in the digits of the vlaues.'''
    count = 0
    for _, value in sequences:
        for digit in value:
            if len(digit) in [2, 3, 4, 7]:
                count += 1
    return count

def find_digit_with_length(digits: List[str], length: int) -> str:
    '''Finds the digit with the given number of letters (segments).'''
    for digit in digits:
        if len(digit) == length:
            return digit

def decode_digit(digit: str, mapping: Dict[str, str]) -> int:
    '''Decodes the digit using the given mapping.'''
    decoded_seven_seg = ''
    for letter in digit:
        decoded_seven_seg += mapping[letter]
    return SEVEN_SEG_MAPPING[''.join(sorted(decoded_seven_seg))]

def decode_value(value: List[str], mapping: Dict[str, str]) -> int:
    '''Decodes the 4-digit value using the given mapping.'''
    decoded_value = 0
    for digit in value:
        decoded_value = (10 * decoded_value) + decode_digit(digit, mapping)
    return decoded_value

def decode_seven_seg(digits: List[str]) -> Dict[str, str]:
    '''Uses the 10 unique digits to decode the seven segment display, generating a mapping.'''
    mapping = {}
    letter_counts = {
        'a': 0,
        'b': 0,
        'c': 0,
        'd': 0,
        'e': 0,
        'f': 0,
        'g': 0
    }

    # Count the number of digits each letter appears in
    for digit in digits:
        for letter in digit:
            letter_counts[letter] += 1

    # Find the letters in a unique number of digits (e in 4, b in 6, f in 9)
    to_decode = 'abcdefg'
    for letter in 'abcdefg':
        if letter_counts[letter] == 4:
            mapping[letter] = 'e'
            to_decode = to_decode.replace(letter, '')
        elif letter_counts[letter] == 6:
            mapping[letter] = 'b'
            to_decode = to_decode.replace(letter, '')
        elif letter_counts[letter] == 9:
            mapping[letter] = 'f'
            to_decode = to_decode.replace(letter, '')
    assert(len(to_decode) == 4)
    
    # Since f has already been found, c is the only one left in "1" (the only 2-letter digit)
    one = find_digit_with_length(digits, 2)
    for letter in to_decode:
        if letter in one:
            mapping[letter] = 'c'
            to_decode = to_decode.replace(letter, '')
            break
    assert(len(to_decode) == 3)
    
    # Since c and f have already been found, a is the only one left in "7" (the only 3-letter digit)
    seven = find_digit_with_length(digits, 3)
    for letter in to_decode:
        if letter in seven:
            mapping[letter] = 'a'
            to_decode = to_decode.replace(letter, '')
            break
    assert(len(to_decode) == 2)

    # Since b, c, and f have already been found, d is the only one left in "4" (the only 4-letter digit)
    four = find_digit_with_length(digits, 4)
    for letter in to_decode:
        if letter in four:
            mapping[letter] = 'd'
            to_decode = to_decode.replace(letter, '')
            break
    assert(len(to_decode) == 1)

    # The only letter remaining is g
    mapping[to_decode] = 'g'

    return mapping

def main():
    # Load in the data
    sequences = load_input('day8/puzzle_input.txt')

    print('--- Part 1 ---')
    print(f'There are {count_1478(sequences)} occurrances of 1, 4, 7, or 8.')
    
    print('')

    print('--- Part 2 ---')
    total_sum = 0
    for digits, value in sequences:
        mapping = decode_seven_seg(digits)
        total_sum += decode_value(value, mapping)
    print(f'The total sum of all decoded values is {total_sum}.')
    
if __name__ == '__main__':
    main()