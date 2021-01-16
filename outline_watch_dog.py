import os
import pyinotify


def change_permissions(path):
    result = os.stat(path)
    mode = result.st_mode
    if mode & os.stat.S_IROTH != os.stat.S_IROTH:
        os.chmod(path, mode | os.stat.S_IROTH)
    if os.path.isdir(path) and mode & os.stat.S_IXOTH != os.stat.S_IXOTH:
        os.chmod(path, mode | os.stat.S_IXOTH)


def change_permissions_recursive(path):
    change_permissions(path)
    for root, dirs, files in os.walk(path, True):
        for name in files + dirs:
            change_permissions(os.path.join(root, name))


class EventHandler(pyinotify.ProcessEvent):
    def process_IN_ATTRIB(self, event):
        change_permissions(event.pathname)

    def process_IN_CREATE(self, event):
        change_permissions(event.pathname)


def main():
    path = '/opt/outline'
    change_permissions_recursive(path)

    wm = pyinotify.WatchManager()
    mask = pyinotify.IN_ATTRIB | pyinotify.IN_CREATE
    wm.add_watch(path, mask, rec=True)
    handler = EventHandler()
    notifier = pyinotify.Notifier(wm, handler)
    notifier.loop()


if __name__ == '__main__':
    main()
