import os
import sys
import pika
import json
import signal
from threading import Timer
from datetime import datetime
import RPi.GPIO as GPIO

pin = 7

schedule_id = sys.argv[1]
duration = sys.argv[2]
start_time = datetime.now()
pid_root = "/tmp/"


def get_pid(pid_file):
    f = open(pid_root + pid_file, 'r')
    pid = f.read()
    f.close()
    return int(pid)


def status_file_exists(name):
    return os.path.isfile(pid_root + name)


def create_status_file(name):
    status_file = open(pid_root + str(name), "w")
    status_file.write(str(os.getpid()))
    status_file.close()


def delete_status_file(name):
    if status_file_exists(name):
        os.remove(pid_root + name)


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
    message = parse_message(body)
    if message is not False and message['ts'] > start_time and message['action'] == "stop":
	GPIO.output(pin, False)
        pid = get_pid(schedule_id)
        delete_status_file(schedule_id)
        os.kill(pid, signal.SIGTERM)


# Check if schedule is running in another thread
if status_file_exists(schedule_id):
    sys.exit(0)

# Write file indicating this schedule is running
create_status_file(schedule_id)

# Setup GPIO Output
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)
GPIO.output(7, True)

# Establish local RMQ connection and listen schedule_id channel
connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()
channel.queue_declare(queue=schedule_id)
channel.basic_consume(rmq_listener, queue=schedule_id, no_ack=True)

# Set the shutdown timer and start consuming
timer = Timer(float(duration), shutdown, [channel, schedule_id]).start()
channel.start_consuming()
