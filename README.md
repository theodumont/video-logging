[![License](https://img.shields.io/github/license/theodumont/video-logging)](https://github.com/theodumont/video-logging/blob/master/LICENSE)
![Windows Support](https://img.shields.io/badge/Windows-Support-brightgreen.svg)

# Video logging for editing

Python script that can be used to quickly organize rushes from a video shooting session.

> :warning: Work in progress!

## Table of contents

1. [ Installation ](#1-installation)  
2. [ Features ](#2-features)  
    2.1. [ Sort by extension ](#21-sort-by-extension)  
    2.2. [ Trash useless videos ](#22-trash-useless-videos)  
    2.3. [ Sort by date ](#23-sort-by-date)  

## To do

- [ ] Store help messages in separate file
    - Find right structure of dict
- [ ] Find a cleaner way to get EXTENSIONS
- [ ] Add renamning option
- [x] Issue when space in name of file
- [ ] Issue when more than two consecutive spaces in name of file

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

### 2.1. Sort by extension
To sort files by extension, type:
```bash
>> folder
```

### 2.2. Trash useless videos
To trash the videos of length shorter than `time_limit`, type:
```bash
>> trash <time_limit>
```

### 2.3. Sort by date
To sort files by date, type:
```bash
>> date
```
