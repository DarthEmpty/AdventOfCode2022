from typing import List
from grid_map import GridMap, Node, contains_coords

FILENAME = "12/input.txt"


def part_1(contents: List[str]) -> int:
    letter_map = GridMap(contents)
    nodes = [Node(letter_map.start)]
    
    while nodes:
        # Consider the neighbours of one of the nodes that we're at
        current_node = nodes.pop(0)
        neighbours = letter_map.reachable_neighbours(current_node.coords)
        
        # Return the number of steps if we see the end!
        if contains_coords(letter_map.end, neighbours):
            current_node.add_children(letter_map.end)
            return current_node.children[0].count_steps()
        
        # Otherwise, visit all the neighbours by adding them to the queue
        letter_map.visit(neighbours)
        current_node.add_children(neighbours)
        nodes.extend(current_node.children)
    
    # Something went wrong!
    print("We ran out of nodes to explore... here's what we did find:")
    print(letter_map)    
    return -1


# TODO: Similar to Part 1 but in reverse! (From End to an "a")
def part_2(contents: List[str]) -> int:
    return 0


if __name__ == "__main__":
    with open(FILENAME) as file:
        contents = file.read().splitlines()
    
    print(part_1(contents))
    print(part_2(contents))

