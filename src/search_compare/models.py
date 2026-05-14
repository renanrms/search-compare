from dataclasses import dataclass, field
from typing import NamedTuple

import pandas as pd
from pandas.io.formats.style import Styler

_TABLE_STYLES: list[dict[str, str | list[tuple[str, str]]]] = [
    {"selector": "th", "props": [("text-align", "left")]}
]


def _apply_style(df: pd.DataFrame) -> Styler:
    return (
        df.style
        .hide()
        .set_properties(**{"text-align": "left"})
        .set_table_styles(_TABLE_STYLES)  # type: ignore[arg-type]
    )


_ALL_COLS = ["eid", "year", "title", "source", "authors", "doi"]


def _docs_to_df(documents: "list[Document]", columns: list[str] | None = None) -> Styler:
    rows = [
        {
            "eid": doc.eid,
            "year": doc.year,
            "title": doc.title,
            "source": doc.source,
            "authors": "; ".join(doc.authors),
            "doi": doc.doi,
        }
        for doc in documents
    ]
    df = pd.DataFrame(rows, columns=_ALL_COLS).sort_values("year", ascending=False, na_position="last")
    if columns:
        df = df[columns]
    return _apply_style(df)


@dataclass
class ControlArticle:
    title: str
    year: int | None = None
    eid: str | None = None  # populated by SearchManager.check()


@dataclass
class ValidationResult:
    found: list[ControlArticle]
    not_found: list[ControlArticle]

    def summary(self) -> str:
        total = len(self.found) + len(self.not_found)
        return (
            f"Encontrados    : {len(self.found)}/{total}\n"
            f"Não encontrados: {len(self.not_found)}/{total}"
        )


class ComparisonDataFrames(NamedTuple):
    common: Styler
    only_in_1: Styler
    only_in_2: Styler


@dataclass
class Document:
    eid: str
    title: str
    authors: list[str]
    year: int | None
    doi: str | None
    source: str | None


@dataclass
class SearchResult:
    query: str
    documents: list[Document]
    total_count: int

    def __len__(self) -> int:
        return len(self.documents)


_SHOW_COLS = ["year", "title", "authors", "source"]


@dataclass
class ComparisonResult:
    result1: SearchResult
    result2: SearchResult
    common: list[Document] = field(default_factory=list)
    only_in_1: list[Document] = field(default_factory=list)
    only_in_2: list[Document] = field(default_factory=list)

    def to_dataframes(self) -> ComparisonDataFrames:
        return ComparisonDataFrames(
            common=_docs_to_df(self.common),
            only_in_1=_docs_to_df(self.only_in_1),
            only_in_2=_docs_to_df(self.only_in_2),
        )

    def show(self) -> None:
        from IPython.display import Markdown, display

        sections = [
            (f"Documentos em comum ({len(self.common)})", self.common),
            (f"Apenas na query 1 ({len(self.only_in_1)})", self.only_in_1),
            (f"Apenas na query 2 ({len(self.only_in_2)})", self.only_in_2),
        ]
        for label, docs in sections:
            display(Markdown(f"### {label}"))
            display(_docs_to_df(docs, columns=_SHOW_COLS))

    def summary(self) -> str:
        return (
            f"Total in query 1 : {len(self.result1)}\n"
            f"Total in query 2 : {len(self.result2)}\n"
            f"Common           : {len(self.common)}\n"
            f"Only in query 1  : {len(self.only_in_1)}\n"
            f"Only in query 2  : {len(self.only_in_2)}"
        )
