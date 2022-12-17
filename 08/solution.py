import numpy as np
from typing import List

FILENAME = "08/input.txt"


def setup_grid(contents: List[str]) -> np.ndarray:
    return np.array([list(row) for row in contents]).astype(int)


def cardinals(row: int, column: int, grid: np.ndarray):
    # North and West are sliced in reverse so that all values
    # are ordered by distance from grid[row, column]
    
    return [
        grid[row - 1::-1, column],   # North
        grid[row + 1:, column],      # South
        grid[row, column - 1::-1],   # West
        grid[row, column + 1:]       # East
    ]


# def visible_trees(current_tree, other_trees):
    


def is_visible(row: int, column: int, grid: np.ndarray) -> bool:
    # If either row or column is 0, then the tree is visible
    if not (row and column):
        return True
    
    # The tree is visible if it's bigger than ALL trees in ANY direction
    return any(
        all(grid[row, column] > direction)
        for direction in cardinals(row, column, grid)
    )


def scenic_score(row: int, column: int, grid: np.ndarray) -> int:
    # Trees on the edge have a score of 0
    if not (row and column):
        return 0
    
    # for direction in cardinals(row, column, grid)
    
    
    # return np.prod(cardinals_to_boundaries)


def part_1(contents: List[str]) -> int:
    grid = setup_grid(contents)      
    
    return len([
        True for row, column in np.ndindex(grid.shape)
        if is_visible(row, column, grid)
    ])


def part_2(contents: List[str]) -> int:
    grid = setup_grid(contents)
    
    return max(
        scenic_score(row, column, grid)
        for row, column in np.ndindex(grid.shape)
    )


if __name__ == "__main__":
    with open(FILENAME) as file:
        contents = file.read().splitlines()
    
    print(part_1(contents))
    # print(part_2(contents))

