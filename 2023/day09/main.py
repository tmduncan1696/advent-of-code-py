#!/usr/bin/env python3

from copy import deepcopy
import itertools
import re
import typing as t

def pairwise(iterable: t.Iterable) -> t.Iterable:
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

def create_pattern_list(lst: list[int]):
    x = [deepcopy(lst)]
    for i in range(len(lst)):
        next = [b - a for a, b in pairwise(x[i])]
        x.append(next)
        if all([y == 0 for y in next]):
            return x

def get_next_value_from_pattern_list(pattern_list: list[list[int]]) -> int:
    extrapolated_pattern_list = deepcopy(pattern_list)
    for i in range(len(pattern_list) - 1, 0, -1):
        a = extrapolated_pattern_list[i]
        b = extrapolated_pattern_list[i - 1]
        extrapolated_pattern_list[i - 1].append(a[len(a) - 1] + b[len(b) - 1])

    out_list = extrapolated_pattern_list[0]
    return out_list[len(out_list) - 1]

def get_next_value(lst: list[int]) -> int:
    pattern_list = create_pattern_list(lst)
    next_value = get_next_value_from_pattern_list(pattern_list)
    return next_value

def get_prev_value_from_pattern_list(pattern_list: list[list[int]]) -> int:
    extrapolated_pattern_list = deepcopy(pattern_list)
    for i in range(len(pattern_list) - 1, 0, -1):
        a = extrapolated_pattern_list[i]
        b = extrapolated_pattern_list[i - 1]
        extrapolated_pattern_list[i-1].insert(0, b[0] - a[0])

    out_list = extrapolated_pattern_list[0]
    return out_list[0]

def get_prev_value(lst: list[int]) -> int:
    pattern_list = create_pattern_list(lst)
    prev_value = get_prev_value_from_pattern_list(pattern_list)
    return prev_value

def part1(input: str) -> None:
    print(f'Part 1: {sum([get_next_value(x) for x in input])}')

def part2(input: str) -> None:
    print(f'Part 2: {sum([get_prev_value(x) for x in input])}')


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-e', '--example', action='store_true')

    args = parser.parse_args()

    input_file = 'data/example_input.txt' if args.example else 'data/input.txt'

    with open(input_file) as f:
        input = [[int(x.group()) for x in re.finditer(r'-?\d+', line.strip())] for line in f.readlines() if line.strip() != '']

    part1(input)
    part2(input)

if __name__ == '__main__':
    main()
