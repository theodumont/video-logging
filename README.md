[![License](https://img.shields.io/github/license/theodumont/video-logging)](https://github.com/theodumont/video-logging/blob/master/LICENSE)
![Windows Support](https://img.shields.io/badge/Windows-Support-brightgreen.svg)
<!-- ![Linux Support](https://img.shields.io/badge/Linux-Support-brightgreen.svg) -->

# Video logging for editing

Python script that can be used to quickly organize rushes from a video shooting session, by:

- sorting files (type, date)
- renaming files
- removing very short videos

> :pushpin: The tool is not perfect but don't worry, it doesn't break anything :smile:

## Table of contents

1. [ Installation ](#1-installation)
2. [ How to use ](#2-how-to-use)
3. [ Customize ](#3-customize)
4. [ Example ](#4-example)

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

With this tool, you can navigate trough directories using the `>> cd` command. For instance, if you're in the `C:/Users/Foo` directory, you can type
```bash
>> cd bar
```
and you will be in the `C:/Users/Foo/bar` directory. To go back in the directories structure, you can use `>> cd ..`. Navigate like this to the folder you would like to sort.

Once you are in the right folder, you can realize multiple operations, such as:

- sorting files by their extension, using:
 ```bash
 >> folder
 ```
- trashing the videos of length shorter than a certain value, getting rid of the useless ones, using:
 ```bash
 >> trash $TIME_LIMIT
 ```
 where `$TIME_LIMIT` is a positive integer;
- sorting files by date, using:
 ```bash
 >> date
 ```
 The folders will be in the form of `YYMMDD-Day`.
- renaming files one by one, using:
 ```bash
 >> rename [$TYPE]
 ```
 where `$TYPE` is a type of files, such as `Videos`, `Documents`, `Audio`...

If you are lost, you can always type `>> help`, or even `>> help <command>` for help on a specific command among the previously evoked ones.

## 3. Customize

You can customize a number of elements of the tool:

- if the tool runs in `sudo` mode by default;
- the default folder where to boot the tool;
- the name of the folder for trashing files (`'Trash'`);
- the names of the folders for sorting files (`'Documents'`, `'Audio'`, `'Videos'`...), and which extension corresponds to which folder;
- whether or not opening files while renaming them.

In order to change some stuff, just go to `video-logging/data.json` and change the values of the variables.

## 4. Example

When I have to sort my files after a video shooting, I tend to execute these commands:

```bash
>>> f    # 'folder' command, sort files
>>> cd Videos
>>> t 3  # 'trash' command, remove videos shorter than 3 seconds
>>> d    # 'date' command, sort files by date
>>> cd $ANY_VIDEO_FOLDER
# with `open_while_renaming` set to True
>>> r    # renaming videos, moving them to trash if needed
```
