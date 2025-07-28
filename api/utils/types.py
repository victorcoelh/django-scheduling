from typing import TypedDict


class JwtTokens(TypedDict):
    access: str
    refresh: str
