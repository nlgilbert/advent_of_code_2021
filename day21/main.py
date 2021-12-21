from errno import ENOENT
from os import strerror
from os.path import exists
from typing import List, Tuple

class Die:

    def __init__(self, size):
        self.size = size
        self.num_rolls = 0
    
    def roll(self):
        value = (self.num_rolls % self.size) + 1
        self.num_rolls += 1
        return value

class Player:

    def __init__(self, starting_position, starting_points = 0):
        self.position = starting_position
        self.points = starting_points
    
    def move(self, spaces):
        self.position += spaces
        self.position = ((self.position - 1) % 10) + 1
        self.points += self.position

def load_input(path: str) -> Tuple[str, List[str]]:
    '''Loads the input and returns it as a cipher and an image with 60 pixels of padding.'''
    if not exists(path):
        raise FileNotFoundError(ENOENT, strerror(ENOENT), path)
    
    with open(path, 'r') as input_file:
        players = []
        for line in input_file:
            players.append(Player(int(line.split()[-1])))
    return players

def play_game(players, end_score):
    die = Die(100)
    while True:
        player = players.pop(0)
        total_roll = 0
        for _ in range(3):
            total_roll += die.roll()
        player.move(total_roll)
        if player.points >= end_score:
            loser = players[0]
            return loser.points * die.num_rolls
        players.append(player)

def play_quantum_game(players, end_score, roll_value, roll_count, player_turn):
    player = players[player_turn]
    if roll_count == 3:
        player.move(roll_value)
        if player.points >= end_score:
            if player_turn == 0:
                return (1, 0)
            return (0, 1)
        roll_count = 0
        roll_value = 0
        player_turn = (player_turn + 1) % 2
        player = players[player_turn]
    win_counts_list = []
    for value in range(1, 4):
        players_copy = [
            Player(players[0].position, players[0].points),
            Player(players[1].position, players[1].points)
        ]
        win_counts_list.append(play_quantum_game(players_copy, end_score, roll_value + value, roll_count + 1, player_turn))
    win_count_p1 = sum([win_counts[0] for win_counts in win_counts_list])
    win_count_p2 = sum([win_counts[1] for win_counts in win_counts_list])
    return (win_count_p1, win_count_p2)

def main():
    # Load in the data
    # players = load_input('day21/test_input.txt')
    players = load_input('day21/puzzle_input.txt')

    print('--- Part 1 ---')
    print(f'Loser points * number of rolls: {play_game(players, 1000)}')

    print('')
    players = load_input('day21/test_input.txt')
    # players = load_input('day21/puzzle_input.txt')

    print('--- Part 2 ---')
    win_counts = play_quantum_game(players, 21, 0, 1, 0)
    if win_counts[0] > win_counts[1]:
        winner = 0
    else:
        winner = 1
    print(f'The winner wins in {win_counts[winner]} universes.')
    
if __name__ == '__main__':
    main()