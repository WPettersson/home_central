"""A relay controller class."""


from os import environ
import RPi.GPIO as GPIO

from homecentral.controller import Controller

PIN = 2
if "HC_RELAY_PIN" in environ:
    PIN = environ["HC_RELAY_PIN"]


class PiRelayController(Controller):
    """Controls a relay
    """
    def __init__(self, ident):
        super().__init__(ident)
        # Don't keep warning about mode if it's already set
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN, GPIO.OUT)

    def trigger(self, switch_on):
        """If switch_on is True, switch the thing on, else switch it off.
        """
        if switch_on:
            GPIO.output(PIN, 0)
        else:
            GPIO.output(PIN, 1)
