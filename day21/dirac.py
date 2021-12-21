class Die:
    '''A deterministic die.'''
    def __init__(self, size: int):
        self.size = size
        self.num_rolls = 0
    
    def roll(self) -> int:
        '''Rolls the die, returning the next number consecutively.'''
        value = (self.num_rolls % self.size) + 1
        self.num_rolls += 1
        return value

class Player:
    '''A Player in a game of Dirac Dice.'''
    def __init__(self, starting_position: int, starting_points: int = 0):
        self.position = starting_position
        self.points = starting_points
    
    def move(self, spaces: int) -> None:
        '''Moves the player the given numebr of spaces.'''
        self.position += spaces
        self.position = ((self.position - 1) % 10) + 1
        self.points += self.position
    
    def as_key(self) -> str:
        '''Gets a string representation of the player, in the form "position,points".'''
        return f'{self.position},{self.points}'