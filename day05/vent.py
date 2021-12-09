from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Vent:
    x1: int
    y1: int
    x2: int
    y2: int

    def is_horizontal(self) -> bool:
        '''Checks if the vent is horizontal.'''
        return self.x1 == self.x2

    def is_vertical(self) -> bool:
        '''Checks if the vent is vertical.'''
        return self.y1 == self.y2
    
    def is_diagonal(self) -> bool:
        '''Checks if the vent is diagonal.'''
        return abs(self.x2 - self.x1) == abs(self.y2 - self.y1)

    def get_x_range(self) -> List[int]:
        '''Gets a list of the x values in order from x1 to x2.'''
        x_range = range(min(self.x1, self.x2), max(self.x1, self.x2) + 1)
        if self.x1 > self.x2:
            return reversed(x_range)
        return x_range

    def get_y_range(self) -> List[int]:
        '''Gets a list of the y values in order from y1 to y2.'''
        y_range = range(min(self.y1, self.y2), max(self.y1, self.y2) + 1)
        if self.y1 > self.y2:
            return reversed(y_range)
        return y_range

    def get_covered_points(self) -> List[Tuple[int, int]]:
        '''Gets a list of the points covered by this vent.'''
        covered_points = []
        if self.is_horizontal():
            for y in self.get_y_range():
                covered_points.append((self.x1, y))
        elif self.is_vertical():
            for x in self.get_x_range():
                covered_points.append((x, self.y1))
        elif self.is_diagonal():
            for x, y in zip(self.get_x_range(), self.get_y_range()):
                covered_points.append((x, y))
        else:
            print(f'{self.x1}, {self.y1} -> {self.x2}, {self.y2}')
        return covered_points