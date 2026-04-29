"""API response schemas."""
from pydantic import BaseModel


class HealthStatus(BaseModel):
    """Health check response data."""

    status: str


class Contributor(BaseModel):
    """Repository contributor data."""

    username: str
    url: str
    avatar: str


class Repository(BaseModel):
    """Trending repository response data."""

    rank: int
    username: str
    repositoryName: str
    url: str
    description: str | None
    language: str | None
    languageColor: str | None
    totalStars: int | None
    forks: int | None
    starsSince: int | None
    since: str
    builtBy: list[Contributor]


class PopularRepository(BaseModel):
    """Trending developer popular repository data."""

    repositoryName: str | None
    description: str | None
    url: str | None


class Developer(BaseModel):
    """Trending developer response data."""

    rank: int
    username: str
    name: str | None
    url: str
    avatar: str | None
    since: str
    popularRepository: PopularRepository
