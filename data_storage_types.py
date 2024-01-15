"""Generic types for data storage."""

from typing import NotRequired, TypedDict


class UpdateDict(TypedDict):
    """Type for data for update own_data."""

    email_status: str
    email_result: str


class MainDataDict(TypedDict):
    """Type for main data in own_data."""

    id: str
    domains: list[str]
    email_status: NotRequired[str]
    email_result: NotRequired[str]
