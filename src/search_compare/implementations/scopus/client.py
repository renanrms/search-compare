from __future__ import annotations

import time

import requests

from .config import get_api_key
from ...models import Document, SearchResult
from ...picoc import PicocString
from ...query import Query

_VALID_FIELDS = {"TITLE-ABS-KEY", "TITLE", "ABS", "KEY"}
_VALID_DOC_TYPES = {"ar", "re", "cp", "ch", "bk", "ed", "le", "no", "sh"}

_BASE_URL = "https://api.elsevier.com/content/search/scopus"
_PAGE_SIZE = 25


class ScopusClient:
    """Client for the Scopus Search API."""

    def __init__(self, api_key: str | None = None) -> None:
        self._api_key = api_key or get_api_key()
        self._headers = {
            "X-ELS-APIKey": self._api_key,
            "Accept": "application/json",
        }

    def build_query(
        self,
        core: str | PicocString,
        field: str = "TITLE-ABS-KEY",
        year_min: int | None = None,
        year_max: int | None = None,
        language: str | None = None,
        doc_type: str | list[str] | None = None,
    ) -> Query:
        if field not in _VALID_FIELDS:
            raise ValueError(f"Invalid field '{field}'. Valid options: {sorted(_VALID_FIELDS)}")

        doc_types = [doc_type] if isinstance(doc_type, str) else (doc_type or [])
        invalid = [t for t in doc_types if t not in _VALID_DOC_TYPES]
        if invalid:
            raise ValueError(f"Invalid doc_type {invalid}. Valid options: {sorted(_VALID_DOC_TYPES)}")

        core_str = core.build() if isinstance(core, PicocString) else core
        parts = [f"{field}({core_str})"]

        if year_min is not None:
            parts.append(f"PUBYEAR > {year_min}")
        if year_max is not None:
            parts.append(f"PUBYEAR < {year_max}")
        if language is not None:
            parts.append(f"LANGUAGE({language})")
        if doc_types:
            parts.append(f"DOCTYPE({' OR '.join(doc_types)})")

        picoc_ref = core if isinstance(core, PicocString) else None
        return Query(" AND ".join(parts), self, picoc=picoc_ref)

    def search(self, query: str, max_results: int = 500) -> SearchResult:
        """Executes a Scopus search and returns a SearchResult.

        Args:
            query: Full Scopus query string.
            max_results: Maximum number of documents to retrieve. The actual
                total available is reported in SearchResult.total_count.
        """
        entries: list[dict] = []
        total_count = 0
        start = 0

        while start < max_results:
            count = min(_PAGE_SIZE, max_results - start)
            params = {"query": query, "view": "STANDARD", "count": count, "start": start}

            response = requests.get(_BASE_URL, headers=self._headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            results = data.get("search-results", {})
            if start == 0:
                total_count = int(results.get("opensearch:totalResults", 0))

            page_entries = results.get("entry", [])
            if not page_entries or page_entries == [{"@_fa": "true", "error": "Result set was empty"}]:
                break

            entries.extend(page_entries)

            if len(page_entries) < _PAGE_SIZE:
                break

            start += len(page_entries)
            time.sleep(0.1)

        return SearchResult(
            query=query,
            documents=[_parse_entry(e) for e in entries],
            total_count=total_count,
        )


def _parse_entry(entry: dict) -> Document:
    authors: list[str] = []
    for author in entry.get("author", []):
        given = author.get("given-name", "")
        surname = author.get("surname", "")
        name = f"{given} {surname}".strip() if given or surname else author.get("authname", "")
        if name:
            authors.append(name)

    if not authors and entry.get("dc:creator"):
        authors = [entry["dc:creator"]]

    year: int | None = None
    cover_date = entry.get("prism:coverDate", "")
    if cover_date:
        try:
            year = int(cover_date[:4])
        except (ValueError, IndexError):
            pass

    return Document(
        eid=entry.get("eid", ""),
        title=entry.get("dc:title", ""),
        authors=authors,
        year=year,
        doi=entry.get("prism:doi") or None,
        source=entry.get("prism:publicationName") or None,
    )
