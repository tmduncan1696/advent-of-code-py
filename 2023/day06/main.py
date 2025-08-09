from copy import copy
import math
import re

DIGIT = re.compile(r'\d+')

def calculate_distance(time_held: int, total_time: int) -> int:
    if time_held > total_time:
        raise ValueError('time_held cannot exceed total_time')

    if time_held < 0:
        raise ValueError('time_held cannot be negative')

    if total_time < 0:
        raise ValueError('total_time cannot be negative')

    time_moving = total_time - time_held

    speed = time_held

    distance = time_moving * speed

    return distance

def wins_race(time_held: int, total_time: int, distance: int) -> bool:
    return calculate_distance(time_held, total_time) > distance


def min_time_held(total_time: int, distance: int) -> int:
    time = 0
    for x in range(1, total_time + 1):
        if wins_race(x, total_time, distance):
            time = x
            break

    return time

def max_time_held(total_time: int, distance: int) -> int:
    time = copy(distance)
    for x in reversed(range(1, total_time)):
        if wins_race(x, total_time, distance):
            time = x
            break

    return time


def get_num_ways_to_win(*args, **kwargs) -> int:
    return max_time_held(*args, **kwargs) - min_time_held(*args, **kwargs) + 1


def part1(time_input: list[str], distance_input: list[str]) -> None:
    time = [int(x.group()) for x in DIGIT.finditer(time_input)]
    distance = [int(x.group()) for x in DIGIT.finditer(distance_input)]

    num_ways_to_win_races = [
        get_num_ways_to_win(*race)
        for race in zip(time, distance)
    ]

    ways_to_win = math.prod(num_ways_to_win_races)

    print(f'Part 1: {ways_to_win}')


def part2(time_input: list[str], distance_input: list[str]) -> None:
    time = int(''.join([x.group() for x in DIGIT.finditer(time_input)]))
    distance = int(''.join([x.group() for x in DIGIT.finditer(distance_input)]))

    ways_to_win = get_num_ways_to_win(time, distance)

    print(f'Part 2: {ways_to_win}')


def main() -> None:
    with open('data/input.txt') as f:
        time_input, distance_input = [
            x.strip()
            for x
            in f.readlines()
        ]

    part1(time_input, distance_input)
    part2(time_input, distance_input)


if __name__ == "__main__":
    main()
