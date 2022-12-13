import string

FILENAME = "03/input.txt"


def midpoint(l: list):
    return int(len(l)/2)


def type_priority(letter: str):
    return 1 + string.ascii_letters.index(letter)


def part_1(contents):
    duplicates = [
        set(bag[:midpoint(bag)]) & set(bag[midpoint(bag):])
        for bag in contents
    ]

    priorities = [type_priority(dup.pop()) for dup in duplicates]

    return sum(priorities)


def part_2(contents):
    trios = [
        (contents[3*i], contents[3*i + 1], contents[3*i + 2])
        for i in range(int(len(contents)/3))
    ]
    
    triplicates = [
        set(trio[0]) & set(trio[1]) & set(trio[2])
        for trio in trios
    ]
    
    priorities = [type_priority(trip.pop()) for trip in triplicates]
    
    return sum(priorities)


if __name__ == "__main__":
    with open(FILENAME) as file:
        contents = file.read().splitlines()
    
    print(part_1(contents))
    print(part_2(contents))
