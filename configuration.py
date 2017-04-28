import logging

__author__ = 'zmiller'

# Rabbit MQ Configuration
id = "6ec32790"
rmq_host = "lawncron.com"

# Cron configuration
python = "/usr/bin/python"
driver = "/home/zmiller/PycharmProjects/LawnCronPi/valve_driver.py"

pid_files = "/tmp/lcpids"

log_file="log"
log_level = logging.INFO

cleanup_frequency = 60.0  # in seconds