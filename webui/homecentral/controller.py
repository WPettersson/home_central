"""A base controller class."""

from time import sleep

from homecentral.db import DB
from homecentral.plugins import check_plugin


class Controller:
    """Controls something by checking conditions according to the database.
    """

    def __init__(self, ident):
        self._ident = ident
        self._refresh = None  # Time in seconds between checking conditions
        self._current_mode = None
        self._name = None
        print(f"Starting {self.get_name()}")

    def get_name(self):
        """Get the short name."""
        if not self._name:
            db = DB()
            cursor = db.cursor()
            cursor.execute("SELECT description FROM controllers "
                           "WHERE id = %s", (self._ident,))
            self._name = cursor.fetchone()[0]
        return self._name

    @property
    def poll_time(self):
        if not self._refresh:
            db = DB()
            cursor = db.cursor()
            cursor.execute("SELECT poll_time FROM controllers "
                           "WHERE id = %s", (self._ident,))
            self._refresh = cursor.fetchone()[0]
        return self._refresh

    @property
    def mode(self):
        """Is the controller on or off right now?"""
        return self._current_mode

    @mode.setter
    def mode(self, new_values):
        """Set the mode.
        :param new_values: a (mode, rule) pair where mode is the new mode, and
        rule is the triggering rule for the change"""
        try:
            new_mode, rule = new_values
        except ValueError:
            raise ValueError("Needs a tuple: pass in (mode, rule)")
        if new_mode != self._current_mode:
            self.trigger(new_mode)
            self.log_action(new_mode, rule)
        self._current_mode = new_mode

    def check_rules(self):
        """Go through the rules, and set the mode if necessary
        """
        db = DB()
        cursor = db.cursor()
        cursor.execute("SELECT rule_id FROM rule_map WHERE controller_id = %s "
                       "ORDER BY priority DESC", (self._ident,))
        for row in cursor.fetchall():
            rule = int(row[0])
            if check_rule(rule):
                cursor = db.cursor()  # Refresh cursor
                cursor.execute("SELECT output FROM rules WHERE id = %s",
                               (rule,))
                self.mode = (cursor.fetchone()[0], rule)
                return

    def log_action(self, action, rule):
        """Log any action being taken.
        """
        db = DB()
        cursor = db.cursor()
        cursor.execute("INSERT INTO log (relay_id, rule_id, action) "
                       "VALUES (%s, %s, %s)", (self._ident, rule, action))
        db.commit()

    def trigger(self, switch_on):
        """If switch_on is True, switch the thing on, else switch it off.
        """
        raise Exception("Not implemented")

    def run(self):
        """Run the controller."""
        while True:
            self.check_rules()
            sleep(self.poll_time)


def check_rule(rule_id):
    """Check a given rule, and see if it is activated.
    :return: (fired, controller_status) where fired is True if the rule fired,
    False otherwise, and controller_status is True if the controller is to be
    turned on, False otherwise.
    """
    db = DB()
    cursor = db.cursor()
    cursor.execute("SELECT condition_id FROM condition_map "
                   "WHERE rule_id = %s "
                   "ORDER BY priority DESC", (rule_id,))
    for row in cursor.fetchall():
        condition = int(row[0])
        # If condition fails, bail out
        if not check_condition(condition):
            return False
    # We didn't bail, so everything happened
    return True


def check_condition(condition_id):
    """Check a given condition, returning either True or False.
    """
    db = DB()
    cursor = db.cursor()
    cursor.execute("SELECT plugin, options FROM conditions "
                   "WHERE id = %s", (condition_id,))
    row = cursor.fetchone()
    plugin_name = row[0]
    options = row[1]
    return check_plugin(plugin_name, options)
