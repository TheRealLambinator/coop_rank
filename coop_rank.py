""" Rank coops script, download the bundle package as individual pdfs and put in a directory """

import argparse
import json
from pathlib import Path

from ranking.resume import Resume
from ranking.weighted_pattern import WeightedPattern


def main():
    """main"""
    parser = argparse.ArgumentParser(description="Coop rank utility")

    parser.add_argument("--config", "-c", help="supply arguments via a json config file", required=True)

    args = parser.parse_args()

    with open(args.config, "rt", encoding="UTF-8") as f:
        config = json.loads(f.read())

    directory = Path(config["directory"])
    print(f"Scanning {str(directory)} for resumes")

    patterns = [WeightedPattern.from_json(x) for x in config["patterns"]]
    patterns_str = "\n".join([str(x) for x in patterns])
    print(f"Using the following patterns with weights:\n{patterns_str}")

    resumes = []
    for file in {x for x in directory.iterdir() if x.is_file()}:
        try:
            resume = Resume(file, patterns)
            print(str(resume))
            resumes.append(resume)
        except ValueError:
            pass


if __name__ == "__main__":
    main()
