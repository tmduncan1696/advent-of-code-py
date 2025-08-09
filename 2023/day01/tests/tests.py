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

def tests() -> None:
    assert get_numbers('one') == ['1']
    assert get_numbers('two') == ['2']
    assert get_numbers('three') == ['3']
    assert get_numbers('four') == ['4']
    assert get_numbers('five') == ['5']
    assert get_numbers('six') == ['6']
    assert get_numbers('seven') == ['7']
    assert get_numbers('eight') ==['8']
    assert get_numbers('nine') == ['9']
    assert get_numbers('twone') == ['2', '1']
    assert get_numbers('eightwo') == ['8', '2']
    assert get_numbers('nineight') == ['9', '8']
    assert get_numbers('eighthree') == ['8', '3']
    assert get_numbers('nineeight') == ['9', '8']
    assert get_numbers('eeeight') == ['8']
    assert get_numbers('oooneeone') == ['1', '1']


if __name__ == '__main__':
    tests()
