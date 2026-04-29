"""Github-Trending-API
===================
API serving data about trending github repositories/developers.
"""
# Copyright (c) 2021, Niklas Tiede.
# All rights reserved. Distributed under the MIT License.
from typing import Any, Dict, List

import fastapi
import uvicorn

from app.allowed_parameters import (
    AllowedDateRanges,
    AllowedProgrammingLanguages,
    AllowedSpokenLanguages,
)
from app.scraping import (
    UpstreamRequestError,
    filter_articles,
    get_request,
    make_soup,
    scraping_developers,
    scraping_repositories,
)

app = fastapi.FastAPI()


async def fetch_trending_html(url: str, payload: Dict[str, str]) -> str:
    """Fetch GitHub Trending HTML and translate upstream failures."""
    try:
        return await get_request(url, compress=True, params=payload)
    except UpstreamRequestError as request_error:
        raise fastapi.HTTPException(
            status_code=502,
            detail="Unable to fetch GitHub Trending data",
        ) from request_error


@app.get("/")
def help_routes(request: fastapi.Request) -> Dict[str, str]:
    """ API endpoints and documentation. """
    base_url = str(request.base_url).rstrip("/")
    return {
        "repositories": f"{base_url}/repositories",
        "developers": f"{base_url}/developers",
        "docs": f"{base_url}/docs",
        "redoc": f"{base_url}/redoc",
    }


@app.get("/repositories")
async def trending_repositories(
    since: AllowedDateRanges | None = None,
    spoken_language_code: AllowedSpokenLanguages | None = None,
) -> List[Any]:
    """Returns data about trending repositories (all programming
    languages, cannot be specified on this endpoint).
    """
    payload = {"since": "daily"}
    if since:
        payload["since"] = since.value
    if spoken_language_code:
        payload["spoken_language_code"] = spoken_language_code.value

    url = "https://github.com/trending"
    raw_html = await fetch_trending_html(url, payload)
    articles_html = filter_articles(raw_html)
    soup = make_soup(articles_html)
    return scraping_repositories(soup, since=payload["since"])


@app.get("/repositories/{prog_lang}")
async def trending_repositories_by_progr_language(
    prog_lang: AllowedProgrammingLanguages,
    since: AllowedDateRanges | None = None,
    spoken_language_code: AllowedSpokenLanguages | None = None,
) -> List[Any]:
    """Returns data about trending repositories. A specific programming
    language can be added as path parameter to specify search.
    """
    payload = {"since": "daily"}
    if since:
        payload["since"] = since.value
    if spoken_language_code:
        payload["spoken_language_code"] = spoken_language_code.value

    url = f"https://github.com/trending/{prog_lang.value}"
    raw_html = await fetch_trending_html(url, payload)
    articles_html = filter_articles(raw_html)
    soup = make_soup(articles_html)
    return scraping_repositories(soup, since=payload["since"])


@app.get("/developers")
async def trending_developers(
    since: AllowedDateRanges | None = None,
) -> List[Any]:
    """Returns data about trending developers (all programming languages,
    cannot be specified on this endpoint).
    """
    payload = {"since": "daily"}
    if since:
        payload["since"] = since.value

    url = "https://github.com/trending/developers"
    raw_html = await fetch_trending_html(url, payload)
    articles_html = filter_articles(raw_html)
    soup = make_soup(articles_html)
    return scraping_developers(soup, since=payload["since"])


@app.get("/developers/{prog_lang}")
async def trending_developers_by_progr_language(
    prog_lang: AllowedProgrammingLanguages,
    since: AllowedDateRanges | None = None,
) -> List[Any]:
    """Returns data about trending developers. A specific programming
    language can be added as path parameter to specify search.
    """
    payload = {"since": "daily"}
    if since:
        payload["since"] = since.value

    url = f"https://github.com/trending/developers/{prog_lang.value}"
    raw_html = await fetch_trending_html(url, payload)
    articles_html = filter_articles(raw_html)
    soup = make_soup(articles_html)
    return scraping_developers(soup, since=payload["since"])


if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")
