[![License](https://img.shields.io/github/license/theodumont/video-logging)](https://github.com/theodumont/video-logging/blob/master/LICENSE)
![Windows Support](https://img.shields.io/badge/Windows-Support-brightgreen.svg)

# Video logging for editing

Python script that can be used to quickly organize rushes from a video shooting session.

> :warning: Work in progress!

## Table of contents

1. [ Installation ](#1-installation)  
2. [ How to use ](#2-how-to-use)  

## 1. Installation

To use this tool, type in a terminal:
```bash
# clone the repo
git clone https://github.com/theodumont/video-logging.git
# go to folder
cd video-logging
# install dependencies
pip install -r requirements.txt
# launch tool
python cli.py
```
It will run the tool, waiting for your input.

## 2. How to use

With this tool, you can navigate trough directories using the `>> cd` command. For instance, if you're in the `C:\Users\Foo` directory, you can type
```bash
>> cd bar
```
and you will be in the `C:\Users\Foo\bar` directory. To go back in the directories structure, you can use `>> cd ..`. Navigate like this to the folder you would like to sort.

Once you are in the right folder, you can realize multiple operations, such as:

- sorting files by their extension, using:
```bash
>> folder
```
- trashing the videos of length shorter than a certain value, getting rid of the useless ones, using:
```bash
>> trash <time_limit>
```
where `time_limit` is a positive integer;
- sorting files by date, using:
```bash
>> date
```
The folders will be in the form of `YYMMDD-Day`.

If you are lost, you can always type `>> help`, or even `>> help <command>` for help on a specific command among the previously evoked ones.

## To do

- [x] Store help messages in separate file
    - Find right structure of dict
- [x] Find a cleaner way to get EXTENSIONS
- [ ] Add renaming option
- [ ] Issue when space in name of file
- [ ] Issue when more than two consecutive spaces in name of file
- [x] Add progress bar
- [x] Add warning when sorting folder where `video-logging` is
    - [x] Add possibility to choose sudo mode (don't check)
    - [ ] Use custom exception
- [x] Add color in terminal ?
- [ ] Notify when folder empty
