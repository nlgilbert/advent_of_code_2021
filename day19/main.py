from errno import ENOENT
from os import strerror
from os.path import exists
from typing import List

from sensors import Beacon, Scanner

def load_input(path: str) -> List[Scanner]:
    '''Loads the input and returns it as a list of Scanners.'''
    if not exists(path):
        raise FileNotFoundError(ENOENT, strerror(ENOENT), path)
    
    with open(path, 'r') as input_file:
        input_str = ''
        for line in input_file:
            input_str += line
        scanner_inputs = input_str.split('\n\n')
        scanners = []
        for scanner_input in scanner_inputs:
            beacon_strs = scanner_input.strip().split('\n')[1:]
            beacons = []
            for beacon_str in beacon_strs:
                coords = beacon_str.split(',')
                beacons.append(Beacon(int(coords[0]), int(coords[1]), int(coords[2])))
            scanners.append(Scanner(beacons))
        return scanners

def align_scanners(scanners: List[Scanner]) -> Scanner:
    '''Aligns all the scanners, returning the map as a single scanner with all the beacons.'''
    map = Scanner(scanners[0].beacons[:])
    to_align = scanners[1:]
    final_scanners = []
    print(f'Scanners left to align: {len(to_align)}')
    while len(to_align) > 0:
        scanner = to_align.pop(0)
        if scanner.try_align(map):
            for beacon in scanner.beacons:
                if beacon not in map.beacons:
                    map.beacons.append(beacon)
            final_scanners.append(scanner)
        else:
            to_align.append(scanner)
        print(f'Scanners left to align: {len(to_align)}')
    return map, final_scanners

def get_dist(scanner_1: Scanner, scanner_2: Scanner) -> int:
    '''Computes the Manhattan distance between two scanners.'''
    x_dist = abs(scanner_1.translation[0] - scanner_2.translation[0])
    y_dist = abs(scanner_1.translation[1] - scanner_2.translation[1])
    z_dist = abs(scanner_1.translation[2] - scanner_2.translation[2])
    return x_dist + y_dist + z_dist
        
def main():
    # Load in the data
    # scanners = load_input('day19/test_input.txt')
    scanners = load_input('day19/puzzle_input.txt')
    print('WARNING: This code takes a long time to run. PyPy is highly recommended.')

    print('--- Part 1 ---')
    map, aligned_scanners = align_scanners(scanners)
    print(f'Total number of beacons: {len(map.beacons)}')

    print('')

    print('--- Part 2 ---')
    max_dist = 0
    for scanner_1 in aligned_scanners:
        for scanner_2 in aligned_scanners:
            dist = get_dist(scanner_1, scanner_2)
            max_dist = max(max_dist, dist)
    print(f'Maximum Manhattan distance between scanners: {max_dist}')
    
if __name__ == '__main__':
    main()