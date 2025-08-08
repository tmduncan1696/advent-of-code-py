"""
Utils module
"""


def read_input_file(input_file: str):
    """
    Read input file
    """
    with open(input_file, encoding='utf-8') as f:
        input_data = f.read().strip()

    return input_data
