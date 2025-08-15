from typing import List

from game.game import Game


def power_set(x: List[int]) -> int:
    out = 1
    for val in x:
        out *= val

    return out


def main() -> None:

    BAG_DICT = {"red": 12, "green": 13, "blue": 14}

    with open("data/input.txt", "r") as f:
        game_strings = [x.strip() for x in f.readlines()]

    games = [Game.from_string(game_string) for game_string in game_strings]

    possible_game_ids = [game.id for game in games if game.is_possible(BAG_DICT)]

    print(f"Part 1: {sum(possible_game_ids)}")

    min_games = [game.min_possible_game() for game in games]

    power_sets = [power_set(min_game.values()) for min_game in min_games]

    print(f"Part 2: {sum(power_sets)}")


if __name__ == "__main__":
    main()
