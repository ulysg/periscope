from gi.repository import Adw
from gi.repository import Gtk

import time

from .subsonic import SubsonicConfig
from .song_thumbnail import SongThumbnail
from .errors import SonicError
from .player import player

@Gtk.Template(resource_path = "/ch/ulys/Periscope/view/song_grid.ui")
class SongGrid(Adw.Bin):
    __gtype_name__ = "SongGrid"

    grid = Gtk.Template.Child()

    def __init__(self, **kwargs):
        self.subsonic = SubsonicConfig()
        super().__init__(**kwargs)

    async def show_playlist(self, id):
        try:
            playlist = await self.subsonic.get_playlist(id)

        except Execption as e:
            print(e)

        for song in playlist.songs:
            song_ui = SongThumbnail(song)
            self.grid.append(song_ui)

        try:
            player.set_playlist(playlist.songs)
            player.play()

        except Exception as e:
            print(e)


