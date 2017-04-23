__author__ = 'zmiller'

import pika
import configuration
import json
import schedule

def parseRequest(request):

    try:
        return json.loads(request)

    except ValueError:
        return False

def callback(ch, method, properties, body):

    request = parseRequest(body)
    if request != False:

        action = request['method']
        id = request["id"] if "id" in request else ""
        zone = request["zone"] if "zone" in request else ""
        duration = request["duration"] if "duration" in request else {}
        time = request["time"] if "time" in request else {}
        days = request["days"] if "days" in request else []

        if action == 'add':
            schedule.add(id, zone, duration, time, days)

        elif action == "delete":
            schedule.delete(id)

        elif action == "play":
            schedule.play(id, zone, duration)

        elif action == "stop":
            schedule.stop(id)

        elif action == "update":
            schedule.update(id, zone, duration, time, days)

connection = pika.BlockingConnection(pika.ConnectionParameters(host=configuration.rmq_host))
channel = connection.channel()
channel.queue_declare(queue=configuration.id)
channel.basic_consume(callback, queue=configuration.id, no_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()