
<h1 align="center">Github Trending API</h1>


[comment]: <> (# https://shields.io/)

[comment]: <> ([![license]&#40;https://img.shields.io/conda/&#41;]&#40;&#41; # https://shields.io/category/license)

[comment]: <> ([![codecov]&#40;https://img.shields.io/&#41;]&#40;https://codecov.io/&#41; # https://shields.io/category/coverage)

[comment]: <> (![total lines]&#40;https://img.shields.io/&#41; # https://shields.io/category/size)

<p align="center">
...written in Python!
</p>

The motivation behind this API for me was to learn web scraping and how to create an API. It is based on the idea of [github-trending-api](https://github.com/huchenme/github-trending-api) except that this one is written in python and it is available :wink:!

This project runs on Python 3.9 and uses...

- beautifulsoup4 | *scraping*
- aiohttp | *async GET requests*
- fastAPI | *web framework*
- uvicorn | *ASGI server*


<h1 id="example" ><img src="docs/example.png" width="34px"#> Examples</h1>

FastAPI has a fantastic built-in documentation, it can be reached on the `/docs` or `/redocs` route. 

Two examples to visualize how a repositories/developers reponse body looks like:

repositories

```json
❯ http -b http://gh-trending.com/repositories
[
  {
    "rank": 1,
    "username": "sherlock-project",
    "repositoryName": "sherlock",
    "url": "https://github.com/sherlock-project/sherlock",
    "description": "Hunt down social media accounts by username across social networks",
    "language": "Python",
    "languageColor": "#3572A5",
    "totalStars": 21977,
    "forks": 2214,
    "StarsSince": 462,
    "since": "daily",
    "builtBy": [
      {
        "username": "hoadlck",
        "url": "https://github.com/hoadlck",
        "avatar": "https://avatars.githubusercontent.com/u/1666888?s=40&v=4"
      },
      {
        "username": "sdushantha",
        "url": "https://github.com/sdushantha",
        "avatar": "https://avatars.githubusercontent.com/u/27065646?s=40&v=4"
      },
      ...
    ]
  },
...
]
```

developers:

```json
❯ http -b http://gh-trending.com/repositories
[
  {
    "rank": 1,
    "username": "felangel",
    "name": "Felix Angelov",
    "url": "https://github.com/felangel",
    "avatar": "https://avatars.githubusercontent.com/u/8855632?s=96&v=4",
    "since": "daily",
    "popularRepository": {
      "repositoryName": "bloc",
      "description": "A predictable state management library that helps implement the BLoC design pattern",
      "url": "https://github.com/felangel/bloc"
    }
  },
...
]
```

<h1 id="how-to-use-spasco" ><img src="docs/tutorial.png" width="27px"#> How to use Github-Trending-API</h1>

fastAPI offers a nice documentation, so visit it and explore the API.

The endpoints are similar to the routes on github:

a path parameter is used for the programming language
a query parameter is used for the date range and the spoken language

example:
repositories?since=weekly&spoken_lang=en  -> returns all repos with a weekly daterange and english language
repositories/python?since=monthly  -> return als repos using python, with a monthly daterange.



same applies for the developers endpoint, but here you cannot select the spoken language.

http://gh-trending.com/developers?since=weekly&spoken_lang=en




Path and Query parameters:


```console
❯ spasco --help
usage: spasco [-s [search_value]] [-n [new_value]] [-p [pattern_only]] 

```
