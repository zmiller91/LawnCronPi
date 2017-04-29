from datetime import datetime
import logging
import configuration
import os
import errno

logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("pika").setLevel(logging.ERROR)
logging.basicConfig(filename=configuration.log_file, level=configuration.log_level)


def create_dirs():
    dir = os.path.dirname(configuration.log_file)
    try:
        os.makedirs(dir)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(dir):
            pass
        else:
            raise


def get_log_line(identifier, message):
    return "{0}\t{1}\t{2}".format(str(datetime.now()), identifier, message)


def debug(identifier, message):
    logging.debug(get_log_line(identifier, message))


def info(identifier, message):
    logging.info(get_log_line(identifier, message))


def warn(identifier, message):
    logging.warning(get_log_line(identifier, message))


def error(identifier, message):
    logging.error(get_log_line(identifier, message))

create_dirs()