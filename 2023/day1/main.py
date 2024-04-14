import re
from typing import List

DIGIT_DICT = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}

def get_numbers(x: str) -> List[str]:
    pattern = re.compile(r'(?=(\d|one|two|three|four|five|six|seven|eight|nine))')
    matches = [match.group(1) for match in pattern.finditer(x)]
    return [
        DIGIT_DICT.get(num) or num
        for num in matches
    ]


def main() -> None:

    with open('data/input.txt', 'r') as f:
        input = [x.strip() for x in f.readlines()]

    numbers = [
        get_numbers(x)
        for x in input
    ]

    calibration_values = [
        int(x[0] + x[-1])
        for x in numbers
    ]

    print(sum(calibration_values))


if __name__ == '__main__':
    main()
