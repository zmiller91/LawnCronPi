__author__ = 'zmiller'
from crontab import CronTab
import configuration as conf
import logger

SCHEDULE = "schedule.py"

# TODO: Specifying this as a global means the service will have to be restarted if the cron file changes. This library
# TODO: holds the cronfile in memory, so if you delete one manually then the next time this library adds one, it'll
# TODO: undo your manual delete. Figure out if this if good behavior or not.
# Global cron file
cron_file = CronTab(tabfile="/etc/cron.d/lawn")

def add(id, zone, duration, time, days):

    # Format input
    duration_in_secs = (int(duration['hours']) * 60 + int(duration['minutes'])) * 60

    # Create the cron
    job = cron_file.new(comment=id, command="root {0} {1} {2} {3}".format(conf.python, conf.driver, zone, duration_in_secs))
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
    logger.info(SCHEDULE, "Adding schedule {0} in zone {1} for {2} minutes starting at {3} on {4}"\
        .format(str(id), str(zone), str(duration_in_secs), pretty_time, ", ".join(days)))


def delete(id):

    cron_file.remove_all(comment=id)
    cron_file.write()
    logger.info(SCHEDULE, "Removing schedule " + id)


def update(id, zone, duration, time, days):

    delete(id)
    add(id, zone, duration, time, days)
