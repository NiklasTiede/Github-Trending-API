"""This script executes GET requests asynchronously 
thereby it can test if the API works also asynchronously.
"""

import asyncio
import time
import aiohttp
import ssl


the_url = "http://0.0.0.0:8000/repositories/c++?since=weekly"


url_list = list([the_url]*10)


async def fetch(session, url):
    async with session.get(url, ssl=ssl.SSLContext()) as response:
        return await response.json()


async def fetch_all(urls, loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        results = await asyncio.gather(*[fetch(session, url) for url in urls], return_exceptions=True)
        return results

if __name__ == '__main__':
    t1_start = time.perf_counter()

    loop = asyncio.get_event_loop()
    urls = url_list
    htmls = loop.run_until_complete(fetch_all(urls, loop))

    t1_stop = time.perf_counter()
    print("elapsed:", t1_stop-t1_start)
