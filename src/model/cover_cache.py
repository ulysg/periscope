import xdg_base_dirs
import os

from .subsonic import SubsonicConfig

CACHE_DIR_NAME = "covers"

class CoverCache:
    def __init__(self):
        self._subsonic = SubsonicConfig()

        cache_dir = os.path.join(xdg_base_dirs.xdg_cache_home(), CACHE_DIR_NAME)

        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

    async def get_file_location(self, id: str) -> str:
        filepath = self._get_file_path(id)

        if os.path.isfile(filepath):
            return filepath

        return await self._fetch_and_save(id)

    async def _fetch_and_save(self, id) -> str:
        filepath = self._get_file_path(id)

        with open(filepath, "wb") as file:
            async for data in await self._subsonic.get_cover(id):
                file.write(data)

        return filepath

    def _get_file_path(self, id: str) -> str:
        return os.path.join(xdg_base_dirs.xdg_cache_home(), CACHE_DIR_NAME, id)

