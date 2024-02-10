from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import GLib

import time

from .subsonic import SubsonicConfig
from .cover_thumbnail import CoverThumbnail
from .errors import SonicError
from .player import player

@Gtk.Template(resource_path = "/ch/ulys/Periscope/view/song_grid.ui")
class SongGrid(Adw.Bin):
    __gtype_name__ = "SongGrid"

    grid = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subsonic = SubsonicConfig()

    async def show_playlist(self, id):
        playlist = await self.subsonic.get_playlist(id)
        player.set_playlist(playlist.songs)
        player.play()

        playlists = await self.subsonic.get_playlists()

        try:
            for playlist in playlists:
                GLib.idle_add(self._add_song, playlist)

        except Exception as e:
            print(e)

    def _add_song(self, song):
        song_ui = CoverThumbnail(song)
        GLib.idle_add(self.grid.append, song_ui)


