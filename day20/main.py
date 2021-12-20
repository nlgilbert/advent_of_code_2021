from errno import ENOENT
from os import strerror
from os.path import exists
from typing import List, Tuple

PADDING = 60

def load_input(path: str) -> Tuple[str, List[str]]:
    '''Loads the input and returns it as a cipher and an image with 60 pixels of padding.'''
    if not exists(path):
        raise FileNotFoundError(ENOENT, strerror(ENOENT), path)
    
    with open(path, 'r') as input_file:
        input_str = ''
        for line in input_file:
            input_str += line
        sections = input_str.split('\n\n')
        cipher = sections[0].strip()
        rows = sections[1].split('\n')
        grid = [row.strip() for row in rows[:-1]]
        image = []
        for _ in range(PADDING):
            image.append('.' * ((PADDING * 2) + len(grid[0])))
        for row in grid:
            image.append(('.' * PADDING) + row + ('.' * PADDING))
        for _ in range(PADDING):
            image.append('.' * ((PADDING * 2) + len(grid[0])))
        return cipher, image

def get_cipher_idx(image: List[str], coords: Tuple[int, int]) -> int:
    row, col = coords
    adj_coords = [
        (row-1, col-1),
        (row-1, col),
        (row-1, col+1),
        (row, col-1),
        (row, col),
        (row, col+1),
        (row+1, col-1),
        (row+1, col),
        (row+1, col+1)
    ]
    bit_str = ''
    for adj_coord in adj_coords:
        adj_row, adj_col = adj_coord
        adj_row = max(adj_row, 1)
        adj_row = min(adj_row, len(image) - 2)
        adj_col = max(adj_col, 1)
        adj_col = min(adj_col, len(image[0]) - 2)
        if image[adj_row][adj_col] == '.':
            bit_str += '0'
        else:
            bit_str += '1'
    return int(bit_str, base=2)

def enhance_image(cipher: str, image: List[str]) -> List[str]:
    enhanced_image = []
    for row in range(len(image)):
        enhanced_row = ''
        for col in range(len(image[0])):
            enhanced_row += cipher[get_cipher_idx(image, (row, col))]
        enhanced_image.append(enhanced_row)
    return enhanced_image

def count_lit_pixels(image: List[str]) -> int:
    num_lit_pixels = 0
    for row in image:
        for pixel in row:
            if pixel == '#':
                num_lit_pixels += 1
    return num_lit_pixels

def print_image(image: List[str]) -> None:
    for row in image:
        print(row)
    print('')
        
def main():
    # Load in the data
    # cipher, image = load_input('day20/test_input.txt')
    cipher, image = load_input('day20/puzzle_input.txt')

    print('--- Part 1 ---')
    enhanced_image = image[:]
    for _ in range(2):
        enhanced_image = enhance_image(cipher, enhanced_image)
    print(f'Number of lit pixels after 2 enchancements: {count_lit_pixels(enhanced_image)}')

    print('')

    print('--- Part 2 ---')
    enhanced_image = image[:]
    for _ in range(50):
        enhanced_image = enhance_image(cipher, enhanced_image)
    print(f'Number of lit pixels after 50 enchancements: {count_lit_pixels(enhanced_image)}')
    
if __name__ == '__main__':
    main()