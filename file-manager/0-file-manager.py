# encoding: utf-8

import os
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# relative path to folder to track
path_to_track = "./experiments"
# refresh frequency (seconds)
frequency = 1


class MyHandler(FileSystemEventHandler):

    def on_any_event(self, event):
        pass

    def on_created(self, event):
        print("File {0} has been created.".format(event.src_path))
        pass

    def on_deleted(self, event):
        print("File {0} has been deleted.".format(event.src_path))
        pass

    def on_modified(self, event):
        print("File {0} has been modified.".format(event.src_path))
        pass

    def on_moved(self, event):
        print("File {0} has been moved.".format(event.src_path))
        pass


if __name__ == '__main__':
    name = 'my.file.txt'
    print(os.path.splitext(name)[1])
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path_to_track, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(frequency)
    except KeyboardInterrupt:
        print("Process stopped.")
        observer.stop()
    observer.join()
