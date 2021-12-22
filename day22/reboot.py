
from dataclasses import dataclass
from typing import Tuple, Union

def clip(x: int, bounds: Tuple[int, int]) -> int:
    '''Constrains the value to be within the given bounds.'''
    lower_bound, upper_bound = bounds
    return min(max(lower_bound, x), upper_bound + 1)

@dataclass
class Cuboid():
    '''A 3D cuboid. Lower bounds are inclusive, upper bounds are exclusive.'''
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    z_min: int
    z_max: int

    def size(self) -> int:
        '''Computes the volume of the cuboid.'''
        return (self.x_max - self.x_min) * (self.y_max - self.y_min) * (self.z_max - self.z_min)

    def constrain(self, bounds: Tuple[int, int]) -> None:
        '''Constrains all cuboid bounds to be within the given bounds.'''
        self.x_min = clip(self.x_min, bounds)
        self.x_max = clip(self.x_max, bounds)
        self.y_min = clip(self.y_min, bounds)
        self.y_max = clip(self.y_max, bounds)
        self.z_min = clip(self.z_min, bounds)
        self.z_max = clip(self.z_max, bounds)
    
    def as_key(self) -> Tuple[int, int, int, int, int, int]:
        '''Returns the six cuboid bounds as a tuple that can be used as a dict key.'''
        return self.x_min, self.x_max, self.y_min, self.y_max, self.z_min, self.z_max

class RebootStep:
    '''A step in the reboot process, consisting of a region and whether to turn that region on or off.'''
    def __init__(self, line: str) -> None:
        space_split = line.split(' ')
        self.on = space_split[0] == 'on'
        coords = space_split[1].split(',')
        x_bounds = [int(value) for value in coords[0][2:].split('..')]
        y_bounds = [int(value) for value in coords[1][2:].split('..')]
        z_bounds = [int(value) for value in coords[2][2:].split('..')]
        self.region = Cuboid(
            x_min=x_bounds[0],
            x_max=x_bounds[1] + 1,
            y_min=y_bounds[0],
            y_max=y_bounds[1] + 1,
            z_min=z_bounds[0],
            z_max=z_bounds[1] + 1
        )

def cuboid_intersection(cuboid_1: Cuboid, cuboid_2: Cuboid) -> Union[Cuboid, None]:
    '''Determines the intersection of the two cuboids, returning None if the cuboids don't intersect.'''
    x_min = max(cuboid_1.x_min, cuboid_2.x_min)
    x_max = min(cuboid_1.x_max, cuboid_2.x_max)
    y_min = max(cuboid_1.y_min, cuboid_2.y_min)
    y_max = min(cuboid_1.y_max, cuboid_2.y_max)
    z_min = max(cuboid_1.z_min, cuboid_2.z_min)
    z_max = min(cuboid_1.z_max, cuboid_2.z_max)
    if x_min >= x_max or y_min >= y_max or z_min >= z_max:
        return None
    return Cuboid(x_min, x_max, y_min, y_max, z_min, z_max)