from gi.repository import Adw
from gi.repository import Gtk

@Gtk.Template(resource_path = "/ch/ulys/Periscope/view/song_thumbnail.ui")
class SongThumbnail(Adw.Bin):
    __gtype_name__ = "SongThumbnail"

    cover = Gtk.Template.Child()
    title = Gtk.Template.Child()

    def __init__(self, song, **kwargs):
        super().__init__(**kwargs)

        self.song = song
        self.title.set_text(self.song.title)

