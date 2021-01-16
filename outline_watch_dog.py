import os
import pyinotify


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


class EventHandler(pyinotify.ProcessEvent):
    def process_IN_ATTRIB(self, event):
        add_read_privilege(event.pathname)

    def process_IN_CREATE(self, event):
        add_read_privilege(event.pathname)


def main():
    path = '/opt/outline'
    add_read_privilege_recursive(path)

    wm = pyinotify.WatchManager()
    mask = pyinotify.IN_ATTRIB | pyinotify.IN_CREATE
    wdd = wm.add_watch(path, mask, rec=True)
    handler = EventHandler()
    notifier = pyinotify.Notifier(wm, handler)
    notifier.loop()


if __name__ == '__main__':
    main()
