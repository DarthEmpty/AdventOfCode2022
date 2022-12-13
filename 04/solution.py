FILENAME = "04/input.txt"


def str_to_range(string: str) -> set:
    start, stop = string.split("-")
    return set(range(int(start), int(stop) + 1))


def str_to_range_pair(string: str) -> tuple:
    range_1, range_2 = string.split(",")
    return str_to_range(range_1), str_to_range(range_2)   


def part_1(contents) -> int:
    range_pairs = [str_to_range_pair(pair) for pair in contents]
    subsets = [
        pair[0].issubset(pair[1]) or pair[1].issubset(pair[0])
        for pair in range_pairs
    ]
    
    return subsets.count(True)


def part_2(contents) -> int:
    range_pairs = [str_to_range_pair(pair) for pair in contents]
    intersections = [bool(pair[0] & pair[1]) for pair in range_pairs]
    
    return intersections.count(True)


if __name__ == "__main__":
    with open(FILENAME) as file:
        contents = file.read().splitlines()
    
    print(part_1(contents))
    print(part_2(contents))
