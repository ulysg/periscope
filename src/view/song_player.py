from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import Pango
import time

from .player import player

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

    _is_scale_pressed = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        player.add_change_listener(self._on_state_change)
        self._on_time_out()

        attribute = Pango.AttrFontFeatures.new("tnum=1")
        attributes = Pango.AttrList()
        attributes.insert(attribute)

        self.start_label.set_attributes(attributes)
        self.end_label.set_attributes(attributes)

        start_ctrl = Gtk.GestureClick()
        start_ctrl.connect("pressed", self._on_scale_pressed)

        end_ctrl = Gtk.GestureClick()
        end_ctrl.connect("unpaired-release", self._on_scale_released)
        end_ctrl.set_touch_only(True)

        self.progress_scale.add_controller(start_ctrl)
        self.progress_scale.add_controller(end_ctrl)

    def _update_scale(self):
        if self._is_scale_pressed:
            return

        position = player.get_position()

        if position < 0:
            return

        self._progress = position
        self.progress_scale.set_value(self._progress)

        self.start_label.set_text(self._time_to_str(position))

    def _time_to_str(self, seconds):
        return time.strftime("%-M:%S", time.gmtime(seconds))

    def _on_time_out(self):
        self._timeout = GLib.timeout_add(100, self._on_time_out)
        self._update_scale()

    def _update_thumbnail(self, song):
        self.title.set_text(song.title)

    def _on_state_change(self, is_playing):
        if is_playing:
            self.play_image.set_from_icon_name("media-playback-pause")

        else:
            self.play_image.set_from_icon_name("media-playback-start")

        self.prev_button.set_sensitive(bool(player.get_last_played()))
        self.next_button.set_sensitive(bool(player.get_queue()) or player.is_looping())

        song = player.get_current_song()
        self._update_scale()

        if song:
            self._update_thumbnail(song)
            self.end_label.set_text(self._time_to_str(song.duration))
            self.progress_scale.get_adjustment().set_upper(round(song.duration, 1))

    def _seek(self):
        song = player.get_current_song()

        if not song:
            return

        player.seek(self.progress_scale.get_value(), self._on_seek_finished)

    def _on_scale_pressed(self, *args):
        self._is_scale_pressed = True

    def _on_scale_released(self, *args):
        self._seek()

    def _on_seek_finished(self):
        self._is_scale_pressed = False

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
        if not self._is_scale_pressed:
            return

        self.start_label.set_text(self._time_to_str(scale.get_value()))
