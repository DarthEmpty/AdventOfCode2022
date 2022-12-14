from typing import List
import re

FILENAME = "05/input.txt"


def crates(string: str):
    while string:
        crate, string = string[:4], string[4:]
        yield crate


def setup(strings: List[str]) -> List[List[str]]:
    # Find the number of stacks to make
    stack_no = int(strings.pop().rstrip()[-1])
    stacks = [[] for _ in range(stack_no)]    
    
    # Fill in the stacks row by row from the bottom up
    stack_idx = 0
    for row in reversed(strings):
        for crate in crates(row):
            if not crate.isspace():
                crate = crate.strip("[] ")
                stacks[stack_idx].append(crate)
                
            stack_idx = (stack_idx + 1) % stack_no
    
    return stacks


def move_from_to(x: int, y: int, z: int, config: List[List[str]], move_multiple=False):
    # Each procedure has the pattern "move x from y to z". 
    config[y], crates = config[y][:-x], config[y][-x:] 
    config[z].extend(
        # If the crates are moved 1 at a time, then they are
        # put on the stack in reverse order.
        crates if move_multiple else reversed(crates)
    )


def part_1(contents: List[str]) -> str:
    split_idx = contents.index("")
    config, proc = contents[:split_idx], contents[split_idx + 1:]
    
    config = setup(config)
    
    proc = [re.findall("\d+", p) for p in proc]
    
    for x, y, z in proc:
        move_from_to(int(x), int(y) - 1, int(z) - 1, config)
    
    return "".join([stack.pop() for stack in config])


def part_2(contents: List[str]) -> str:
    split_idx = contents.index("")
    config, proc = contents[:split_idx], contents[split_idx + 1:]
    
    config = setup(config)
    
    proc = [re.findall("\d+", p) for p in proc]
    
    for x, y, z in proc:
        move_from_to(
            int(x), int(y) - 1, int(z) - 1,
            config,
            move_multiple=True
        )
    
    return "".join([stack.pop() for stack in config])


if __name__ == "__main__":
    with open(FILENAME) as file:
        contents = file.read().splitlines()
    
    print(part_1(contents))
    print(part_2(contents))

