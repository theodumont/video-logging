# Video logging for editing

Python script that can be used to quickly organize rushes from a video shooting session.

> :warning: Work in progress!

## Table of contents

1. [ Installation ](#1-installation)  
2. [ Features ](#2-features)  
    2.1. [ Sort by extension ](#21-sort-by-extension)  
    2.2. [ Trash useless videos ](#22-trash-useless-videos)  
    2.3. [ Sort by date ](#23-sort-by-date)  
    2.4. [ Rename files ](#24-rename-files)  
3. [ Tests ](#3-tests)

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

### 2.4. Rename files
To rename the files of type `file_type`, type:
```bash
>> rename <file_type>
```
where `file_type` can take the values `videos`.


## 3. Tests
I implemented the tests with the Python module `pytest` that can be installed through `pip`. To run the tests, run:
```bash
>> cd video-logging
>> py.test
>> py.test -s  # verbose
```
