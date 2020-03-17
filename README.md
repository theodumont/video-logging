# Video Editing Derushing

Python script that can be used to quickly organize rushes from a video shooting session.

## Installation

To derush the `foo` folder, run in shell:
```bash
cd location_of_foo
pip install -r requirements
python derushing.py foo -sd
```
The parameters are:
```bash
usage: derushing.py [-h] [-f] [-t] [-d] folder_to_sort

positional arguments:
  folder_to_sort  folder to clean

optional arguments:
  -h, --help      show this help message and exit
  -f, --folder    organize the folder by file type
  -t, --trash     trash the very short videos
  -d, --date      sort videos in directories by date
```
