from errno import ENOENT
from os import strerror
from os.path import exists
from typing import List, Tuple

from dirac import Die, Player

def load_input(path: str) -> List[Player]:
    '''Loads the input and returns it as a list of players.'''
    if not exists(path):
        raise FileNotFoundError(ENOENT, strerror(ENOENT), path)
    
    with open(path, 'r') as input_file:
        players = []
        for line in input_file:
            players.append(Player(int(line.split()[-1])))
    return players

def play_game(players: List[Player], end_score: int) -> int:
    '''Plays a game of Dirac Dice with a deterministic D100.
    Returns the product of the loser's score and the number of dice rolls.'''
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

def as_key(players: List[Player], turn: int) -> str:
    '''Returns a string representation of the current game state.'''
    return f'{players[0].as_key()},{players[1].as_key()},{turn}'

def from_key(key: str) -> Tuple[List[Player], int]:
    '''Returns a game state by decoding the given key.'''
    values = [int(value) for value in key.split(',')]
    return [Player(*values[0:2]), Player(*values[2:4])], values[4]

def play_quantum_game(players: List[Player], end_score: int) -> List[int]:
    '''Plays a game of Dirac Dice with a quantum D3.
    Returns the number of universes in which each player wins.'''
    # Generate a list of the number of roll combinations to move each possible number of spaces
    spaces_combos = {}
    for roll_1 in range(1, 4):
        for roll_2 in range(1, 4):
            for roll_3 in range(1, 4):
                total_roll = roll_1 + roll_2 + roll_3
                spaces_combos[total_roll] = spaces_combos.get(total_roll, 0) + 1
    
    # Keep track of how many universes exist for a given game state
    universe_counts = {as_key(players, 0): 1}
    win_counts = [0, 0]
    while len(universe_counts) > 0:
        next_universe_counts = {}
        for key, u_count in universe_counts.items():
            for spaces, combos in spaces_combos.items():
                # Play a turn in this game state
                local_players, turn = from_key(key)
                local_players[turn].move(spaces)
                updated_u_count = u_count * combos
                if local_players[turn].points >= end_score:
                    # Winner!
                    win_counts[turn] += updated_u_count
                else:
                    # Add the game state to the list of game states to run in the next iteration
                    next_turn = (turn + 1) % 2
                    next_key = as_key(local_players, next_turn)
                    next_universe_counts[next_key] = next_universe_counts.get(next_key, 0) + updated_u_count
        universe_counts = next_universe_counts
    return win_counts

def main():
    # Load in the data
    # players = load_input('day21/test_input.txt')
    players = load_input('day21/puzzle_input.txt')

    print('--- Part 1 ---')
    print(f'Loser points * number of rolls: {play_game(players, 1000)}')

    print('')
    # players = load_input('day21/test_input.txt')
    players = load_input('day21/puzzle_input.txt')

    print('--- Part 2 ---')
    print(f'The overall winner wins in {max(play_quantum_game(players, 21))} universes.')
    
if __name__ == '__main__':
    main()