import numpy as np
from collections import namedtuple
from typing import List, Tuple

_COORDS = Tuple[int, int]


class GridMap:
    def __init__(self, strings: List[str]):
        self._contents = np.array([list(line) for line in strings])
        self._visited = np.zeros(self._contents.shape, dtype=bool)
        
        self._start = np.where(self._contents == "S")
        self._end = np.where(self._contents == "E")
        
        self._visited[self._start] = 1
        self._contents[self._start] = "a"
        self._contents[self._end] = "z"
    
    def __str__(self) -> str:       
        return "\n".join(["".join(row) for row in self._contents])
    
    def is_valid(self, coords: _COORDS) -> bool:
        return coords[0] in range(self._contents.shape[0]) \
            and coords[1] in range(self._contents.shape[1])
    
    def is_reachable(self, start: _COORDS, end: _COORDS) -> bool:
        start_value = ord(self._contents[start])
        end_value = ord(self._contents[end])
        
        return end_value in range(start_value - 1, start_value + 2)
    
    def has_been_visited(self, coords: _COORDS) -> bool:
        return self._visited[coords]
    
    def reachable_neighbours(self, coords: _COORDS) -> List[_COORDS]:
        row, column = coords
        
        cardinals = [
            (row + 1, column),  # North
            (row - 1, column),  # South
            (row, column + 1),  # West
            (row, column - 1),  # East
        ]
        
        return [
            direction for direction in cardinals 
            if self.is_valid(direction)
            and self.is_reachable(coords, direction)
            and not self.has_been_visited(direction)
        ]
    
    def visit(self, coords: _COORDS):       
        self._visited[coords] = True