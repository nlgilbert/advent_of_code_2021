from errno import ENOENT
from os import name, strerror
from os.path import exists
from typing import List, Dict

from cave import Cave

def load_input(path: str) -> Dict[str, Cave]:
    '''Loads the input and returns it as a dictionary of caves by name.'''
    if not exists(path):
        raise FileNotFoundError(ENOENT, strerror(ENOENT), path)
    
    with open(path, 'r') as input_file:
        caves_by_name = {}
        for line in [line.strip() for line in input_file.readlines()]:
            link = line.split('-')
            name_1 = link[0]
            name_2 = link[1]
            if name_1 not in caves_by_name:
                caves_by_name[name_1] = Cave(name_1)
            if name_2 not in caves_by_name:
                caves_by_name[name_2] = Cave(name_2)
            caves_by_name[name_1].add_link(caves_by_name[name_2])
            caves_by_name[name_2].add_link(caves_by_name[name_1])
        return caves_by_name

def has_double_small(path: List[Cave]) -> bool:
    for cave in path:
        if cave.is_small and path.count(cave) >= 2:
            return True
    return False

def get_num_paths(start: Cave, end: Cave, path: List[Cave], allow_double_small: bool) -> int:
    path.append(start)
    if start == end:
        return 1
    num_paths = 0
    for cave in start.links:
        # Start is only allowed once
        if cave.name == 'start':
            continue
        # Maybe allow one double small
        if allow_double_small:
            if has_double_small(path) and cave.is_small and cave in path:
                continue
        else:
            if cave.is_small and cave in path:
                continue
        num_paths += get_num_paths(cave, end, path[:], allow_double_small)
    return num_paths

def main():
    # Load in the data
    # caves_by_name = load_input('day12/test_input.txt')
    caves_by_name = load_input('day12/puzzle_input.txt')

    print('--- Part 1 ---')
    num_paths = get_num_paths(caves_by_name['start'], caves_by_name['end'], [], False)
    print(f'Paths with no double smalls: {num_paths}')
    
    print('')

    print('--- Part 2 ---')
    num_paths = get_num_paths(caves_by_name['start'], caves_by_name['end'], [], True)
    print(f'Paths with no more than 1 double small: {num_paths}')
    
if __name__ == '__main__':
    main()