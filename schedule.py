from crontab import CronTab
import configuration as conf
import logger
from datetime import datetime
import json
import pika
import subprocess

SCHEDULE = "schedule.py"

# TODO: Specifying this as a global means the service will have to be restarted if the cron file changes. This library
# TODO: holds the cronfile in memory, so if you delete one manually then the next time this library adds one, it'll
# TODO: undo your manual delete. Figure out if this if good behavior or not.
# Global cron file
cron_file = CronTab(tabfile="/etc/cron.d/lawn")


def get_driver_command(schedule_id, zone, duration):

    duration_in_secs = (int(duration['hours']) * 60 + int(duration['minutes'])) * 60
    return "{0} {1} {2} {3} {4}".format(conf.python, conf.driver, schedule_id, zone, duration_in_secs)


def add(schedule_id, zone, duration, time, days):

    # Create the cron
    job = cron_file.new(comment=schedule_id, command="root " + get_driver_command(schedule_id, zone, duration))

    job.hour.on(time["hours"])
    job.minute.on(time["minutes"])
    job.dow.on(days[0])
    if len(days) > 1:
        for d in range(1, len(days)):
            job.dow.also.on(days[d])

    # Write to cron file
    cron_file.write()

    # Log
    pretty_time = str(time['hours']) + ":" + str(time['minutes'])
    logger.info(SCHEDULE, "Adding schedule {0} in zone {1} for {2} minutes starting at {3} on {4}" \
                .format(str(schedule_id), str(zone), str(duration), pretty_time, ", ".join(days)))


def delete(schedule_id):

    cron_file.remove_all(comment=schedule_id)
    cron_file.write()
    logger.info(SCHEDULE, "Removing schedule " + schedule_id)


def update(schedule_id, zone, duration, time, days):

    delete(schedule_id)
    add(schedule_id, zone, duration, time, days)


def play(schedule_id, zone, duration):

    logger.info(SCHEDULE, "Playing schedule " + schedule_id)
    cmd = get_driver_command(schedule_id, zone, duration)
    subprocess.Popen(cmd.split(" "))


def stop(schedule_id):

    logger.info(SCHEDULE, "Stopping schedule " + schedule_id)
    message = json.dumps({'action': 'stop', 'ts': str(datetime.now())})

    logger.debug(SCHEDULE, "Sending: " + message + "To: " + schedule_id)
    local_connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    schedule_channel = local_connection.channel()
    schedule_channel.queue_declare(queue=schedule_id)
    schedule_channel.basic_publish(exchange='', routing_key=schedule_id, body=message)
    local_connection.close()


def refresh(schedules):

    logger.info(SCHEDULE, "Refreshing cron file")
    cron_file.remove_all()
    cron_file.write()
    for schedule in schedules:
        add(schedule["id"], schedule['zone'], schedule['duration'], schedule['time'], schedule['days'])


