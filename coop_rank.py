""" Rank coops script, download the bundle package as individual pdfs and put in a directory """

import argparse
import re
from dataclasses import dataclass
from io import StringIO
from pathlib import Path

from PyPDF4.pdf import PdfFileReader

# first group is student name, second group is student id
PDF_FILENAME_PATTERN = re.compile(r"([a-zA-Z ]*)-([a-zA-Z]+)-([0-9]+)-(.*)")


class LoadFromFile(argparse.Action):
    """load arguments from a file"""

    def __call__(self, parser, namespace, values, option_string=None):
        with values as file:
            # parse arguments in the file and store them in the target namespace
            parser.parse_args(file.read().split(), namespace)


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
class WeightedPattern:
    """ class to hold patterns with a weight associated with it """

    pattern: re.Pattern
    weight: int
    used: bool

    def __init__(self, values) -> None:
        self._pattern_string = values[0]
        self.pattern = re.compile(values[0])
        self.weight = values[1]

    def __str__(self) -> str:
        return f"{self._pattern_string}: {self.weight}"


class Resume:
    """ class to hold a resume """

    total_weight: int = 0
    first_name: str
    last_name: str
    student_number: int

    def __init__(self, pdf_filename: Path, patterns: list[WeightedPattern]) -> None:

        name_match = PDF_FILENAME_PATTERN.match(pdf_filename.name)
        if name_match is None:
            raise ValueError("Not a coop resume")

        self.first_name = name_match.group(1)
        self.last_name = name_match.group(2)
        self.student_number = int(name_match.group(3))

        with open(str(pdf_filename), "rb") as f:
            pdf = PdfFileReader(f)

            text = StringIO()
            for i in range(pdf.numPages):
                page = pdf.getPage(i)
                text.write(page.extractText())

            for p in patterns:
                p.used = False

            text.seek(0)
            for line in text.readlines():
                for p in patterns:
                    if p.used:  # don't double count key words
                        break
                    match = p.pattern.match(line)
                    if match:
                        self.total_weight += p.weight

        print(f"{self.last_name}, {self.first_name} ({self.student_number}): {self.total_weight}")


def main():
    """main"""
    parser = argparse.ArgumentParser(description="Coop rank utility")

    parser.add_argument("--directory", "-d", help="Directory to scan resumes", required=True, type=Path)
    parser.add_argument("--pattern", "-p", action="append", nargs="*", type=NargsTypeChecker((str, int)), dest="patterns")
    parser.add_argument("--file", type=open, action=LoadFromFile)

    args = parser.parse_args()

    print(f"Scanning {args.directory} for resumes")
    patterns = [WeightedPattern(x) for x in args.patterns]
    patterns_str = "\n".join([str(x) for x in patterns])
    print(f"Using the following patterns with weights:\n{patterns_str}")

    resumes = []
    for file in {x for x in args.directory.iterdir() if x.is_file()}:
        try:
            resumes.append(Resume(file, patterns))
        except ValueError:
            pass

    print(len(resumes))


if __name__ == "__main__":
    main()
