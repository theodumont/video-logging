# encoding: utf-8
"""Functions used by the cli.py script.

Makes the process of cleaning a folder easier and simplifies the
video logging process.
"""

import os
import time
from moviepy.video.io.VideoFileClip import VideoFileClip
from progress.bar import IncrementalBar
from subprocess import Popen
from psutil import Process


def folder_sort(extensions, sudo):
    """Sort the files into directories according to their extension.
    Create the extensions directories if they don't exist.

    Parameters
    ----------
    extensions : dict
        Contains the lists of extensions for each type of file.
    sudo : bool
        Whether sudo mode is activated or not.
    """
    check_parent(sudo)
    n = get_number_files(extensions)
    if n == 0:
        raise EmptyFolder("Nothing to do here, this folder is empty.")
    bar = IncrementalBar("Sorting files...", max=n)

    for file in os.listdir():
        move_to_dir(file, get_folder_from_extension(file, extensions))
        bar.next()
    bar.finish()
    return "Files sorted by type."


def trash_videos(time_limit, extensions, trash_folder_name, sudo):
    """Trash the videos that are shorter than time_limit to get rid of
    the shooting errors.

    Parameters
    ----------
    time_limit : int
        Duration limit. If a video has a duration smaller than time_limit, it is
        moved into trash_folder_name.
    extensions : dict
        Contains the lists of extensions for each type of file.
    trash_folder_name : string
        Name of the folder where to put the trashed videos. Equal to 'Trash' by
        default but can be change in the videologging/data.yaml file.
    sudo : bool
        Whether sudo mode is activated or not.
    """
    def move_to_trash(file, duration, trash_folder_name):
        """Move a video to trash if it is too short.

        Check if a directory named trash_folder_name exists in current directory.
        If not, create it. Then, move `file` in trash_folder_name if `duration`
        is smaller than `time_limit`.

        Parameters
        ----------
        file : string
            File to check.
        duration : int
            Duration of video file.
        trash_folder_name : string
            Name of the folder where to put the trashed videos. Equal to 'Trash'
            by default but can be change in the videologging/data.yaml file.
        """
        if duration < time_limit:
            if os.path.exists(trash_folder_name):  # if 'trash_folder_name' already exists
                if os.path.isfile(trash_folder_name):  # if 'trash_folder_name' is a regular file
                    raise BadFolderName(f"You have a file named '{trash_folder_name}' in the current working directory, which is not a valid file name because this tool uses it as a directory name. You may consider changing the 'trash_folder_name' default in 'data.yaml'.")
                else:  # if 'trash_folder_name' is a directory
                    pass
            else:  # if 'trash_folder_name' does not exist
                os.mkdir(f'./{trash_folder_name}')

            os.rename(file, os.path.join(trash_folder_name, file))
            return True
        return False

    check_parent(sudo)
    n = get_number_files(extensions, directory='Videos')
    if n == 0:
        raise EmptyFolder("Nothing to do here, this folder does not countain any video.")

    bar = IncrementalBar(f"Trashing videos of duration <= {time_limit}s...", max=n)
    nb_trashed = 0
    for file in os.listdir():
        extension = os.path.splitext(file)[1]
        if extension in extensions['Videos']:
            with VideoFileClip(file) as clip:
                # we need to wait a little so that bad things do not happen
                time.sleep(.001)
                duration = clip.duration
            is_moved = move_to_trash(file, duration, trash_folder_name)  # warning: side effect happening here
            if is_moved:
                nb_trashed += 1
            bar.next()

    bar.finish()
    term = "s" if nb_trashed >= 2 else ""
    return f"{nb_trashed} video{term} trashed."


def sort_by_date(extensions, sudo, directory=None):
    """Sort files in directories by creation date.

    Repositories will be in the form of 'YYMMDD-Day'.

    Parameters
    ----------
    extensions : dict
        Contains the lists of extensions for each type of file.
    sudo : bool
        Whether sudo mode is activated or not.
    directory : string
        Type of files to move. If None, all the files are moved.
    """
    check_parent(sudo)
    n = get_number_files(extensions, directory)
    if n == 0:  # i.e. no file match the request
        if directory is not None:
            raise EmptyFolder(f"Nothing to do here, this folder does not contain any element of the type '{directory}'.")
        else:
            raise EmptyFolder("Nothing to do here, this folder is empty.")

    bar = IncrementalBar(f"Sorting files by date...", max=n)
    for file in os.listdir():
        extension = os.path.splitext(file)[1]
        if not directory or extension in extensions[directory]:
            if not os.path.isdir(file):
                creation = time.localtime(os.path.getmtime(file))
                destination_directory = time.strftime('%y%m%d-%a', creation)
                move_to_dir(file, destination_directory)

                bar.next()

    bar.finish()
    return f"Files sorted by date."


def rename_files(extensions, open_while_renaming, directory=None):
    """Open and rename the files in current directory.

    Parameters
    ----------
    extensions : dict
        Contains the lists of extensions for each type of file.
    open_while_renaming : bool
        Whether or not opening files while renaming them.
    directory : string
        Type of files to rename. If None, all the files are renamed.

    Notes
    -----
    * Folders are not renamed;
    * The process of opening and renaming files is as follows:
        1. run the command `start /WAIT $file` in shell;
        2. wait for the input of the user;
        3. if the window hasn't been closed yet by the user, close it using
        `psutil`.
    This method is inspired by https://stackoverflow.com/a/20820644.
    """
    n = get_number_files(extensions, directory, ignore_folders=True)
    if n == 0:  # i.e. no file match the request
        if directory is not None:
            raise EmptyFolder(f"Nothing to do here, this folder does not contain any element of the type '{directory}'.")
        else:
            raise EmptyFolder("Nothing to do here, this folder is empty.")

    nb_renamed = 0
    nb_trashed = 0
    try:
        for file in os.listdir():
            extension = os.path.splitext(file)[-1]
            if os.path.isdir(file) or (directory is not None and extension not in extensions[directory]):
                # we don't have to rename this file
                continue

            if open_while_renaming:
                # run subprocess
                process = Popen("start /WAIT " + file, shell=True)
            # loop until new name for file is ok
            new_name = ""
            while new_name in ["", "help"]:
                if new_name == "help":
                    print("help on renaming")
                    new_name = ""
                new_name = input(f"[{file}] >> new name: ")
            if open_while_renaming:
                # kill subprocess if not closed
                if process.poll() is None:
                    Process(process.pid).children()[0].kill()
                    time.sleep(.1)
            # use input
            if new_name == "trash":
                move_to_dir(file, "Trash")
                nb_trashed += 1
            elif new_name == "exit":
                raise UserInterrupt()  # to leave the two loops
            else:
                os.rename(file, new_name + extension)
                nb_renamed += 1

    except UserInterrupt:
        print("Stopping file renaming...")
    except (EOFError, KeyboardInterrupt):
        print("exit\nStopping file renaming...")
    except Exception as e:
        print(e)
    finally:
        if open_while_renaming:
            # kill subprocess if not closed
            if process.poll() is None:
                Process(process.pid).children()[0].kill()
        # print result in shell
        term_renamed = "s" if nb_renamed >= 2 else ""
        sentence_renamed = f"{nb_renamed} file{term_renamed} renamed."
        term_trashed = "s" if nb_trashed >= 2 else ""
        sentence_trashed = f"{nb_trashed} file{term_trashed} trashed."
        if nb_renamed >= 1 and nb_trashed >= 1:
            return f"{sentence_renamed}\n{sentence_trashed}"
        elif nb_renamed != 0:
            return sentence_renamed
        elif nb_trashed != 0:
            return sentence_trashed
        else:  # both are 0
            return "Nothing has been modified."


def move_to_dir(file, directory):
    """Move file to directory.

    Check if a directory named `directory` exists in current directory. If not,
    create it. Then, move `file` in `directory`.

    Parameters
    ----------
    file : string
        File to move.
    directory : string
        Target directory.
    """
    if directory is not None:
        if os.path.exists(directory):  # if 'directory' already exists
            if os.path.isfile(directory):  # if 'directory' is a regular file
                raise BadFolderName(f"You have a file named '{directory}' in the current working directory, which is not a valid file name because this tool uses it as a directory name. You may consider changing the 'EXTENSIONS' directories default in 'data.yaml'.")
            else:  # if 'directory' is a directory
                pass
        else:  # if 'directory' does not exist
            os.mkdir(f'./{directory}')
        os.rename(file, os.path.join(directory, file))

def check_parent(sudo):
    """Check if 'video-logging' scripts are in cwd to prevent bad things from
    happening.

    Parameters
    ----------
    sudo : bool
        Whether sudo mode is activated or not.
    """
    if not sudo:
        for root, dirs, files in os.walk("./"):
            if ".videolog" in files:
                raise SudoException()
    else:
        # maybe print a message here if verbose
        pass


def get_number_files(extensions, directory=None, ignore_folders=False):
    """Return number of file of a certain type in cwd.

    Parameters
    ----------
    extensions : dict
        Contains the lists of extensions for each type of file.
    directory : string
        Target directory. If None, return total number of files.
    """
    count = 0
    for file in os.listdir():
        extension = os.path.splitext(file)[1]
        if directory is None or extension in extensions[directory]:
            if not ignore_folders or os.path.isfile(file):
                count += 1
    return count


def get_folder_from_extension(file, extensions):
    """Return the folder corresponding to an extension.

    Parameters
    ----------
    file : string
        File whose extension is targetted.
    extensions : dict
        Contains the lists of extensions for each type of file.
    """
    name, extension = os.path.splitext(file)
    if os.path.isdir(file):
        if name not in extensions:
            return 'Folders'
        else:
            return None
    else:
        for directory in extensions:
            if extension in extensions[directory]:
                return directory
        return 'Other'

class EmptyFolder(Exception):
    pass

class BadFolderName(Exception):
    pass

class SudoException(Exception):
    pass

class UserInterrupt(Exception):
    pass
