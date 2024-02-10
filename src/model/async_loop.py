import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor

from typing import Awaitable

class AsyncLoop:
    def __init__(self):
        self._loop = asyncio.new_event_loop()
        threading.Thread(target = self._loop.run_forever).start()

    def submit_async(self, coroutine: Awaitable):
        asyncio.run_coroutine_threadsafe(coroutine, self._loop)

    def stop(self):
        self._loop.call_soon_threadsafe(self.loop.stop)

loop = AsyncLoop()
