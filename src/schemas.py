

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
