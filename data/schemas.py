"""Schemas
===================
schemas for repositories/developers.
"""
# Copyright (c) 2021, Niklas Tiede.
# All rights reserved. Distributed under the MIT License.


from dataclasses import dataclass
from typing import Optional


@dataclass
class BuiltBy:
    """Data about developers that build the repository."""

    username: int
    url: str
    avatar: str


# schema of repository data:
@dataclass
class Repository:
    """Data of a trending repository."""

    rank: int
    username: str
    repository_name: str
    url: str
    since: str
    stars_since: int
    total_stars: int
    forks: int
    language: Optional[str] = None
    language_color: Optional[str] = None
    description: Optional[str] = None
    built_by: Optional[BuiltBy] = None


@dataclass
class PopularRepository:
    """Data about a trending developers popular repository."""

    repository_name: Optional[str] = None
    url: Optional[str] = None
    description: Optional[int] = None


# schema of developer data:
@dataclass
class Developer:
    """Data about a trending developer."""

    rank: int
    username: str
    url: str
    since: str
    avatar: Optional[str] = None
    name: Optional[str] = None
    popular_repository: Optional[PopularRepository] = None


# class TrendingData():
#     def __init__(self, url, html) -> None:
#         self.url = url
#         self.html = html

#     def request_html(self):
#         # self.url is used
#         return

#     def filter_articles(self):
#         pass

#     @classmethod
#     def from_repositories(cls, URL):
#         cls.request_html()
#         return ''

# # rs = RepoScraper()
# # rs(URL, )
# # TrendingData.from_developers(URL, )
# # TrendingData.from_repositories(URL, )


# data = TrendingData.from_developers()
# data = TrendingData.from_repositories()
