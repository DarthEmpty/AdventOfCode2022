FILENAME = "06/input.txt"

def find_marker(size: int, signal: str):
    for idx in range(len(signal) - size + 1):
        marker = set(signal[idx:idx + size])
        if len(marker) == size:
            return idx + size
    
    return "No marker detected"


def part_1(contents):
    return find_marker(4, contents)


def part_2(contents):
    return find_marker(14, contents)


if __name__ == "__main__":
    with open(FILENAME) as file:
        contents = file.read()
    
    print(part_1(contents))
    print(part_2(contents))

