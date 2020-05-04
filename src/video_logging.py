# encoding: utf-8
"""
Cleans a folder to simplify the video logging process.
"""

import os
import time
import json
import subprocess
from moviepy.video.io.VideoFileClip import VideoFileClip


def folder_sort():
    """
    Sort the files into directories according to their extension.
    Create the directories if they don't exist.
    """

    print("Sorting files...")

    for file in os.listdir():
        time.sleep(.001)
        name, extension = os.path.splitext(file)
        if os.path.isdir(file):
            if name not in EXTENSIONS:
                move_to_dir(file, 'Folders')
            else:
                pass
        else:
            treated = False
            for directory in EXTENSIONS:
                if extension in EXTENSIONS[directory]:
                    move_to_dir(file, directory)
                    treated = True
                    break
            if not treated:
                move_to_dir(file, 'Other')

    print("Files sorted by type!")


def trash_videos(time_limit):
    """
    Trash the videos that are shorter than time_limit to get rid of
    all the shooting errors.
    """

    def move_to_trash(file, duration):
        """
        Move a video to Trash if it is too short.
        """
        if duration < time_limit:
            if not os.path.isdir('Trash'):
                os.mkdir('./Trash')
            os.rename(file, os.path.join('Trash', file))
        else:
            pass

    print(f"Trashing videos of duration <= {time_limit}s...")

    for file in os.listdir():
        extension = os.path.splitext(file)[1]
        if extension in EXTENSIONS['Videos']:
            with VideoFileClip(file) as clip:
                time.sleep(.001)
                duration = clip.duration
            move_to_trash(file, duration)

    print("Files trashed!")


def sort_by_date():
    """
    Sort files in directories by date.
    """

    print("Sorting files by date...")

    for file in os.listdir():
        if not os.path.isdir(file):
            time.sleep(.001)
            creation = time.localtime(os.path.getmtime(file))
            directory = time.strftime('%y%m%d-%a', creation)
            move_to_dir(file, directory)

    print("Videos sorted by date!")


def move_to_dir(file, directory):
    """
    Move file to directory
    """
    if not os.path.isdir(directory):
        os.mkdir('./{}'.format(directory))
    os.rename(file, os.path.join(directory, file))



if __name__ != '__main__':
    with open('src/data.json', 'r') as file:
        data = json.load(file)
    EXTENSIONS = data["EXTENSIONS"]
    PATH_TO_VLC = data["PATH_TO_VLC"]
