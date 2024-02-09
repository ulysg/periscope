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

        self._state_listeners = []
        self._song_listeners = []
        self._seek_callback = None

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

        self._player.set_state(Gst.State.READY)
        self._play_next()

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

        self._player.set_state(Gst.State.READY)

        self._queue.insert(0, self._current_song)
        self._queue.insert(0, self._last_played.pop(-1))
        self._play_next()

        self._player.set_state(Gst.State.PLAYING)

    def next(self):
        self._player.set_state(Gst.State.READY)
        self._play_next()
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

    def seek(self, position, finished_callback: Callable):
        self._player.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT,
                position * Gst.SECOND)

        self._seek_callback = finished_callback

    def get_position(self):
        return self._player.query_position(Gst.Format.TIME)[1] / Gst.SECOND

    def get_current_song(self):
        return self._current_song

    def get_queue(self):
        return self._queue.copy()

    def get_last_played(self):
        return self._last_played.copy()

    def add_state_listener(self, listener: Callable[[bool], None]):
        self._state_listeners.append(listener)

    def add_song_listener(self, listener: Callable[[Song], None]):
        self._song_listeners.append(listener)

    def _play_next(self):
        url = self._subsonic.get_stream_url(self._queue[0].id)
        self._player.set_property("uri", url)

    def _pop_queue(self):
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

        if self._queue and self._last_played and self._last_played[-1] is self._queue[0]:
            self._last_played.pop(-1)

    def _on_about_to_change(self, _):
        self._play_next()

    def _on_message(self, bus, message):
        match message.type:
            case Gst.MessageType.STATE_CHANGED:
                old, new, _ = message.parse_state_changed()
                self._is_playing = new == Gst.State.PLAYING

                [listener(self._is_playing) for listener in self._state_listeners]

            case Gst.MessageType.STREAM_START:
                self._is_playing = True
                self._pop_queue()

                [listener(self._current_song) for listener in self._song_listeners]

            case Gst.MessageType.ASYNC_DONE:
                if self._seek_callback:
                    self._seek_callback()
                    self._seek_callback = None

player = Player()
