from copy import copy
from dataclasses import dataclass, field
from enum import Enum
from typing import Protocol, Self

import numpy as np

from utils import read_input_file


class Direction(Enum):
    North = [-1, 0]
    South = [1, 0]
    East = [0, 1]
    West = [0, -1]


def reverse_direction(direction: Direction) -> Direction:
    return Direction([-x for x in direction.value])


@dataclass
class Cell(Protocol):
    directions = list[Direction]


@dataclass
class Ground:
    directions = []


@dataclass
class Start:
    directions = [Direction.North, Direction.South, Direction.East, Direction.West]


@dataclass
class Pipe:
    directions: list[Direction]


def get_cell_from_string(string: str) -> Cell:
    if string == ".":
        return Ground()
    if string == "S":
        return Start()
    if string == "|":
        return Pipe([Direction.North, Direction.South])
    if string == "-":
        return Pipe([Direction.East, Direction.West])
    if string == "L":
        return Pipe([Direction.North, Direction.East])
    if string == "J":
        return Pipe([Direction.North, Direction.West])
    if string == "7":
        return Pipe([Direction.South, Direction.West])
    if string == "F":
        return Pipe([Direction.South, Direction.East])

    raise NotImplementedError(f"{string} is not implemented as a Cell")


@dataclass
class Location:
    x: int
    y: int

    def as_array(self) -> np.typing.ArrayLike:
        return np.asarray([self.x, self.y])


class BadDirectionError(Exception):
    """
    Exception raised for moving in a bad direction

    Attributes:
        message - explanation of error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


class LoopError(Exception):
    """
    Exception raised for when no loop is found

    Attributes:
        message - explanation of error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


@dataclass
class Map:
    matrix: list[list[Cell]]
    starting_location: Location = field(init=False)
    active_location: Location = field(init=False)
    dim: list[int] = field(init=False)
    loop: list[Location] = field(init=False)

    def __post_init__(self):
        self.dim = [len(self.matrix[0]), len(self.matrix)]

        for x in range(self.dim[0]):
            for y in range(self.dim[1]):
                loc = Location(x, y)
                if isinstance(self.get_cell(loc), Start):
                    self.starting_location = loc

        self.active_location = copy(self.starting_location)
        self.loop = self._find_loop()

    @classmethod
    def from_string(cls, string: str) -> Self:
        str_mat = [list(x) for x in string.split("\n")]
        matrix = [[get_cell_from_string(c) for c in row] for row in str_mat]
        return cls(matrix)

    def reset(self) -> None:
        self.active_location = copy(self.starting_location)

    def is_loc_valid(self, loc: list) -> bool:
        return (0 <= loc.x < self.dim[0]) and (0 <= loc.y < self.dim[1])

    def get_cell(self, loc: Location) -> Cell:
        return self.matrix[loc.y][loc.x]

    def move(self, direction: Direction) -> None:
        start_loc = self.active_location
        start_cell = self.get_cell(start_loc)

        if direction not in start_cell.directions:
            raise BadDirectionError(f"Cannot move {direction.name} from {start_loc}")

        new_loc = start_loc
        if direction == Direction.North:
            new_loc.y -= 1
        elif direction == Direction.South:
            new_loc.y += 1
        elif direction == Direction.East:
            new_loc.x += 1
        elif direction == Direction.West:
            new_loc.x -= 1

        if not self.is_loc_valid(new_loc):
            raise IndexError("Location is not valid")

        if reverse_direction(direction) not in self.get_cell(new_loc).directions:
            raise BadDirectionError(f"Cannot move {direction.name} into {new_loc}")

        self.active_location = new_loc

    def _find_loop(self) -> list[Location]:
        directions_to_try = [
            Direction.North,
            Direction.South,
            Direction.East,
            Direction.West,
        ]

        for d in directions_to_try:
            self.reset()
            prior_d = None
            locations = [self.active_location]
            keep_running = True
            while keep_running:
                try:
                    self.move(d)
                    prior_d = d
                    d = copy(self.get_cell(self.active_location).directions)
                    d = [x for x in d if x != reverse_direction(prior_d)][0]
                    locations.append(copy(self.active_location))
                    if isinstance(self.get_cell(self.active_location), Start):
                        return locations
                except BadDirectionError:
                    keep_running = False

        raise LoopError("No loop found")

    @property
    def area(self) -> float:
        a = np.vstack([loc.as_array() for loc in self.loop])
        s1 = sum(a[:-1, 0] * a[1:, 1])
        s2 = sum(a[:-1, 1] * a[1:, 0])

        return abs(s1 - s2) / 2

    @property
    def interior_points(self) -> int:
        return int(self.area + 1 - (len(self.loop) - 1) / 2)


def main(input_file: str) -> None:
    input_data = read_input_file(input_file)

    input_map = Map.from_string(input_data)

    part1_sol = int(len(input_map.loop) / 2)
    print(f"Part 1: {part1_sol}")

    print(f"Part 2: {input_map.interior_points}")
