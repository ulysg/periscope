from gi.repository import Adw
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import Graphene
from gi.repository import Gsk

import time

class CoverImage(GObject.GObject, Gdk.Paintable):
    __gtype_name__ = "CoverImage"

    def __init__(self, radius, **kwargs):
        super().__init__(**kwargs)

        self._texture = None
        self._radius = radius

    def do_snapshot(self, snapshot, width, height):
        size = min(width, height)

        rect = Graphene.Rect().init(0, 0, size, size)
        rounded_rect = Gsk.RoundedRect()
        rounded_rect.init_from_rect(rect, self._radius)
        snapshot.push_rounded_clip(rounded_rect)

        if self._texture:
            snapshot.append_scaled_texture(self._texture,
                    Gsk.ScalingFilter.TRILINEAR, rect)

        snapshot.pop()

    def set_cover(self, filename):
        self._texture = Gdk.Texture.new_from_filename(filename)
        self.invalidate_contents()
