from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import Pango
import time

from .player import player

SEEK_TIMEOUT = 0.1

@Gtk.Template(resource_path = "/ch/ulys/Periscope/view/song_player.ui")
class SongPlayer(Gtk.ActionBar):
    __gtype_name__ = "SongPlayer"

    cover = Gtk.Template.Child()
    title = Gtk.Template.Child()

    play_image = Gtk.Template.Child()
    prev_button = Gtk.Template.Child()
    next_button = Gtk.Template.Child()

    progress_scale = Gtk.Template.Child()
    start_label = Gtk.Template.Child()
    end_label = Gtk.Template.Child()

    _last_scale_value = -1
    _last_seek = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        player.add_change_listener(self._on_state_change)
        self._on_time_out()

        attribute = Pango.AttrFontFeatures.new("tnum=1")
        attributes = Pango.AttrList()
        attributes.insert(attribute)

        self.start_label.set_attributes(attributes)
        self.end_label.set_attributes(attributes)

    def _update_scale(self):
        song = player.get_current_song()
        position = player.get_position()

        if not song or position < 0:
            return

        progress = self.progress_scale.get_adjustment().get_upper() * position / song.duration
        self._last_scale_value = progress
        self.progress_scale.set_value(progress)

        self.start_label.set_text(self._time_to_str(position))
        self.end_label.set_text(self._time_to_str(song.duration))

    def _time_to_str(self, seconds):
        return time.strftime("%-M:%S", time.gmtime(seconds))

    def _on_time_out(self):
        self._timeout = GLib.timeout_add(100, self._on_time_out)
        self._update_scale()

    def _update_thumbnail(self):
        if not player.get_current_song():
            return

        self.title.set_text(player.get_current_song().title)

    def _on_state_change(self, is_playing):
        if is_playing:
            self.play_image.set_from_icon_name("media-playback-pause")

        else:
            self.play_image.set_from_icon_name("media-playback-start")

        self.prev_button.set_sensitive(bool(player.get_last_played()))
        self.next_button.set_sensitive(bool(player.get_queue()) or player.is_looping())

        self._update_thumbnail()
        self._update_scale()

    def _seek(self, progress_value):
        song = player.get_current_song()

        if not song:
            return

        now = time.monotonic()

        if now - self._last_seek < SEEK_TIMEOUT:
            return

        self._last_seek = now

        position = progress_value / self.progress_scale.get_adjustment().get_upper()
        player.seek(position * song.duration)

    @Gtk.Template.Callback()
    def _on_toggle_play(self, button):
        player.toggle_play()

    @Gtk.Template.Callback()
    def _on_toggle_shuffle(self, button):
        player.toggle_shuffle()
        self._on_state_change(player.is_playing())

    @Gtk.Template.Callback()
    def _on_toggle_loop(self, button):
        player.toggle_loop()
        self._on_state_change(player.is_playing())

    @Gtk.Template.Callback()
    def _on_previous_clicked(self, button):
        player.previous()

    @Gtk.Template.Callback()
    def _on_next_clicked(self, button):
        player.next()

    @Gtk.Template.Callback()
    def _on_progress_changed(self, scale):
        if self._last_scale_value != scale.get_value():
            self._seek(scale.get_value())
