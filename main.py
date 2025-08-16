import importlib
import os


def main(year, day, example):
    INPUT_FOLDER = f"{args.year}/day{args.day}"
    MODULE_FILE = os.path.join(INPUT_FOLDER, "main")
    MODULE_FILE = MODULE_FILE.replace("/", ".")
    INPUT_FILE = os.path.join(
        INPUT_FOLDER, f'data/{"example_" if args.example else ""}input.txt'
    )

    module = importlib.import_module(MODULE_FILE)

    module.main(INPUT_FILE)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("year", type=str)
    parser.add_argument("day", type=str)
    parser.add_argument("-e", "--example", action="store_true")

    args = parser.parse_args()
    main(**vars(args))
