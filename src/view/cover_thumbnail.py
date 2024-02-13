from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import Pango

from .cover_cache import CoverCache
from .async_loop import loop
from .cover_image import CoverImage
from .medias import *

@Gtk.Template(resource_path = "/ch/ulys/Periscope/view/cover_thumbnail.ui")
class CoverThumbnail(Adw.Bin):
    __gtype_name__ = "CoverThumbnail"

    cover = Gtk.Template.Child()
    title = Gtk.Template.Child()
    artist = Gtk.Template.Child()

    def __init__(self, media, **kwargs):
        super().__init__(**kwargs)

        self._media = media

        self._cover_cache = CoverCache()
        self._cover_image = CoverImage(12, self)
        self.cover.set_from_paintable(self._cover_image)

        attribute = Pango.AttrFontDesc.new(Pango.FontDescription.from_string("Bold"))
        attributes = Pango.AttrList()
        attributes.insert(attribute)

        self.title.set_attributes(attributes)

        match self._media:
            case Song():
                self.title.set_text(self._media.title)
                self.artist.set_text(self._media.artist)

            case Playlist():
                self.title.set_text(self._media.name)

            case Album():
                self.title.set_text(self._media.title)
                self.artist.set_text(self._media.artist)

        loop.submit_async(self._set_cover())

    async def _set_cover(self):
        try:
            GLib.idle_add(self._cover_image.unset_cover)
            cover_location = await self._cover_cache.get_file_location(self._media.coverArt)
            GLib.idle_add(self._cover_image.set_cover, cover_location)

        except Exception as e:
            print(e)



