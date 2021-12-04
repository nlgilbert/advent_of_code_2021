from errno import ENOENT
from os import strerror
from os.path import exists
from typing import List, Tuple
from bingo_board import BingoBoard

import os
from typing import Optional

def load_input(path: str) -> Tuple[List[int], List[BingoBoard]]:
    '''Loads the input and returns it as a list of called numbers and a list of bingo boards.'''
    if not exists(path):
        raise FileNotFoundError(ENOENT, strerror(ENOENT), path)
    
    with open(path, 'r') as input_file:
        called_numbers = [int(value) for value in input_file.readline().strip().split(',')]
        boards = []
        rows = []
        while (line := input_file.readline()) != '':
            if len(line.split()) == 5:
                rows.append(line.strip())
            elif len(rows) == 5:
                boards.append(BingoBoard(rows))
                rows.clear()
        return called_numbers, boards

def get_winning_score(called_numbers: List[int], boards: List[BingoBoard]) -> int:
    '''Plays bingo, returning the score of the first bingo card to win.'''
    for board in boards:
        board.clear()
    for number in called_numbers:
        for board in boards:
            board.mark(number)
            if board.has_won():
                return board.get_score(number)

def get_losing_score(called_numbers: List[int], boards: List[BingoBoard]) -> int:
    '''Plays bingo, returning the score of the last bingo card to win.'''
    for board in boards:
        board.clear()
    for number in called_numbers:
        for board in boards:
            board.mark(number)
        for board in boards:
            if board.has_won():
                if len(boards) == 1:
                    return board.get_score(number)
                else:
                    boards.remove(board)

def main():
    # Load in the data
    called_numbers, boards = load_input('day4/puzzle_input.txt')

    print('--- Part 1 ---')
    print(f'The first board to win gets a score of {get_winning_score(called_numbers, boards)}.')
            
    print('')

    print('--- Part 2 ---')
    print(f'The last board to win gets a score of {get_losing_score(called_numbers, boards)}.')
    
if __name__ == '__main__':
    main()