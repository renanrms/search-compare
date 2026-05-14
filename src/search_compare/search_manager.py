from __future__ import annotations

import pandas as pd

from .interfaces import SearchClientProtocol
from .models import (
    ControlArticle,
    SearchResult,
    ValidationResult,
    _apply_style,
    _SHOW_COLS,
    _docs_to_df,
)
from .comparison import compare


class SearchManager:
    def __init__(self, client: SearchClientProtocol) -> None:
        self._client = client
        self._controls: list[ControlArticle] = []

    def set_control_articles(self, articles: list[ControlArticle]) -> None:
        self._controls = articles

    def check_control_articles_exists(self) -> ValidationResult:
        """Searches Scopus for each control article and stores the found EID."""
        found: list[ControlArticle] = []
        not_found: list[ControlArticle] = []

        for article in self._controls:
            query = f'TITLE("{article.title}")'
            if article.year:
                query += f" AND PUBYEAR IS {article.year}"
            result = self._client.search(query, max_results=3)
            if result.documents:
                article.eid = result.documents[0].eid
                found.append(article)
            else:
                not_found.append(article)
                print(
                    f"✗ Artigo não encontrado na base: '{article.title}' ({article.year})\n"
                    "Verifique os dados inseridos e a existência do artigo na base de dados."
                )

        return ValidationResult(found=found, not_found=not_found)

    def compare(self, result1: SearchResult, result2: SearchResult) -> None:
        from IPython.display import Markdown, display

        diff = compare(result1, result2)
        eids1 = {doc.eid for doc in result1.documents}
        eids2 = {doc.eid for doc in result2.documents}

        # --- Artigos de controle (primeiro) ---
        if self._controls:
            rows = []
            for article in self._controls:
                if article.eid is None:
                    in1 = in2 = "Não encontrado na base"
                else:
                    in1 = "✓" if article.eid in eids1 else "✗"
                    in2 = "✓" if article.eid in eids2 else "✗"
                rows.append(
                    {"year": article.year, "title": article.title, "query 1": in1, "query 2": in2})

            total = len(self._controls)
            found = sum(1 for a in self._controls if a.eid is not None)
            df = pd.DataFrame(rows).sort_values(
                "year", ascending=False, na_position="last")
            display(
                Markdown(f"### Artigos de controle ({found}/{total} encontrados na base)"))
            display(_apply_style(df))

        # --- Comparação dos resultados ---
        diff.show()
