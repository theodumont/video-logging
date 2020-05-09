[![License](https://img.shields.io/github/license/theodumont/video-logging)](https://github.com/theodumont/video-logging/blob/master/LICENSE)
![Windows Support](https://img.shields.io/badge/Windows-Support-brightgreen.svg)

# Video logging for editing

Python script that can be used to quickly organize rushes from a video shooting session.

> :warning: Work in progress!

## Table of contents

1. [ Installation ](#1-installation)  
2. [ Features ](#2-features)  

## To do

- [x] Store help messages in separate file
    - Find right structure of dict
- [x] Find a cleaner way to get EXTENSIONS
- [ ] Add renaming option
- [x] Issue when space in name of file
- [ ] Issue when more than two consecutive spaces in name of file
- [x] Add progress bar
- [x] Add warning when sorting folder where `video-logging` is
- [ ] Add color in terminal ?

## 1. Installation

To use this tool, type in a shell:
```bash
>> cd location_of_cli
>> pip install -r requirements
>> python cli.py
```

Don't hesitate to use the `help` command to understand the different functions of the tool.

## 2. Features

To naviguate trough directories, you can use the `>> cd` command.

To sort files by extension, type:
```bash
>> folder
```

To trash the videos of length shorter than `time_limit`, type:
```bash
>> trash <time_limit>
```

To sort files by date, type:
```bash
>> date
```
