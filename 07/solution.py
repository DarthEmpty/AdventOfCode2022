from typing import List, Tuple
from treenode import Node, Directory, Leaf

FILENAME = "07/input.txt"


def node_gen(commands: List[str]):
    while commands and not commands[0].startswith("$ "):
        yield commands.pop(0)


def cd(path: str, current_node: Node) -> Node:
    if path == "/":
        while current_node.name != "/":
            current_node = current_node.parent
    
    elif path == "..":
        current_node = current_node.parent
    
    else:
        current_node = current_node.children[path]
    
    return current_node


def ls(commands: List[str], current_node: Directory) -> Node:
    children = [child.split() for child in node_gen(commands)]

    return {
        name:
        Directory(name, current_node) if prefix == "dir"
        else Leaf(name, current_node, int(prefix))
        for prefix, name in children
    }


def construct_tree(command_list: List[str]) -> Node:
    current_node = Directory("/", None)
    
    while command_list:
        command = command_list.pop(0).split()
        
        if command[1] == "cd":
            current_node = cd(command[2], current_node)
            
        elif command[1] == "ls":
            current_node.children = ls(command_list, current_node)
      
    return cd("/", current_node)


def small_sum(root: Directory, limit = 1e5) -> int:
    total = 0
    nodes = [root]
    
    # bfs
    # Probably not as time efficient as possible since sizes are worked out multiple times
    # (once for each node between root and current inclusive)
    while nodes:
        current = nodes.pop(0)
        size = current.size()
        total += size if size <= limit else 0
        
        nodes.extend([
            child for child in current.children.values()
            if isinstance(child, Directory)
        ])
    
    return total


def big_collection(root: Directory, start: int, minimum=0):
    nodes = [root]
    smallest = start
    
    while nodes:
        current = nodes.pop(0)
        size = current.size()
        smallest = size if size >= minimum and size < smallest else smallest
        
        nodes.extend([
            child for child in current.children.values()
            if isinstance(child, Directory)
        ])
    
    return smallest


def part_1(contents: List[str]) -> Tuple[Node, int]:    
    return (
        current_node := construct_tree(contents),
        small_sum(current_node)
    )


def part_2(tree: Node) -> int:
    tree_size = tree.size()
    minimum = int(tree_size - 4e7)
    
    return big_collection(tree, tree_size, minimum)


if __name__ == "__main__":
    with open(FILENAME) as file:
        contents = file.read().splitlines()
    
    tree, size =part_1(contents)
    print(size)
    
    print(part_2(tree))
