# encoding: utf-8
"""
Cleans a folder to simplify the video logging process.
"""

import os
import time
import subprocess
from textwrap import fill
from moviepy.video.io.VideoFileClip import VideoFileClip


EXTENSIONS = {
    'Audio': ['.wav', '.mp3', '.raw', '.wma', '.aif', '.cda', '.mid', '.midi',
              '.mpa', '.ogg', '.wpl'],
    'Videos': ['.mp4', '.m4a', '.m4v', '.f4v', '.f4a', '.f4b', '.m4b', '.m4r',
               '.avi', '.wmv', '.flv', '.MOV'],
    'Images': ['.ai', '.bmp', '.gif', '.ico', '.jpeg', '.jpg', '.png', '.ps',
               '.svg', '.tif', '.tiff'],
    'Documents': ['.txt', '.pdf', '.doc', '.docx', '.odt', '.html', '.md',
                  '.rtf', '.xlsx', '.pptx', '.tex', '.key', '.odp', '.pps',
                  '.ppt', '.pptx', '.ods'],
    'Folders': ['.rar', '.zip', '7z', '.pkg', '.z', '.tar.gz'],
    'Python': ['.py', '.pyc'],
    'Internet': ['.css', '.htm', '.html', '.js', '.php', '.xhtml'],
    'Data': ['.csv', '.dat', '.db', '.dbf', '.log', '.mdb', '.sav', '.sql',
             '.tar', '.xml'],
    'Fonts': ['.fnt', '.fon', '.otf', '.ttf'],
    'Other': ['']
}

PATH_TO_VLC = "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe"


def folder_sort():
    """
    Sort the files into directories according to their extension.
    Create the directories if they don't exist.
    """

    print("")
    bprint("Sorting files...\n")

    cprint("File type", "File name")
    bprint(" " + 27 * "-", 3)
    for file in os.listdir():
        time.sleep(.001)
        name, extension = os.path.splitext(file)
        if os.path.isdir(file):
            if name not in EXTENSIONS:
                move_to_dir(file, 'Folders')
            else:
                print("script")
        else:
            treated = False
            for directory in EXTENSIONS:
                if extension in EXTENSIONS[directory]:
                    move_to_dir(file, directory)
                    treated = True
                    break
            if not treated:
                move_to_dir(file, 'Other')

    print("")
    bprint("Files sorted by type!")


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
            cprint(file, duration, "(trashed)", is_long=True)
        else:
            cprint(file, duration, is_long=True)

    print("")
    bprint("Trashing videos of duration <= {}s...\n".format(time_limit))

    cprint("File name", "Duration", is_long=True)
    bprint(" " + 32 * "-", 3)
    for file in os.listdir():
        extension = os.path.splitext(file)[1]
        if extension in EXTENSIONS['Videos']:
            with VideoFileClip(file) as clip:
                time.sleep(.001)
                duration = clip.duration
            to_trash = ""
            move_to_trash(file, duration)

    print("")
    bprint("Files trashed!")


def sort_by_date():
    """
    Sort files in directories by date.
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


def file_rename(directory, exit_list, trash_list):
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
        try:
            new_name = input('       >> new name: ')
            if new_name in exit_list:
                return
            elif new_name in trash_list:
                if not os.path.isdir('Trash'):
                    os.mkdir('./Trash')
                os.rename(file, os.path.join('Trash', file))
            elif new_name != "":
                os.rename(file, new_name + extension)
        except (EOFError, KeyboardInterrupt):
            print("ctrl + c")  # In order to avoid ugly output
            return

    print("")
    bprint("Renaming the {}...\n".format(directory.lower()))

    cprint("File type", "Original name")
    bprint(" " + 34 * "-", 3)
    for file in os.listdir():
        extension = os.path.splitext(file)[1]
        if not os.path.isdir(file) and extension in EXTENSIONS[directory]:
            time.sleep(.001)
            open_and_rename(file, extension, directory)

    bprint("Videos renamed!")



def move_to_dir(file, directory):
    """
    Move file to directory
    """
    if not os.path.isdir(directory):
        os.mkdir('./{}'.format(directory))
    os.rename(file, os.path.join(directory, file))


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
    elif mode == 2:
        print(f"---X {wrapped_msg}")
    elif mode == 3:
        print(f"     {wrapped_msg}")
    elif mode == 4:
        print(f"(log)  {wrapped_msg}")
    else:   # i.e. mode == 0
        print(f"---> {wrapped_msg}")


def cprint(col1, col2="", col3="", is_long=False):
    """
    Prettily display columns using bprint.
    """
    if is_long:
        str1 = f"  {col1}".ljust(25)
    else:
        str1 = f"  {col1}".ljust(17)
    str2 = f"{col2}".ljust(25)
    bprint(str1 + str2 + col3, 3)
