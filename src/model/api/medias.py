class Media:
    def __init__(self, response: dict, keys: list[str]):
        for key in keys:
            try:
                setattr(self, key, response[key])

            except KeyError:
                pass

class Song(Media):
    keys = ["id", "parent", "isDir", "title", "album", "artist", "track", "year"
            "coverArt", "size", "contentType", "suffix", "duration", "bitRate", "path",
            "discNumber", "created", "albumId", "artistId", "type", "isVideo", "bpm",
            "comment", "sortName", "mediaType", "musicBrainzId", "genres", "replayGain"]

    def __init__(self, response: dict):
        super().__init__(response, Song.keys)

class Playlist(Media):
    keys = ['id', 'name', 'comment', 'songCount', 'duration', 'public', 'owner',
            'created', 'changed', 'coverArt']

    def __init__(self, response: dict):
        super().__init__(response, Playlist.keys)

        if "entry" in response:
            self.songs = [Song(entry) for entry in response["entry"]]
