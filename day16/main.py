from errno import ENOENT
from os import strerror
from os.path import exists

from packets import Packet, convert_to_packet

hex_to_bin = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
}

def load_input(path: str) -> Packet:
    '''Loads the input and returns it as a grid of risks.'''
    if not exists(path):
        raise FileNotFoundError(ENOENT, strerror(ENOENT), path)
    
    with open(path, 'r') as input_file:
        hex_string = input_file.readline().strip()
        bit_string = ''
        for nibble in hex_string:
            bit_string += hex_to_bin[nibble]
        return convert_to_packet(bit_string)

def main():
    # Load in the data
    # packet = load_input('day16/test_input.txt')
    packet = load_input('day16/puzzle_input.txt')

    print('--- Part 1 ---')
    print(f'Packet version sum: {packet.get_version_sum()}')

    print('')

    print('--- Part 2 ---')
    print(f'Packet value: {packet.get_value()}')
    
if __name__ == '__main__':
    main()