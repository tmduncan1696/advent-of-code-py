import functools

from utils import read_input_file


@functools.lru_cache(maxsize=None)
def calculate_combination(record: str, groups: tuple[int]) -> int:

    # BASE CASE LOGIC
    # Did we run out of groups?
    if not groups:
        # Make sure there are no more damaged springs
        if "#" not in record:
            return 1
        return 0

    # Did we run out of characters?
    if not record:
        return 0

    next_character = record[0]
    next_group = groups[0]

    # LOGIC FOR DOT
    def handle_dot() -> int:
        # Skip character
        return calculate_combination(record[1:], groups)

    # LOGIC FOR POUND
    def handle_pound() -> int:
        # If the first character is a #, then this must be a group
        this_group = record[:next_group]
        this_group = this_group.replace("?", "#")

        # Check that there are only damaged springs
        if this_group != next_group * "#":
            return 0

        # If the rest of the record is the last group, then abort
        if len(record) == next_group:
            if len(groups) == 1:
                return 1
            return 0

        # Make sure the next character can be a separator
        if record[next_group] in "?.":
            # Skip the separator and move on
            return calculate_combination(record[next_group+1:], groups[1:])

        return 0

    if next_character == ".":
        out = handle_dot()
    elif next_character == "#":
        out = handle_pound()
    elif next_character == "?":
        out = handle_dot() + handle_pound()
    else:
        raise RuntimeError

    return out


def main(input_file: str) -> None:
    input_data = read_input_file(input_file).split("\n")

    input_data = [
        line.split()
        for line in input_data
    ]

    input_data = [
        [record, tuple(int(g) for g in groups.split(","))]
        for record, groups in input_data
    ]

    part1 = sum(
        calculate_combination(*args)
        for args in input_data
    )

    print(f"Part 1: {part1}")

    input_data = [
        ["?".join(record for _ in range(5)), groups * 5]
        for record, groups in input_data
    ]

    part2 = sum(
        calculate_combination(*args)
        for args in input_data
    )

    print(f"Part 2: {part2}")
