from errno import ENOENT
from os import strerror
from os.path import exists
from typing import List, Union

from sensors import Beacon, Scanner

def load_input(path: str) -> None:
    '''Loads the input and returns it as a list of snailfish numbers.'''
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

def align_scanners(scanners: List[Scanner]):
    map = Scanner(scanners[0].beacons[:])
    to_align = scanners[1:]
    print(len(to_align))
    while len(to_align) > 0:
        scanner = to_align.pop(0)
        if scanner.try_align(map):
            for beacon in scanner.beacons:
                if beacon not in map.beacons:
                    map.beacons.append(beacon)
        else:
            to_align.append(scanner)
        print(len(to_align))
    return map

        
def main():
    # Load in the data
    # scanners = load_input('day19/test_input.txt')
    scanners = load_input('day19/puzzle_input.txt')

    print('--- Part 1 ---')
    map = align_scanners(scanners)
    print(f'Total number of beacons: {len(map.beacons)}')

    print('')

    print('--- Part 2 ---')
    print(f'')
    
if __name__ == '__main__':
    main()