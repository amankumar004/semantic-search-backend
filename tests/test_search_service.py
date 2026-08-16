from app.services.search_service import SearchService


def test_search_returns_results():

    search_service = SearchService()

    results = search_service.search(
        query="How does the system find documents based on meaning instead of exact words?",
        document_id=3,
        limit=5
    )

    assert results
    
def test_search_results_belong_to_requested_document():

    search_service = SearchService()

    results = search_service.search(
        query="How does the system find documents based on meaning instead of exact words?",
        document_id=3,
        limit=5
    )

    assert results

    for result in results:

        payload = result.payload or {}

        assert payload.get("document_id") == 3


def test_search_respects_limit():

    search_service = SearchService()

    results = search_service.search(
        query="semantic search",
        document_id=3,
        limit=2
    )

    assert len(results) <= 2
    
def test_search_result_contains_payload():

    search_service = SearchService()

    results = search_service.search(
        query="semantic search",
        document_id=3,
        limit=5
    )

    assert results

    for result in results:

        payload = result.payload or {}

        assert "document_id" in payload
        assert "chunk_index" in payload
        assert "text" in payload