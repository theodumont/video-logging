# encoding: utf-8
"""
CLI for the 'video_logging' module.
"""

import os
import sys
try:
    import src.video_logging as log
except ImportError:
    print("---X This command line tool is an interface to a python module called video_logging. In order to use this tool you must first make sure that this module is available (it currently isn't). The recommended way to do this is to grab the source code video_logging.py and put it in the same directory as this cli.py file. The source code for video_logging is available freely on GitHub at https://github.com/theodumont/video_logging-python.")
    sys.exit(1)


class CLI(object):
    """CLI for the 'video_logging' module."""

    def __init__(self):
        """
        Class constructor.
        """
        # List of all parameters accepted to trigger the different modes.
        self.change_list = ["cd", "change", "c", "go"]
        self.folder_list = ["folder", "f", "folders"]
        self.trash_list = ["trash", "t", "short"]
        self.date_list = ["date", "d", "when"]
        self.rename_list = ["rename", "name", "r"]
        self.help_list = ["help", "h", "?", "what", "how"]
        self.exit_list = ["exit", "e", "leave", "l", "quit", "q"]
        # folder to clean
        self.folder = os.getcwd()

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

        if instruction.lower() in self.change_list:
            self.process_change_dir(split_command, cursor)

        elif instruction.lower() in self.folder_list:
            self.process_folder()

        elif instruction.lower() in self.trash_list:
            self.process_trash(split_command, cursor)

        elif instruction.lower() in self.date_list:
            self.process_date()

        elif instruction.lower() in self.rename_list:
            self.process_rename(split_command, cursor)

        elif instruction.lower() in self.help_list:
            self.process_help(split_command, cursor)

        elif instruction.lower() in self.exit_list:
            self.exit()
        else:
            log.bprint(f"The input command {command} could not be parsed, because the tool did not understand the term '{instruction}'. If you wish to you can use :\n'>> help'\nThat instruction will bring a list of the available instruction and their use cases.", 2)

    def exit(self):
        """
        Used to leave the tool.
        """
        log.bprint("Leaving the tool...")
        sys.exit(0)

    def process_change_dir(self, split_command, cursor):
        """
        When the 'cd' command is read.
        """
        if len(split_command) == cursor:
            # i.e. we have no more arguments available
            log.bprint(f"What folder do you want to clean?", 1)
            log.bprint(f"The syntax to change directory is:\n'>> cd <directory>'")
        else:
            directory = split_command[cursor]
            cursor += 1
            try:
                os.chdir(directory)
                self.folder = os.getcwd()
                # display(self)
            except FileNotFoundError as e:
                log.bprint(f"The tool could not find the {directory} directory. The correct syntax to change the directory is :\n'>> cd <directory>'", 2)

    def process_folder(self):
        """
        When the 'folder' command is read.
        """
        log.folder_sort()

    def process_trash(self, split_command, cursor):
        """
        When the 'trash' command is read.
        """
        if len(split_command) == cursor:
            # i.e. we have no more arguments available
            log.bprint(f"What time limit do you want to impose?", 1)
            log.bprint(f"The syntax to choose the time limit is:\n'>> trash <time limit>'\nTime limit has to be a positive int value.")
        else:
            time_limit = split_command[cursor]
            cursor += 1
            try:
                int_time_limit = int(time_limit)
                if int_time_limit <= 0:
                    log.bprint(f"You asked the tool to take {time_limit} as a time limit, but negative (zero included) values are not valid in that context. Please input a positive integer.", 2)
                else:
                    log.trash_videos(int_time_limit)
            except ValueError as e:
                log.bprint(f"The value of the time_limit has to be a positive int, but the tool could not parse {time_limit} as an int. The correct syntax to choose the time limit is :\n'>> trash <time_limit>'", 2)

    def process_date(self):
        """
        When the 'date' command is read.
        """
        log.sort_by_date()

    def process_rename(self, split_command, cursor):
        """
        When the 'rename' command is read.
        """
        if len(split_command) == cursor:
            # i.e. we have no more arguments available
            log.bprint(f"What files do you want to rename?", 1)
            log.bprint(f"The syntax to rename all files of a specific type is:\n'>> rename <file type>'\nfile type can take the values:\nvideos, \n")
        else:
            file_type = split_command[cursor]
            cursor += 1
            try:
                assert file_type in ['videos']
                log.file_rename(file_type.capitalize(), self.exit_list, self.trash_list)
            except AssertionError as e:
                log.bprint(f"The tool is not able to rename the '{file_type}' files. The correct syntax to rename all files of a specific type is:\n'>> rename <file_type>'\nwhere file_type can take the values:\nvideos, \n", 2)

    def process_unsort(self):
        """
        When the 'unsort' command is read.
        """
        log.unsort()

    def process_help(self, split_command, cursor):
        """
        When the 'help' command is read.
        """
        print("")
        if len(split_command) == cursor:
            # i.e. no more arguments to read, just printing command list.
            command_help = (
            "All possible input commands are :\n\n"
            " - change : Changes the current directory. For more information about change, please use 'help change'.\n"
            " - folder : Sorts the current directory files in folders. For more information about folder, please use 'help folder'.\n"
            " - trash : Trashes the useless videos. For more information about trash, please use 'help trash'.\n"
            " - date : Sorts the current directory files in folders by date. For more information about date, pleasse use 'help date'.\n"
            " - rename : Opens and renames the current directory files. For more information about rename, please use 'help rename'.\n"
            " - help : Brings out various help message, including this one.\n"
            " - exit : Leaves this tool. If your are using a keyboard you can also use EOF shortcut (Ctrl + D on Linux for instance).\n\n"
            "The usual way to use the tool is to type the following successive instructions:\n"
            "'>> cd foo'\n"
            "'>> folder'\n"
            "'>> cd Videos'\n"
            "'>> trash 3'\n"
            "'>> rename videos'\n"
            "'>> date'\n"
            "but you can do what you want!\n"
            )
            log.bprint(command_help)
        else:
            topic = split_command[cursor]
            cursor += 1
            if topic in self.exit_list:
                log.bprint("The 'exit' command leaves this tool. If your are using a keyboard you can also use EOF shortcut (Ctrl + D on Linux for instance).")
            elif topic in self.change_list:
                log.bprint("The 'change' command changes the current directory. The syntax to change directory is:\n'>> cd <directory>'")
            elif topic in self.folder_list:
                log.bprint("The 'folder' command sorts the files in the current directory by type. The syntax to use the command is:\n'>> folder'\n\nThe repositories and the extensions they will contain are:")
                for directory in log.EXTENSIONS:
                    print(f"{directory}:".ljust(11, ' ') + str(log.EXTENSIONS[directory]))
                print("If they do not already exist and if a file of a corresponding extension is found in the current directory, these directories will be created and then filled.")
            elif topic in self.trash_list:
                log.bprint("The 'trash' command puts the videos of the current directory that are too short in a 'Trash' directory. The syntax to use the command is,\n'>> trash <time_limit>'\nwhere time_limit is the video length threshold.")
            elif topic in self.date_list:
                log.bprint("The 'date' command sorts the files in the current directory by creation date. The syntax to use the command is:\n'>> date'\nThe repositories will be in the form of 'YYMMDD-Day'.\n")
            elif topic in self.rename_list:
                log.bprint("The 'rename' command opens the files one by one and lets you rename them. The syntax to rename all files of a specific type is:\n'>> rename <file_type>'\nwhere file_type can take the values:\nvideos, \n")
            elif topic in self.help_list:
                log.bprint("Why are you here?")

    def display(self):
        """
        Display a banner.
        """
        header = (
        "\n"
        "##############################################################################\n"
        "  This tool was designed by Théo Dumont and all the source code is available  \n"
        "   at https://github.com/theodumont/video-logging under the GPL 3 License.    \n"
        "##############################################################################\n"
                 )
        os.system('cls')
        print(header)


if __name__ == '__main__':
    os.system('cls')
    cli = CLI()

    cli.display()

    while True:
        try:
            log.bprint("", 3)
            log.bprint(cli.folder, 4)
            command = input(">> ")
            cli.read_command(command)
        except (EOFError, KeyboardInterrupt):
            print("exit")  # In order to avoid ugly output
            cli.exit()
            break
