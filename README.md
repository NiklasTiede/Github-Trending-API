<p align="center">
<img src="docs/trending.png" width="500">
</p>

<p align="center">
...written in Python!
</p>

<p id="Icons" align="center">

  <a alt="Uptime Robot Status" href="https://stats.uptimerobot.com/5KMN7t0E5M">
    <img src="https://img.shields.io/uptimerobot/status/m787484641-cc42e583e4fe0a25564a29e1" />
  </a>

  <!-- <a alt="dockr build" href="">
    <img src="" />
  </a> -->

  <a alt="Issues" href="">
    <img src="https://img.shields.io/github/issues/NiklasTiede/Github-Trending-API" />
  </a>

  <!-- <a alt="Github Release" href="">
    <img src="" />
  </a> -->

  <!-- <a alt="codecov" href="">
    <img src="" />
  </a> -->

  <a alt="License" href="">
    <img src="https://img.shields.io/github/license/NiklasTiede/Github-Trending-API" />
  </a>

</p>



<h1><img src="docs/example.png" width="30px"#> Examples</h1>

Data you can retrieve from this API. 

## Trending Repositories

```json
❯ curl -X GET "https://gh-trending-api.herokuapp.com/developers" -H  "accept: application/json"
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

## Trending Developers

```json
❯ curl -X GET "https://gh-trending-api.herokuapp.com/repositories" -H  "accept: application/json"
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

---

The motivation behind this API for me was to learn web scraping and how to create an API. It is based on the idea of the [github-trending-api](https://github.com/huchenme/github-trending-api) except that this one is written in python and it is available :wink:!

This project runs on Python 3.9 and uses...

- beautifulsoup4 | *scraping*
- aiohttp | *async GET requests*
- fastAPI | *web framework*
- uvicorn | *ASGI server*

See [UptimeRobot](https://stats.uptimerobot.com/5KMN7t0E5M) to ensure yourself that this API is reliable.


<h1><img src="docs/tutorial.png" width="25px"#> How to Use</h1>

FastAPI has a fantastic built-in documentation, so feel free to visit and explore the [API](https://gh-trending-api.herokuapp.com) by yourself. Data about trending repositories/developers are provided via the `/repositories` and `/developers` routes. The endpoints are similar to the routes on github. 

- a path parameter for the programming language can be used to limit the scope of the search to this language
- a query parameter for the date range (`since`) let you select the trending projects within the specified period of time (daily, weekly or monthly)
- moreover, repositories can be limited to a spoken language (`spoken_lang`)

Here are some examples. Repositories can be queried for 3 parameters...

| example                                                                                                                                   | pogramming lang    | date range         | spoken lang        |
| ----------------------------------------------------------------------------------------------------------------------------------------- | ------------------ | ------------------ | ------------------ |
| [/repositories](https://gh-trending-api.herokuapp.com/repositories)                                                                       | :x:                | :x:                | :x:                |
| [/repositories?since=weekly](https://gh-trending-api.herokuapp.com/repositories?since=weekly)                                             | :x:                | :heavy_check_mark: | :x:                |
| [/repositories/python](https://gh-trending-api.herokuapp.com/repositories/python)                                                         | :heavy_check_mark: | :x:                | :x:                |
| [/repositories/python?since=monthly](https://gh-trending-api.herokuapp.com/repositories/python?since=monthly)                             | :heavy_check_mark: | :heavy_check_mark: | :x:                |
| [/repositories/python?since=weekly&spoken_lang=zh](https://gh-trending-api.herokuapp.com/repositories/python?since=weekly&spoken_lang=zh) | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |

...whereas developers can only be queried for 2 parameters.

| example                                                                                           | pogramming lang    | date range         |
| ------------------------------------------------------------------------------------------------- | ------------------ | ------------------ |
| [/developers](https://gh-trending-api.herokuapp.com/developers)                                   | :x:                | :x:                |
| [/developers?since=weekly](https://gh-trending-api.herokuapp.com/developers?since=weekly)         | :x:                | :heavy_check_mark: |
| [/developers/c++](https://gh-trending-api.herokuapp.com/developers/c++)                           | :heavy_check_mark: | :x:                |
| [/developers/c++?since=weekly](https://gh-trending-api.herokuapp.com/developers/c++?since=weekly) | :heavy_check_mark: | :heavy_check_mark: |

## Running from Source

YOu can easily clone the project and run it locally:

```
❯ git clone
❯ cd Github-Trending-API
❯ uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
```

Or pull the [docker image](https://hub.docker.com/r/niklastiede/github-trending-api) and run it:

```
❯ docker pull niklastiede/github-trending-api:1.0.0
❯ docker run -p 5000:5000 niklastiede/github-trending-api:1.0.0
```

