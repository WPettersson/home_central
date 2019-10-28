"""Check whether IP address can be pinged"""


from subprocess import run, DEVNULL

from homecentral.plugins import Plugin


class Ping(Plugin):
    """A plugin to check whether an IP address can be pinged."""
    plugin_name = 'ping'

    def check(self, host):
        """Check if the host can be pinged
        """
        return_obj = run(["ping", "-c", "1", host], stdout=DEVNULL,
                         stderr=DEVNULL) == 0
        return return_obj.returncode == 0
