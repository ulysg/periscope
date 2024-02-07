from gi.repository import Adw
from gi.repository import Gtk

from .song_grid import SongGrid
from .song_player import SongPlayer
from .async_loop import loop

@Gtk.Template(resource_path = "/ch/ulys/Periscope/view/window.ui")
class Window(Adw.ApplicationWindow):
    __gtype_name__ = "Window"

    song_player = Gtk.Template.Child()
    song_grid = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        loop.submit_async(self.song_grid.show_playlist("bb052612-f834-4ff2-9937-e01351941b3d"))
