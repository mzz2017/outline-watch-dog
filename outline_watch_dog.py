import os
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def add_read_privilege(path):
    result = os.stat(path)
    mode = result.st_mode
    rr = 0o0004
    if mode & rr != rr:
        os.chmod(path, mode | rr)


def add_read_privilege_recursive(path):
    add_read_privilege(path)
    for root, dirs, files in os.walk(path, True):
        for name in files + dirs:
            add_read_privilege(os.path.join(root, name))


class Handler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()

    def on_created(self, event):
        super().on_created(event)
        add_read_privilege(event.src_path)

    def on_modified(self, event):
        super().on_modified(event)
        add_read_privilege(event.src_path)


def main():
    path = '/opt/outline'
    add_read_privilege_recursive(path)

    observer = Observer()
    handler = Handler()
    observer.schedule(handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1000)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == '__main__':
    main()
