
from enum import Enum
from fastapi import FastAPI, params
from typing import Optional
from pprint import pprint

import requests
from condensed import soup_matches, filter_articles, repo_extraction, dev_extraction

from allowed_parameters import AllowedProgrammingLanguages, AllowedDateRanges, AllowedSpokenLanguages


app = FastAPI()


# # https://github.com/trending?since=daily

# @app.get("/repositories")
# def repositories():
#     """ Returns data about trending daily repositories regardless
#     of spoken language or programming language. """
#     URL = "https://github.com/trending"

#     return "data"

# def url_generator(prog_lang=None, since="daily", spoken_lang=None):
#     base_url = "https://github.com/trending"

#     base_url = f"https://github.com/trending/{prog_lang}"
#     base_url = f"https://github.com/trending"
#     base_url = f"https://github.com/trending"

#     return base_url + url_end


@app.get("/repositories")
def repositories(since: AllowedDateRanges = None, spoken_lang: AllowedSpokenLanguages = None):
    """ Returns data about trending repos. Search can be more specific. """

    payload = {}
    if since:
        payload["since"] = since._value_
    if spoken_lang:
        payload["spoken_lang"] = spoken_lang._value_

    resp = requests.get(
        "https://github.com/trending", params=payload)

    articles_html = filter_articles(resp.text)
    matches = soup_matches(articles_html)
    data = repo_extraction(matches, since=since._value_)
    return data

# @app.get("/developers")
# def repositories(since: AllowedDateRanges = None):
#     """ Returns data about trending repos. Search can be more specific. """

#     payload = {}
#     if since:
#         payload["since"] = since._value_

#     resp = requests.get(
#         "https://github.com/trending/developers", params=payload)

#     articles_html = filter_articles(resp.text)
#     matches = soup_matches(articles_html)
#     data = dev_extraction(matches)
#     return data


# @app.get("/repositories/{prog_lang}")
# def repositories(prog_lang: AllowedProgrammingLanguages, since: AllowedDateRanges = None, spoken_lang: AllowedSpokenLanguages = None):
#     """ Returns data about trending repos. Search can be more specific. """

#     payload = {}
#     if since:
#         payload["since"] = since._value_
#     if spoken_lang:
#         payload["spoken_lang"] = spoken_lang._value_

#     print('payload:', payload)
#     resp = requests.get(
#         f"https://github.com/trending/{prog_lang}", params=payload)

#     articles_html = filter_articles(resp.text)
#     matches = soup_matches(articles_html)
#     data = repo_extraction(matches, since=since._value_)
#     return data


# @app.get("/developers/{prog_lang}")
# def repositories(prog_lang: AllowedProgrammingLanguages, since: AllowedDateRanges = None):
#     """ Returns data about trending repos. Search can be more specific. """

#     payload = {}
#     if AllowedDateRanges:
#         payload["since"] = since._value_

#     resp = requests.get(
#         f"https://github.com/trending/{prog_lang}", params=payload)

#     articles_html = filter_articles(resp.text)
#     matches = soup_matches(articles_html)
#     data = dev_extraction(matches, since='daily')
#     return data


# @app.get("/about")
# def about():
#     """ Returns information on how to use the API. """
#     return "This API serves information about trending repositories/developers."

# @app.get("/")
# def index(limit: int = 2, sort: Optional[bool] = None):
#     """ Returns all data. """
#     if sort:
#         return f"some sorted data, sort: {sort}"
#     if limit and limit <= len(data):
#         return data[:limit]
#     else:
#         return data

# @app.get("/{ID}")
# def index(ID: int):
#     """ Returns specific datapoint by ID. """
#     for datapoint in data:
#         if datapoint.get("ID") == ID:
#             return datapoint
