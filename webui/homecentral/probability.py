"""A plugin allowing probabilities in rules"""

from random import random

from homecentral.db import get_temp
from homecentral.plugins import Plugin


class Probability(Plugin):
    """A plugin allowing probabilities in rules"""
    plugin_name = 'prob'

    def check(self, value):
        """Randomly (with value probability) return true
        """
        return random() <= value
