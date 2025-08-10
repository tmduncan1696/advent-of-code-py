#!/usr/bin/python3

"""
Advent of Code 2023 Day 5
"""

import functools
import re

from utils import read_input_file


def main(input_file: str) -> None:
    """
    Main Function
    """
    input_data = read_input_file(input_file)

    input_lines = input_data.split('\n\n')

    # Part 1
    seed_string = input_lines[0]
    seeds = [
        int(x)
        for x in re.findall(r'\d+', seed_string)
    ]

    map_names = [
        re.search(r'(.*) map:(.*)', x)
        for x in input_lines
    ]

    map_names = [
        x.group(1)
        for x in map_names
        if x is not None
    ]

    maps = dict(zip(map_names, input_lines[1:]))

    maps = {
        k: [
            [int(d) for d in re.search(r'\d+ \d+ \d+', x).group(0).split(' ')]
            for x in v.split('\n')
            if re.search(r'\d+ \d+ \d+', x) is not None
        ]
        for k, v in maps.items()
    }

    def get_location(seed, maps):
        val = seed
        for m in maps.values():
            for x in m:
                diff = val - x[1]
                if 0 <= diff < x[2]:
                    val = x[0] + diff
                    break

        return val

    def get_min_location(seeds, maps):
        return min(get_location(s, maps) for s in seeds)

    print(f'Part 1: {get_min_location(seeds, maps)}')

    seed_ranges = [
        [seeds[i], seeds[i] + seeds[i + 1] - 1]
        for i in range(0, len(seeds), 2)
    ]

    def flatten_list(matrix):
        return list(functools.reduce(lambda x, y: x + y, matrix, []))

    def split_range(range1, range2):
        if max(range1) <= min(range2):
            return [range1]
        if min(range1) >= max(range2):
            return [range1]
        if min(range2) <= min(range1) < max(range1) <= max(range2):
            return [range1]
        if min(range1) < min(range2) < max(range2) < max(range1):
            return [
                [min(range1), min(range2) - 1],
                range2,
                [max(range2) + 1, max(range1)]
            ]
        if min(range1) < min(range2):
            return [
                [min(range1), min(range2) - 1],
                [min(range2), max(range1)]
            ]
        return [
            [min(range1), max(range2)],
            [max(range2) + 1, max(range1)]
        ]

    def get_new_ranges(start_ranges, mappings):
        split_ranges = start_ranges
        for mapping in mappings:
            range2 = [mapping[1], mapping[1] + mapping[2] - 1]
            split_ranges = flatten_list(
                [split_range(r, range2) for r in split_ranges]
            )

        new_ranges = []
        for mapping in mappings:
            diff = mapping[0] - mapping[1]
            range2 = [mapping[1], mapping[1] + mapping[2] - 1]
            remove_split_ranges = []
            for x in split_ranges:
                if min(range2) <= min(x) <= max(range2):
                    new_ranges.append([y + diff for y in x])
                    remove_split_ranges.append(x)

            split_ranges = [x for x in split_ranges if x not in remove_split_ranges]

        new_ranges += split_ranges
        return new_ranges

    def get_location_ranges(seed_ranges, map_ranges):
        r = seed_ranges
        for m in map_ranges.values():
            r = get_new_ranges(r, m)
        return r

    def get_min_location_from_ranges(seed_ranges, map_ranges):
        location_ranges = get_location_ranges(seed_ranges, map_ranges)
        return min(min(x) for x in location_ranges)

    print(f'Part 2: {get_min_location_from_ranges(seed_ranges, maps)}')
