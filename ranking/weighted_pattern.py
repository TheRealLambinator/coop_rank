""" Weighted Pattern class """

import json
import re
from dataclasses import dataclass


@dataclass
class WeightedPattern:
    """class to hold patterns with a weight associated with it"""

    pattern_string: str
    pattern: re.Pattern
    weight: int
    count_all: bool

    def __init__(self, pattern, weight, count_all) -> None:
        self.pattern_string = pattern
        self.pattern = re.compile(pattern)
        self.weight = int(weight)
        self.count_all = count_all

    def __str__(self) -> str:
        return f"{self.pattern_string}: {self.weight}"

    @staticmethod
    def from_json(json_blob: json):
        return WeightedPattern(json_blob["pattern"], json_blob["weight"], json_blob["count_all"])
