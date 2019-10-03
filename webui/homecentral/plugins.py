"""Manage all the plugins."""


import os
import sys


PLUGINS = {}
"""All plugins are stored here as a name->function pointer pair.
"""


class Plugin():
    """A base plugin class."""
    _plugins = {}
    _loaded = False

    def register(self, name):
        """Register the plugin."""
        # Note that this will be called by subclasses (hopefully) so this does
        # make sense.
        Plugin._plugins[name] = self

    def check(self, options):
        """Check a plugin."""
        raise Exception("Not an actual plugin.")


def check_plugin(name, options):
    """Check a plugin based on its name.
    """
    if not Plugin._loaded:
        load_plugins()
    if name not in Plugin._plugins:
        raise Exception(f"Could not find {name} in plugins")
    return Plugin._plugins[name].check(**options)


def load_plugins():
    """Load all plugins."""
    if Plugin._loaded:
        return
    plugin_dir = (os.path.dirname(os.path.realpath(__file__)))
    plugin_files = [x[:-3] for x in os.listdir(plugin_dir)
                    if x.endswith(".py")]
    sys.path.insert(0, plugin_dir)
    for plugin in plugin_files:
        __import__(plugin)
    for plugin_class in Plugin.__subclasses__():
        if hasattr(plugin_class, "plugin_name"):
            plugin = plugin_class()
            plugin.register(plugin.plugin_name)
    Plugin._loaded = True
