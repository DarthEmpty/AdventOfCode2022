import numpy as np
from typing import List, Tuple, Generator

FILENAME = "10/input.txt"


def interpreted(commands: List[str]) -> Generator[Tuple[int, int], None, None]:
    while commands:
        current = commands.pop(0)
        
        if current.startswith("addx"):
            yield 2, int(current.split()[1])
        
        else:  # `current` is "noop"
            yield 1, 0   


def execute(commands: List[str]) -> List[int]:
    register = 1
    history = []
    
    for duration, value in interpreted(commands):
        history.extend(register for _ in range(duration))
        register += value
    
    return history


def margin(centre: int, error: int) -> range:
    return range(centre - error, centre + error + 1)


def part_1(contents: List[str]) -> int:
    history = execute(contents)    
    
    return sum(
        (cycle + 1) * history[cycle]
        for cycle in range(19, 220, 40)
    )


def part_2(contents: List[str]) -> List[List[str]]:
    history = execute(contents)
    crt = [
        "#" if cycle % 40 in margin(history[cycle], 1)
        else "." for cycle in range(len(history))
    ]
    
    return np.reshape(crt, (6, 40))


if __name__ == "__main__":
    with open(FILENAME) as file:
        contents = file.read().splitlines()
    
    np.set_printoptions(linewidth=163)
    
    print(part_1(contents.copy()))
    print(part_2(contents))

