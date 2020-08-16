# encoding: utf-8
"""
CLI for videologging.
"""

import os
import sys
import yaml
import videologging.functions as fun


class CLI(object):
    """CLI for videologging."""

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
        self.rename_list = ["rename", "r", "name"]
        self.help_list = ["help", "h", "?", "what", "how"]
        self.sudo_list = ["sudo"]
        self.exit_list = ["exit", "e", "leave", "l", "quit", "q"]
        # Using a dictionary that translates an accepted user input into its internal representation.
        # Several keywords can have the same internal representation (if they trigger the same command).
        self.preprocess = dict()
        for instruction in ["cd", "folder", "trash", "date", "rename", "help", "sudo", "exit"]:
            instruction_list = getattr(self, instruction + "_list")
            self.preprocess.update({keyword: instruction for keyword in instruction_list})

        # current folder
        self.folder = os.getcwd() if self.PARAMETERS["default_folder"] is None else self.PARAMETERS["default_folder"]
        os.chdir(self.folder)
        # trash folder name
        self.trash_folder_name = self.PARAMETERS["trash_folder_name"]
        # open while renaming
        self.open_while_renaming = self.PARAMETERS["open_while_renaming"]
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
            # empty line, we can just ignore it
            return
        # else ...
        instruction = split_command[0].lower()
        cursor += 1

        if instruction in self.preprocess:
            # the instruction is recognized by the application, we now branch depending on the internal representation of the instruction.
            internal_instruction = self.preprocess[instruction]

            if internal_instruction == "cd":
                self.process_change_dir(command, split_command, cursor)

            elif internal_instruction == "exit":
                self.exit()

            else:
                # for instance:
                # self.process_folder(split_command, cursor)
                process_instruction = getattr(self, "process_" + internal_instruction)
                process_instruction(split_command, cursor)

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
            # we cannot use split_command here because it does not take spaces into account
            # remove command word
            command = command.split(' ', 1)[1]
            # remove spaces at the beginning
            directory = command.lstrip()

            cursor += 1
            try:
                os.chdir(directory)
                self.folder = os.getcwd()
                # display(self)
            except FileNotFoundError as e:
                print(err(f"Cannot find the '{directory}' directory."))

    def process_folder(self, split_command, cursor):
        """
        When the 'folder' command is read.
        """
        print(info(fun.folder_sort(self.EXTENSIONS, self.sudo)))

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
                    print(info(fun.trash_videos(int_time_limit, self.EXTENSIONS, self.trash_folder_name, self.sudo)))
            except ValueError as e:
                print(err(f"Could not parse '{time_limit}' as a positive int. Please input a positive integer."))

    def process_date(self, split_command, cursor):
        """
        When the 'date' command is read.
        """
        if len(split_command) == cursor:
            # i.e. we have no more arguments available
            print(info(fun.sort_by_date(self.EXTENSIONS, self.sudo)))
        else:
            directory = split_command[cursor]
            cursor += 1
            if directory not in self.EXTENSIONS:
                print(err(f"{directory} is not a valid directory. Please input a valid directory."))
            else:
                print(info(fun.sort_by_date(self.EXTENSIONS, self.sudo, directory)))

    def process_rename(self, split_command, cursor):
        """
        When the 'rename' command is read.
        """
        if len(split_command) == cursor:
            # i.e. we have no more arguments available
            print(info(fun.rename_files(self.EXTENSIONS, self.open_while_renaming)))
        else:
            directory = split_command[cursor]
            cursor += 1
            if directory not in self.EXTENSIONS:
                print(err(f"{directory} is not a valid directory. Please input a valid directory."))
            else:
                print(info(fun.rename_files(self.EXTENSIONS, self.open_while_renaming, directory)))


    def process_sudo(self, split_command, cursor):
        """
        When the 'sudo' command is read.
        """
        if len(split_command) == cursor:
            # i.e. we have no more arguments available
            print(warning(self.WARNINGS["syntax-sudo"]))
        else:
            mode = split_command[cursor].lower()
            cursor += 1
            if mode == "on":
                self.sudo = True
                print(warning(self.WARNINGS["sudo-on"]))
            elif mode == "off":
                self.sudo = False
                print(warning(self.WARNINGS["sudo-off"]))
            else:
                print(err("The possible values for sudo mode are 'on' and 'off'."))

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
            # also using the preprocessing dictionary here
            if topic in self.preprocess:
                # getting the internal representation
                internal_instruction = self.preprocess[topic]

                # we can almost grab the help directly, except for the help keyword itself, whose help section is called "help-twice"
                if internal_instruction == "help":
                    internal_instruction == "help-twice"

                # now we can print the help for the desired instruction.
                print(self.HELP[internal_instruction])

                # if the instruction was "folder", then we output some more contextual help
                if internal_instruction == "folder":
                    for directory in self.EXTENSIONS:
                        print(f"{directory}:".ljust(11, ' '), str(self.EXTENSIONS[directory]), sep='')
                        print(self.HELP["folder-creation"])
            else:  # the instruction is not recognized
                print(self.HELP["other"])

    def print_header(self):
        """Print header."""
        print(self.HEADER)


    def pretty_dir(self):
        """Return the input headline."""
        prefix = warning("(sudo) ") if self.sudo else ""
        suffix = dir_style(self.folder + ">")
        return f"{prefix}{suffix}"


def err(text):
    """Create a pretty error string from text."""
    return f"\033[91m{text}\033[m"

def warning(text):
    """Create a pretty warning string from text."""
    return f"\033[93m{text}\033[m"

def info(text):
    """Create a pretty informative string from text."""
    return f"\033[92m{text}\033[m"

def dir_style(text):
    """Create a pretty directory string from text."""
    return f"\033[94m{text}\033[m"


def main():
    import platform
    platform = platform.system()
    if platform == "Windows":
        os.system('cls')
    elif platform == "Linux":
        os.system('clear')
    else:
        sys.exit(f"Your platform ({platform}) isn't supported yet...")

    with open('videologging/data.yaml') as yaml_file:
        data = yaml.load(yaml_file, Loader=yaml.FullLoader)
    cli = CLI(data)
    cli.print_header()

    while True:
        try:
            print()
            print(cli.pretty_dir())
            command = input(dir_style(">> "))
            cli.read_command(command)
        except fun.EmptyFolder as e:
            print(info(str(e)))
        except fun.BadFolderName as e:
            print()  # to avoid ugly output
            print(err(str(e)))
        except fun.SudoException as e:
            print(warning(cli.WARNINGS["sudo-exception"]))
        except OSError as e:
            print(error(str(e)))
        except (EOFError, KeyboardInterrupt):
            print("exit")  # to avoid ugly output
            cli.exit()
            break

if __name__ == '__main__':
    main()
