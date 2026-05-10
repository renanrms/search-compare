from .models import ComparisonResult, Document, SearchResult


def compare(result1: SearchResult, result2: SearchResult) -> ComparisonResult:
    """Compares two SearchResults by EID, returning common and exclusive document sets."""
    index1: dict[str, Document] = {doc.eid: doc for doc in result1.documents}
    index2: dict[str, Document] = {doc.eid: doc for doc in result2.documents}

    eids1 = set(index1)
    eids2 = set(index2)

    return ComparisonResult(
        result1=result1,
        result2=result2,
        common=[index1[e] for e in sorted(eids1 & eids2)],
        only_in_1=[index1[e] for e in sorted(eids1 - eids2)],
        only_in_2=[index2[e] for e in sorted(eids2 - eids1)],
    )
