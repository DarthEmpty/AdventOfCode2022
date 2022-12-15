from typing import List
from treenode import Node, Directory, Leaf

FILENAME = "07/input.txt"


def node_gen(commands: List[str]):
    while commands and not commands[0].startswith("$ "):
        yield commands.pop(0)


def cd_mode(path: str, current_node: Node):
    if path == "/":
        while current_node.name != "/":
            current_node = current_node.parent
    
    elif path == "..":
        current_node = current_node.parent
    
    else:
        current_node = current_node.children[path]
    
    return current_node


def ls_mode(commands: List[str], current_node: Directory):
    children = [child.split() for child in node_gen(commands)]
    children = {
        name:
        Directory(name, current_node) if prefix == "dir"
        else Leaf(name, current_node, int(prefix))
        for prefix, name in children
    }
    
    current_node.children = children


def small_sum(root: Directory) -> int:
    total = 0
    limit = 1e5
    nodes = [root]
    
    while nodes:
        current = nodes.pop(0)
        size = current.size()
        total += size if size <= limit else 0
        
        if isinstance(current, Directory):
            nodes.extend([
                child for child in current.children.values()
                if isinstance(child, Directory)
            ])
    
    return total


def part_1(contents: List[str]):
    current_node = Directory("/", None)
    
    # Initialise tree
    while contents:
        command = contents.pop(0).split()
        
        if command[1] == "cd":
            current_node = cd_mode(command[2], current_node)
            
        elif command[1] == "ls":
            ls_mode(contents, current_node)
    
    current_node = cd_mode("/", current_node)
    
    return small_sum(current_node)


def part_2(contents):
    return ""


if __name__ == "__main__":
    with open(FILENAME) as file:
        contents = file.read().splitlines()
    
    print(part_1(contents))
    print(part_2(contents))

