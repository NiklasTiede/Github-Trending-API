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
    URL: str
    proj_name: str
    since_data_range: str
    total_stars: int
    description: Optional[str] = None
    language: Optional[str] = None
    since_stars: Optional[int] = None


# schema of developer data:
@dataclass
class Developer:
    rank: int
    URL: str
    account_name: str
    since_data_range: str
    mini_avatar_URL: Optional[str] = None
    full_name: Optional[str] = None
    popular_repo: Optional[str] = None
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




# from typing import Optional

# @dataclass
# class Repository:
#     rank: int
#     URL: str
#     proj_name: str
#     since_data_range: str
#     total_stars: int
#     description: Optional[str] = None
#     language: Optional[str] = None
#     since_stars: Optional[int] = None

