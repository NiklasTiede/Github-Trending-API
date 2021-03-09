<p align="center">
  <img  align="center" height="130" src="docs/spasco_heading.png" />
  <h1 align="center">Github-Trending-API</h1>
<p>

[comment]: <> (# https://shields.io/)

[comment]: <> ([![license]&#40;https://img.shields.io/conda/&#41;]&#40;&#41; # https://shields.io/category/license)

[comment]: <> ([![codecov]&#40;https://img.shields.io/&#41;]&#40;https://codecov.io/&#41; # https://shields.io/category/coverage)

[comment]: <> (![total lines]&#40;https://img.shields.io/&#41; # https://shields.io/category/size)

...written in Python!

The motivation behind this API for me was to learn web scraping and how to create an API. It is based on the idea of [github-trending-api](https://github.com/huchenme/github-trending-api) except that this one is written in python and it is available :wink:!

This project runs on Python 3.9 and uses...

- beautifulsoup4 | scraping
- aiohttp | async GET requests
- fastAPI | web framework
- uvicorn | ASGI server


<h1 id="example" ><img src="docs/example.png" width="34px"#> Examples</h1>

FastAPI has a fantastic built-in documentation, it can be reached on the `/docs` or `/redocs` route.

Two examples to visualize how a repositories/developers reponse body looks like:

```json
❯ http -b 0.0.0.0:8000

[
  {
    "rank": 1,
    "URL": "https://github.com/gskinnerTeam/flutter-folio",
    "name": "flutter-folio",
    "description": "A platform adaptive Flutter app for desktop, mobile and web.",
    "language": "Dart",
    "since_stars": 279,
    "since_data_range": "daily",
    "total_stars": 1001
  },
  {
    "rank": 2,
    "URL": "https://github.com/flutter/flutter",
    "name": "flutter",
    "description": "Flutter makes it easy and fast to build beautiful apps for mobile and beyond.",
    "language": "Dart",
    "since_stars": 203,
    "since_data_range": "daily",
    "total_stars": 114645
  },
...
]
```

Information about developers can also be requested:

```json
❯ http -b 0.0.0.0:8000/developers

[
  {
    "rank": 1,
    "URL": "https://github.com/oblador",
    "account_name": "oblador",
    "full_name": "Joel Arvidsson",
    "mini_avatar_URL": "https://avatars.githubusercontent.com/u/378279?s=96&v=4",
    "popular_repo": "react-native-vector-icons",
    "popular_repo_url": "https://github.com/oblador/react-native-vector-icons",
    "repo_description": "Customizable Icons for React Native with support for image source and full styling.",
    "since_data_range": "daily"
  },
  {
    "rank": 2,
    "URL": "https://github.com/willdurand",
    "account_name": "willdurand",
    "full_name": "William Durand",
    "mini_avatar_URL": "https://avatars.githubusercontent.com/u/217628?s=96&v=4",
    "popular_repo": "Negotiation",
    "popular_repo_url": "https://github.com/willdurand/Negotiation",
    "repo_description": "Content Negotiation tools for PHP.",
    "since_data_range": "daily"
  },
...
]
```

<h1 id="how-to-use-spasco" ><img src="docs/tutorial.png" width="27px"#> How to use Github-Trending-API</h1>

Path and Query parameters:


```console
❯ spasco --help
usage: spasco [-s [search_value]] [-n [new_value]] [-p [pattern_only]] 

```
