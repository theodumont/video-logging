import pytest
import os
import src.video_logging as log
from json import load
from shutil import rmtree
from pathlib import Path


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
        file_name = f"test_{directory.lower()}{EXTENSIONS[directory][0]}"
        if not os.path.isfile(file_name):
            Path(file_name).touch()
    # folders
    os.mkdir('Videos')
    os.mkdir('test_folder')

    yield()

    # destruction
    print('\nTest files destruction...')
    os.chdir("..")
    if os.path.isdir('test_foo'):
        rmtree('test_foo')


@pytest.fixture()
def EXTENSIONS():
    os.chdir("..")
    with open('src/data.json', 'r') as file:
        data = load(file)
    os.chdir('test_foo')
    return data["EXTENSIONS"]


def test_folder(initialize, EXTENSIONS):
    log.folder_sort()
    for directory in os.listdir():
        assert os.path.isdir(directory)  # only folders
        assert directory in EXTENSIONS  # script folders
        for file in os.listdir(directory):
            if os.path.isdir(os.path.join(directory, file)):  # is a folder
                assert directory == 'Folders'  # folders only in 'Folders'
                assert file not in EXTENSIONS  # script folders not here
            else:  # is not a folder
                name, extension = os.path.splitext(file)
                assert extension in EXTENSIONS[directory]  # right folder
