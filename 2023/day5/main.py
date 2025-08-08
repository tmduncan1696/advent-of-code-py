#!/usr/bin/python3

"""
Advent of Code 2023 Day 5
"""


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


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--example', action='store_true')
    args = parser.parse_args()

    INPUT_FILE = 'data/example_input.txt' if args.example else 'data/input.txt'

    main(INPUT_FILE)
