# encoding: utf-8
"""
CLI for the video_logging.py module.
"""

import os
import platform
import sys
import yaml
import src.video_logging as log
from src.video_logging import EmptyFolder, BadFolderName, SudoException


class CLI(object):
    """CLI for the video_logging module."""

    def __init__(self, data):
        """Class constructor."""
        # data files
        self.PARAMETERS = data["PARAMETERS"]
        self.EXTENSIONS = data["EXTENSIONS"]
        self.HELP = data["HELP"]
        self.WARNINGS = data["WARNINGS"]
        self.HEADER = data["HEADER"]
        # list of all parameters accepted to trigger the different modes.
        self.cd_list = ["cd", "c", "go"]
        self.folder_list = ["folder", "f", "folders"]
        self.trash_list = ["trash", "t", "short"]
        self.date_list = ["date", "d", "when"]
        self.help_list = ["help", "h", "?", "what", "how"]
        self.sudo_list = ["sudo"]
        self.exit_list = ["exit", "e", "leave", "l", "quit", "q"]
        # current folder
        self.folder = os.getcwd() if self.PARAMETERS["default_folder"] is None else self.PARAMETERS["default_folder"]
        os.chdir(self.folder)
        # trash folder name
        self.trash_folder_name = self.PARAMETERS["trash_folder_name"]
        # sudo mode
        self.sudo = self.PARAMETERS["default_sudo"]

    def read_command(self, command):
        """
        Read from the users command.
        """
        # cursor is used to keep track of how many argument we read from the users command.
        cursor = 0
        split_command = str.split(command)
        if len(split_command) == 0:
            # Empty line, we can just ignore it
            return
        # else ...
        instruction = split_command[0]
        cursor += 1

        if instruction.lower() in self.cd_list:
            self.process_change_dir(command, split_command, cursor)

        elif instruction.lower() in self.folder_list:
            self.process_folder()

        elif instruction.lower() in self.trash_list:
            self.process_trash(split_command, cursor)

        elif instruction.lower() in self.date_list:
            self.process_date(split_command, cursor)

        elif instruction.lower() in self.help_list:
            self.process_help(split_command, cursor)

        elif instruction.lower() in self.sudo_list:
            self.process_sudo(split_command, cursor)

        elif instruction.lower() in self.exit_list:
            self.exit()
        else:
            print(err(f"The input command {command} could not be parsed, because the tool did not understand the term '{instruction}'. If you wish to you can use :\n'>> help'\nThat instruction will bring a list of the available instruction and their use cases."))

    def exit(self):
        """
        Used to leave the tool.
        """
        print("Leaving the tool...\n")
        sys.exit(0)

    def process_change_dir(self, command, split_command, cursor):
        """
        When the 'cd' command is read.
        """
        if len(split_command) == cursor:
            # i.e. we have no more arguments available
            print(warning(self.WARNINGS["syntax-dir"]))
        else:
            # we cannot use split_command here because it does not take spaces
            # into account
            # remove command word
            command = command.split(' ', 1)[1]
            # remove spaces at the beginning
            nb_spaces = 0
            while command[nb_spaces] == ' ':
                nb_spaces += 1
            directory = command[nb_spaces:]

            cursor += 1
            try:
                os.chdir(directory)
                self.folder = os.getcwd()
                # display(self)
            except FileNotFoundError as e:
                print(err(f"Cannot find the '{directory}' directory."))

    def process_folder(self):
        """
        When the 'folder' command is read.
        """
        print(info(log.folder_sort(self.EXTENSIONS, self.sudo)))

    def process_trash(self, split_command, cursor):
        """
        When the 'trash' command is read.
        """
        if len(split_command) == cursor:
            # i.e. we have no more arguments available
            print(warning(self.WARNINGS["syntax-time"]))
        else:
            time_limit = split_command[cursor]
            cursor += 1
            try:
                int_time_limit = int(time_limit)
                if int_time_limit <= 0:
                    print(err(f"Negative (zero included) values are not valid. Please input a positive integer."))
                else:
                    print(info(log.trash_videos(int_time_limit, self.EXTENSIONS, self.trash_folder_name, self.sudo)))
            except ValueError as e:
                print(err(f"Could not parse '{time_limit}' as a positive int. Please input a positive integer."))

    def process_date(self, split_command, cursor):
        """
        When the 'date' command is read.
        """
        if len(split_command) == cursor:
            # i.e. we have no more arguments available
            print(info(log.sort_by_date(self.EXTENSIONS, self.sudo)))
        else:
            directory = split_command[cursor]
            cursor += 1
            if directory not in self.EXTENSIONS:
                print(err(f"{directory} is not a valid directory. Please input a valid directory."))
            else:
                print(info(log.sort_by_date(self.EXTENSIONS, self.sudo, directory)))

    def process_sudo(self, split_command, cursor):
        """
        When the 'sudo' command is read.
        """
        if len(split_command) == cursor:
            # i.e. we have no more arguments available
            print(warning(self.WARNINGS["syntax-sudo"]))
        else:
            mode = split_command[cursor]
            cursor += 1
            if mode.lower() == "on":
                self.sudo = True
                print(warning(self.WARNINGS["sudo-on"]))
            elif mode.lower() == "off":
                self.sudo = False
                print(warning(self.WARNINGS["sudo-off"]))
            else:
                print(err(
                    "The possible values for sudo mode are 'on' and 'off'."
                ))

    def process_help(self, split_command, cursor):
        """
        When the 'help' command is read.
        """
        if len(split_command) == cursor:
            # i.e. no more arguments to read, just printing command list.
            print(self.HELP["help"])
        else:
            topic = split_command[cursor]
            cursor += 1
            if topic in self.exit_list:
                print(self.HELP["exit"])
            elif topic in self.cd_list:
                print(self.HELP["cd"])
            elif topic in self.folder_list:
                print(self.HELP["folder"])
                for directory in self.EXTENSIONS:
                    print(f"{directory}:".ljust(11, ' ') + str(self.EXTENSIONS[directory]))
                print(self.HELP["folder-creation"])
            elif topic in self.trash_list:
                print(self.HELP["trash"])
            elif topic in self.date_list:
                print(self.HELP["date"])
            elif topic in self.sudo_list:
                print(self.HELP["sudo"])
            elif topic in self.help_list:
                print(self.HELP["help-twice"])
            else:
                print(self.HELP["other"])

    def print_header(self):
        """
        Print header.
        """
        print(self.HEADER)


    def pretty_dir(self):
        """
        Return the input headline.
        """
        prefix = warning("(sudo) ") if self.sudo else ""
        suffix = dir_style(self.folder + ">")
        return f"{prefix}{suffix}"


def err(text):
    """
    Create a pretty error String from text.
    """
    return f"\033[91m{text}\033[m"

def warning(text):
    """
    Create a pretty warning String from text.
    """
    return f"\033[93m{text}\033[m"

def info(text):
    """
    Create a pretty informative String from text.
    """
    return f"\033[92m{text}\033[m"

def dir_style(text):
    """
    Create a pretty directory String from text.
    """
    return f"\033[94m{text}\033[m"


def run():
    platform = platform.system()
    if platform == "Windows":
        os.system('cls')
    elif platform == "Linux":
        os.system('clear')
    else:
        sys.exit(f"Your platform ({platform}) isn't supported yet...")

    with open('src/data.yaml') as yaml_file:
        data = yaml.load(yaml_file, Loader=yaml.FullLoader)
    cli = CLI(data)
    cli.print_header()

    while True:
        try:
            print()
            print(cli.pretty_dir())
            command = input(dir_style(">> "))
            cli.read_command(command)
        except EmptyFolder as e:
            print(info(str(e)))
        except BadFolderName as e:
            print()  # to avoid ugly output
            print(err(str(e)))
        except SudoException as e:
            print(warning(cli.WARNINGS["sudo-exception"]))
        except OSError as e:
            print(error(str(e)))
        except (EOFError, KeyboardInterrupt):
            print("exit")  # to avoid ugly output
            cli.exit()
            break

if __name__ == '__main__':
    run()
