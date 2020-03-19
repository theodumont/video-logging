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

EXTENSIONS = {
    'Audio': ['.wav', '.mp3', '.raw', '.wma'],
    'Videos': ['.mp4', '.m4a', '.m4v', '.f4v', '.f4a', '.f4b', '.m4b', '.m4r', '.avi', '.wmv', '.flv', '.MOV'],
    'Images': ['.jpeg', '.jpg', '.png', '.svg', '.bmp', '.gif'],
    'Documents': ['.txt', '.pdf', '.doc', '.docx', '.odt', '.html', '.md', '.rtf', '.xlsx', '.pptx'],
    'Folders': ['', '.rar', '.zip'],
    'Other': []
}


def move_to_subdir(file, subdir, to_move):
    if not os.path.isdir(subdir):
        os.mkdir('./{}'.format(subdir))
    if to_move:
        os.rename(file, f'{subdir}/{file}')
        bprint(" {1}          {0}{2}".format(file, subdir, "    (moved)"), 3)


def folder_sort(folder):
    """
    Sorts the files into directories according to their extension.
    Creates the directories if they don't exist.
    """
    print("")
    bprint("Sorting files...\n")

    bprint("  File type    File name\n", 3)
    bprint(" -------------------------", 3)
    for file in os.listdir():
        time.sleep(.001)
        name, extension = os.path.splitext(file)
        treated = False
        for d in DIRS:
            if extension in EXTENSIONS[d]:
                if not d == 'Folders':
                    move_to_subdir(file, d, True)
                else:  # is a folder
                    if name not in DIRS:
                        move_to_subdir(file, d, True)
                    else:
                        move_to_subdir(file, d, False)
                treated = True
                break  # on ne regarde pas les autres dirs
        if not treated:
            move_to_subdir(file, d, True)

    print("")
    bprint("Files sorted by type!")


def trash_videos(folder, time_limit):
    """
    Trashes the videos that are shorter than .time_limit to get rid of
    all the shooting errors.
    """
    if not os.path.isdir('Audio'):
        folder_sort(folder)
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
                    # os.mkdir('Videos/Trash')
                    pass
                # os.rename('Videos/' + file, 'Videos/Trash/' + file)
                deleted = "   -> moved to '/Trash'"
            bprint(" {0}     {1:.1f} s{2}".format(file, duration, deleted), 3)
    bprint("Files trashed!")


def sort_videos(folder):
    """
    Sorts videos in directories by date to simplifiy the derushing process.
    """
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
                # os.mkdir('Videos/' + destination)
                pass
            # os.rename('Videos/' + file, 'Videos/' + destination + '/' + file)

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
    elif mode == 4:
        print(f"(derush) {wrapped_msg}")
        return
    else:   # i.e. mode == 0
        print(f"---> {wrapped_msg}")
        return
