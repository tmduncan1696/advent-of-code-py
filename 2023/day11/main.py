from dataclasses import dataclass
from itertools import combinations
from typing import Self

import numpy as np

from utils import read_input_file


@dataclass
class Universe:
    map: np.typing.ArrayLike

    @classmethod
    def from_string(cls, string: str) -> Self:
        string = string.replace("#", "1")
        string = string.replace(".", "0")
        string_list = [list(x) for x in string.split("\n")]

        return cls(np.array([[int(x) for x in l] for l in string_list]))

    def _get_galaxy_pairs(self) -> list:
        galaxies = np.argwhere(self.map == 1).tolist()
        galaxy_pairs = combinations(galaxies, 2)
        return list(galaxy_pairs)

    @staticmethod
    def _get_galaxy_distance(a: list[int], b: list[int]) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @classmethod
    def _get_expanded_galaxy_distance(
        cls,
        a: list[int],
        b: list[int],
        expanded_rows: list[int],
        expanded_cols: list[int],
        expansion_multiplier: int,
    ) -> int:
        unexpanded_distance = cls._get_galaxy_distance(a, b)
        expansion = (
            len(
                [
                    x
                    for x in range(min(a[0], b[0]), max(a[0], b[0]))
                    if x in expanded_rows
                ]
            )
            + len(
                [
                    y
                    for y in range(min(a[1], b[1]), max(a[1], b[1]))
                    if y in expanded_cols
                ]
            )
        ) * (expansion_multiplier - 1)
        return unexpanded_distance + expansion

    def expand_and_sum_galaxy_distances(self, expansion_multiplier: int):
        rows_to_expand = []
        for i in range(self.map.shape[0]):
            if self.map[[i], :].sum() == 0:
                rows_to_expand.append(i)

        cols_to_expand = []
        for i in range(self.map.shape[1]):
            if self.map[:, [i]].sum() == 0:
                cols_to_expand.append(i)

        galaxy_pairs = self._get_galaxy_pairs()
        galaxy_distances = [
            self._get_expanded_galaxy_distance(
                a, b, rows_to_expand, cols_to_expand, expansion_multiplier
            )
            for a, b in galaxy_pairs
        ]
        return sum(galaxy_distances)


def main(input_file: str) -> None:
    input_data = read_input_file(input_file)

    universe = Universe.from_string(input_data)
    print(f"Part 1: {universe.expand_and_sum_galaxy_distances(2)}")

    print(f"Part 2: {universe.expand_and_sum_galaxy_distances(1_000_000)}")
