import numpy as np
from typing import List

FILENAME = "08/input.txt"


def is_visible(row: int, column: int, grid: np.ndarray):
    # If either row or column is 0, then the tree is visible
    if not (row and column):
        return True
    
    tree = grid[row, column]
    cardinal_dirs = [
        grid[:row, column],      # North
        grid[row + 1:, column],  # South
        grid[row, :column],      # West
        grid[row, column + 1:]   # East
    ]
    
    # The tree is visible if it's bigger than ALL trees in ANY direction
    return any(
        all(tree > other for other in direction)
        for direction in cardinal_dirs
    )
    

def part_1(contents: List[str]):
    grid = np.array([list(row) for row in contents]).astype(int)      
    
    return [
        is_visible(row, column, grid)
        for row, column in np.ndindex(grid.shape)
    ].count(True)


def part_2(contents):
    return ""


if __name__ == "__main__":
    with open(FILENAME) as file:
        contents = file.read().splitlines()
    
    print(part_1(contents))
    print(part_2(contents))

