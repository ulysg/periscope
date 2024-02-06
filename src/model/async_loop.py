import asyncio
import threading

from typing import Awaitable

class AsyncLoop:
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        threading.Thread(target = self.loop.run_forever).start()

    def submit_async(self, coroutine: Awaitable):
        asyncio.run_coroutine_threadsafe(coroutine, self.loop)

    def stop(self):
        self.loop.call_soon_threadsafe(self.loop.stop)

loop = AsyncLoop()
