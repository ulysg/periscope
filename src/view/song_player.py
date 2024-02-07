from gi.repository import Adw
from gi.repository import Gtk

from .player import player

@Gtk.Template(resource_path = "/ch/ulys/Periscope/view/song_player.ui")
class SongPlayer(Gtk.ActionBar):
    __gtype_name__ = "SongPlayer"

    cover = Gtk.Template.Child()
    title = Gtk.Template.Child()

    play_image = Gtk.Template.Child()
    prev_button = Gtk.Template.Child()
    next_button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        player.add_change_listener(self._on_state_change)

    def _update_thumbnail(self):
        self.title.set_text(player.get_current_song().title)

    def _on_state_change(self, is_playing):
        if is_playing:
            self.play_image.set_from_icon_name("media-playback-pause")

        else:
            self.play_image.set_from_icon_name("media-playback-start")

        self.prev_button.set_sensitive(bool(player.get_last_played()))
        self.next_button.set_sensitive(bool(player.get_queue()) or player.is_looping())

        self._update_thumbnail()

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

