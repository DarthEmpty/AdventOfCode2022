import numpy as np
from collections import namedtuple
from typing import List, Any
from colorama import init as color_init, Fore, Style

_COORDS = namedtuple("Coordinates", "row column")

color_init()  # Using colours because why not?


class GridMap:
    def __init__(self, strings: List[str], backwards=False):
        self._contents = np.array([list(line) for line in strings])
        self._visited = np.zeros(self._contents.shape, dtype=bool)
        self._backwards = backwards
        
        self._start = _COORDS(*np.where(self._contents == "S"))
        self._end = _COORDS(*np.where(self._contents == "E"))
        
        self._contents[self._start] = "a"
        self._contents[self._end] = "z"
    
    def __str__(self) -> str:
        color_in = np.vectorize(
            lambda s: Fore.GREEN + s if s != "." else Fore.RED + s
        )
        revealed = color_in(np.where(self._visited, self._contents, "."))
        
        return "\n".join(["".join(row) for row in revealed]) + Style.RESET_ALL
    
    @property
    def start(self) -> _COORDS:
        return self._start
    
    @property
    def end(self) -> _COORDS:
        return self._end
    
    def _is_in_bounds(self, coords: _COORDS) -> np.ndarray[Any, bool]:
        grid_idxs = _COORDS(
            np.arange(self._contents.shape[0]),
            np.arange(self._contents.shape[1])
        )
        
        return contains_coords(coords, grid_idxs)
    
    def _is_reachable(self, start: _COORDS, end: _COORDS) -> np.ndarray[Any, bool]:
        start_value = self._contents[start].view(np.uint32)
        end_value = self._contents[end].view(np.uint32)
        
        if self._backwards:
            return np.isin(end_value, np.arange(start_value - 1, ord("z") + 1))
        
        return np.isin(end_value, np.arange(start_value + 2))
    
    def _has_been_visited(self, coords: _COORDS) -> np.ndarray[Any, bool]:
        return self._visited[coords]
    
    def reachable_neighbours(self, coords: _COORDS) -> _COORDS:
        row, column = coords
        
        cardinals = _COORDS(
            #         North    South    West        East
            np.array((row + 1, row - 1, row,        row       )),  # Rows
            np.array((column,  column,  column + 1, column - 1))   # Columns
        )
        
        # Remove any out of bounds coordinates immediately
        # to avoid ArrayIndexOutOfBounds errors
        in_bounds = self._is_in_bounds(cardinals)
        cardinals = _COORDS(cardinals.row[in_bounds], cardinals.column[in_bounds])
        
        validity = np.logical_and(
            self._is_reachable(coords, cardinals),
            np.logical_not(self._has_been_visited(cardinals))
        )
        
        return _COORDS(cardinals.row[validity], cardinals.column[validity])
    
    def visit(self, coords: _COORDS):
        self._visited[coords] = True
    
    def height_of(self, coords: _COORDS) -> str:
        return self._contents[coords][0]


class Node:
    def __init__(self, coords: _COORDS, parent=None):
        self._coords = coords
        self._parent = parent
        self._children = []
    
    def __str__(self) -> str:
        return str(self._coords)
    
    @property
    def coords(self) -> _COORDS:
        return self._coords
    
    @property
    def children(self) -> List:
        return self._children
    
    def add_children(self, children: _COORDS):
        self._children.extend(
            Node(_COORDS(children.row[i], children.column[i]), self)
            for i in range(len(children.row))
        )
    
    def count_steps(self):
        if not self._parent:
            return 0
        
        return 1 + self._parent.count_steps()
    

def contains_coords(coords: _COORDS, others: _COORDS) -> np.ndarray[Any, bool]:
    return np.logical_and(
        np.isin(coords.row, others.row),
        np.isin(coords.column, others.column)
    )
        