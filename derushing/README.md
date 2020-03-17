## Video Editing Derushing

To derush the `foo` folder, run in shell:
```bash
cd location_of_foo
pip install -r requirements
python derushing.py foo -sd
```
The parameters are:
```bash
usage: derushing.py [-h] [-s] [-d] folder_to_sort

positional arguments:
  folder_to_sort  folder to clean

optional arguments:
  -h, --help      show this help message and exit
  -s, --sort      organizes the folder
  -d, --delete    puts the videos of duration inferior to 2 seconds in a `Trash` folder
```
