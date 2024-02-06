from gi.repository import Gst

from .medias import Song
from .subsonic import SubsonicConfig
from .errors import SonicError

class Player:
    def __init__(self):
        Gst.init(None)
        self.player = Gst.ElementFactory.make("playbin", "player")
        self.subsonic = SubsonicConfig()

    def play_now(self, song: Song):
        url = self.subsonic.get_stream_url(song.id)

        self.player.set_property("uri", url)
        self.player.set_state(Gst.State.PLAYING)

player = Player()
