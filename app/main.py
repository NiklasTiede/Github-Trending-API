"""Github-Trending-API
===================
API serving data about trending github repositories/developers.
"""
# Copyright (c) 2021, Niklas Tiede.
# All rights reserved. Distributed under the MIT License.
import time
from typing import Dict, List

import fastapi
import uvicorn

from app.allowed_parameters import (
    AllowedDateRanges,
    AllowedProgrammingLanguages,
    AllowedSpokenLanguages,
)
from app.schemas import Developer, HealthStatus, Metadata, Repository
from app.scraping import (
    UpstreamRequestError,
    get_request,
    make_soup,
    scraping_developers,
    scraping_repositories,
)

app = fastapi.FastAPI()
APP_NAME = "GitHub Trending API"
APP_VERSION = "1.0.2"
CACHE_TTL_SECONDS = 300
CacheKey = tuple[str, tuple[tuple[str, str], ...]]
_trending_html_cache: dict[CacheKey, tuple[float, str]] = {}


def build_payload(
    since: AllowedDateRanges | None = None,
    spoken_language_code: AllowedSpokenLanguages | None = None,
) -> Dict[str, str]:
    """Build GitHub Trending query parameters."""
    payload = {"since": "daily"}
    if since:
        payload["since"] = since.value
    if spoken_language_code:
        payload["spoken_language_code"] = spoken_language_code.value
    return payload


async def fetch_trending_html(url: str, payload: Dict[str, str]) -> str:
    """Fetch GitHub Trending HTML and translate upstream failures."""
    cache_key = (url, tuple(sorted(payload.items())))
    cached_at, cached_html = _trending_html_cache.get(cache_key, (0.0, ""))
    if cached_html and time.monotonic() - cached_at < CACHE_TTL_SECONDS:
        return cached_html

    try:
        raw_html = await get_request(url, compress=True, params=payload)
    except UpstreamRequestError as request_error:
        raise fastapi.HTTPException(
            status_code=502,
            detail="Unable to fetch GitHub Trending data",
        ) from request_error

    _trending_html_cache[cache_key] = (time.monotonic(), raw_html)
    return raw_html


def clear_trending_cache() -> None:
    """Clear cached GitHub Trending HTML responses."""
    _trending_html_cache.clear()


async def get_repository_trends(
    url: str,
    payload: Dict[str, str],
) -> List[Repository]:
    """Fetch and parse GitHub Trending repository data."""
    raw_html = await fetch_trending_html(url, payload)
    soup = make_soup(raw_html)
    repositories = scraping_repositories(soup, since=payload["since"])
    return [Repository.model_validate(repository) for repository in repositories]


async def get_developer_trends(
    url: str,
    payload: Dict[str, str],
) -> List[Developer]:
    """Fetch and parse GitHub Trending developer data."""
    raw_html = await fetch_trending_html(url, payload)
    soup = make_soup(raw_html)
    developers = scraping_developers(soup, since=payload["since"])
    return [Developer.model_validate(developer) for developer in developers]


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


@app.get("/health", response_model=HealthStatus)
def health() -> HealthStatus:
    """Return application health status."""
    return HealthStatus(status="ok")


@app.get("/metadata", response_model=Metadata)
def metadata(request: fastapi.Request) -> Metadata:
    """Return API metadata for clients."""
    base_url = str(request.base_url).rstrip("/")
    return Metadata(
        name=APP_NAME,
        version=APP_VERSION,
        docs=f"{base_url}/docs",
        redoc=f"{base_url}/redoc",
        health=f"{base_url}/health",
        repositories=f"{base_url}/repositories",
        developers=f"{base_url}/developers",
        cacheTtlSeconds=CACHE_TTL_SECONDS,
        supportedDateRanges=[date_range.value for date_range in AllowedDateRanges],
        supportedProgrammingLanguagesCount=len(AllowedProgrammingLanguages),
        supportedSpokenLanguagesCount=len(AllowedSpokenLanguages),
    )


@app.get("/repositories", response_model=list[Repository])
async def trending_repositories(
    since: AllowedDateRanges | None = None,
    spoken_language_code: AllowedSpokenLanguages | None = None,
) -> List[Repository]:
    """Returns data about trending repositories (all programming
    languages, cannot be specified on this endpoint).
    """
    payload = build_payload(since, spoken_language_code)
    return await get_repository_trends("https://github.com/trending", payload)


@app.get("/repositories/{prog_lang}", response_model=list[Repository])
async def trending_repositories_by_progr_language(
    prog_lang: AllowedProgrammingLanguages,
    since: AllowedDateRanges | None = None,
    spoken_language_code: AllowedSpokenLanguages | None = None,
) -> List[Repository]:
    """Returns data about trending repositories. A specific programming
    language can be added as path parameter to specify search.
    """
    payload = build_payload(since, spoken_language_code)
    url = f"https://github.com/trending/{prog_lang.value}"
    return await get_repository_trends(url, payload)


@app.get("/developers", response_model=list[Developer])
async def trending_developers(
    since: AllowedDateRanges | None = None,
) -> List[Developer]:
    """Returns data about trending developers (all programming languages,
    cannot be specified on this endpoint).
    """
    payload = build_payload(since)
    return await get_developer_trends("https://github.com/trending/developers", payload)


@app.get("/developers/{prog_lang}", response_model=list[Developer])
async def trending_developers_by_progr_language(
    prog_lang: AllowedProgrammingLanguages,
    since: AllowedDateRanges | None = None,
) -> List[Developer]:
    """Returns data about trending developers. A specific programming
    language can be added as path parameter to specify search.
    """
    payload = build_payload(since)
    url = f"https://github.com/trending/developers/{prog_lang.value}"
    return await get_developer_trends(url, payload)


if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")
