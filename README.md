These instructions are primarily for Windows, for Linux/Mac you'll need to modify accordingly (i.e. instead of python it will be python3)
Create virtual environment

```
python -m venv .venv

# if you  don't have python, it might be "py" on Windows
py -m venv .venv
```

Activate the environment

```
./.venv/Scripts/Activate.ps1
```

Install requirements

```
pip install -r requirements.txt
```

Update the config.json to point to a folder where all the resumes of interest are.  Also set the output directory to where you want
the "taken" resumes to be copied to.

Run the script

```
python ./coop_rank.py -c .\config.json
```

The output will show all the resumes and their ranking, then will display a line "----Taken----" and list all of the resumes that were
taken as the highest ranked by the script.

That's usually where I copy paste the "taken" ones from the console into an excel spreadsheet (google sheets) and separate columns by spaces
to start you off on having an easy way to track the resumes you want to read.


* TODO *
1. More analysis on the resume formats and split parsing by sections (i.e. previous workterm page parse separately from written resume parts)
2. Come up with a course list to highlight certain courses taken and pick up the grades to help with ranking
