"""A plugin to compare date/times to current."""

from datetime import datetime

from homecentral.plugins import Plugin


DATETIME_FMT = "%d %m %Y %H:%M"
DATE_FMT = "%d %m %Y"
TIME_FMT = "%H:%M"


class DateTimePlugin(Plugin):
    def check(self, comparison, value, value_type, second_value=None):
        """Check the date/time currently against the database.
        comparison is one of "LE", "E", "NE", or "GE", standing for:
        LE - less than or equal to, earlier than
        E - equal to
        NE - not equal to
        GE - greater than or equal to, later than
        IN - between two values
        OUT - not between two values

        value is the date or time to compare. It's exact format is specified by
        value_type, which is one of:
        DATETIME
        WEEKDAY
        DATE
        TIME
        """
        now = datetime.now()
        if value_type == "WEEKDAY":
            if comparison not in ["NE", "E", "WEEKDAY", "WEEKEND"]:
                raise Exception(f"Comparison {comparison} "
                                "not valid for WEEKDAY")
            if comparison == "E":
                return now.weekday() == value
            elif comparison == "NE":
                return now.weekday() != value
            elif comparison == "WEEKDAY":
                return now.weekday() < 5  # ISO counts from 0
            else:
                return now.weekday() > 4  # so Sat,Sun are 5,6
        if value_type == "DATE":
            dt = datetime.strptime(value, DATE_FMT)
            dt = dt.date()
            now = now.date()
        elif value_type == "TIME":
            dt = datetime.strptime(value, TIME_FMT)
            dt = dt.time()
            now = now.time()
        else:
            dt = datetime.strptime(value, DATETIME_FMT)
        if comparison == "LE":
            return now <= dt
        elif comparison == "E":
            return now == dt
        elif comparison == "GE":
            return now >= dt
        # At this point, we're doing either IN or OUT, so read second time
        # format
        if value_type == "DATE":
            second = datetime.strptime(second_value, DATE_FMT)
            second = second.date()
        elif value_type == "TIME":
            second = datetime.strptime(second_value, TIME_FMT)
            second = second.time()
        else:
            second = datetime.strptime(second_value, DATETIME_FMT)
        if comparison == "IN":
            return now >= dt and now <= second
        elif comparison == "OUT":
            return now <= dt or now >= second
