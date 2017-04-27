import configuration
import os
import json
import signal


def create_pid_file_path(name):
    return os.path.join(configuration.pid_files, str(name))


def read_pid_file(file_path):

    if not status_file_exists(file_path):
        return False

    f = open(file_path, 'r')
    contents = f.read()
    f.close()
    return json.loads(contents)


def status_file_exists(file_path):
    return os.path.isfile(file_path)


def create_status_file(file_path, schedule_zone, start, end):

    contents = {
        "pid": str(os.getpid()),
        "zone": schedule_zone,
        "start": str(start),
        "end": str(end)
    }

    status_file = open(file_path, "w")
    status_file.write(json.dumps(contents))
    status_file.close()


def delete_status_file(file_path):
    if status_file_exists(file_path):
        os.remove(file_path)


def kill(pid):
    os.kill(int(pid), signal.SIGTERM)
