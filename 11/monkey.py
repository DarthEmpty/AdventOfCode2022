import re
import numpy as np
from typing import List, Callable, Tuple


class Monkey:
    def __init__(self, items: List[int], op: Callable, test: Callable, anxious=False) -> None:
        # Fields
        self._items = _int_array(items)
        self._anxious = anxious
        self._total = 0
        
        # Methods
        self._op = op
        self._test = test
    
    def __call__(self) -> List[Tuple[int, int]]:
        items = self._items
        self._total += np.size(items)
        self._items = _int_array([])
        
        items = self._op(items)

        if not self._anxious:
            items = items // 3

        return np.stack((self._test(items), items), axis=1)
    
    def __str__(self) -> str:
        return str(self._items)
    
    def receive(self, item: int) -> None:
        self._items = np.append(self._items, item)
    
    def total_inspections(self) -> int:
        return self._total


def _int_array(arraylike) -> np.ndarray:
    return np.array(arraylike, dtype=np.int)


def _find_num(string: str):
    return int(re.search("\d+", string).group(0))


def make_monkey(desc: str, anxious=False) -> Monkey:
    desc = desc.split("\n")
    
    items = [int(item) for item in re.findall("\d+", desc[1])]
    op = lambda old: eval(desc[2].lstrip().removeprefix("Operation: new = "))
    
    divisor = _find_num(desc[3])
    test = lambda new: np.where(
        new % divisor == 0, 
        _find_num(desc[4]),
        _find_num(desc[5])
    )
    
    return Monkey(items, op, test, anxious), divisor
    