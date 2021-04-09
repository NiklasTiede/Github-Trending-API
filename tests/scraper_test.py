"""Functions for web scraping are tested
"""

import json

import pytest

from app.scraping import (
    filter_articles,
    make_soup,
    scraping_developers,
    scraping_repositories,
)


@pytest.mark.parametrize(
    "input_html,expected_json",
    [
        pytest.param(
            "data/repodata1.html",
            "data/repodata1.json",
            id="25 typescript repositories, normal data",
        ),
        pytest.param(
            "data/repodata2.html",
            "data/repodata2.json",
            id="4 repositories instead of 25",
        ),
        pytest.param(
            "data/repodata3.html",
            "data/repodata3.json",
            id="Missing description of one repository",
        ),
        pytest.param(
            "data/repodata4.html",
            "data/repodata4.json",
            id="""1 repo which contains neither total_stars nor
            forks and a repo which has no since_stars""",
        ),
    ],
)
def test_repository_scraping(input_html, expected_json):
    """Tests functions which scrape data about repositories from HTML."""
    with open(expected_json) as file:
        correct_repo_json = json.loads(file.read())
    with open(input_html) as file:
        raw_html = file.read()
    articles_html = filter_articles(raw_html)
    soup = make_soup(articles_html)
    repo_json = scraping_repositories(soup, since="daily")
    assert repo_json == correct_repo_json


@pytest.mark.parametrize(
    "input_html,expected_json",
    [
        pytest.param(
            "data/devdata1.html",
            "data/devdata1.json",
            id="25 developers, normal data.",
        ),
        pytest.param(
            "data/devdata2.html",
            "data/devdata2.json",
            id="1 missing popular repository of developer.",
        ),
        pytest.param(
            "data/devdata3.html",
            "data/devdata3.json",
            id="15 developers, description of 1 popular repository is missing.",
        ),
    ],
)
def test_developer_scraping(input_html, expected_json):
    """Tests functions which scrape data about developers from HTML."""
    with open(expected_json) as file:
        correct_repo_json = json.loads(file.read())
    with open(input_html) as file:
        raw_html = file.read()
    articles_html = filter_articles(raw_html)
    soup = make_soup(articles_html)
    repo_json = scraping_developers(soup, since="daily")
    assert repo_json == correct_repo_json
