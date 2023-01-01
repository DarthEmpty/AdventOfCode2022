import numpy as np
import re
from tqdm import tqdm
from collections import namedtuple
from sympy import solve, Symbol, Abs
from typing import List, Tuple, Set

FILENAME = "15/input.txt"
LIMIT = int(4e6)
POINT = Tuple[int, int]
SENSOR = namedtuple("Sensor", "pos radius")


def manhattan_distance(point: POINT, other: POINT) -> int:
    return sum([abs(p - o) for p, o in zip(point, other)])


# SO! The equation for a circle is (x-h)^2 + (y-k)^2 = r^2
# where (h, k) is its centre and r is the radius.
# This is very similar to the l2 norm (euclidean distance).
# But we're using l1 norm (manhattan distance).
# So the equation changes to |x-h| + |y-k| = r
# (This is probably a known fact, but I'm happy to have figured it out)
    
def solve_for_x(centre: POINT, radius: int, y:int):
    x = Symbol("x", integer=True)
    eq = Abs(x - centre[0]) + Abs(y - centre[1]) - radius
    return solve(eq, x)


def corners(centre: POINT, radius: int) -> List[POINT]:
    return [
        (centre[0], centre[1] + radius),  # North
        (centre[0] + radius, centre[1]),  # East
        (centre[0], centre[1] - radius),  # South
        (centre[0] - radius, centre[1]),  # West
    ]


def outer_perimeter(sensor: SENSOR) -> np.ndarray:
    corner_points = corners(sensor.pos, sensor.radius + 1)
    
    return np.vstack([
        np.linspace(corner,
                corner_points[(i+1) % 4],
                num=sensor.radius + 2,
                dtype=int)
        for i, corner in enumerate(corner_points)
    ])


def intersect2d(array1, array2):
    mask = np.logical_and(
        np.isin(array1[:,0], array2[:,0]),
        np.isin(array1[:,1], array2[:,1])
    )
    
    return array1[mask]


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
        if (intersections := solve_for_x(sensor.pos, sensor.radius, line)):
            scanned.update(range(intersections[0], intersections[-1] + 1))
    
    return len(
        scanned - set(beacon[0] for beacon in beacons if beacon[1] == line)
    )


# Had to look up the theory for this one.
def part_2(contents: List[str]) -> int:
    sensors, _ = interpret(contents)
    
    # Find the pairs of squares that are separated by
    # a manhattan distance of 2
    pairs = set()
    for sensor in sensors:
        pairs.update(
            (sensor, sensors[i])
            for i in range(sensors.index(sensor), len(sensors))
            if sensor != sensors[i]
            and manhattan_distance(sensor.pos, sensors[i].pos) == \
                sensor.radius + sensors[i].radius + 2
        )

    # Find the points that each pair shares just outside their perimiters.
    # These are the points to test.
    shared_perim = np.unique(np.vstack([
        intersect2d(outer_perimeter(a), outer_perimeter(b)) for a, b in pairs
    ]), axis=0)
    
    # Filter out negatives
    # (Would recommend filtering out ones that are too big too
    # but this works for the task and I'm sick of this one, lmao)
    shared_perim = shared_perim[
        np.logical_and(shared_perim[:,0] >= 0, shared_perim[:,1] >= 0)
    ]
    
    # Filter out the points that are detected by a sensor
    for sensor in tqdm(sensors):
        shared_perim = shared_perim[
            # Manhattan distance, in numpy form
            np.sum(abs(shared_perim - sensor.pos), axis=1) > sensor.radius
        ]
    
    # We are left with a single point undetected by all sensors
    point = shared_perim[0]
    return int(4e6) * point[0] + point[1]


if __name__ == "__main__":
    with open(FILENAME) as file:
        contents = file.read().splitlines()
    
    print(part_1(contents))
    print(part_2(contents))
