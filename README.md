# Video Editing Derushing

Python script that can be used to quickly organize rushes from a video shooting session.

## Installation

To derush the `foo` folder, run in shell:
```bash
cd location_of_foo
pip install -r requirements
python cli.py -f foo
```
The arguments are:
```bash
usage: cli.py [-h] [-f FOLDER]

Command line frontend used to derush before video editing.

optional arguments:
  -h, --help            show this help message and exit
  -f FOLDER, --folder FOLDER
                        folder to sort

This tool was designed by Théo Dumont and all the source code is available at
https://github.com/theodumont/derushing-python under the GPL 3 License.
```
