"""Generic types for HunterClient and HunterHelper."""

from typing import TypedDict


class ParserDict(TypedDict):
    """Type for returned data in parsers."""

    id: str
    domains: list[str]
