"""Github-Trending-API
===================
API serves data about trending github repositories/developers.
"""
# Copyright (c) 2021, Niklas Tiede.
# All rights reserved. Distributed under the MIT License.

import requests
from fastapi import FastAPI
import uvicorn

from allowed_parameters import (
    AllowedDateRanges, 
    AllowedProgrammingLanguages,
    AllowedSpokenLanguages
    )
from scraper import (
    dev_extraction, 
    filter_articles, 
    repo_extraction,
    soup_matches
    )

app = FastAPI()



@app.get("/about")
def about():
    """ Returns information on how to use the API. """
    # return {"this": "is"}
    return "This API serves information about trending repositories/developers. Docs can be called by adding '/docs' to the URL"


@app.get("/")
def repositories(since: AllowedDateRanges = None, spoken_lang: AllowedSpokenLanguages = None):
    """ Returns data about trending repositories (all programming languages). """
    payload = {}
    if since:
        since_value = since._value_
        payload["since"] = since._value_
    else:
        since_value = "daily"
    if spoken_lang:
        payload["spoken_lang"] = spoken_lang._value_
    resp = requests.get(
        "https://github.com/trending", params=payload)
    articles_html = filter_articles(resp.text)
    matches = soup_matches(articles_html)
    data = repo_extraction(matches, since=since_value)
    return data


@app.get("/developers")
def developers(since: AllowedDateRanges = None):
    """ Returns data about trending developers (all programming languages). """
    payload = {}
    if since:
        since_value = since._value_
        payload["since"] = since._value_
    else:
        since_value = "daily"
    resp = requests.get(
        "https://github.com/trending/developers", params=payload)
    articles_html = filter_articles(resp.text)
    matches = soup_matches(articles_html)
    data = dev_extraction(matches, since=since_value)
    return data


@app.get("/{prog_lang}")
def repositories_lang_spec(prog_lang: AllowedProgrammingLanguages, since: AllowedDateRanges = None, spoken_lang: AllowedSpokenLanguages = None):
    """ Returns data about trending repositories. A specific programming language can be added as path parameter to specify search. """
    payload = {}
    if since:
        since_value = since._value_
        payload["since"] = since_value
    else:
        since_value = "daily"
    if spoken_lang:
        payload["spoken_lang"] = spoken_lang._value_
    resp = requests.get(
        f"https://github.com/trending/{prog_lang}", params=payload)
    articles_html = filter_articles(resp.text)
    matches = soup_matches(articles_html)
    data = repo_extraction(matches, since=since_value)
    return data


@app.get("/developers/{prog_lang}")
def developers_lang_spec(prog_lang: AllowedProgrammingLanguages, since: AllowedDateRanges = None):
    """ Returns data about trending developers. A specific programming language 
    can be added as path parameter to specify search.  
    """
    payload = {}
    if since:
        since_value = since._value_
        payload["since"] = since_value
    else:
        since_value = "daily"
    resp = requests.get(
        f"https://github.com/trending/developers/{prog_lang}", params=payload)
    articles_html = filter_articles(resp.text)
    matches = soup_matches(articles_html)
    data = dev_extraction(matches, since=since_value)
    return data


if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")
