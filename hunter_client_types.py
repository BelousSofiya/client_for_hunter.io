"""Generic types."""

from typing import NotRequired, TypedDict


class MainDataDict(TypedDict):
    """Type for main data in own_data."""

    id: str
    domains: list[str]
    email_status: NotRequired[str]
    email_result: NotRequired[str]


class UpdateDict(TypedDict):
    """Type for data for update own_data."""

    email_status: str
    email_result: str


class ParserDict(TypedDict):
    """Type for returned data in parsers."""

    id: str
    domains: list[str]
