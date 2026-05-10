from .comparison import compare
from .interfaces import QueryBackendProtocol
from .models import ComparisonResult, Document, SearchResult
from .query_builder import QueryBuilder
from .implementations.scopus import ScopusClient, ScopusQueryBuilder

__all__ = [
    "compare",
    "ComparisonResult",
    "Document",
    "QueryBackendProtocol",
    "QueryBuilder",
    "SearchResult",
    "ScopusClient",
    "ScopusQueryBuilder",
]
