import sys
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("Gst", "1.0")

from gi.repository import Gtk, Gio, Adw
from .window import Window
from .config import config

class PeriscopeApplication(Adw.Application):
    def __init__(self):
        super().__init__(application_id = "ch.ulys.Periscope",
                         flags = Gio.ApplicationFlags.DEFAULT_FLAGS)

    def do_activate(self):
        win = self.props.active_window

        if not win:
            win = Window(application = self)

        win.present()

def main(version):
    app = PeriscopeApplication()
    return app.run(sys.argv)
