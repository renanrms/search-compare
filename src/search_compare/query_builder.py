from __future__ import annotations

from .interfaces import QueryBackendProtocol

_PICOC_COMPONENTS = ("population", "intervention",
                     "comparison", "outcome", "context")


class QueryBuilder:
    """Builds a PICOC-based search query and delegates final formatting to a backend."""

    def __init__(self, backend: QueryBackendProtocol) -> None:
        self._backend = backend
        self._components: dict[str, list[str]] = {
            c: [] for c in _PICOC_COMPONENTS}

    def population(self, *terms: str) -> QueryBuilder:
        self._components["population"] = list(terms)
        return self

    def intervention(self, *terms: str) -> QueryBuilder:
        self._components["intervention"] = list(terms)
        return self

    def comparison(self, *terms: str) -> QueryBuilder:
        self._components["comparison"] = list(terms)
        return self

    def outcome(self, *terms: str) -> QueryBuilder:
        self._components["outcome"] = list(terms)
        return self

    def context(self, *terms: str) -> QueryBuilder:
        self._components["context"] = list(terms)
        return self

    def build_core(self) -> str:
        """Returns the pure boolean expression of PICOC terms without any backend-specific syntax."""
        parts = []
        for component in _PICOC_COMPONENTS:
            terms = self._components[component]
            if terms:
                inner = " OR ".join(terms)
                parts.append(f"({inner})")
        return " AND ".join(parts)

    def build(self) -> str:
        """Returns the full query string by delegating to the configured backend."""
        return self._backend.build(self.build_core())
