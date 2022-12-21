from typing import List
from monkey import Monkey, make_monkey
from math import prod

FILENAME = "11/small.txt"


def rounds(amount: int, monkeys: List[Monkey]):
    for _ in range(amount):
        for monkey in monkeys:
            for target, item in monkey():
                monkeys[target].receive(item)


def part_1(contents: List[str]) -> int:
    monkeys = [make_monkey(desc) for desc in contents]

    rounds(20, monkeys)
    
    activity = [monkey.total_inspections() for monkey in monkeys]
    return prod(sorted(activity)[-2:])


def part_2(contents: List[str]) -> int:
    monkeys = [make_monkey(desc, anxious=True) for desc in contents]
    
    rounds(10000, monkeys)
    
    activity = [monkey.total_inspections() for monkey in monkeys]
    return prod(sorted(activity)[-2:])


if __name__ == "__main__":
    with open(FILENAME) as file:
        contents = file.read().split("\n\n")
    
    print(part_1(contents))
    print(part_2(contents))

