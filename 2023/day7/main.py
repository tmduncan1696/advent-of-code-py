#!/usr/bin/env python3

from collections import Counter
from dataclasses import dataclass
from typing import Any, Self

def element_exists(lst: list, element: Any) -> bool:
    try:
        lst.index(element)
        return True
    except ValueError:
        return False

class Card:
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

    def __init__(self, rank: str):
        self.rank = rank
        self.value = self.RANKS.index(rank)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Card):
            return False

        return self.rank == other.rank

    def __lt__(self, other) -> bool:
        if not isinstance(other, Card):
            raise TypeError(f"'< is not supported between instances of 'Card' and '{type(other)}'")

        return self.value < other.value

    def __gt__(self, other) -> bool:
        if not isinstance(other, Card):
            raise TypeError(f"'> is not supported between instances of 'Card' and '{type(other)}'")

        return self.value < other.value

    def __le__(self, other) -> bool:
        if not isinstance(other, Card):
            raise TypeError(f"'<= is not supported between instances of 'Card' and '{type(other)}'")

        return self.value < other.value

    def __ge__(self, other) -> bool:
        if not isinstance(other, Card):
            raise TypeError(f"'>= is not supported between instances of 'Card' and '{type(other)}'")

        return self.value < other.value

    def __repr__(self) -> None:
        return f'Card(rank=\'{self.rank}\')'

    def __hash__(self) -> int:
        return hash(self.rank)

class Hand:
    RANKS = ['High Card', 'One Pair', 'Two Pair', 'Three of a Kind', 'Full House', 'Four of a Kind', 'Five of a Kind']
    cards: tuple[Card]

    def __init__(self, cards: tuple[Card]):
        self.cards = cards
        self.count = Counter(self.cards)
        self.count_of_counts = Counter(self.count.values())
        if self.is_five_of_a_kind():
            self.rank = 'Five of a Kind'
        elif self.is_four_of_a_kind():
            self.rank = 'Four of a Kind'
        elif self.is_full_house():
            self.rank = 'Full House'
        elif self.is_three_of_a_kind():
            self.rank = 'Three of a Kind'
        elif self.is_two_pair():
            self.rank = 'Two Pair'
        elif self.is_one_pair():
            self.rank = 'One Pair'
        elif self.is_high_card():
            self.rank = 'High Card'
        else:
            raise ValueError('Cannot determine hand rank')

        self.rank_value = self.RANKS.index(self.rank)

    def __repr__(self) -> str:
        return f'Hand({self.cards})'

    def __eq__(self, other) -> bool:
        if not isinstance(other, Hand):
            return False

        return self.cards == other.cards

    def __lt__(self, other) -> bool:
        if not isinstance(other, Hand):
            raise TypeError(f"'< is not supported between instances of 'Hand' and '{type(other)}'")

        if self == other:
            return False

        if self.rank_value == other.rank_value:
            for c1, c2 in zip(self.cards, other.cards):
                if c1 != c2:
                    return c1 < c2

        return self.rank_value < other.rank_value

    def __gt__(self, other) -> bool:
        if not isinstance(other, Hand):
            raise TypeError(f"'> is not supported between instances of 'Hand' and '{type(other)}'")

        if self == other:
            return False

        if self.rank_value == other.rank_value:
            for c1, c2 in zip(self.cards, other.cards):
                if c1 != c2:
                    return c1 > c2

        return self.rank_value > other.rank_value



    @classmethod
    def from_string(cls, s: str) -> Self:
        cards = (
            Card(card)
            for card in list(s)
        )
        return cls(tuple(cards))

    def is_five_of_a_kind(self) -> bool:
        return self.count_of_counts[5] == 1

    def is_four_of_a_kind(self) -> bool:
        return self.count_of_counts[4] == 1

    def is_full_house(self) -> bool:
        return self.count_of_counts[3] == 1 and self.count_of_counts[2] == 1

    def is_three_of_a_kind(self) -> bool:
        return self.count_of_counts[3] == 1 and self.count_of_counts[2] == 0

    def is_two_pair(self) -> bool:
        return self.count_of_counts[2] == 2

    def is_one_pair(self) -> bool:
        return self.count_of_counts[2] == 1 and self.count_of_counts[1] == 3

    def is_high_card(self) -> bool:
        return self.count_of_counts[1] == 5


def part1(input: list[str]) -> None:
    hand_input = [x.split() for x in input]
    hand_bets = [
        (Hand.from_string(hand), int(bet))
        for hand, bet in hand_input
    ]

    sorted_hand_bets = sorted(hand_bets)

    sorted_bets = [bet for _, bet in sorted_hand_bets]

    total_winnings = sum([(i + 1) * bet for i, bet in enumerate(sorted_bets)])

    print(f'Part 1: {total_winnings}')

def main() -> None:
    with open('data/input.txt') as f:
        input = [line.strip() for line in f.readlines()]

    part1(input)



if __name__ == '__main__':
    main()
