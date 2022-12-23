from typing import List, Callable
from grid_map import GridMap, Node, contains_coords

FILENAME = "12/input.txt"


def bfs(grid_map: GridMap, start_node: Node, end_condition: Callable) -> int:
    grid_map.visit(start_node.coords)
    nodes = [start_node]
    
    while nodes:
        # Consider one of the nodes that we're at
        current_node = nodes.pop(0)
        
        # Return the number of steps if we're at the end!
        if end_condition(current_node):
            return current_node.count_steps()
        
        # Otherwise, visit all the neighbours by adding them to the queue
        neighbours = grid_map.reachable_neighbours(current_node.coords)
        grid_map.visit(neighbours)
        current_node.add_children(neighbours)
        nodes.extend(current_node.children)
    
    # Something went wrong!  
    raise Exception(
        "Ran out of nodes to explore, but here's what we did find:",
        str(grid_map)
    )
    

def part_1(contents: List[str]) -> int:
    letter_map = GridMap(contents)
    
    return bfs(
        letter_map,
        Node(letter_map.start),
        lambda current: contains_coords(current.coords, letter_map.end)
    )


# Similar to Part 1 but in reverse! (From End to an "a")
def part_2(contents: List[str]) -> int:
    letter_map = GridMap(contents, backwards=True)
    
    return bfs(
        letter_map,
        Node(letter_map.end),
        lambda current: letter_map.height_of(current.coords) == "a"
    )


if __name__ == "__main__":
    with open(FILENAME) as file:
        contents = file.read().splitlines()

    try:
        print(part_1(contents))
        print(part_2(contents))
    
    except Exception as e:
        print(e.args[0])
        print(e.args[1])

