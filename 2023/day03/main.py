import re
from typing import List, Tuple


def get_symbol_locs(x: List[str]) -> List[Tuple[int, int]]:
    SYMBOL_REGEX = re.compile(r"[^\dA-Za-z\.]")

    return [
        (row, m.start())
        for row, line in enumerate(x)
        for m in SYMBOL_REGEX.finditer(line)
    ]


def get_digits(x: List[str]) -> List[Tuple[int, Tuple[int, int], int]]:
    DIGIT_REGEX = re.compile(r"\d+")
    return [
        (row, m.span(), int(m.group()))
        for row, line in enumerate(x)
        for m in DIGIT_REGEX.finditer(line)
    ]


def get_engine_parts(
    symbol_locs: List[Tuple[int, int]], digits: List[Tuple[int, Tuple[int, int], int]]
) -> List[int]:
    return [
        num
        for row, span, num in digits
        for loc in symbol_locs
        if (abs(row - loc[0]) < 2)
        and ((abs(span[0] - loc[1]) < 2) or (abs((span[1] - 1) - loc[1]) < 2))
    ]


def get_gears(x: List[str]) -> List[Tuple[int, int]]:
    GEAR_REGEX = re.compile(r"\*")
    return [
        (row, m.start())
        for row, line in enumerate(x)
        for m in GEAR_REGEX.finditer(line)
    ]


def get_gear_ratios(
    gear_locs: List[Tuple[int, int]], digits: List[Tuple[int, Tuple[int, int], int]]
) -> List[int]:
    potential_gears = []
    for gear_row, gear_col in gear_locs:
        nums = []
        for num_row, num_span, num in digits:
            if abs(num_row - gear_row) > 1:
                continue
            if (
                abs(num_span[0] - gear_col) > 1
                and abs((num_span[1] - 1) - gear_col) > 1
            ):
                continue
            nums.append(num)
        potential_gears.append(nums)
    gears = [x for x in potential_gears if len(x) == 2]

    return [x * y for x, y in gears]


def main(input_file: str) -> None:
    with open(input_file, "r") as f:
        input = [x.strip() for x in f.readlines()]

    symbol_locs = get_symbol_locs(input)
    digits = get_digits(input)
    engine_parts = get_engine_parts(symbol_locs, digits)
    print(f"Part 1: {sum(engine_parts)}")

    gear_locs = get_gears(input)
    gear_ratios = get_gear_ratios(gear_locs, digits)

    print(f"Part 2: {sum(gear_ratios)}")


if __name__ == "__main__":
    main("data/input.txt")
