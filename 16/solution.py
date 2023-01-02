import re
from collections import namedtuple
from typing import List, Tuple, Dict, Union

FILENAME = "16/input.txt"
VALVE = namedtuple("Valve", ["flow_rate", "neighbours"])


def interpret(specs: List[str]) -> Dict[str, VALVE]:
    pattern = "Valve ([A-Z]{2}) has flow rate=(\d+); " + \
        "tunnels* leads* to valves* ((?:[A-Z]{2}, )*(?:[A-Z]{2}))"
        
    matches = [re.search(pattern, spec).groups() for spec in specs]
    
    return {
        name: VALVE(int(flow_rate), neighbours.split(", "))
        for name, flow_rate, neighbours in matches
    }


def get_priorities(
    graph: Dict[str, VALVE],
    paths: Dict[str, list]
) -> List[Tuple[str, int]]:

    ratios = [
        ( key, graph[key].flow_rate / len(paths[key])**2 )
        for key in graph if paths[key]
    ]
    
    return sorted(ratios, key=lambda item: item[1], reverse=True)


def shortest_paths(graph: Dict[str, VALVE], start: str) -> Dict[str, list]:
    node_queue = [start]
    paths = {key: [] for key in graph}
    
    while node_queue:
        node = node_queue.pop(0)
        current = graph[node]
        
        for neighbour in current.neighbours:
            if not paths[neighbour] and neighbour != start:
                paths[neighbour] = paths[node] + [node]
                node_queue.append(neighbour)
    
    return paths


# TODO: Consider opening valves en route
def next_destination(
    graph: Dict[str, VALVE],
    start: str,
    time_left=float("inf"),
    opened=[]
) -> Union[Tuple[str, List[str]], None]:

    paths = shortest_paths(graph, start)
    priorities = get_priorities(graph, paths)
       
    for dest, _ in priorities:
        if dest not in opened and len((path := paths[dest])) <= time_left:
            return dest, path
    
    return None


def apply_ticks(
    duration: int,
    time_left: int,
    accumulated: int,
    new_value: int,
    history: List[int]
) -> Tuple[int, int, List[int]]:
    
    for _ in range(duration):
        if time_left <= 0:
            return time_left, accumulated, history
        else:
            time_left -= 1
        
        if not history:
            history = [0]
        else:
            history.append(accumulated)
    
    return time_left, accumulated + new_value, history
        

def part_1(contents: List[str]) -> int:
    graph = interpret(contents)
    valves = set(graph.keys())
    current = "AA"
    opened = set()
    time_left = 30
    pressure = 0
    released = []
    
    while valves.difference(opened) and time_left > 0:
        if (result := next_destination(graph, current, time_left, opened)):
            dest, path = result
            time_left, pressure, released = apply_ticks(
                len(path) + 1,
                time_left,
                pressure,
                graph[dest].flow_rate,
                released
            )
            current = dest
            opened.add(dest)
        
        else:
            time_left, _, released = apply_ticks(
                time_left,
                time_left,
                pressure,
                0,
                released
            )
    
    return sum(released)


def part_2(contents: List[str]) -> int:
    return 0


if __name__ == "__main__":
    with open(FILENAME) as file:
        contents = file.read().splitlines()
    
    print(part_1(contents))
    print(part_2(contents))

