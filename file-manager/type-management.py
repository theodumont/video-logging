# encoding: utf-8

import os


DIRS = ['Audio', 'Videos', 'Images', 'Documents', 'Folders', 'Other']
EXT_AUDIO = ['.wav', '.mp3', '.raw', '.wma']
EXT_VIDEO = ['.mp4', '.m4a', '.m4v', '.f4v', '.f4a', '.f4b', '.m4b', '.m4r', '.avi', '.wmv', '.flv']
EXT_IMAGE = ['.jpeg', '.jpg', '.png', '.svg', '.bmp', '.gif']
EXT_DOCUMENT = ['.txt', '.pdf', '.doc', '.docx', '.odt', '.html', '.md', '.rtf', '.xlsx', '.pptx']
EXT_FOLDER = ['.rar']


# folder we want to sort
folder_to_sort = 'foo'
os.chdir(folder_to_sort)


if __name__ == '__main__':
    print('** Cleanup of the {} folder **\n'.format(folder_to_sort).upper())

    # Create directories if they don't exist
    if not os.path.isdir('Audio'):
        for d in DIRS:
            os.mkdir('./{}'.format(d))
        print('Directories successfully created.')

    for file in os.listdir():
        name, extension = os.path.splitext(file)

        if extension in EXT_AUDIO:
            print('Audio: {}{}'.format(name, extension))
            os.rename(file, 'Audio/' + file)
        elif extension in EXT_VIDEO:
            print('Video: {}{}'.format(name, extension))
            os.rename(file, 'Videos/' + file)
        elif extension in EXT_IMAGE:
            print('Image: {}{}'.format(name, extension))
            os.rename(file, 'Images/' + file)
        elif extension in EXT_DOCUMENT:
            print('Document: {}{}'.format(name, extension))
            os.rename(file, 'Documents/' + file)
        else:
            if os.path.isdir(name) or extension in EXT_FOLDER:
                if name not in DIRS:
                    print('Folder: {}'.format(name))
                    os.rename(file, 'Folders/' + file)
            else:
                print('Some other file: {}'.format(name, extension))
                os.rename(file, 'Other/' + file)
