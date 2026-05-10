from typing import Protocol


class QueryBackendProtocol(Protocol):
    def build(self, core: str) -> str: ...
