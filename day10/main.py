from errno import ENOENT
from os import strerror
from os.path import exists
from typing import List

CLOSERS = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}

SYNTAX_ERROR_POINT_VALUES = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

AUTOCOMPLETE_POINT_VALUES = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}

def load_input(path: str) -> List[str]:
    '''Loads the input and returns it as a list of lines.'''
    if not exists(path):
        raise FileNotFoundError(ENOENT, strerror(ENOENT), path)
    
    with open(path, 'r') as input_file:
        return [line.strip() for line in input_file]

def get_syntax_error_score(line: str) -> int:
    '''Computes the syntax error score for the line.'''
    opens = []
    for char in line:
        if char in '([{<':
            opens.append(char)
        elif char in ')]}>':
            if char != CLOSERS[opens.pop()]:
                return SYNTAX_ERROR_POINT_VALUES[char]
    return 0

def get_autocomplete_score(line: str) -> int:
    '''Computes the autocomplete score for an incomplete line'''
    # Corrupt lines don't get an autocomplete score
    if get_syntax_error_score(line) != 0:
        return 0

    opens = []
    for char in line:
        if char in '([{<':
            opens.append(char)
        elif char in ')]}>':
            opens.pop()
    
    score = 0
    for char in reversed(opens):
        score *= 5
        score += AUTOCOMPLETE_POINT_VALUES[CLOSERS[char]]   
    return score

def main():
    # Load in the data
    lines = load_input('day10/puzzle_input.txt')

    print('--- Part 1 ---')
    syntax_error_score = 0
    for line in lines:
        syntax_error_score += get_syntax_error_score(line)
    print(f'Total syntax error score: {syntax_error_score}')
    
    print('')


    print('--- Part 2 ---')
    scores = []
    for line in lines:
        score = get_autocomplete_score(line)
        if score > 0:
            scores.append(score)
    scores = sorted(scores)
    middle_score = scores[len(scores) // 2]
    print(f'Middle score: {middle_score}')
    
if __name__ == '__main__':
    main()