# encoding: utf-8

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
parser.add_argument("-s", "--sort", action="store_true",
                    help="organizes the folder")
parser.add_argument("-d", "--delete", action="store_true",
                    help="deletes the useless videos")
args = parser.parse_args()

os.chdir(args.folder_to_sort)


class MyCleaner():

    def __init__(self, folder_to_sort):
        """
        Class initialization
        """
        self.folder_to_sort = folder_to_sort
        self.time_limit = time_limit

    def sort(self):
        """
        Sort the files in folders according to their extension.
        Create directories if they don't exist.
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
        print(">> Files sorted!\n")

    def delete_trash_videos(self):
        """
        Delete the videos that are shorter than self.time_limit
        """
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


if __name__ == '__main__':
    print('** Cleanup of the {} folder **\n'.format(args.folder_to_sort))
    cleaner = MyCleaner(args.folder_to_sort)
    if args.sort:
        cleaner.sort()
    if args.delete:
        cleaner.delete_trash_videos()
