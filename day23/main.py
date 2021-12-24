from errno import ENOENT
from os import strerror
from os.path import exists
from heapq import heappop, heappush

from burrow import Burrow, Node

def load_input(path: str) -> Burrow:
    '''Loads the input and returns it as a burrow.'''
    if not exists(path):
        raise FileNotFoundError(ENOENT, strerror(ENOENT), path)
    
    with open(path, 'r') as input_file:
        burrow_layout = []
        for line in input_file:
            if line[-1] == '\n':
                burrow_layout.append(line[:-1])
            else:
                burrow_layout.append(line)
        return Burrow(burrow_layout)
    
def get_organized_burrow(height: int) -> Burrow:
    '''Constructs the organized burrow with the given height.'''
    organized_burrow = [
        '#############',
        '#...........#',
        '###A#B#C#D###',
        '  #########'
    ]
    while len(organized_burrow) < height:
        organized_burrow.insert(3, '  #A#B#C#D#')
    return Burrow(organized_burrow)

def get_min_energy_to_organize(burrow: Burrow) -> int:
    '''Gets the minimum energy to organize the amphipods in the burrow.'''
    to_visit = [Node(burrow, 0)]
    burrow_history = {burrow.as_string(): [to_visit[0]]}
    burrow_energy = {burrow.as_string(): 0}
    organized_burrow = get_organized_burrow(len(burrow.layout))

    # Use Dijkstra's to find the minimum energy
    while len(to_visit) > 0:
        node = heappop(to_visit)
        burrow_str = node.burrow.as_string()
        # Check for organized burrow
        if node.burrow == organized_burrow:
            print('Found minimum energy to organize:')
            for step_node in burrow_history[burrow_str]:
                print(step_node.as_string())
            return node.energy
        
        # Check all possible next burrows
        for next_burrow, energy in node.burrow.get_possible_next_burrows():
            next_node = Node(next_burrow, node.energy + energy)
            next_burrow_str = next_node.burrow.as_string()
            assert burrow_str in burrow_history
            
            # Skip this node if we have already found a lower-energy path to the same burrow state
            if next_burrow_str in burrow_energy and burrow_energy[next_burrow_str] <= next_node.energy:
                continue

            # Update the history
            history = burrow_history[burrow_str]
            next_history = history[:]
            next_history.append(next_node)

            # Keep track of burrow energy and history
            burrow_energy[next_burrow_str] = next_node.energy
            burrow_history[next_burrow_str] = next_history
            heappush(to_visit, next_node)
    
def main():
    # Load in the data
    # burrow = load_input('day23/test_input.txt')
    burrow = load_input('day23/puzzle_input.txt')

    print('--- Part 1 ---')
    print(f'Minimum energy to organize original: {get_min_energy_to_organize(burrow)}')

    print('')
    burrow.layout.insert(3, '  #D#C#B#A#')
    burrow.layout.insert(4, '  #D#B#A#C#')

    print('--- Part 2 ---')
    print(f'Minimum energy to organize unfolded: {get_min_energy_to_organize(burrow)}')
    
if __name__ == '__main__':
    main()