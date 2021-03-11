"""Schemas
===================
schemas for repositories/developers.
"""
# Copyright (c) 2021, Niklas Tiede.
# All rights reserved. Distributed under the MIT License.


from typing import Optional
from dataclasses import dataclass


# schema of repository data:
@dataclass
class Repository:
    rank: int
    username: str
    repositoryName: str
    url: str
    since: str
    StarsSince: int
    totalStars: int
    forks: int
    language: Optional[str] = None
    languageColor: Optional[str] = None
    description: Optional[str] = None
    builtBy: Optional[BuiltBy] = None


@dataclass
class BuiltBy:
    username: int
    url: str
    avatar: str


# schema of developer data:
@dataclass
class Developer:
    rank: int
    account_name: str
    URL: str
    since_data_range: str
    full_name: Optional[str] = None
    mini_avatar_URL: Optional[str] = None
    popular_repo: Optional[str] = None


@dataclass
class popularRepository:
    popular_repo_url: Optional[str] = None
    repo_description: Optional[int] = None


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
