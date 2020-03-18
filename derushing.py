# encoding: utf-8
"""
Cleans a folder to simplify the derushing process.
"""

import os
import time
import argparse
from moviepy.video.io.VideoFileClip import VideoFileClip
from textwrap import fill


DIRS = ['Audio', 'Videos', 'Images', 'Documents', 'Folders', 'Other']
EXT_AUDIO = ['.wav', '.mp3', '.raw', '.wma']
EXT_VIDEO = ['.mp4', '.m4a', '.m4v', '.f4v', '.f4a', '.f4b', '.m4b', '.m4r', '.avi', '.wmv', '.flv', '.MOV']
EXT_IMAGE = ['.jpeg', '.jpg', '.png', '.svg', '.bmp', '.gif']
EXT_DOCUMENT = ['.txt', '.pdf', '.doc', '.docx', '.odt', '.html', '.md', '.rtf', '.xlsx', '.pptx']
EXT_FOLDER = ['.rar', '.zip']


os.chdir('foo')


def folder_sort(folder):
    """
    Sorts the files into directories according to their extension.
    Creates the directories if they don't exist.
    """
    # os.chdir(folder)
    bprint("Sorting files...\n")
    moved = "   -> moved"
    if not os.path.isdir('Audio'):
        for d in DIRS:
            os.mkdir('./{}'.format(d))

    bprint("  File type    File name\n", 3)
    bprint(" -------------------------", 3)
    for file in os.listdir():
        name, extension = os.path.splitext(file)

        if extension in EXT_AUDIO:
            bprint(" Audio          {0}{1}".format(file, moved), 3)
            os.rename(file, 'Audio/' + file)
        elif extension in EXT_VIDEO:
            bprint(" Video          {0}{1}".format(file, moved), 3)
            os.rename(file, 'Videos/' + file)
        elif extension in EXT_IMAGE:
            bprint(" Image          {0}{1}".format(file, moved), 3)
            os.rename(file, 'Images/' + file)
        elif extension in EXT_DOCUMENT:
            bprint(" Document       {0}{1}".format(file, moved), 3)
            os.rename(file, 'Documents/' + file)
        else:
            if os.path.isdir(name) or extension in EXT_FOLDER:
                if name not in DIRS:
                    bprint(" Folder         {0}{1}".format(file, moved), 3)
                    os.rename(file, 'Folders/' + file)
                else:
                    bprint(" Script         {}".format(file), 3)
            else:
                bprint(" Other          {0}{1}".format(file, moved), 3)
                os.rename(file, 'Other/' + file)
        time.sleep(.04)
    bprint("Files sorted by type!")


def trash_videos(folder, time_limit):
    """
    Trashes the videos that are shorter than .time_limit to get rid of
    all the shooting errors.
    """
    # os.chdir(folder)
    if not os.path.isdir('Audio'):
        folder_sort()
    bprint("Trashing files of duration <= {}s...\n".format(time_limit))
    bprint("  File name      Duration\n", 3)
    bprint(" -------------------------", 3)
    for file in os.listdir('./Videos'):
        if not os.path.isdir('Videos/' + file):
            clip = VideoFileClip('Videos/' + file)
            duration = clip.duration
            clip.close()
            time.sleep(.1)
            deleted = ""
            if duration < time_limit:
                if not os.path.isdir('Videos/Trash'):
                    os.mkdir('Videos/Trash')
                os.rename('Videos/' + file, 'Videos/Trash/' + file)
                deleted = "   -> moved to '/Trash'"
            bprint(" {0}     {1:.1f} s{2}".format(file, duration, deleted), 3)
    bprint("Files trashed!")


def sort_videos(folder):
    """
    Sorts videos in directories by date to simplifiy the derushing process.
    """
    # os.chdir(folder)
    bprint("Sorting videos by date...\n")
    if not os.path.isdir('Audio'):
        folder_sort(folder)
    sep = ' ' + 50*'-'
    bprint("File name".center(25) + "      Created on\n"+sep, 3)
    for file in os.listdir('./Videos'):
        if not os.path.isdir('Videos/' + file):
            path = 'Videos/' + file
            creation = time.localtime(os.path.getmtime(path))
            destination = time.strftime('%y%m%d-%a', creation)
            bprint((file.center(25) + '{0}   -> moved to {1}').format(
                  time.strftime('%c', creation),
                  destination), 3)
            if not os.path.isdir('Videos/' + destination):
                os.mkdir('Videos/' + destination)
            os.rename('Videos/' + file, 'Videos/' + destination + '/' + file)

            time.sleep(.04)
    bprint("Videos sorted by date!")


def bprint(msg, mode=0):
    # mode 0 means information, 1 means warning and 2 means error
    wrapped_msg_list = []
    for line in iter(msg.splitlines()):
        wrapped_msg_list.append(fill(line, width=80))
    wrapped_msg = "\n".join(wrapped_msg_list)
    if mode == 1:
        print(f"---! {wrapped_msg}")
        return
    elif mode == 2:
        print(f"---X {wrapped_msg}")
        return
    elif mode == 3:
        print(f"     {wrapped_msg}")
        return
    else:   # i.e. mode == 0
        print(f"---> {wrapped_msg}")
        return
