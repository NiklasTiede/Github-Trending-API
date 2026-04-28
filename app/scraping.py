"""Scraping
===================
Functions to scrape repository/developer data (HTML -> list of dicts).
"""
# Copyright (c) 2021, Niklas Tiede.
# All rights reserved. Distributed under the MIT License.
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import aiohttp
import bs4


async def get_request(
    *args: str,
    **kwargs: Any,
) -> Union[str, aiohttp.ClientConnectorError]:
    """Asynchronous GET request with aiohttp."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(*args, **kwargs) as resp:
                return await resp.text()
    except aiohttp.ClientConnectorError as cce:
        return cce


def filter_articles(raw_html: str) -> str:
    """Filters HTML out, which is not enclosed by article-tags.
    Beautifulsoup is inaccurate and slow when applied on a larger
    HTML string, this filtration fixes this.
    """
    raw_html_lst = raw_html.split("\n")

    # count number of article tags within the document (varies from 0 to 50):
    article_tags_count = 0
    tag = "article"
    for line in raw_html_lst:
        if tag in line:
            article_tags_count += 1

    # copy HTML enclosed by first and last article-tag:
    articles_arrays, is_article = [], False
    for line in raw_html_lst:
        if tag in line:
            article_tags_count -= 1
            is_article = True
        if is_article:
            articles_arrays.append(line)
        if not article_tags_count:
            is_article = False
    return "".join(articles_arrays)


def make_soup(articles_html: str) -> bs4.element.ResultSet:
    """HTML enclosed by article-tags is converted into a
    soup for further data extraction.
    """
    soup = bs4.BeautifulSoup(articles_html, "lxml")
    return soup.find_all("article", class_="Box-row")


def _parse_int(raw_text: Optional[str]) -> Optional[int]:
    """Extract the first integer from GitHub's formatted count labels."""
    if not raw_text:
        return None
    raw_number = raw_text.strip().split()[0].replace(",", "")
    try:
        return int(raw_number)
    except ValueError as missing_number:
        print(missing_number)
        return None


def _find_repository_link(match: bs4.element.Tag) -> Optional[bs4.element.Tag]:
    """Find the repository heading link in old h1 and current h2 markup."""
    headings = match.find_all(["h1", "h2"], class_="h3")
    for heading in headings:
        link = heading.find("a", href=True)
        if link and link["href"].count("/") >= 2:
            return link
    return None


def _find_repository_meta(match: bs4.element.Tag) -> bs4.element.Tag:
    """Find the section with language, stars, forks, and builders."""
    for section in match.find_all("div", class_="f6"):
        if (
            section.find("span", itemprop="programmingLanguage")
            or section.find(
                "a",
                href=lambda href: href and "stargazers" in href,
            )
            or "stars" in section.get_text(" ", strip=True)
        ):
            return section
    return match


def _find_link_by_href_part(
    section: bs4.element.Tag,
    href_parts: List[str],
) -> Optional[bs4.element.Tag]:
    """Find the first link whose href contains one of the given fragments."""
    for link in section.find_all("a", href=True):
        if any(href_part in link["href"] for href_part in href_parts):
            return link
    return None


def _find_built_section(section: bs4.element.Tag) -> Optional[bs4.element.Tag]:
    """Find the contributor avatar wrapper."""
    for span in section.find_all("span"):
        if "Built by" in span.get_text(" ", strip=True):
            return span
    return None


def scraping_repositories(
    matches: bs4.element.ResultSet,
    since: str,
) -> List[Dict[Any, Any]]:
    """Data about all trending repositories are extracted."""
    trending_repositories = []
    for rank, match in enumerate(matches):

        # description
        if match.p:
            description = match.p.get_text(strip=True)
        else:
            description = None

        # relative url
        repo_link = _find_repository_link(match)
        if not repo_link:
            continue
        rel_url = repo_link["href"]

        # absolute url:
        repo_url = "https://github.com" + rel_url

        # name of repo
        repository_name = rel_url.split("/")[-1]

        # author (username):
        username = rel_url.split("/")[-2]

        # language and color
        progr_language = match.find("span", itemprop="programmingLanguage")
        if progr_language:
            language = progr_language.get_text(strip=True)
            lang_color_tag = match.find("span", class_="repo-language-color")
            lang_color = (
                lang_color_tag["style"].split()[-1].rstrip(";")
                if lang_color_tag
                else None
            )
        else:
            lang_color, language = None, None

        stars_built_section = _find_repository_meta(match)

        # total stars:
        total_stars_link = _find_link_by_href_part(
            stars_built_section,
            ["stargazers"],
        )
        total_stars = _parse_int(
            total_stars_link.get_text(strip=True)
            if total_stars_link
            else None,
        )

        # forks
        forks_link = _find_link_by_href_part(
            stars_built_section,
            ["forks", "network/members"],
        )
        forks = _parse_int(
            forks_link.get_text(strip=True) if forks_link else None,
        )

        # stars in period
        raw_stars_since = stars_built_section.find(
            "span",
            class_="float-sm-right",
        )
        stars_since = _parse_int(
            raw_stars_since.get_text(strip=True) if raw_stars_since else None,
        )

        # builtby
        built_by = []
        built_section = _find_built_section(stars_built_section)
        if built_section:
            contributors = built_section.find_all("a", href=True)
            for contributor in contributors:
                if not contributor.img:
                    continue
                contr_data = {}
                contr_data["username"] = contributor["href"].strip("/")
                contr_data["url"] = "https://github.com" + contributor["href"]
                contr_data["avatar"] = contributor.img["src"]
                built_by.append(dict(contr_data))
        repositories = {
            "rank": rank + 1,
            "username": username,
            "repositoryName": repository_name,
            "url": repo_url,
            "description": description,
            "language": language,
            "languageColor": lang_color,
            "totalStars": total_stars,
            "forks": forks,
            "starsSince": stars_since,
            "since": since,
            "builtBy": built_by,
        }
        trending_repositories.append(repositories)
    return trending_repositories


def scraping_developers(
    matches: bs4.element.ResultSet,
    since: str,
) -> List[Dict[Any, Any]]:
    """Data about all trending developers are extracted."""
    all_trending_developers = []
    for rank, match in enumerate(matches):

        # relative url of developer
        rel_url = match.div.a["href"]

        # absolute url of developer
        dev_url = "https://github.com" + rel_url

        # username of developer
        username = rel_url.strip("/")

        # developers full name
        name = match.h1.a.get_text(strip=True) if match.h1.a else None

        # avatar url of developer
        avatar = match.img["src"] if match.img else None

        # data about developers popular repo:
        if match.article:
            raw_description = match.article.find(
                "div",
                class_="f6 color-text-secondary mt-1",
            )
            repo_description = (
                raw_description.get_text(
                    strip=True,
                )
                if raw_description
                else None
            )
            pop_repo = match.article.h1.a
            if pop_repo:
                repo_name = pop_repo.get_text(strip=True)
                repo_url = "https://github.com" + pop_repo["href"]
            else:
                repo_name = None
                repo_url = None
        else:
            repo_description = None
            repo_name = None
            repo_url = None

        one_developer = {
            "rank": rank + 1,
            "username": username,
            "name": name,
            "url": dev_url,
            "avatar": avatar,
            "since": since,
            "popularRepository": {
                "repositoryName": repo_name,
                "description": repo_description,
                "url": repo_url,
            },
        }
        all_trending_developers.append(one_developer)
    return all_trending_developers
