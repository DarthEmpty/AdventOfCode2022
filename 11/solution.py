from typing import List
from monkey import Monkey, make_monkey
from math import prod

FILENAME = "11/input.txt"


def rounds(amount: int, monkeys: List[Monkey], anxious_mod=0):
    for _ in range(amount):
        for monkey in monkeys:
            for target, item in monkey():                
                monkeys[target].receive(
                    item % anxious_mod if anxious_mod else item
                )


def part_1(contents: List[str]) -> int:
    monkeys = [make_monkey(desc)[0] for desc in contents]

    rounds(20, monkeys)
    
    activity = sorted(monkey.total_inspections() for monkey in monkeys)
    return activity[-1] * activity[-2]


# Had to look this one up and I still don't understand it.
# My confusion as to why this works primarily hinges on the fact that
# the modulo operation doesn't conserve the magnitude of the original number.
# So, 17 mod 12 = 5, but then 17 * 2 = 34, whereas 5 * 2 = 10.
# 17 = 5 (mod 12), which makes sense, but then surely the largest number
# one could get by multiplying 2 numbers from the mod space is (mod - 1) * (mod - 1)?
def part_2(contents: List[str]) -> int:
    monkeys = []
    mod = 1
    
    for desc in contents:
        monkey, divisor = make_monkey(desc, anxious=True)
        monkeys.append(monkey)
        mod *= divisor
    
    rounds(10000, monkeys, anxious_mod=mod)
    
    activity = sorted(monkey.total_inspections() for monkey in monkeys)
    return activity[-1] * activity[-2]


if __name__ == "__main__":
    with open(FILENAME) as file:
        contents = file.read().split("\n\n")
    
    print(part_1(contents))
    print(part_2(contents))
