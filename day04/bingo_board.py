from typing import List

class BingoBoard:
    '''A bingo board'''

    def __init__(self, rows: List[str]):
        '''Takes the five rows (in string format) and creates a bingo board.'''
        self.numbers = [([int(number) for number in row.split()]) for row in rows]
        self.marked = [([False] * 5) for _ in range(5)]
    
    def mark(self, number: int) -> None:
        '''Marks the given number on the board.'''
        for i in range(5):
            for j in range(5):
                if self.numbers[i][j] == number:
                    self.marked[i][j] = True
    
    def clear(self) -> None:
        '''Clears the board, removing all the markings.'''
        for i in range(5):
            for j in range(5):
                self.marked[i][j] = False
    
    def has_won(self) -> bool:
        '''Checks if any of the rows or columns are completely marked.'''
        for i in range(5):
            row_winner = True
            column_winner = True
            for j in range(5):
                row_winner &= self.marked[i][j]
                column_winner &= self.marked[j][i]
            if row_winner or column_winner:
                return True

        return False

    def get_score(self, winning_value: int) -> int:
        '''Gets the sum of all unmarked numbers, then multiplies it by the winning value.'''
        unmarked_sum = 0
        for i in range(5):
            for j in range(5):
                if not self.marked[i][j]:
                    unmarked_sum += self.numbers[i][j]
        return unmarked_sum * winning_value

    def print_board(self) -> None:
        '''Print the numbers in the bingo board.'''
        for row in self.numbers:
            row_str = ''
            for value in row:
                row_str += f'{value} '
            print(row_str)

    def print_marked(self) -> None:
        '''Print the markers of the bingo board.'''
        for row in self.marked:
            row_str = ''
            for value in row:
                row_str += f'{int(value)} '
            print(row_str)
