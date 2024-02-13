from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import GLib

import time

from .subsonic import SubsonicConfig
from .cover_thumbnail import CoverThumbnail
from .errors import SonicError
from .player import player
from .async_loop import loop

ALBUM_PER_PAGE = 24

ORDERING = (
    "alphabeticalByName",
    "alphabeticalByArtist",
    "random",
    "newest"
)

@Gtk.Template(resource_path = "/ch/ulys/Periscope/view/album_view.ui")
class AlbumView(Adw.Bin):
    __gtype_name__ = "AlbumView"

    grid = Gtk.Template.Child()
    prev_button = Gtk.Template.Child()
    next_button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._subsonic = SubsonicConfig()
        self._offset = 0
        self._order_index = 0

        loop.submit_async(self.update_albums())

    async def update_albums(self):
        GLib.idle_add(self.grid.remove_all)
        GLib.idle_add(self.prev_button.set_visible, False)
        GLib.idle_add(self.next_button.set_visible, False)

        ordering = ORDERING[self._order_index]

        albums = await self._subsonic.get_albums(self._offset * ALBUM_PER_PAGE, ALBUM_PER_PAGE, ordering)
        next_albums = await self._subsonic.get_albums((self._offset + 1) * ALBUM_PER_PAGE, 1, ordering)

        for album in albums:
            GLib.idle_add(self._add_album, album)

        GLib.idle_add(self.prev_button.set_visible, self._offset != 0)
        GLib.idle_add(self.next_button.set_visible, bool(next_albums))

    def _add_album(self, album):
        album_ui = CoverThumbnail(album)
        self.grid.append(album_ui)

    @Gtk.Template.Callback()
    def _on_prev_pressed(self, button):
        self._offset -= 1
        loop.submit_async(self.update_albums())

    @Gtk.Template.Callback()
    def _on_next_pressed(self, button):
        self._offset += 1
        loop.submit_async(self.update_albums())

    @Gtk.Template.Callback()
    def _on_order_changed(self, dropdown, selected):
        self._offset = 0
        self._order_index = dropdown.get_selected()
        loop.submit_async(self.update_albums())
