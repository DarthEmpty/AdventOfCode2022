import re
from collections import namedtuple
from sympy import solve, Symbol, Abs, Eq
from typing import List, Tuple, Set

FILENAME = "15/input.txt"
POINT = Tuple[int, int]
SENSOR = namedtuple("Sensor", "pos radius")


def manhattan_distance(point: POINT, other: POINT) -> int:
    return sum([abs(p - o) for p, o in zip(point, other)])


def solve_for_x(centre: POINT, radius: int, y:int):
    # SO! The equation for a circle is (x-h)^2 + (y-k)^2 = r^2
    # where (h, k) is its centre and r is the radius.
    # This is very similar to the l2 norm (euclidean distance).
    # But we're using l1 norm (manhattan distance).
    # So the equation changes to |x-h| + |y-k| = r
    # (This is probably a known fact, but I'm happy to have figured it out)
    
    x = Symbol("x", real=True)
    eq = Eq(Abs(x - centre[0]) + Abs(y - centre[1]), radius)
    return solve(eq, x)


def interpret(specs: List[str]) -> Tuple[List[SENSOR], Set[POINT]]:
    sensors = []
    beacons = set()
    
    for spec in specs:
        coords = re.findall("x=(-?\d+), y=(-?\d+)", spec)
        sensor_pos = int(coords[0][0]), int(coords[0][1])
        beacon_pos = int(coords[1][0]), int(coords[1][1])
        
        sensors.append(SENSOR(
            sensor_pos, manhattan_distance(sensor_pos, beacon_pos)
        ))
        beacons.add(beacon_pos)
    
    return sensors, beacons


def part_1(contents: List[str]) -> int:
    sensors, beacons = interpret(contents)
    scanned = set()
    line = int(2e6)  # = y
       
    for sensor in sensors:
        intersections = solve_for_x(sensor.pos, sensor.radius, line)
        
        if intersections:
            scanned.update(intersections)
            scanned.update(range(intersections[0], intersections[-1] + 1))
    
    return len(
        scanned - set(beacon[0] for beacon in beacons if beacon[1] == line)
    )


def part_2(contents: List[str]) -> int:
    return 0


if __name__ == "__main__":
    with open(FILENAME) as file:
        contents = file.read().splitlines()
    
    print(part_1(contents))
    print(part_2(contents))
