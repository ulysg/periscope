import hashlib
import secrets
import aiohttp
import asyncio
import urllib.parse
from typing import Generator

from .config import config
from . import errors
from .medias import *

API_VERSION = "1.16.1"
APP_NAME = "ch.ulys.Periscope"

class Subsonic:
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url
        self.username = username
        self.password = password

    async def get_albums(self, offset: int = 0, size: int = 24,
            ordering: str = "alphabeticalByName") -> list[Playlist]:

        result = await self._request_json("getAlbumList",
                {"type": ordering, "offset": offset, "size": size})
        return [Album(album) for album in result["albumList"]["album"]]

    async def get_playlists(self) -> list[Playlist]:
        result = await self._request_json("getPlaylists")
        return [Playlist(playlist) for playlist in result["playlists"]["playlist"]]

    async def get_playlist(self, id: str) -> Playlist:
        result = await self._request_json("getPlaylist", {"id": id})
        return Playlist(result["playlist"])

    async def stream(self, id: str) -> Generator[bytes, None, None]:
        return self._request_bin("stream", {"id": id})

    def get_stream_url(self, id: str) -> str:
        url = f"{self.base_url}/rest/stream?"
        params = self._get_params()
        params["id"] = id
        return url + urllib.parse.urlencode(params)

    async def get_cover(self, id: str) -> Generator[bytes, None, None]:
        return self._request_bin("getCoverArt", {"id": id})

    def get_cover_url(self, id: str) -> str:
        url = f"{self.base_url}/rest/getCoverArt?"
        params = self._get_params()
        params["id"] = id
        return url + urllib.parse.urlencode(params)

    async def _request_json(self, endpoint: str, query: dict = {}) -> dict:
        url = f"{self.base_url}/rest/{endpoint}"
        data = self._get_params()
        data.update(query)

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data = data) as response:
                response.raise_for_status()
                result = await response.json()
                result = result["subsonic-response"]

                if result["status"] == "failed":
                    exc = errors.getExcByCode(result["error"]["code"])
                    raise exc(result["error"]["message"])

                return result

    async def _request_bin(self, endpoint: str, query: dict = {}) -> Generator[bytes, None, None]:
        url = f"{self.base_url}/rest/{endpoint}"
        data = self._get_params()
        data.update(query)

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data = data) as response:
                response.raise_for_status()

                if response.content_type == "application/json":
                    result = await response.json()
                    result = result["subsonic-response"]

                    exc = errors.getExcByCode(result["error"]["code"])
                    raise exc(result["error"]["message"])

                async for data, _ in response.content.iter_chunks():
                    yield data

    def _get_params(self) -> dict[str, str]:
        salt = secrets.token_hex(16)
        token = hashlib.md5((self.password + salt).encode("utf-8")).hexdigest()

        return {
            "u": self.username,
            "t": token,
            "s": salt,
            "v": API_VERSION,
            "c": APP_NAME,
            "f": "json"
        }

class SubsonicConfig(Subsonic):
    def __init__(self):
        base_url = config.get("connection", "url")
        username = config.get("connection", "username")
        password = config.get("connection", "password")

        super().__init__(base_url, username, password)

