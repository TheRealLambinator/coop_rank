""" Rank coops script, download the bundle package as individual pdfs and put in a directory """

import argparse
from dataclasses import dataclass


class NargsTypeChecker:
    """allows specifying multiple types to an argument"""

    def __init__(self, types):
        self.types = types
        self.index = 0

    def __repr__(self):
        return self.types[self.index].__name__

    def __call__(self, arg):
        value = self.types[self.index](arg)
        self.index = (self.index + 1) % len(self.types)
        return value


@dataclass
class WeightedKeyWord:
    keyword: str
    weight: int

    def __init__(self, values) -> None:
        self.keyword = values[0]
        self.weight = values[1]

    def __str__(self) -> str:
        return f"{self.keyword}: {self.weight}"


def main():
    """main"""
    parser = argparse.ArgumentParser(description="Coop rank utility")

    parser.add_argument("--directory", "-d", help="Directory to scan resumes", required=True)
    parser.add_argument("--keywords", "-k", action="append", nargs="*", type=NargsTypeChecker((str, int)))

    args = parser.parse_args()

    print(f"Scanning {args.directory} for resumes")
    keywords = [WeightedKeyWord(x) for x in args.keywords]
    keywords_str = "\n".join([str(x) for x in keywords])
    print(f"Using the following keyword with weights:\n{keywords_str}")


if __name__ == "__main__":
    main()
