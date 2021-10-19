""" read a pdf file, useful for trying to debug rank script """
import argparse
import json
from pathlib import Path

from ranking.resume import Resume
from ranking.weighted_pattern import WeightedPattern

parser = argparse.ArgumentParser(description="PDF reader")
parser.add_argument("--pdf", "-p", help="pdf file to read", required=True, action="append", dest="pdfs")
parser.add_argument("--full-debug", "-f", help="full debug mode", action="store_true", dest="full_debug")

args = parser.parse_args()

with open("config.json", "rt", encoding="UTF-8") as f:
    config = json.loads(f.read())

patterns = [WeightedPattern.from_json(x) for x in config["patterns"]]

for pdf in args.pdfs:
    resume = Resume(Path(pdf), patterns, full_debug=args.full_debug)
    print(str(resume))
