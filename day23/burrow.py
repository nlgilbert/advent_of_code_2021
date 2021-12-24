from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple

Coords = Tuple[int, int]
ENERGY_PER_STEP = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000
}

@dataclass
class Burrow:
    layout: List[str]

    def get_vacant_neighbors(self, coords: Coords) -> List[Coords]:
        '''Returns a list of all vacant spaces adjacent to the given coordinates.'''
        row, col = coords
        adj_coords = []
        for adj_coord in [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]:
            adj_row, adj_col = adj_coord
            if self.layout[adj_row][adj_col] == '.':
                adj_coords.append(adj_coord)
        return adj_coords
    
    def get_wrong_amphipods_in_room(self, col: int, desired_apod: str) -> List[Tuple[Coords, str]]:
        '''Returns the coordinates of every amphipod in the given room that still needs to move.'''
        wrong = []
        wrong_below = False
        # Check from the bottom up
        for row in range(len(self.layout) - 2, 1, -1):
            apod = self.layout[row][col]
            if apod != desired_apod or wrong_below:
                wrong_below = True
                if apod in 'ABCD':
                    wrong.append(((row, col), apod))
        return wrong

    def get_wrong_amphipods(self) -> List[Tuple[Coords, str]]:
        '''Returns the coordinates of every amphipod in the burrow that still needs to move.'''
        wrong = []
        # Check hallway
        for col in range(1, 12):
            if self.layout[1][col] != '.':
                wrong.append(((1, col), self.layout[1][col]))
        # Check room 1
        wrong += self.get_wrong_amphipods_in_room(3, 'A')
        # Check room 2
        wrong += self.get_wrong_amphipods_in_room(5, 'B')
        # Check room 3
        wrong += self.get_wrong_amphipods_in_room(7, 'C')
        # Check room 4
        wrong += self.get_wrong_amphipods_in_room(9, 'D')

        return wrong

    def can_move_into_room(self, col: int, desired_apod: str, apod: str) -> bool:
        '''Checks whether the given amphipod can move into the given room.'''
        if apod != desired_apod:
            return False
        hit_empty_space = False
        for row in range(len(self.layout) - 2, 1, -1):
            if hit_empty_space:
                if self.layout[row][col] != '.':
                    return False
            else:
                if self.layout[row][col] == '.':
                    hit_empty_space = True
                elif self.layout[row][col] != desired_apod:
                    return False
        return True
    
    def can_move_through_coords(self, start: Coords, target: Coords) -> bool:
        '''Checks whether the amphipod at the start coords can move to the target coords.'''
        start_row, start_col = start
        apod = self.layout[start_row][start_col]
        assert apod in 'ABCD'
        target_row, target_col = target

        # Can't move there if it's already occupied
        if self.layout[target_row][target_col] != '.':
            return False
        # All amphipodss can move through the hallway
        if target_row == 1:
            return True
        # We can move out of any room
        if target_row > 1 and start_row > target_row and target_col == start_col:
            return True
        # Don't move into a room unless you are the proper amphipod and it only contains the proper amphipod
        if target_row > 1:
            if target_col == 3:
                return self.can_move_into_room(3, 'A', apod)
            if target_col == 5:
                return self.can_move_into_room(5, 'B', apod)
            if target_col == 7:
                return self.can_move_into_room(7, 'C', apod)
            if target_col == 9:
                return self.can_move_into_room(9, 'D', apod)
        # We should have caught all cases by now
        assert False
    
    def can_stop_on_coords(self, start: Coords, target: Coords) -> bool:
        '''Checks whether the amphipod at the start coords can stop at the target coords.'''
        start_row, start_col = start
        apod = self.layout[start_row][start_col]
        assert apod in 'ABCD'
        target_row, target_col = target

        # If we can't move through it, we can't stop on it
        if not self.can_move_through_coords(start, target):
            return False
        # If the target is in the hallway, don't stop in front of a room
        if target_row == 1 and self.layout[target_row+1][target_col] != '#':
            return False
        # If we started in the hallway, we have to move into a room
        if start_row == 1 and target_row == 1:
            return False
        # If the target is in a room, don't stop on our way out
        if target_row > 1 and start_row > target_row and target_col == start_col:
            return False
        # If the target is in a room, don't stop on our way in
        if target_row > 1 and self.layout[target_row + 1][target_col] == '.':
            return False
        return True

    def get_valid_next_coords(self, start: Coords) -> List[Tuple[Coords, int]]:
        '''Gets a list of all valid next coordinates and its distance for the given amphipod.'''
        row, col = start
        apod = self.layout[row][col]
        assert apod in 'ABCD'

        # Use Depth First Search to get all valid coords
        valid_coords = []
        visited = []
        coords_to_try = [(start, 0)]
        while len(coords_to_try) > 0:
            coords, steps = coords_to_try.pop()
            visited.append(coords)
            for adj_coords in self.get_vacant_neighbors(coords):
                if adj_coords in visited:
                    continue
                if not self.can_move_through_coords(start, adj_coords):
                    continue
                coords_to_try.append((adj_coords, steps + 1))
                if self.can_stop_on_coords(start, adj_coords):
                    valid_coords.append((adj_coords, steps + 1))
        return valid_coords
        
    def get_burrow_after_move(self, start: Coords, end: Coords) -> Burrow:
        '''Returns a copy of the burrow after moving an amphipod.'''
        start_row, start_col = start
        apod = self.layout[start_row][start_col]
        assert apod in 'ABCD'
        end_row, end_col = end
        assert self.layout[end_row][end_col] == '.'

        burrow_after_move = []
        for row in range(len(self.layout)):
            line = self.layout[row]
            if row == start_row and row == end_row:
                after_clear = line[:start_col] + '.' + line[start_col+1:]
                burrow_after_move.append(after_clear[:end_col] + apod + after_clear[end_col+1:])
            elif row == start_row:
                burrow_after_move.append(line[:start_col] + '.' + line[start_col+1:])
            elif row == end_row:
                burrow_after_move.append(line[:end_col] + apod + line[end_col+1:])
            else:
                burrow_after_move.append(line)
        return Burrow(burrow_after_move)
    
    def get_possible_next_burrows(self) -> List[Tuple[Burrow, int]]:
        '''Returns a list of all burrows and energy used after making a single move.'''
        next_burrows = []
        for start_coords, apod in self.get_wrong_amphipods():
            for end_coords, steps in self.get_valid_next_coords(start_coords):
                burrow_after_move = self.get_burrow_after_move(start_coords, end_coords)
                energy = ENERGY_PER_STEP[apod] * steps
                next_burrows.append((burrow_after_move, energy))
        return next_burrows
    
    def as_string(self) -> str:
        '''Gets a string representation of the burrow.'''
        burrow_str = ''
        for line in self.layout:
            burrow_str += f'{line}\n'
        return burrow_str
    
    def __eq__(self, other: Burrow) -> bool:
        '''Compares the string representation of each burrow to determine equality.'''
        return self.as_string() == other.as_string()

@dataclass
class Node:
    burrow: Burrow
    energy: int

    def __lt__(self, other: Node):
        '''Compares energy of each node.'''
        return self.energy < other.energy

    def as_string(self) -> str:
        '''Gets a string representation of the node.'''
        return f'Energy: {self.energy}\n{self.burrow.as_string()}'