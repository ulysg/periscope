from gi.repository import Gst
import random
from typing import Callable

from .medias import Song
from .subsonic import SubsonicConfig, Song
from .errors import SonicError

class Player:
    def __init__(self):
        self._subsonic = SubsonicConfig()
        self._current_song = None

        self._playlist = []
        self._queue = []
        self._last_played = []
        self._current_song = None

        self._is_shuffling = False
        self._is_looping = False
        self._is_playing = False

        self._change_listeners = []

        Gst.init(None)
        self._player = Gst.ElementFactory.make("playbin3", "player")

        fakesink = Gst.ElementFactory.make("fakesink", "fakesink")
        self._player.set_property("video-sink", fakesink)

        self._player.connect("about-to-finish", self._on_about_to_change)

        bus = self._player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self._on_message)

    def set_playlist(self, playlist: list[Song]):
        self._playlist = playlist.copy()
        self._queue = playlist.copy()

        if self._is_shuffling:
            random.shuffle(self._queue)

        self._pop_and_play()

    def play(self):
        self._player.set_state(Gst.State.PLAYING)

    def pause(self):
        self._player.set_state(Gst.State.PAUSED)

    def toggle_play(self):
        if self._is_playing:
            self.pause()

        else:
            self.play()

    def previous(self):
        if not self._last_played:
            return

        was_playing = self._is_playing
        self._player.set_state(Gst.State.READY)

        self._queue.insert(0, self._current_song)
        self._current_song = self._last_played.pop(-1)

        url = self._subsonic.get_stream_url(self._current_song.id)
        self._player.set_property("uri", url)

        self._player.set_state(Gst.State.PLAYING)

    def next(self):
        self._player.set_state(Gst.State.READY)
        self._pop_and_play()

        if self._current_song:
            self._player.set_state(Gst.State.PLAYING)

    def toggle_shuffle(self):
        if self._is_shuffling:
            current_index = self._playlist.index(self._current_song)

            if current_index != len(self._playlist) - 1:
                self._queue = self._playlist[current_index + 1:].copy()

            else:
                self._queue = []

        else:
            self._queue = self._playlist.copy()
            random.shuffle(self._queue)

        self._is_shuffling = not self._is_shuffling

    def toggle_loop(self):
        self._is_looping = not self._is_looping

    def is_playing(self):
        return self._is_playing

    def is_shuffling(self):
        return self._is_shuffling

    def is_looping(self):
        return self._is_looping

    def get_current_song(self):
        return self._current_song

    def get_queue(self):
        return self._queue.copy()

    def get_last_played(self):
        return self._last_played.copy()

    def add_change_listener(self, listener: Callable[[bool], None]):
        self._change_listeners.append(listener)

    def _pop_and_play(self):
        if not self._queue:
            if not self._is_looping:
                self._current_song = None
                return

            self._queue = self._playlist.copy()

            if self._is_shuffling:
                random.shuffle(self._queue)

        if self._current_song:
            self._last_played.append(self._current_song)

        self._current_song = self._queue.pop(0)

        url = self._subsonic.get_stream_url(self._current_song.id)
        self._player.set_property("uri", url)

    def _on_about_to_change(self, _):
        self._pop_and_play()
        [listener(self._is_playing) for listener in self._change_listeners]

    def _on_message(self, bus, message):
        match message.type:
            case Gst.MessageType.STATE_CHANGED:
                state = message.parse_state_changed()[1].value_name
                self._is_playing = state == "GST_STATE_PLAYING"

                [listener(self._is_playing) for listener in self._change_listeners]

            case Gst.MessageType.BUFFERING:
                pass

            case Gst.MessageType.EOS:
                pass

player = Player()
