# encoding: utf-8
"""Functions used by the cli.py script.

Makes the process of cleaning a folder easier and simplifies the
video logging process.
"""

import os
import time
from moviepy.video.io.VideoFileClip import VideoFileClip
from progress.bar import IncrementalBar


def folder_sort(extensions, sudo):
    """Sort the files into directories according to their extension.
    Create the extensions directories if they don't exist.

    Parameters
    ----------
    extensions : dict
        Contains the lists of extensions for each type of file.
    sudo : bool
        Sudo mode is activated or not.
    """
    check_parent(sudo)
    n = get_number_files(extensions)
    if n == 0:
        raise EmptyFolder(
            "Nothing to do here, this folder is empty."
        )
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
        Duration limit.
    extensions : dict
        Contains the lists of extensions for each type of file.
    sudo : bool
        Sudo mode is activated or not.
    """
    def move_to_trash(file, duration, trash_folder_name):
        """Move a video to trash if it is too short.

        Check if a directory named trash_folder_name exists in current directory. If not,
        create it. Then, move `file` in trash_folder_name if `duration` is smaller than
        `time_limit`.

        Parameters
        ----------
        file : string
            File to check.
        duration : int
            Duration of video file.
        """
        if duration < time_limit:
            if os.path.exists(trash_folder_name):  # if 'trash_folder_name' already exists
                if os.path.isfile(trash_folder_name):  # if 'trash_folder_name' is a regular file
                    raise BadFolderName(
                        f"You have a file named '{trash_folder_name}' in the current working directory, which is not a valid file name because this tool uses it as a directory name. You may consider changing the 'trash_folder_name' default in 'data.yaml'."
                    )
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
        raise EmptyFolder(
            "Nothing to do here, this folder does not countain any video."
        )
    bar = IncrementalBar(f"Trashing videos of duration <= {time_limit}s...", max=n)

    nb_trashed = 0
    for file in os.listdir():
        extension = os.path.splitext(file)[1]
        if extension in extensions['Videos']:
            with VideoFileClip(file) as clip:
                # we need to wait a little so that bad things do not happen
                time.sleep(.001)
                duration = clip.duration
            is_moved = move_to_trash(file, duration, trash_folder_name)  # side effect warning
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
    directory : string
        Type of files to move. If None, all the files are moved.
    extensions : dict
        Contains the lists of extensions for each type of file.
    sudo : bool
        Sudo mode is activated or not.
    """
    check_parent(sudo)
    n = get_number_files(extensions, directory)
    if n == 0:  # no file match the request
        if directory is not None:
            raise EmptyFolder(
                    f"Nothing to do here, this folder does not contain any element of the type '{directory}'."
                )
        else:
            raise EmptyFolder(
                "Nothing to do here, this folder is empty."
            )
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
                raise BadFolderName(
                    f"You have a file named '{directory}' in the current working directory, which is not a valid file name because this tool uses it as a directory name. You may consider changing the 'EXTENSIONS' directories default in 'data.yaml'."
                )
            else:  # if 'directory' is a directory
                pass
        else:  # if 'directory' does not exist
            os.mkdir(f'./{directory}')
        os.rename(file, os.path.join(directory, file))

def check_parent(sudo):
    """Check if 'video-logging' scripts are in cwd to prevent bad things
    from happening.

    Parameters
    ----------
    sudo : bool
        Sudo mode is activated or not.
    """
    if not sudo:
        for root, dirs, files in os.walk("./"):
            if ".videolog" in files:
                raise SudoException()
    else:
        # maybe print a message here
        pass


def get_number_files(extensions, directory=None):
    """Return number of file of a certain type in cwd.

    Parameters
    ----------
    extensions : dict
        Contains the lists of extensions for each type of file.
    directory : string
        Target directory. If None, return total number of files.
    """
    if directory is None:  # all the files
        return len(os.listdir())
    count = 0
    for file in os.listdir():
        extension = os.path.splitext(file)[1]
        if extension in extensions[directory]:
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
