import numpy as np
import re
from typing import List, Set, Tuple, Union

FILENAME = "14/input.txt"
POINT = Tuple[int, int]
SAND_SOURCE = (500, 0)


def init_rocks(rock_specs: List[str]) -> Set[POINT]:
    rocks = set()
    
    for spec in rock_specs:
        
        # Extract the given points
        coords = np.array([
            (int(x), int(y))
            for x, y in re.findall("(\d+),(\d+)", spec)
        ])

        # Calculate the points between the given points
        delta_X, delta_Y = np.diff(coords[:, 0]), np.diff(coords[:, 1])
        between = np.vstack([
            np.linspace(
                coords[i], coords[i+1],
                num=abs(delta_X[i] if delta_X[i] else delta_Y[i]), 
                endpoint=False, dtype=int
            )
            for i in range(len(coords) - 1)
        ])
        
        # Add them all to the set
        coords = np.vstack((coords, between))
        rocks.update([tuple(c) for c in coords])
    
    return rocks


def fall_into(sand: POINT, rocks: Set[POINT]) -> Union[POINT, None]:
    new_height = sand[1] + 1
    
    # Test falling directly down, then down-left, then down-right
    if (new_sand := (sand[0], new_height)) not in rocks \
        or (new_sand := (sand[0] - 1, new_height)) not in rocks \
        or (new_sand := (sand[0] + 1, new_height)) not in rocks:
            
        return new_sand
    
    # The sand cannot fall further
    return None


def part_1(contents: List[str]) -> int:
    rocks = init_rocks(contents)
    abyss_height = max([rock[1] for rock in rocks])
    count = 0
    
    while True:
        sand = SAND_SOURCE
        while (new_sand := fall_into(sand, rocks)) is not None:
            if new_sand[1] == abyss_height:
                return count
        
            sand = new_sand
        
        rocks.add(sand)
        count += 1


def part_2(contents: List[str]) -> int:
    return 0


if __name__ == "__main__":
    with open(FILENAME) as file:
        contents = file.read().splitlines()
    
    print(part_1(contents))
    print(part_2(contents))

