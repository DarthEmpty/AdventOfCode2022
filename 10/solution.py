from typing import List, Tuple, Union, Generator

FILENAME = "10/input.txt"


def interpreted(commands: List[str]) -> Generator[Tuple[int, int], None, None]:
    while commands:
        current = commands.pop(0)
        
        if current.startswith("addx"):
            yield 2, int(current.split()[1])
        
        else:  # `current` is "noop"
            yield 1, 0


# TODO: Answer is too low
def part_1(contents: List[str]) -> int:
    register = 1
    history = []
    
    for duration, value in interpreted(contents):
        history.extend(register for _ in range(duration))
        register += value
    
    history.append(register)
    
    return sum(cycle * history[cycle] for cycle in range(20, 200, 40))


def part_2(contents: List[str]) -> int:
    return 0


if __name__ == "__main__":
    with open(FILENAME) as file:
        contents = file.read().splitlines()
    
    print(part_1(contents.copy()))
    print(part_2(contents))

