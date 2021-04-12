"""This script executes GET requests asynchronously thereby it
can test if the API works also asynchronously. This script is used manually.
"""
import asyncio
import time

import aiohttp


# URL = "https://github.com/trending"
URL = "http://0.0.0.0:5000/repositories/c++?since=weekly"

# URL = "http://127.0.0.1:8000/repositories/c++?since=weekly"
# URL = """https://gh-trending-api.herokuapp.com/
# repositories?since=weekly&spoken_language_code=de"""

url_list = list([URL] * 20)


async def fetch(session, url):
    """requesting a url asynchronously"""
    async with session.get(url) as response:
        print('sending request')
        return await response.json()


async def fetch_all(urls, loop):
    """performaning multiple requests asynchronously"""
    async with aiohttp.ClientSession(loop=loop) as session:
        results = await asyncio.gather(
            *[fetch(session, url) for url in urls],
            return_exceptions=True,
        )
        return results


if __name__ == "__main__":
    t1_start = time.perf_counter()

    event_loop = asyncio.get_event_loop()
    urls_duplicates = url_list
    htmls = event_loop.run_until_complete(
        fetch_all(urls_duplicates, event_loop),
    )

    for html in htmls:
        print(html[0:1])
        print()
    t1_stop = time.perf_counter()
    print("elapsed:", t1_stop - t1_start)
