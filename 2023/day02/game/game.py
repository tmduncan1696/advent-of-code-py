import re
from typing import Dict, List, Self


class Pull:
    pull: Dict[str, int]

    def __init__(self, pull: Dict[str, int]) -> None:
        self.pull = pull

    @classmethod
    def from_string(cls, string: str) -> Self:
        pull_regex = re.compile(r"(\d+)\s([A-Za-z]+)")

        pull = {color: int(num) for num, color in pull_regex.findall(string)}

        obj = cls(pull)

        return obj

    def is_possible(self, bag_dict=Dict[str, int]) -> bool:
        is_color_possible = {
            color: (self.pull.get(color) <= bag_dict.get(color))
            for color in self.pull.keys()
        }

        return all(is_color_possible.values())


class Game:
    id: int
    pulls: List[Pull]

    def __init__(self, id: int, pulls: List[Pull]) -> None:
        self.id = id
        self.pulls = pulls

    @classmethod
    def from_string(cls, string: str) -> Self:
        regex = re.compile(r"Game\s(\d+):\s(.*)")

        match = regex.match(string)

        id = int(match.group(1))
        pull_string = match.group(2)

        pull_strings = [x.strip() for x in pull_string.split(";")]

        pulls = [Pull.from_string(pull_string) for pull_string in pull_strings]

        obj = cls(id, pulls)

        return obj

    def is_possible(self, bag_dict: Dict[str, int]) -> bool:
        if self.pulls is None:
            return bag_dict is None

        is_pull_possible = [pull.is_possible(bag_dict) for pull in self.pulls]

        return all(is_pull_possible)

    def min_possible_game(self) -> Dict[str, int]:
        out = {}

        if not self.pulls:
            return out

        for pull in self.pulls:
            for color, num in pull.pull.items():
                out[color] = max(out.get(color) or 0, num)

        return out
