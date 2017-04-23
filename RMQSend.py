__author__ = 'zmiller'

import pika
import sys
import configuration

rpi = sys.argv[1]
message = sys.argv[2]

connection = pika.BlockingConnection(pika.ConnectionParameters(configuration.rmq_host))
channel = connection.channel()
channel.queue_declare(queue=rpi)
channel.basic_publish(exchange='',
                      routing_key=rpi,
                      body = message)


print 'Sent: ' + message + " To: " + rpi

f = open('log', 'w');
f.write('Sent: ' + message + " To: " + rpi)
f.close()
connection.close()