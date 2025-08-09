import re
from typing import Dict

with open('2023/day4/data/example_input.txt', 'r') as f:
    input = [x.strip() for x in f.readlines()]


def get_num_matches(x: str) -> Dict[int, int]:
    CARD_REGEX = re.compile(r'Card\s+(\d+):(.*)\|(.*)')

    match = CARD_REGEX.search(x)

    if not match:
        return {0: 0}

    card_number = int(match.group(1))

    winning_numbers = [int(n) for n in re.findall(r'\d+', match.group(2))]

    my_numbers = [int(n) for n in re.findall(r'\d+', match.group(3))]

    matching_numbers = sum(
        [
            w in my_numbers
            for w in winning_numbers
        ]
    )

    return {card_number: matching_numbers}


def test() -> None:
    num_matches = [get_num_matches(x) for x in input]
    num_matches_list = [
        v
        for m in num_matches
        for v in m.values()
    ]
    assert num_matches_list == [4, 2, 2, 1, 0, 0]
