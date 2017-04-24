__author__ = 'zmiller'

import pika
import configuration
import json
import schedule
from datetime import datetime
import logger
import sys

#TODO: clean up pids

def parseRequest(request):

    try:
        return json.loads(request)

    except ValueError:
        return False


def log(message):
    status_file = open("/tmp/lawn-cron-log", "w")
    status_file.write(message)
    status_file.close()

def callback(ch, method, properties, body):
    logger.log(body)
    request = parseRequest(body)
    if request != False:

        action = request['method']
        id = request["id"] if "id" in request else ""
        zone = request["zone"] if "zone" in request else ""
        duration = request["duration"] if "duration" in request else {}
        time = request["time"] if "time" in request else {}
        days = request["days"] if "days" in request else []

        if action == 'add':
            logger.log("adding...")
            schedule.add(id, zone, duration, time, days)

        elif action == "delete":
            logger.log("deleting...")
            schedule.delete(id)

        elif action == "play":
            logger.log("playing...")
            # execute command and don't block
            schedule.play(id, zone, duration)

        elif action == "stop":
            logger.log("stopping...")
            message = json.dumps({'action': 'stop', 'ts': str(datetime.now())})

            logger.log("sending: " + message)
            local_connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
            schedule_channel = local_connection.channel()
            schedule_channel.queue_declare(queue=zone)
            schedule_channel.basic_publish(exchange='', routing_key=zone, body=message)
            log(message)
            local_connection.close()

        elif action == "update":
            schedule.update(id, zone, duration, time, days)

while True:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=configuration.rmq_host))
        channel = connection.channel()
        channel.queue_declare(queue=configuration.id)
        channel.basic_consume(callback, queue=configuration.id, no_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except Exception:
        logger.log(sys.exc_info()[0])
        continue;
