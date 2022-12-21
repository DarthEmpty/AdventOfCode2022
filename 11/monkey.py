import re
import numpy as np
from typing import List, Callable, Tuple


class Monkey:
    def __init__(self, items: List[int], op: Callable, test: Callable, anxious=False) -> None:
        # Fields
        self._items = items
        self._anxious = anxious
        self._total = 0
        
        # Methods
        self._op = op
        self._test = test
    
    def __call__(self) -> List[Tuple[int, int]]:
        self._items = [
            self._op(item) if self._anxious
            else int(self._op(item) / 3)
            for item in self._items
        ]
        self._total += len(self._items)
        targets = [(self._test(item), item) for item in self._items]
        self._items.clear()
        
        return targets
    
    def __str__(self) -> str:
        return str(self._items)
    
    def receive(self, item: int) -> None:
        self._items.append(item)
    
    def total_inspections(self) -> int:
        return self._total


def find_num(string: str):
    return int(re.search("\d+", string).group(0))


def make_monkey(desc: str, anxious=False) -> Monkey:
    desc = desc.split("\n")
    
    items = [int(item) for item in re.findall("\d+", desc[1])]
    op = lambda old: eval(desc[2].lstrip().removeprefix("Operation: new = "))
    
    test = lambda new: np.where(
        new % find_num(desc[3]) == 0, 
        find_num(desc[4]),
        find_num(desc[5])
    )
    
    return Monkey(items, op, test, anxious)
    