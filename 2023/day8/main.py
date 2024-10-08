#!/usr/bin/env python3

import numpy as np
import re

def create_map(input_str: str) -> dict[str, dict[str, str]]:
    MAP_REGEX = re.compile(r'(\w{3}) = \((\w{3}), (\w{3})\)')

    matches = [
        MAP_REGEX.match(s)
        for s in input_str
    ]

    mapping = {
        m.group(1): {
            'L': m.group(2),
            'R': m.group(3)
        }
        for m in matches
    }

    return mapping

def get_steps(instructions: str, map_dict: dict[str, dict[str, str]], current_loc: str = 'AAA', ending_loc: str = 'ZZZ') -> int:
    steps = 0
    while True:
        for i in instructions:
            current_loc = map_dict.get(current_loc).get(i)
            steps += 1
            if re.match(ending_loc, current_loc):
                return steps

def get_ghost_steps(instructions: str, map_dict: dict[str, dict[str, str]]) -> int:
    current_locs = [
        x
        for x in map_dict.keys()
        if x[2] == 'A'
    ]

    steps = [
        get_steps(instructions, map_dict, loc, r'\w\wZ')
        for loc in current_locs
    ]

    return np.lcm.reduce(steps)


def part1(input) -> None:
    instructions = input[0]

    map_input = input[1:]

    map_dict = create_map(map_input)

    steps = get_steps(instructions, map_dict)

    print(f'Part 1: {steps}')


def part2(input) -> None:
    instructions = input[0]

    map_input = input[1:]

    map_dict = create_map(map_input)

    steps = get_ghost_steps(instructions, map_dict)

    print(f'Part 2: {steps}')


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-e', '--example', action='store_true')

    args = parser.parse_args()

    input_file = 'data/example_input.txt' if args.example else 'data/input.txt'

    with open(input_file) as f:
        input = [line.strip() for line in f.readlines() if line.strip() != '']

    part1(input)
    part2(input)

if __name__ == '__main__':
    main()
