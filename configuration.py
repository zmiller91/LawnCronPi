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

# GPIO configuration
gpio_zone_map = {
    1: 31,
    2: 33,
    3: 35,
    4: 37
}

cleanup_frequency = 60.0  # in seconds