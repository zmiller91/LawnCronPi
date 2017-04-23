__author__ = 'zmiller'
from crontab import CronTab
import configuration as conf

# Global cron file
cron_file = CronTab(tabfile="/etc/cron.d/lawn")

def add(id, zone, duration, time, days):

    # Format input
    mins = int(duration['hours']) * 60 + int(duration['minutes'])

    # Create the cron
    job = cron_file.new(comment=id, command="root {0} {1} {2} {3}".format(conf.python, conf.driver, zone, mins))
    job.hour.on(time["hours"])
    job.minute.on(time["minutes"])
    job.dow.on(days[0])
    if len(days) > 1:
        for d in range(1, len(days)):
            job.dow.also.on(days[d])

    # Write to cron file
    cron_file.write()

    if conf.debug:
        pretty_time = str(time['hours']) + ":" + str(time['minutes'])
        print "Adding schedule {0} in zone {1} for {2} minutes starting at {3} on {4}"\
            .format(str(id), str(zone), str(mins), pretty_time, ", ".join(days))


def delete(id):

    cron_file.remove_all(comment=id)
    cron_file.write()

    if conf.debug:
        print "Removing schedule " + id


def update(id, zone, duration, time, days):
    delete(id)
    add(id, zone, duration, time, days)


def play(id, zone, duration):

    if conf.debug:
        duration_in_mins = int(duration['hours']) * 60 + int(duration['minutes'])
        print "Playing schedule {0} in zone {1} for {2} minutes"\
            .format(str(id), str(zone), str(duration_in_mins))


def stop(id):

    if conf.debug:
        print "Stopping schedule " + id
