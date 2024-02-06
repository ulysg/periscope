from gi.repository import Adw
from gi.repository import Gtk

from .song_grid import SongGrid
from .async_loop import loop

@Gtk.Template(resource_path = "/ch/ulys/Periscope/view/window.ui")
class Window(Adw.ApplicationWindow):
    __gtype_name__ = "Window"

    song_grid = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        loop.submit_async(self.song_grid.show_playlist("d528c0c3-72c2-4769-97e3-318c9b797366"))
