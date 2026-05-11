from typing import Protocol

from ..models import SearchResult


class SearchClientProtocol(Protocol):
    def search(self, query: str, max_results: int = ...) -> SearchResult: ...
