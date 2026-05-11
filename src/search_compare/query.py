from __future__ import annotations

from .interfaces import SearchClientProtocol
from .models import SearchResult
from .picoc import PicocString


class Query:
    def __init__(
        self,
        string: str,
        client: SearchClientProtocol,
        picoc: PicocString | None = None,
    ) -> None:
        self.string = string
        self.client = client
        self.source_picoc = picoc

    def search(self, max_results: int = 500) -> SearchResult:
        return self.client.search(self.string, max_results)

    def __str__(self) -> str:
        return self.string

    def __repr__(self) -> str:
        return f"Query({self.string!r})"
