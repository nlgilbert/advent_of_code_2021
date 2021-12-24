from errno import ENOENT
from os import strerror
from os.path import exists
from typing import List

REG_IDX = {
    'w': 0,
    'x': 1,
    'y': 2,
    'z': 3
}

def load_input(path: str) -> None:
    '''Loads the input and returns it as a burrow.'''
    if not exists(path):
        raise FileNotFoundError(ENOENT, strerror(ENOENT), path)
    
    with open(path, 'r') as input_file:
        return [line.strip() for line in input_file]

def get_b_val(b, regs):
    if b in 'wxyz':
        return regs[REG_IDX[b]]
    return int(b)

def process_instruction(instruction, regs, input_str):
    tokens = instruction.split(' ')
    if tokens[0] == 'inp':
        a = tokens[1]
        regs[REG_IDX[a]] = int(input_str[0])
        input_str = input_str[1:]
    elif tokens[0] == 'add':
        a = tokens[1]
        a_val = regs[REG_IDX[a]]
        b = tokens[2]
        b_val = get_b_val(b, regs)
        regs[REG_IDX[a]] = a_val + b_val
    elif tokens[0] == 'mul':
        a = tokens[1]
        a_val = regs[REG_IDX[a]]
        b = tokens[2]
        b_val = get_b_val(b, regs)
        regs[REG_IDX[a]] = a_val * b_val
    elif tokens[0] == 'div':
        a = tokens[1]
        a_val = regs[REG_IDX[a]]
        b = tokens[2]
        b_val = get_b_val(b, regs)
        regs[REG_IDX[a]] = a_val // b_val
    elif tokens[0] == 'mod':
        a = tokens[1]
        a_val = regs[REG_IDX[a]]
        b = tokens[2]
        b_val = get_b_val(b, regs)
        regs[REG_IDX[a]] = a_val % b_val
    elif tokens[0] == 'eql':
        a = tokens[1]
        a_val = regs[REG_IDX[a]]
        b = tokens[2]
        b_val = get_b_val(b, regs)
        if a_val == b_val:
            regs[REG_IDX[a]] = 1
        else:
            regs[REG_IDX[a]] = 0
    else:
        assert False
    return regs, input_str

def run_program(instructions, input_str):
    regs = [0, 0, 0, 0]
    for instruction in instructions:
        regs, input_str = process_instruction(instruction, regs, input_str)
    return regs

def main():
    # Load in the data
    # monad = load_input('day24/test_input.txt')
    monad = load_input('day24/puzzle_input.txt')

    print('--- Part 1 ---')
    model_number = 91699394894995
    assert run_program(monad, f'{model_number:014}')[REG_IDX['z']] == 0
    print(f'Largest valid model number: {model_number}')

    print('')

    print('--- Part 2 ---')
    model_number = 51147191161261
    assert run_program(monad, f'{model_number:014}')[REG_IDX['z']] == 0
    print(f'Smallest valid model number: {model_number}')
    print(f'')
    
if __name__ == '__main__':
    main()