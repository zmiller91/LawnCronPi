import RPi.GPIO as GPIO
import logger
import configuration

GPIOLOG = "gpio.py"
GPIO.setmode(GPIO.BOARD)


def get_pin(zone):

    pin = configuration.gpio_zone_map['4']
    if str(zone) not in configuration.gpio_zone_map:
        logger.warn(GPIOLOG, "Zone {0} was not found, returning pin {1}".format(str(zone), str(pin)))
        return pin

    pin = configuration.gpio_zone_map[zone]
    logger.info(GPIOLOG, "Returning pin {0} for zone {1}".format(str(pin), str(zone)))
    return pin

def setup(zone):
    pin = get_pin(zone)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, True)
    logger.info(GPIOLOG, "Setting up pin {0}".format(str(pin)))


def output(pin, state):
    GPIO.output(pin, state)
    logger.debug(GPIOLOG, "Outputting pin {0}".format(str(pin)))


def on(zone):
    pin = get_pin(zone)
    output(pin, True)
    logger.info(GPIOLOG, "Turning on pin {0}".format(str(pin)))


def off(zone):
    pin = get_pin(zone)
    output(pin, False)
    logger.info(GPIOLOG, "Turning off pin {0}".format(str(pin)))