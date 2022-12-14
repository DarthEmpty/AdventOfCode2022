DAY_NO_DIGIT=$1
printf -v DAY_NO "%02d" $1


# Check existense before making directory
[ -d $DAY_NO ] && echo "Day ${DAY_NO} already exists!" && exit

mkdir $DAY_NO;


# Initialise the Python file
echo "FILENAME = \"${DAY_NO}/input.txt\"


def part_1(contents):
    return \"\"


def part_2(contents):
    return \"\"


if __name__ == \"__main__\":
    with open(FILENAME) as file:
        contents = file.read().splitlines()
    
    print(part_1(contents))
    print(part_2(contents))
" > $DAY_NO/solution.py


# Download input file
curl --cookie ./cookies.txt https://adventofcode.com/2022/day/$DAY_NO_DIGIT/input > $DAY_NO/input.txt
chmod =r $DAY_NO/input.txt
