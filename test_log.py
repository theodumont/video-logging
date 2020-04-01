import pytest
import os
import src.video_logging as log
from json import load
from shutil import rmtree
from pathlib import Path

@pytest.yield_fixture()
def initialize():
    """
    Create a test folder with test files in it
    """

    # creation
    folder_name = 'test_folder'
    print('\nTest files creation...')
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    with open('src/data.json', 'r') as file:
        data = load(file)
    EXTENSIONS = data["EXTENSIONS"]
    os.chdir(folder_name)
    # files
    for directory in EXTENSIONS:
        Path(f"test_{directory.lower()}{EXTENSIONS[directory][0]}").touch()
    # folders
    os.mkdir('Videos')
    os.mkdir('test_folder')

    yield()

    # destruction
    print('\nTest files destruction...')
    os.chdir("..")
    if os.path.isdir(folder_name):
        rmtree(folder_name)


def test_folder(initialize):
    pass
