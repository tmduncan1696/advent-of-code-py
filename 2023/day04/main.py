import itertools
import re
from typing import Dict, List


def get_num_matches(x: str) -> Dict[int, int]:
    CARD_REGEX = re.compile(r"Card\s+(\d+):(.*)\|(.*)")

    match = CARD_REGEX.search(x)

    if not match:
        return {0: 0}

    card_number = int(match.group(1))

    winning_numbers = [int(n) for n in re.findall(r"\d+", match.group(2))]

    my_numbers = [int(n) for n in re.findall(r"\d+", match.group(3))]

    matching_numbers = sum([w in my_numbers for w in winning_numbers])

    return {card_number: matching_numbers}


def exponential(n: int, a: int) -> int:
    if n < 1:
        return 0
    return a ** (n - 1)


def gain_new_cards(card_num: int, num_matches: int) -> List[int]:
    return list(range(card_num + 1, card_num + num_matches + 1))


def flatten_list(x: List[list]) -> list:
    return list(itertools.chain.from_iterable(x))


def main() -> None:
    with open("data/input.txt", "r") as f:
        input = [x.strip() for x in f.readlines()]

    num_matches = [get_num_matches(x) for x in input]
    num_matches_list = [v for m in num_matches for v in m.values()]
    score = sum([exponential(x, 2) for x in num_matches_list])
    print(f"Part 1: {score}")

    match_dict = {k: v for d in num_matches for k, v in d.items()}
    cards = []
    new_cards = list(match_dict.keys())
    cards.extend(new_cards)

    while new_cards:
        new_cards = flatten_list(
            [
                gain_new_cards(card_num, match_dict.get(card_num) or 0)
                for card_num in new_cards
            ]
        )

        cards.extend(new_cards)

    num_cards = len(cards)

    print(f"Part 2: {num_cards}")


if __name__ == "__main__":
    main()
