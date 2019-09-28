"""A relay controller class."""


import RPi.GPIO as GPIO

from homecentral.controller import Controller


class PiRelayController(Controller):
    """Controls a relay
    """
    def __init__(self, ident, pin):
        super().__init__(ident)
        self._pin = pin
        # Don't keep warning about mode if it's already set
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._pin, GPIO.OUT)

    def trigger(self, switch_on):
        """If switch_on is True, switch the thing on, else switch it off.
        """
        if switch_on:
            GPIO.output(self._pin, 0)
        else:
            GPIO.output(self._pin, 1)
