"""Check whether IP address can be pinged"""


from subprocess import call

from homecentral.plugins import Plugin


class Ping(Plugin):
    """A plugin to check whether an IP address can be pinged."""
    plugin_name = 'ping'

    def check(self, host):
        """Check if the host can be pinged
        """
        return call(["ping", "-c", "1", host]) == 0
