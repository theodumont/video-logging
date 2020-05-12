# encoding: utf-8
"""
CLI for the video_logging.py module.
"""

import os
import sys
import json
import src.video_logging as log
from termcolor import cprint, colored


class CLI(object):
    """CLI for the video_logging module."""

    def __init__(self, data):
        """
        Class constructor.
        """
        # data files
        self.EXTENSIONS = data["EXTENSIONS"]
        self.HELP = data["HELP"]
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
        self.folder = os.getcwd()
        # sudo mode
        self.sudo = False

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
            self.process_change_dir(split_command, cursor)

        elif instruction.lower() in self.folder_list:
            self.process_folder()

        elif instruction.lower() in self.trash_list:
            self.process_trash(split_command, cursor)

        elif instruction.lower() in self.date_list:
            self.process_date()

        elif instruction.lower() in self.help_list:
            self.process_help(split_command, cursor, self.EXTENSIONS, self.HELP)

        elif instruction.lower() in self.sudo_list:
            self.process_sudo(split_command, cursor)

        elif instruction.lower() in self.exit_list:
            self.exit()
        else:
            self.print_error(f"The input command {command} could not be parsed, because the tool did not understand the term '{instruction}'. If you wish to you can use :\n'>> help'\nThat instruction will bring a list of the available instruction and their use cases.")

    def exit(self):
        """
        Used to leave the tool.
        """
        print("Leaving the tool...\n")
        sys.exit(0)

    def process_change_dir(self, split_command, cursor):
        """
        When the 'cd' command is read.
        """
        if len(split_command) == cursor:
            # i.e. we have no more arguments available
            self.print_warning(
                "The syntax to change directory is:\n"
                "'>> cd <directory>'"
            )
        else:
            directory = split_command[cursor]
            cursor += 1
            try:
                os.chdir(directory)
                self.folder = os.getcwd()
                # display(self)
            except FileNotFoundError as e:
                self.print_error(f"Cannot find the '{directory}' directory.")

    def process_folder(self):
        """
        When the 'folder' command is read.
        """
        log.folder_sort(self.EXTENSIONS, self.sudo)

    def process_trash(self, split_command, cursor):
        """
        When the 'trash' command is read.
        """
        if len(split_command) == cursor:
            # i.e. we have no more arguments available
            self.print_warning(
                "The syntax to choose the time limit is:\n"
                "'>> trash <time limit>'"
            )
        else:
            time_limit = split_command[cursor]
            cursor += 1
            try:
                int_time_limit = int(time_limit)
                if int_time_limit <= 0:
                    self.print_error(f"Negative (zero included) values are not valid. Please input a positive integer.")
                else:
                    log.trash_videos(int_time_limit, self.EXTENSIONS, self.sudo)
            except ValueError as e:
                self.print_error(f"Could not parse '{time_limit}' as a positive int. Please input a positive integer.")

    def process_date(self):
        """
        When the 'date' command is read.
        """
        log.sort_by_date(self.sudo)

    def process_sudo(self, split_command, cursor):
        """
        When the 'sudo' command is read.
        """
        if len(split_command) == cursor:
            # i.e. we have no more arguments available
            self.print_warning(
                "The syntax to change sudo mode is:\n"
                "'>> sudo off'"
            )
        else:
            mode = split_command[cursor]
            cursor += 1
            if mode.lower() == "on":
                self.sudo = True
                self.print_warning(
                    "! Warning: sudo mode activated. The tool will not check if the current directory contains the 'video-logging' scripts anymore.\n"
                    "! Moving files may do bad things.\n"
                    "! You can turn the sudo mode back off using:\n"
                    "'>> sudo off'"
                )
            elif mode.lower() == "off":
                self.sudo = False
                self.print_warning(
                    "sudo mode deactivated."
                )
            else:
                self.print_error(
                    "The possible values for sudo mode are 'on' and 'off'."
                )

    def process_help(self, split_command, cursor, EXTENSIONS, HELP):
        """
        When the 'help' command is read.
        """
        if len(split_command) == cursor:
            # i.e. no more arguments to read, just printing command list.
            print("".join(HELP["help"]))
        else:
            topic = split_command[cursor]
            cursor += 1
            if topic in self.exit_list:
                print(HELP["exit"])
            elif topic in self.cd_list:
                print(HELP["cd"])
            elif topic in self.folder_list:
                print(HELP["folder"])
                for directory in EXTENSIONS:
                    print(f"{directory}:".ljust(11, ' ') + str(EXTENSIONS[directory]))
                print(HELP["folder-creation"])
            elif topic in self.trash_list:
                print(HELP["trash"])
            elif topic in self.date_list:
                print(HELP["date"])
            elif topic in self.sudo_list:
                print(HELP["sudo"])
            elif topic in self.help_list:
                print(HELP["help-twice"])
            else:
                print(HELP["other"])

    def print_header(self):
        """
        Print header.
        """
        print("\n".join(self.HEADER))


    def print_dir(self):
        """
        Print the input headline.
        """
        prefix = colored("(sudo) ", "yellow") * self.sudo
        suffix = colored(self.folder + ">", "cyan")
        print(f"{prefix}{suffix}")


    def print_error(self, string):
        """
        Print an error.
        """
        cprint(string, 'red', file=sys.stderr)

    def print_warning(self, string):
        """
        Print a warning.
        """
        cprint(string, 'yellow', file=sys.stderr)



if __name__ == '__main__':
    os.system('cls')
    with open('src/data.json', 'r') as file:
        data = json.load(file)
    cli = CLI(data)

    cli.print_header()

    while True:
        try:
            print()
            cli.print_dir()
            command = input(colored(">> ", "cyan"))
            cli.read_command(command)
        except OSError as e:
            cli.print_warning(str(e))
        except (EOFError, KeyboardInterrupt):
            print("exit")  # in order to avoid ugly output
            cli.exit()
            break
