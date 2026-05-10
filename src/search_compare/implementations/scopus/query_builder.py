from __future__ import annotations

_VALID_FIELDS = {"TITLE-ABS-KEY", "TITLE", "ABS", "KEY"}

_VALID_DOC_TYPES = {
    "ar": "Article",
    "re": "Review",
    "cp": "Conference Paper",
    "ch": "Book Chapter",
    "bk": "Book",
    "ed": "Editorial",
    "le": "Letter",
    "no": "Note",
    "sh": "Short Survey",
}


class ScopusQueryBuilder:
    """Wraps a PICOC core expression with Scopus-specific filters.

    Implements QueryBackendProtocol structurally.
    """

    def __init__(self) -> None:
        self._field: str = "TITLE-ABS-KEY"
        self._year_min: int | None = None
        self._year_max: int | None = None
        self._language: str | None = None
        self._doc_type: str | None = None

    def configure(
        self,
        field: str = "TITLE-ABS-KEY",
        year_min: int | None = None,
        year_max: int | None = None,
        language: str | None = None,
        doc_type: str | None = None,
    ) -> ScopusQueryBuilder:
        if field not in _VALID_FIELDS:
            raise ValueError(f"Invalid field '{field}'. Valid options: {sorted(_VALID_FIELDS)}")
        if doc_type is not None and doc_type not in _VALID_DOC_TYPES:
            raise ValueError(f"Invalid doc_type '{doc_type}'. Valid options: {sorted(_VALID_DOC_TYPES)}")

        self._field = field
        self._year_min = year_min
        self._year_max = year_max
        self._language = language
        self._doc_type = doc_type
        return self

    def build(self, core: str) -> str:
        """Assembles the full Scopus query from a PICOC core expression and stored filters."""
        parts = [f"{self._field}({core})"]

        if self._year_min is not None:
            parts.append(f"PUBYEAR > {self._year_min}")
        if self._year_max is not None:
            parts.append(f"PUBYEAR < {self._year_max}")
        if self._language is not None:
            parts.append(f"LANGUAGE({self._language})")
        if self._doc_type is not None:
            parts.append(f"DOCTYPE({self._doc_type})")

        return " AND ".join(parts)
