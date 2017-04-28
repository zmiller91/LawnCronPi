from datetime import datetime
import logging
import configuration

logging.getLogger("pika").propagate = False
logging.basicConfig(filename=configuration.log_file, level=configuration.log_level)


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
