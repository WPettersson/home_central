"""A plugin to check the temperature in a zone"""


from homecentral.db import get_temp
from homecentral.plugins import Plugin


class Temperature(Plugin):
    """A plugin to check the temperature in a zone."""
    plugin_name = 'temp'

    def check(self, comparison, value, zone, second_value=None):
        """Check the temperature in zone "zone" against "value"
        comparison is one of "LE", "E", "NE", or "GE", standing for:
        LE - less than or equal to, earlier than
        E - equal to
        NE - not equal to
        GE - greater than or equal to, later than
        IN - between two values
        OUT - not between two values
        """
        # We store temperature as milli-celsius in the database
        temp = get_temp(zone) / 1000
        value = float(value)
        if comparison == "LE":
            return temp <= value
        elif comparison == "E":
            return temp == value
        elif comparison == "GE":
            return temp >= value
        elif comparison == "IN":
            return temp >= value and temp <= second_value
        elif comparison == "OUT":
            return temp <= value or temp >= second_value
