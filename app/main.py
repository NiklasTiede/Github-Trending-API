"""Github-Trending-API
===================
API serving data about trending github repositories/developers.
"""
# Copyright (c) 2021, Niklas Tiede.
# All rights reserved. Distributed under the MIT License.

import asyncio

import fastapi
import uvicorn

from allowed_parameters import (
    AllowedDateRanges,
    AllowedProgrammingLanguages,
    AllowedSpokenLanguages,
)
from scraping import (
    filter_articles,
    get_request,
    make_soup,
    scraping_developers,
    scraping_repositories,
)

app = fastapi.FastAPI()


this_apis_domain = "gh-trending.com"

@app.get("/")
def help():
    """ API endpoints and documentation. """
    return {
        "repositories": f"http://{this_apis_domain}/repositories",
        "developers": f"http://{this_apis_domain}/developers",
        "docs": f"http://{this_apis_domain}/docs",
        "redoc": f"http://{this_apis_domain}/redoc",
    }


@app.get("/repositories")
async def trending_repositories(
    since: AllowedDateRanges = None, spoken_lang: AllowedSpokenLanguages = None
):
    """Returns data about trending repositories (all programming
    languages, cannot be specified on this endpoint).
    """
    payload = {"since": "daily"}
    if since:
        payload["since"] = since._value_
    if spoken_lang:
        payload["spoken_lang"] = spoken_lang._value_

    url = "https://github.com/trending"
    sem = asyncio.Semaphore()
    async with sem:
        raw_html = await get_request(url, compress=True, params=payload)
    if not isinstance(raw_html, str):
        return "Unable to connect to Github"

    articles_html = filter_articles(raw_html)
    soup = make_soup(articles_html)
    return scraping_repositories(soup, since=payload["since"])


@app.get("/repositories/{prog_lang}")
async def trending_repositories_by_progr_language(
    prog_lang: AllowedProgrammingLanguages,
    since: AllowedDateRanges = None,
    spoken_lang: AllowedSpokenLanguages = None,
):
    """Returns data about trending repositories. A specific programming
    language can be added as path parameter to specify search.
    """
    payload = {"since": "daily"}
    if since:
        payload["since"] = since._value_
    if spoken_lang:
        payload["spoken_lang"] = spoken_lang._value_

    url = f"https://github.com/trending/{prog_lang}"
    sem = asyncio.Semaphore()
    async with sem:
        raw_html = await get_request(url, compress=True, params=payload)
    if not isinstance(raw_html, str):
        return "Unable to connect to Github"

    articles_html = filter_articles(raw_html)
    soup = make_soup(articles_html)
    return scraping_repositories(soup, since=payload["since"])


@app.get("/developers")
async def trending_developers(since: AllowedDateRanges = None):
    """Returns data about trending developers (all programming languages,
    cannot be specified on this endpoint).
    """
    payload = {"since": "daily"}
    if since:
        payload["since"] = since._value_

    url = "https://github.com/trending/developers"
    sem = asyncio.Semaphore()
    async with sem:
        raw_html = await get_request(url, compress=True, params=payload)
    if not isinstance(raw_html, str):
        return "Unable to connect to Github"

    articles_html = filter_articles(raw_html)
    soup = make_soup(articles_html)
    return scraping_developers(soup, since=payload["since"])


@app.get("/developers/{prog_lang}")
async def trending_developers_by_progr_language(
    prog_lang: AllowedProgrammingLanguages, since: AllowedDateRanges = None
):
    """Returns data about trending developers. A specific programming
    language can be added as path parameter to specify search.
    """
    payload = {"since": "daily"}
    if since:
        payload["since"] = since._value_

    url = f"https://github.com/trending/developers/{prog_lang}"
    sem = asyncio.Semaphore()
    async with sem:
        raw_html = await get_request(url, compress=True, params=payload)
    if not isinstance(raw_html, str):
        return "Unable to connect to Github"

    articles_html = filter_articles(raw_html)
    soup = make_soup(articles_html)
    return scraping_developers(soup, since=payload["since"])


if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")
