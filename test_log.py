import pytest
import os
import src.video_logging as log
from json import load
from shutil import rmtree
from pathlib import Path


# FIXTURES

@pytest.yield_fixture()
def initialize():
    """
    Create a test folder with test files in it, delete it after tests
    """
    # creation
    print('\nTest files creation...')
    if not os.path.isdir('test_foo'):
        os.mkdir('test_foo')
    with open('src/data.json', 'r') as file:
        data = load(file)
    EXTENSIONS = data["EXTENSIONS"]
    os.chdir('test_foo')
    # files
    for directory in EXTENSIONS:
        file_name = f"bar_{directory.lower()}{EXTENSIONS[directory][0]}"
        if not os.path.isfile(file_name):
            Path(file_name).touch()
    # folders
    os.mkdir('Videos')  # folder in scripts
    os.mkdir('bar_folder')  # folder not in scripts

    yield()

    # destruction
    # print('\nTest files destruction...')
    # os.chdir("..")
    # if os.path.isdir('test_foo'):
    #     rmtree('test_foo')


@pytest.fixture()
def sort_the_folder():
    """
    Sort the folder
    """
    log.folder_sort()


@pytest.fixture()
def EXTENSIONS():
    """
    Get the EXTENSION variable from data.json
    """
    os.chdir("..")
    with open('src/data.json', 'r') as file:
        data = load(file)
    os.chdir('test_foo')
    return data["EXTENSIONS"]


# FUNCTIONS TESTS
# Starts in 'test_foo' and has to end in 'test_foo'


def test_folder(initialize, EXTENSIONS):
    """
    Test the folder_sort function
    """
    log.folder_sort()
    for directory in os.listdir():
        assert os.path.isdir(directory)  # only folders
        assert directory in EXTENSIONS  # script folders
        for file in os.listdir(directory):
            # if is a folder
            if os.path.isdir(os.path.join(directory, file)):
                assert directory == 'Folders'  # folders only in 'Folders'
                assert file not in EXTENSIONS  # script folders not here
            # if is not a folder
            else:
                name, extension = os.path.splitext(file)
                assert extension in EXTENSIONS[directory]  # right folder


def WIP_test_trash(initialize, sort_the_folder):
    """
    Test the trash_videos function
    """
    os.chdir('Videos')
    # create videos of different lengths
    lengths = range(1, 5)
    for length in lengths:
        log.trash_videos(length)
        # assertion for each video
    os.chdir('../')


def test_sort_date(initialize, sort_the_folder):
    """
    Test the sort_by_date function
    """
    pass


def test_rename(initialize):
    """
    Test the file_rename function
    """
    pass
