# encoding: utf-8
"""Functions used by the cli.py script.

Makes the process of cleaning a folder easier and simplifies the
video logging process.

"""

import os
import time
import json
import subprocess
from moviepy.video.io.VideoFileClip import VideoFileClip


def folder_sort(EXTENSIONS):
    r"""Sort the files into directories according to their extension.

    Create the extensions directories if they don't exist.
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


def trash_videos(time_limit, EXTENSIONS):
    r"""Trash the videos that are shorter than time_limit to get rid of
    the shooting errors.

    Parameters
    ----------
    time_limit : int
        Duration limit.
    """
    def move_to_trash(file, duration):
        r"""Move a video to trash if it is too short.

        Check if a directory named `Trash` exists in current directory. If not,
        create it. Then, move `file` in `Trash` if `duration` is smaller than
        `time_limit`.

        Parameters
        ----------
        file : string
            File to check.
        duration : int
            Duration of video file.
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
    r"""Sort files in directories by creation date.

    The repositories will be in the form of 'YYMMDD-Day'.
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
    r"""Move file to directory.

    Check if a directory named `directory` exists in current directory. If not,
    create it. Then, move `file` in `directory`.

    Parameters
    ----------
    file : string
        File to move.
    directory : string
        Target directory.
    """
    if not os.path.isdir(directory):
        os.mkdir('./{}'.format(directory))
    os.rename(file, os.path.join(directory, file))
