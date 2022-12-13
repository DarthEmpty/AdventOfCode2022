FILENAME = "01/input.txt"


if __name__ == "__main__":
    with open(FILENAME) as file:
        contents = file.read().split("\n\n")

    contents = [
        sum([int(x) for x in elf.splitlines()])
        for elf in contents
    ]
    
    contents.sort(reverse=True)
    
    print(sum(contents[:3]))        
