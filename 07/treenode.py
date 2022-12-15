class Node:
    def __init__(self, name: str, parent) -> None:
        self.name = name
        self.parent = parent
    
    def size(self) -> int: 
        return 0


class Directory(Node):
    def __init__(self, name: str, parent: Node) -> None:
        super().__init__(name, parent)
        self.children = {}
    
    def size(self) -> int:
        return sum([child.size() for child in self.children.values()])


class Leaf(Node):
    def __init__(self, name: str, parent: Node, size: int) -> None:
        super().__init__(name, parent)
        self._size = size
    
    def size(self) -> int:
        return self._size
    
    