import re
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


def make_monkey(desc: str, anxious=False) -> Monkey:
    num_pattern = re.compile("\d+")
    desc = desc.split("\n")
    
    items = [int(item) for item in re.findall(num_pattern, desc[1])]
    op = lambda old: eval(desc[2].lstrip().removeprefix("Operation: new = "))
    
    divisor = re.search(num_pattern, desc[3]).group(0)
    t_branch = re.search(num_pattern, desc[4]).group(0)
    f_branch = re.search(num_pattern, desc[5]).group(0)
    test = lambda new: int(t_branch) if new % int(divisor) == 0 else int(f_branch)
    
    return Monkey(items, op, test, anxious)
    