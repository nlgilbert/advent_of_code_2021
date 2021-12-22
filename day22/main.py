from collections import Counter
from errno import ENOENT
from os import strerror
from os.path import exists
from typing import List

from reboot import Cuboid, RebootStep, cuboid_intersection

def load_input(path: str) -> List[RebootStep]:
    '''Loads the input and returns it as a list of reboot steps.'''
    if not exists(path):
        raise FileNotFoundError(ENOENT, strerror(ENOENT), path)
    
    with open(path, 'r') as input_file:
        reboot_steps = []
        for line in input_file:
            reboot_steps.append(RebootStep(line.strip()))
        return reboot_steps

def num_on_after_reboot(reboot_steps: List[RebootStep], bounds=None) -> int:
    '''Computes the number of cubes that are on after applying the given reboot steps.'''
    regions = Counter()
    for step in reboot_steps:
        # Constrain to the given bounds
        if bounds is not None:
            step.region.constrain(bounds)
        # Find intersections with any existing cubes
        for region_key, count in list(regions.items()):
            region = Cuboid(*region_key)
            intersection = cuboid_intersection(step.region, region)
            # Cancel out the effects of any previous steps
            if intersection is not None and intersection.size() > 0:
                regions[intersection.as_key()] -= count
        # If this is an "on" step, mark it as such
        if step.on:
            regions[step.region.as_key()] += 1

    # Count the number of "on" cubes
    num_on = 0
    for region_key, count in list(regions.items()):
        region = Cuboid(*region_key)
        num_on += region.size() * count
    return num_on
    
def main():
    # Load in the data
    # reboot_steps = load_input('day22/test_input.txt')
    reboot_steps = load_input('day22/puzzle_input.txt')

    print('--- Part 1 ---')
    print(f'In the range -50..50, there are {num_on_after_reboot(reboot_steps, (-50, 50))} cubes on.')

    print('')
    # reboot_steps = load_input('day22/test_input.txt')
    reboot_steps = load_input('day22/puzzle_input.txt')

    print('--- Part 2 ---')
    print(f'In the full range, there are {num_on_after_reboot(reboot_steps)} cubes on.')
    
if __name__ == '__main__':
    main()