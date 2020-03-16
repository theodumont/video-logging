# encoding: utf-8

import os
import time
import argparse

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# refresh frequency (seconds)
frequency = 2

parser = argparse.ArgumentParser()
parser.add_argument("init", type=str, default='txt',
                    help="extension to replace ('txt', 'py'...)")
parser.add_argument("end", type=str, default='md',
                    help="replace by this extension ('md', 'txt'...)")
args = parser.parse_args()


class MyHandler(FileSystemEventHandler):

    def on_any_event(self, event):
        for filename in os.listdir("./change-extension"):

            src = "./change-extension/" + filename
            if os.path.splitext(filename)[1] == '.' + args.init:
                os.rename(src, "./change-extension/" +
                          os.path.splitext(filename)[0] + "." + args.end)


if __name__ == '__main__':
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, "./change-extension", recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(frequency)
    except KeyboardInterrupt:
        print("Process stopped.")
        observer.stop()
    observer.join()
