from .comparison import compare
from .interfaces import SearchClientProtocol
from .models import (
    ComparisonResult,
    ControlArticle,
    Document,
    SearchResult,
    ValidationResult,
)
from .picoc import PicocString
from .search_manager import SearchManager
from .implementations.scopus import ScopusClient
from .query import Query

__all__ = [
    "compare",
    "ComparisonResult",
    "ControlArticle",
    "Document",
    "PicocString",
    "Query",
    "SearchClientProtocol",
    "SearchManager",
    "SearchResult",
    "ScopusClient",
    "ValidationResult",
]
