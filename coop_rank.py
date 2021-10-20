""" Rank coops script, download the bundle package as individual pdfs and put in a directory """

import argparse
import json
import shutil
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

    resumes: list[Resume] = []
    for file in {x for x in directory.iterdir() if x.is_file()}:
        try:
            resume = Resume(file, patterns)
            resumes.append(resume)
            print(".", end="", flush=True)
        except ValueError:
            pass

    print()
    resumes.sort(key=lambda x: x.total_weight, reverse=True)

    for resume in resumes:
        print(str(resume))

    take_number = int(len(resumes) * float(config["take_percent"]) / 100.0)
    take_resumes = resumes[0:take_number]

    take_directory = Path(config["take_directory"])
    take_directory.mkdir(parents=True, exist_ok=True)

    for resume in take_resumes:
        shutil.copy(str(resume.file_path), str(take_directory / resume.file_path.name))


if __name__ == "__main__":
    main()
