# encoding: utf-8
"""
Cleans a folder to simplify the derushing process.
"""

import os
import time
import argparse
from moviepy.video.io.VideoFileClip import VideoFileClip


DIRS = ['Audio', 'Videos', 'Images', 'Documents', 'Folders', 'Other']
EXT_AUDIO = ['.wav', '.mp3', '.raw', '.wma']
EXT_VIDEO = ['.mp4', '.m4a', '.m4v', '.f4v', '.f4a', '.f4b', '.m4b', '.m4r', '.avi', '.wmv', '.flv', '.MOV']
EXT_IMAGE = ['.jpeg', '.jpg', '.png', '.svg', '.bmp', '.gif']
EXT_DOCUMENT = ['.txt', '.pdf', '.doc', '.docx', '.odt', '.html', '.md', '.rtf', '.xlsx', '.pptx']
EXT_FOLDER = ['.rar', '.zip']


# limit time for deleting (seconds)
time_limit = 2

parser = argparse.ArgumentParser()
parser.add_argument("folder_to_sort", type=str, help="folder to clean")
parser.add_argument("-f", "--folder", action="store_true",
                    help="organize the folder by file type")
parser.add_argument("-t", "--trash", action="store_true",
                    help="trash the very short videos")
parser.add_argument("-d", "--date", action="store_true",
                    help="sort videos in directories by date")
args = parser.parse_args()

os.chdir(args.folder_to_sort)


class MyCleaner():

    """
    Cleans a folder.
    """

    def __init__(self, folder_to_sort, time_limit):
        """
        Class initialization.
        """
        self.folder_to_sort = folder_to_sort
        self.time_limit = time_limit

    def folder_sort(self):
        """
        Sorts the files into directories according to their extension.
        Creates the directories if they don't exist.
        """
        print(">> Sorting files...\n")
        moved = "   -> moved"
        if not os.path.isdir('Audio'):
            for d in DIRS:
                os.mkdir('./{}'.format(d))

        print("  File type    File name\n"
              " -------------------------")
        for file in os.listdir():
            name, extension = os.path.splitext(file)

            if extension in EXT_AUDIO:
                print(" Audio          {0}{1}".format(file, moved))
                os.rename(file, 'Audio/' + file)
            elif extension in EXT_VIDEO:
                print(" Video          {0}{1}".format(file, moved))
                os.rename(file, 'Videos/' + file)
            elif extension in EXT_IMAGE:
                print(" Image          {0}{1}".format(file, moved))
                os.rename(file, 'Images/' + file)
            elif extension in EXT_DOCUMENT:
                print(" Document       {0}{1}".format(file, moved))
                os.rename(file, 'Documents/' + file)
            else:
                if os.path.isdir(name) or extension in EXT_FOLDER:
                    if name not in DIRS:
                        print(" Folder         {0}{1}".format(file, moved))
                        os.rename(file, 'Folders/' + file)
                    else:
                        print(" Script         {}".format(file))
                else:
                    print(" Other          {0}{1}".format(file, moved))
                    os.rename(file, 'Other/' + file)
            time.sleep(.1)
        print(">> Files sorted!\n")

    def trash_videos(self):
        """
        Trashes the videos that are shorter than self.time_limit to get rid of
        all the shooting errors.
        """
        if not os.path.isdir('Audio'):
            self.folder_sort()
        print(">> Trashing files...\n")
        if not os.path.isdir('Videos/Trash'):
            os.mkdir('Videos/Trash')
        print("  File name      Duration\n"
              " -------------------------")
        for file in os.listdir('./Videos'):
            if not os.path.isdir('Videos/' + file):
                clip = VideoFileClip('Videos/' + file)
                duration = clip.duration
                clip.close()
                time.sleep(.1)
                deleted = ""
                if duration < self.time_limit:
                    os.rename('Videos/' + file, 'Videos/Trash/' + file)
                    deleted = "   -> moved to '/Trash'"
                print(" {0}     {1:.1f} s{2}".format(file, duration, deleted))
        print(">> Files trashed!\n")

    def sort_videos(self):
        """
        Sorts videos in directories by date to simplifiy the derushing process.
        """
        print(">> Sorting videos by date...\n")
        if not os.path.isdir('Audio'):
            self.folder_sort()
        sep = ' ' + 50*'-'
        print("File name".center(25) + "      Created on\n"+sep)
        for file in os.listdir('./Videos'):
            if not os.path.isdir('Videos/' + file):
                path = 'Videos/' + file
                creation = time.localtime(os.path.getmtime(path))
                destination = time.strftime('%y%m%d-%a', creation)
                print((file.center(25) + '{0}   -> moved to {1}').format(
                      time.strftime('%c', creation),
                      destination))
                if not os.path.isdir('Videos/' + destination):
                    os.mkdir('Videos/' + destination)
                os.rename('Videos/' + file, 'Videos/' + destination + '/' + file)

                time.sleep(.1)


if __name__ == '__main__':
    # main program
    print('** Cleanup of the {} folder **\n'.format(args.folder_to_sort))

    cleaner = MyCleaner(args.folder_to_sort, time_limit)

    if args.folder:
        cleaner.folder_sort()
    if args.trash:
        cleaner.trash_videos()
    if args.date:
        cleaner.sort_videos()
