""" Resume class """

import re
from io import StringIO
from pathlib import Path

from PyPDF4.pdf import PdfFileReader

from .weighted_pattern import WeightedPattern

# first 2 groups are student name, third group is student id
PDF_FILENAME_PATTERN = re.compile(r"([a-zA-Z ]*)-([a-zA-Z]+)-([0-9]+)-(.*)")


class Resume:
    """class to hold a resume"""

    total_weight: int = 0
    first_name: str
    last_name: str
    student_number: int

    def __init__(self, pdf_filename: Path, patterns: list[WeightedPattern], full_debug: bool = False) -> None:

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

            used_patterns = set()

            text.seek(0)
            for line in text.readlines():
                if full_debug:
                    print(line.encode("utf-8"))
                for p in patterns:
                    if p.pattern_string in used_patterns:  # don't double count key words
                        break
                    search = p.pattern.search(line)
                    if full_debug:
                        print(f"{str(p)} : {str(search)}")
                    if search:
                        self.total_weight += p.weight
                        if not p.count_all:
                            used_patterns.add(p.pattern_string)

    def __str__(self):
        return f"{self.last_name}, {self.first_name} ({self.student_number}): {self.total_weight}"