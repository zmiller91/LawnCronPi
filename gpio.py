# import RPi.GPIO as GPIO
import logger

GPIOLOG = "gpio.py"
# GPIO.setmode(GPIO.BOARD)

def get_pin(schedule_id):
    return 7

def setup(zone):
    pin = get_pin(zone)
    # GPIO.setup(pin, GPIO.OUT)
    # GPIO.output(pin, True)
    logger.info(GPIOLOG, "Setting up pin {0}".format(str(pin)))


def output(pin, state):
    # GPIO.output(pin, state)
    logger.debug(GPIOLOG, "Outputting pin {0}".format(str(pin)))


def on(zone):
    pin = get_pin(zone)
    output(pin, True)
    logger.info(GPIOLOG, "Turning on pin {0}".format(str(pin)))


def off(zone):
    pin = get_pin(zone)
    output(pin, False)
    logger.info(GPIOLOG, "Turning off pin {0}".format(str(pin)))
