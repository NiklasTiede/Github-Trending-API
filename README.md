
<h1 align="center">Github Trending API</h1>


[comment]: <> (# https://shields.io/)

[comment]: <> ([![license]&#40;https://img.shields.io/conda/&#41;]&#40;&#41; # https://shields.io/category/license)

[comment]: <> ([![codecov]&#40;https://img.shields.io/&#41;]&#40;https://codecov.io/&#41; # https://shields.io/category/coverage)

[comment]: <> (![total lines]&#40;https://img.shields.io/&#41; # https://shields.io/category/size)

<p align="center">
...written in Python!
</p>

The motivation behind this API for me was to learn web scraping and how to create an API. It is based on the idea of the [github-trending-api](https://github.com/huchenme/github-trending-api) except that this one is written in python and it is available :wink:!

This project runs on Python 3.9 and uses...

- beautifulsoup4 | *scraping*
- aiohttp | *async GET requests*
- fastAPI | *web framework*
- uvicorn | *ASGI server*


<h1 id="example" ><img src="docs/example.png" width="34px"#> Examples</h1>

FastAPI has a fantastic built-in documentation, it can be reached on the `/docs` or `/redocs` route. Data about trending repositories/developers are provided via the `/repositories` and `/developers` routes. 

Here are two examples to illustrate the data you can request from this API. 

### An Array of Trending Repositories

```json
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
      ...
    ]
  },
...
]
```

### An Array of Trending Developers

```json
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

<h1 id="how-to-use-spasco" ><img src="docs/tutorial.png" width="27px"#> How to</h1>

FastAPI provides a nice built-in documentation, so feel free to visit and explore the [API](https:gh-trending.com) by yourself. The endpoints are similar to the routes on github:

- a path parameter for the programming language can be used to limit the scope of the search to this language
- a query parameter for the date range (`since`) let you select the trending projects within the specified period of time (daily, weekly or monthly)
- moreover, repositories can be limited to a spoken language (`spoken_lang`)

Here are some examples. Repositories can be queried for 3 parameters...

| example                                               | pogramming lang    | date range         | spoken lang        |
| ----------------------------------------------------- | ------------------ | ------------------ | ------------------ |
| [/repositories](https://gh-trending.com/repositories) | :x:                | :x:                | :x:                |
| [/repositories?since=weekly]()                        | :x:                | :heavy_check_mark: | :x:                |
| [/repositories/python]()                              | :heavy_check_mark: | :x:                | :x:                |
| [/repositories/python?since=monthly]()                | :heavy_check_mark: | :heavy_check_mark: | :x:                |
| [/repositories/python?since=weekly&spoken_lang=zh]()  | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |

...whereas developers can only be queried for 2 parameters.

| example                          | pogramming lang    | date range         |
| -------------------------------- | ------------------ | ------------------ |
| [/developers]()                  | :x:                | :x:                |
| [/developers?since=weekly]()     | :x:                | :heavy_check_mark: |
| [/developers/c++]()              | :heavy_check_mark: | :x:                |
| [/developers/c++?since=weekly]() | :heavy_check_mark: | :heavy_check_mark: |

