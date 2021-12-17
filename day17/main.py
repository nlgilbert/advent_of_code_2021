from errno import ENOENT
from os import strerror
from os.path import exists
from typing import List, Tuple
import re

def load_input(path: str) -> None:
    '''Loads the input and returns it as a grid of risks.'''
    if not exists(path):
        raise FileNotFoundError(ENOENT, strerror(ENOENT), path)
    
    with open(path, 'r') as input_file:
        line = input_file.readline().strip()
        match = re.search(r'target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)', line)
        x_min, x_max, y_min, y_max = match.groups()
        return (int(x_min), int(x_max)), (int(y_min), int(y_max))

def triangle_number(n: int) -> int:
    '''Returns the nth triangle number.'''
    return sum(range(n+1))

def get_valid_y_vels(y_range: Tuple[int, int]) -> List[int]:
    '''Gets a list of all potentailly valid initial y velocities.'''
    y_min, y_max = y_range
    min_y_vel = y_min
    max_y_vel = -y_min - 1
    valid_y_vels = []
    for initial_vel_y in range(min_y_vel, max_y_vel + 1):
        pos_y = 0
        vel_y = initial_vel_y
        while pos_y >= y_min:
            pos_y += vel_y
            vel_y -= 1
            if y_min <= pos_y <= y_max:
                valid_y_vels.append(initial_vel_y)
                break
    return valid_y_vels

def get_valid_x_vels(x_range: Tuple[int, int]) -> List[int]:
    '''Gets a list of all potentailly valid initial x velocities.'''
    min_x, max_x = x_range
    assert min_x > 0
    assert max_x > 0
    min_x_vel = 0
    while triangle_number(min_x_vel) < min_x:
        min_x_vel += 1
    if min_x_vel > max_x:
        return []
    max_x_vel = max_x
    valid_x_vels = []
    for initial_vel_x in range(min_x_vel, max_x_vel + 1):
        pos_x = 0
        vel_x = initial_vel_x
        while pos_x <= max_x:
            pos_x += vel_x
            if vel_x < 0:
                vel_x += 1
            elif vel_x > 0:
                vel_x -= 1
            if min_x <= pos_x <= max_x:
                valid_x_vels.append(initial_vel_x)
                break
    return valid_x_vels

def get_target_steps_y(initial_y_vel: int, y_range: Tuple[int, int]) -> List[int]:
    '''Gets the steps during which the y position in in the target range.'''
    min_y, max_y = y_range
    pos_y = 0
    vel_y = initial_y_vel
    step = 0
    target_steps_y = []
    while pos_y >= min_y:
        step += 1
        pos_y += vel_y
        vel_y -= 1
        if min_y <= pos_y <= max_y:
            target_steps_y.append(step)
    return target_steps_y

def do_step(position: Tuple[int, int], velocity: Tuple[int, int]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    '''Performs a single step on the position and velocity.'''
    pos_x, pos_y = position
    vel_x, vel_y = velocity
    pos_x += vel_x
    pos_y += vel_y
    if vel_x < 0:
        vel_x += 1
    elif vel_x > 0:
        vel_x -= 1
    vel_y -= 1
    return (pos_x, pos_y), (vel_x, vel_y)

def is_in_target(position: Tuple[int, int], x_range: Tuple[int, int], y_range: Tuple[int, int]) -> bool:
    '''Checks if the position falls in the target.'''
    pos_x, pos_y = position
    min_x, max_x = x_range
    min_y, max_y = y_range
    return (min_x <= pos_x <= max_x) and (min_y <= pos_y <= max_y)

def get_valid_vels(x_range: Tuple[int, int], y_range: Tuple[int, int]) -> List[Tuple[int, int]]:
    '''Gets a list of all valid initial velicities.'''
    valid_y_vels = get_valid_y_vels(y_range)
    valid_x_vels = get_valid_x_vels(x_range)
    valid_vels = []
    for initial_y_vel in valid_y_vels:
        num_steps = get_target_steps_y(initial_y_vel, y_range)[-1]
        for initial_x_vel in valid_x_vels:
            position = (0, 0)
            velocity = (initial_x_vel, initial_y_vel)
            for _ in range(num_steps):
                position, velocity = do_step(position, velocity)
                if is_in_target(position, x_range, y_range):
                    valid_vels.append((initial_x_vel, initial_y_vel))
                    break
    return valid_vels

def main():
    # Load in the data
    # x_range, y_range = load_input('day17/test_input.txt')
    x_range, y_range = load_input('day17/puzzle_input.txt')

    print('--- Part 1 ---')
    largest_valid_y_vel = get_valid_y_vels(y_range)[-1]
    print(f'Highest possible y value: {triangle_number(largest_valid_y_vel)}')

    print('')

    print('--- Part 2 ---')
    print(f'Number of valid velocities: {len(get_valid_vels(x_range, y_range))}')
    
if __name__ == '__main__':
    main()