import numpy as np
from typing import List
from grid_map import GridMap

FILENAME = "12/input.txt"


def part_1(contents: List[str]) -> int:
    letter_map = GridMap(contents)
    return letter_map


def part_2(contents: List[str]) -> int:
    return 0


if __name__ == "__main__":
    with open(FILENAME) as file:
        contents = file.read().splitlines()
    
    print(part_1(contents))
    print(part_2(contents))

