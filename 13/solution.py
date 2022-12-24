from typing import List, Iterator, Tuple, Union

FILENAME = "13/input.txt"


def enum_pairs(pairs: List[str]) -> Iterator[Tuple[int, List, List]]:
    for idx, pair in enumerate(pairs):
        left, right = pair.split()
        yield idx + 1, eval(left), eval(right)


def larger_int(x: int, y: int) -> Union[int, None]:
    if x == y:
        return None
    
    return x if x > y else y


def to_lists(*xs: Union[int, List]) -> List[List]:
    return [[x] if isinstance(x, int) else x for x in xs]


def in_order(left: List, right: List) -> Union[bool, None]:    
    try:
        for l, r in zip(left, right, strict=True):
            
            if isinstance(l, int) and isinstance(r, int) \
                and (larger := larger_int(l, r)) is not None:
                    return larger == r
            
            elif (isinstance(l, list) or isinstance(r, list)) \
                and (result := in_order(*to_lists(l, r))) is not None:
                    return result

    except ValueError as ve:
        # The ValueError is caused by the input lists
        # being different sizes.
        # The error message always describes the second input
        # as "longer" or "shorter".
        # So, packets are in order if it's "longer".
        return "longer" in ve.args[0]
    
    return None


def packet_quicksort(elements: List[Union[int, List]]) -> List:
    if len(elements) <= 1:
        return elements
    
    left = []
    right = []
    pivot = elements.pop()

    for element in elements:
        side = left if in_order(element, pivot) else right
        side.append(element)
        
    return packet_quicksort(left) + [pivot] + packet_quicksort(right)


def part_1(contents: str) -> int:     
    return sum(
        idx for idx, left, right
        in enum_pairs(contents.split("\n\n"))
        if in_order(left, right)
    )


def part_2(contents: str) -> int:
    packets = [eval(packet) for packet in contents.split()]
    packets.append([[2]])
    packets.append([[6]])
    
    sorted_packs = packet_quicksort(packets)
    
    return (sorted_packs.index([[2]]) + 1) * (sorted_packs.index([[6]]) + 1)


if __name__ == "__main__":
    with open(FILENAME) as file:
        contents = file.read()
    
    print(part_1(contents))
    print(part_2(contents))

