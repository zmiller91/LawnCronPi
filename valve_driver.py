import sys
import pika
import json
from threading import Timer
from datetime import datetime, timedelta
import logger
import gpio
import pids

VALVE_DRIVER = "valve_driver.py"
pin = 7

schedule_id = sys.argv[1]
zone = sys.argv[2]
duration = sys.argv[3]
start_time = datetime.now()


def shutdown(ch, rk):
    message = json.dumps({'action': 'stop', 'ts': str(datetime.now())})
    ch.basic_publish(exchange='', routing_key=rk, body=message)


def parse_message(message):

    try:
        parsed = json.loads(message)
        ts = datetime.strptime(parsed['ts'], '%Y-%m-%d %H:%M:%S.%f')
        parsed['ts'] = ts
        return parsed

    except Exception:
        return False


def rmq_listener(ch, method, properties, body):
    logger.debug(VALVE_DRIVER, "rmq_listener received: " + body)
    message = parse_message(body)
    if message is not False and message['ts'] > start_time and message['action'] == "stop":
        gpio.off(zone)
        pid_file_path = pids.create_pid_file_path(schedule_id)
        pid_file_contents = pids.read_pid_file(pid_file_path)
        pids.delete_status_file(pid_file_path)
        pids.kill(int(pid_file_contents["pid"]))


# PID file
pid_file = pids.create_pid_file_path(schedule_id)

# Check if schedule is running in another thread
if pids.status_file_exists(pid_file):
    logger.info(VALVE_DRIVER, "Schedule {0} already running, exiting".format(schedule_id))
    sys.exit(0)

# Write file indicating this schedule is running
pids.create_status_file(pid_file, zone, datetime.now(), datetime.now() + timedelta(seconds=int(duration)))

# Setup GPIO Output
gpio.setup(zone)
gpio.on(zone)

started = False
last_error_report = None
while True:
    try:

        logger.info(VALVE_DRIVER, "Attempting to establish connection...")
        # Establish local RMQ connection and listen schedule_id channel
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
        logger.info(VALVE_DRIVER, "Connection established with localhost")

        channel = connection.channel()
        logger.info(VALVE_DRIVER, "Created a channel")

        channel.queue_declare(queue=schedule_id)
        logger.info(VALVE_DRIVER, "Declared queue " + schedule_id)

        channel.basic_consume(rmq_listener, queue=schedule_id, no_ack=True)
        logger.info(VALVE_DRIVER, "Consuming queue " + schedule_id)

        # Set the shutdown timer and start consuming
        if not started:
            Timer(float(duration), shutdown, [channel, schedule_id]).start()
            started = True

        channel.start_consuming()

    except Exception:

        if last_error_report is None or (datetime.now() - last_error_report) > timedelta(minutes=20):
            logger.warn(VALVE_DRIVER, "Exception raised.")
            logger.warn(VALVE_DRIVER, sys.exc_info()[0])
            last_error_report = datetime.now()

        else:
            logger.debug(VALVE_DRIVER, "Exception raised.")
            logger.debug(VALVE_DRIVER, sys.exc_info()[0])

        continue
