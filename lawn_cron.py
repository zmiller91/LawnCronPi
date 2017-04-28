import time
import pika
import configuration
import json
import schedule
from threading import Timer
from datetime import datetime, timedelta
import logger
import sys
import os
import pids
import gpio
from multiprocessing.dummy import Pool
import requests

LAWN_CRON = "lawn_cron.py"
network_pool = Pool(10)


def parse_request(request):

    try:
        return json.loads(request)

    except ValueError:
        return False


def send_status_notification():
    logger.info(LAWN_CRON, "Posting status")
    network_pool.apply_async(requests.post, ['http://lawncron.com/api/status', {"rpi": configuration.id}])
    Timer(450, send_status_notification).start()


def cleanup_pids():
    for name in os.listdir(configuration.pid_files):
        pid_file = pids.create_pid_file_path(name)
        pid_contents = pids.read_pid_file(pid_file)
        if pid_contents is not False:
            end = datetime.strptime(pid_contents["end"], '%Y-%m-%d %H:%M:%S.%f')
            if end < datetime.now() + timedelta(minutes=1):
                gpio.setup(pid_contents["zone"])
                gpio.off(pid_contents["zone"])
                pids.kill(int(pid_contents["pid"]))
                pids.delete_status_file(pid_file)
                logger.info(LAWN_CRON, "Cleaned up pid {0}".format(pid_contents["pid"]))

    Timer(configuration.cleanup_frequency, cleanup_pids).start()


def callback(ch, method, properties, body):
    logger.debug(LAWN_CRON, "Received: " + body)
    request = parse_request(body)
    if request is not False:

        action = str(request['method'])
        schedule_id = str(request["id"]) if "id" in request else ""
        zone = str(request["zone"]) if "zone" in request else ""
        duration = request["duration"] if "duration" in request else {}
        start_time = request["time"] if "time" in request else {}
        days = request["days"] if "days" in request else []

        if action == 'add':
            logger.debug(LAWN_CRON, "Adding :" + body)
            schedule.add(schedule_id, zone, duration, start_time, days)

        elif action == "delete":
            logger.debug(LAWN_CRON, "Deleting: " + body)
            schedule.delete(schedule_id)

        elif action == "play":
            logger.debug(LAWN_CRON, "Playing: " + body)
            schedule.play(schedule_id, zone, duration)

        elif action == "stop":
            logger.debug(LAWN_CRON, "Stopping :" + body)
            schedule.stop(schedule_id)

        elif action == "update":
            logger.debug(LAWN_CRON, "Updating: " + body)
            schedule.update(schedule_id, zone, duration, start_time, days)

last_error_report = None
Timer(configuration.cleanup_frequency, cleanup_pids).start()
Timer(450, send_status_notification).start()
while True:
    try:

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=configuration.rmq_host))
        logger.info(LAWN_CRON, "Connected to " + configuration.rmq_host)

        channel = connection.channel()
        logger.info(LAWN_CRON, "Created channel")

        channel.queue_declare(queue=configuration.id)
        logger.info(LAWN_CRON, "Declaring queue: " + configuration.id)

        channel.basic_consume(callback, queue=configuration.id, no_ack=True)
        logger.info(LAWN_CRON, "Consuming queue: " + configuration.id)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

    except Exception as e:

        if last_error_report is None or (datetime.now() - last_error_report) > timedelta(minutes=20):
            print e
            logger.warn(LAWN_CRON, "Exception raised.")
            logger.warn(LAWN_CRON, e.message)
            last_error_report = datetime.now()

        else:
            logger.debug(LAWN_CRON, "Exception raised.")
            logger.debug(LAWN_CRON, sys.exc_info()[0])

        time.sleep(15000)
        continue
