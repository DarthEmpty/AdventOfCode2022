import numpy as np
from typing import List, Generator
from itertools import accumulate

FILENAME = "09/input.txt"
VECTOR = np.array


def commands(comm_list: List[str]) -> Generator[str, None, None]:
    while comm_list:
        yield comm_list.pop(0).split()


def interpret_command(dir: str, mag: int) -> VECTOR:
    if dir == "U":
        return VECTOR([mag, 0])
    
    elif dir == "D":
        return VECTOR([-mag, 0])
    
    elif dir == "R":
        return VECTOR([0, mag])
    
    else:  # dir == "L"
        return VECTOR([0, -mag])
    

def step_along(Vec: VECTOR):
    # A "step" is a vector between [1, 1] and [-1, -1] representing
    # the next step to take to progress along `Vec` on a grid.
    # The elements are integers {1, 0, -1} and are determined by
    # rounding the unit vector of `Vec` away from [0, 0].
    # (So that travelling diagonally is prioritised)
    
    return VECTOR([
        np.ceil(v) if v > 0 else np.floor(v)
        for v in (Vec / np.linalg.norm(Vec))
    ])


def steps(tail: VECTOR, head: VECTOR) -> Generator[VECTOR, None, None]:
    diff = head - tail
    
    # Head and Tail are adjacent if their elements are {1, 0, -1}
    while not (np.all(diff <= 1) and np.all(diff >= -1)):
        next_step = step_along(diff)
        diff -= next_step
        yield next_step
    

def part_1(contents):
    head = np.zeros((2,))
    tail = np.zeros((2,))
    visited = []
    
    for direction, magnitude in commands(contents):
        head += interpret_command(direction, int(magnitude))
        journey = steps(tail, head)
        visited.extend(accumulate(journey, initial=tail))
        tail = visited[-1]
    
    return len(np.unique(visited, axis=0))


# TODO: Figure out why answer is too small
def part_2(contents):
    knots = [np.zeros((2,)) for _ in range(10)]
    visited = []
    
    for direction, magnitude in commands(contents):
        knots[0] += interpret_command(direction, int(magnitude))
        
        for i in range(1, len(knots)):
            journey = steps(knots[i], knots[i - 1])
            path = list(accumulate(journey, initial=knots[i]))
            knots[i] = path[-1]
            
            if i == len(knots) - 1:
                visited.extend(path)

    return len(np.unique(visited, axis=0))


if __name__ == "__main__":
    with open(FILENAME) as file:
        contents = file.read().splitlines()
    
    print(part_1(contents.copy()))
    print(part_2(contents))
