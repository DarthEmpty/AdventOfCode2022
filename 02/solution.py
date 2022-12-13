# Could do a similar thing but with dictionaries mapping pairs to scores.
# Which means that this solution is over engineered...
# I do still like it thought, and cba changing it rn.

FILENAME = "02/input.txt"
CONVERSION = {"A": 0, "B": 1, "C": 2, "X": 0, "Y": 1, "Z": 2}
SCORES_RPS = [  # Scores when XYZ == Rock, Paper Scissors
#   X     Y    Z
    [4,   8,   3],  # A

    [1,   5,   9],  # B

    [7,   2,   6]   # C
]
SCORES_LDW = [  # Scores when XYZ == Lose, Draw, Win
#   X     Y    Z
    [3,   4,   8],  # A

    [1,   5,   9],  # B

    [2,   6,   7]   # C
]


def find_score(pair: str, lookup: list):
    letter_row, letter_col = pair.split()
    row, column = CONVERSION[letter_row], CONVERSION[letter_col]

    return lookup[row][column]


def part_1(contents):
    return sum([
        find_score(pair, SCORES_RPS)for pair in contents
    ])


def part_2(contents):
    return sum([
        find_score(pair, SCORES_LDW) for pair in contents
    ])


if __name__ == "__main__":
    with open(FILENAME) as file:
        contents = file.read().splitlines()
    
    print(part_1(contents))
    print(part_2(contents))
