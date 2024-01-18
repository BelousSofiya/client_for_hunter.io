"""Generic types for HunterClient and HunterHelper."""

from typing import TypedDict


class EmailBaseData(TypedDict):
    """Type for returned data in parsers."""

    id: str
    domains: list[str]


class EmailAccessData(TypedDict):
    """Type for data for update own_data."""

    email_status: str
    email_result: str
