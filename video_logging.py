# encoding: utf-8
"""
Cleans a folder to simplify the video logging process.
"""

import os
import time
from moviepy.video.io.VideoFileClip import VideoFileClip
import subprocess
from textwrap import fill


EXTENSIONS = {
    'Audio': ['.wav', '.mp3', '.raw', '.wma', '.aif', '.cda', '.mid', '.midi', '.mpa', '.ogg', '.wpl'],
    'Videos': ['.mp4', '.m4a', '.m4v', '.f4v', '.f4a', '.f4b', '.m4b', '.m4r', '.avi', '.wmv', '.flv', '.MOV'],
    'Images': ['.ai', '.bmp', '.gif', '.ico', '.jpeg', '.jpg', '.png', '.ps', '.svg', '.tif', '.tiff'],
    'Documents': ['.txt', '.pdf', '.doc', '.docx', '.odt', '.html', '.md', '.rtf', '.xlsx', '.pptx', '.tex', '.key', '.odp', '.pps', '.ppt', '.pptx', '.ods'],
    'Folders': ['', '.rar', '.zip', '7z', '.pkg', '.z', '.tar.gz'],
    'Python': ['.py', '.pyc'],
    'Internet': ['.css', '.htm', '.html', '.js', '.php', '.xhtml'],
    'Data': ['.csv', '.dat', '.db', '.dbf', '.log', '.mdb', '.sav', '.sql', '.tar', '.xml'],
    'Fonts': ['.fnt', '.fon', '.otf', '.ttf'],
    'Other': []
}

PATH_TO_VLC = "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe"
# PATH_TO_VLC = os.path.join("C:", "Program Files", "VideoLAN", "VLC", "vlc.exe")


def folder_sort(folder):
    """
    Sorts the files into directories according to their extension.
    Creates the directories if they don't exist.
    """

    def move_to_subdir(file, subdir, to_move):
        """
        Moves file to subdir if necessary.
        """
        if not os.path.isdir(subdir):
            os.mkdir('./{}'.format(subdir))
        if to_move:
            os.rename(file, os.path.join(subdir, file))
            cprint(subdir, file, "(moved)")
        else:
            cprint('Script', file)

    print("")
    bprint("Sorting files...\n")

    cprint("File type", "File name")
    bprint(" " + 27 * "-", 3)
    for file in os.listdir():
        time.sleep(.001)
        name, extension = os.path.splitext(file)
        treated = False
        for d in EXTENSIONS:
            if extension in EXTENSIONS[d]:
                if not d == 'Folders':
                    move_to_subdir(file, d, True)
                else:  # is a folder
                    if not os.path.isdir(file):  # is a file without extension
                        move_to_subdir(file, 'Documents', True)
                    elif name not in EXTENSIONS:
                        move_to_subdir(file, d, True)
                    else:
                        move_to_subdir(file, d, False)
                treated = True
                break  # don't look at the remaining dirs
        if not treated:
            move_to_subdir(file, d, True)

    print("")
    bprint("Files sorted by type!")


def trash_videos(folder, time_limit):
    """
    Trashes the videos that are shorter than time_limit to get rid of
    all the shooting errors.
    """

    def move_to_trash(file, duration):
        """
        Moves a video to Trash if it is too short.
        """
        if duration < time_limit:
            if not os.path.isdir('Trash'):
                os.mkdir('./Trash')
            os.rename(file, os.path.join('Trash', file))
            cprint(file, duration, "(trashed)", is_long=True)
        else:
            cprint(file, duration, is_long=True)

    print("")
    bprint("Trashing videos of duration <= {}s...\n".format(time_limit))

    cprint("File name", "Duration", is_long=True)
    bprint(" " + 32 * "-", 3)
    for file in os.listdir():
        name, extension = os.path.splitext(file)
        if extension in EXTENSIONS['Videos']:
            with VideoFileClip(file) as clip:
                time.sleep(.001)
                duration = clip.duration
            to_trash = ""
            move_to_trash(file, duration)

    print("")
    bprint("Files trashed!")


def sort_by_date(folder):
    """
    Sorts files in directories by date.
    """

    print("")
    bprint("Sorting files by date...\n")

    cprint("File name", "Created on", is_long=True)
    bprint(" " + 50 * "-", 3)
    for file in os.listdir():
        if not os.path.isdir(file):
            time.sleep(.001)
            creation = time.localtime(os.path.getmtime(file))
            destination = time.strftime('%y%m%d-%a', creation)
            if not os.path.isdir(destination):
                os.mkdir(destination)
            os.rename(file, os.path.join(destination, file))
            cprint(file, time.strftime('%c', creation), "-> moved to " + destination, True)

    bprint("Videos sorted by date!")


def file_rename(folder, directory, exit_list):
    """
    Rename the files.
    """

    def open_and_rename(file, extension, directory):
        """
        Open and rename a file.
        """
        cprint(directory, file)
        # open video
        subprocess.Popen([PATH_TO_VLC, file], stdout=subprocess.PIPE)
        # rename video
        new_name = input('    >> new name: ')
        if new_name != "":
            os.rename(file, new_name + extension)

    print("")
    bprint("Renaming the {}...\n".format(directory.lower()))

    cprint("File type", "Original name")
    bprint(" " + 34 * "-", 3)
    for file in os.listdir():
        name, extension = os.path.splitext(file)
        if not os.path.isdir(file) and extension in EXTENSIONS[directory]:
            time.sleep(.001)
            cprint(directory, file)
            # open video
            subprocess.Popen([PATH_TO_VLC, file], stdout=subprocess.PIPE)
            # rename video
            try:
                new_name = input('       >> new name: ')
                if new_name in exit_list:
                    break
                elif new_name != "":
                    os.rename(file, new_name + extension)
            except (EOFError, KeyboardInterrupt):
                print("ctrl + c")  # In order to avoid ugly output
                break
    bprint("Videos renamed!")


def bprint(msg, mode=0):
    """
    Prettily display the messages.
    """
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
        print(f"(log)  {wrapped_msg}")
        return
    else:   # i.e. mode == 0
        print(f"---> {wrapped_msg}")
        return


def cprint(col1, col2="", col3="", is_long=False):
    if is_long:
        str1 = f"  {col1}".ljust(25)
    else:
        str1 = f"  {col1}".ljust(17)
    str2 = f"{col2}".ljust(25)
    bprint(str1 + str2 + col3, 3)
