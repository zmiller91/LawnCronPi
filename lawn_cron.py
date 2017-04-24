__author__ = 'zmiller'

import pika
import configuration
import json
import schedule
from datetime import datetime
import logger
import sys

#TODO: clean up pids
LAWN_CRON = "lawn_cron.py"


def parseRequest(request):

    try:
        return json.loads(request)

    except ValueError:
        return False

def callback(ch, method, properties, body):
    logger.log(LAWN_CRON, "Received: " + body)
    request = parseRequest(body)
    if request is not False:

        action = request['method']
        id = request["id"] if "id" in request else ""
        zone = request["zone"] if "zone" in request else ""
        duration = request["duration"] if "duration" in request else {}
        time = request["time"] if "time" in request else {}
        days = request["days"] if "days" in request else []

        if action == 'add':
            logger.log(LAWN_CRON, "Adding :" + body)
            schedule.add(id, zone, duration, time, days)

        elif action == "delete":
            logger.log(LAWN_CRON, "Deleting: " + body)
            schedule.delete(id)

        elif action == "play":
            logger.log(LAWN_CRON, "Playing: " + body)
            # execute command and don't block
            schedule.play(id, zone, duration)

        elif action == "stop":
            logger.log(LAWN_CRON, "Stopping: " + body)
            message = json.dumps({'action': 'stop', 'ts': str(datetime.now())})

            logger.log(LAWN_CRON, "Sending: " + message + "To: " + zone)
            local_connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
            schedule_channel = local_connection.channel()
            schedule_channel.queue_declare(queue=zone)
            schedule_channel.basic_publish(exchange='', routing_key=zone, body=message)
            local_connection.close()

        elif action == "update":
            logger.log(LAWN_CRON, "Updating: " + body)
            schedule.update(id, zone, duration, time, days)

while True:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=configuration.rmq_host))
        logger.log(LAWN_CRON, "Connected to " + configuration.rmq_host)

        channel = connection.channel()
        logger.log(LAWN_CRON, "Created channel")

        channel.queue_declare(queue=configuration.id)
        logger.log(LAWN_CRON, "Declaring queue: " + configuration.id)

        channel.basic_consume(callback, queue=configuration.id, no_ack=True)
        logger.log(LAWN_CRON, "Consuming queue: " + configuration.id)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

    except Exception:
        logger.log(LAWN_CRON, "Exception raised.")
        logger.log(LAWN_CRON, sys.exc_info()[0])
        continue;
