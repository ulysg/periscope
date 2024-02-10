from gi.repository import Adw
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import Graphene
from gi.repository import Gsk
from gi.repository import Gtk

import time

class CoverImage(GObject.GObject, Gdk.Paintable):
    __gtype_name__ = "CoverImage"

    def __init__(self, radius, widget, **kwargs):
        super().__init__(**kwargs)

        self._texture = None
        self._radius = radius
        self._icon_theme = Gtk.IconTheme.new().get_for_display(widget.get_display())

        self._style_manager = Adw.StyleManager.get_default()
        self._style_manager.connect("notify::dark", self._on_dark_changed)

    def do_snapshot(self, snapshot, width, height):
        size = min(width, height)

        rect = Graphene.Rect().init(0, 0, size, size)
        rounded_rect = Gsk.RoundedRect()
        rounded_rect.init_from_rect(rect, self._radius)
        snapshot.push_rounded_clip(rounded_rect)

        if self._texture:
            snapshot.append_scaled_texture(self._texture,
                    Gsk.ScalingFilter.TRILINEAR, rect)

        else:
            bg_color = Gdk.RGBA()
            bg_color.parse("#ebebeb")

            if self._style_manager.get_dark():
                bg_color.parse("#303030")

            snapshot.append_color(bg_color, Graphene.Rect().init(0, 0, size, size))

            icon_size = size // 3
            icon = self._icon_theme.lookup_icon("folder-music-symbolic", None, icon_size, icon_size, 0, 0)

            snapshot.translate(Graphene.Point().init(size // 2 - icon_size // 2, size // 2 - icon_size // 2))
            icon.snapshot(snapshot, size // 3, size // 3)

        snapshot.pop()

    def set_cover(self, filename):
        self._texture = Gdk.Texture.new_from_filename(filename)
        self.invalidate_contents()

    def unset_cover(self):
        self._texture = None
        self.invalidate_contents()

    def _on_dark_changed(self, *args):
        if self._texture:
            return

        self.invalidate_contents()
