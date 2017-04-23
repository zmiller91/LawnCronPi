__author__ = 'zmiller'

def add(id, zone, duration, time, days):
    durationInMinutes = int(duration['hours']) * 60 + int(duration['minutes'])
    dayCSV = ", ".join(days)
    prettyTime = str(time['hours']) + ":" + str(time['minutes'])
    print "Adding schedule {0} in zone {1} for {2} minutes starting at {3} on {4}".format(str(id), str(zone), str(durationInMinutes), prettyTime, dayCSV)

def play(id, zone, duration):
    durationInMinutes = int(duration['hours']) * 60 + int(duration['minutes'])
    print "Playing schedule {0} in zone {1} for {2} minutes".format(str(id), str(zone), str(durationInMinutes))

def stop(id):
    print "Stopping schedule " + id

def update(id, zone, duration, time, days):
    delete(id)
    add(id, zone, duration, time, days)

def delete(id):
    print "Removing schedule " + id