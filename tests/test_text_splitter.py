from app.services.text_splitter import TextSplitter


def test_sentence_aware_chunking():

    text = """
    Semantic search retrieves information based on the meaning of a query.
    It converts text into numerical vectors called embeddings.
    These vectors allow us to compare the semantic similarity between texts.
    """

    splitter = TextSplitter(chunk_size=100)

    chunks = splitter.split_text(text)

    assert len(chunks) > 0

    for chunk in chunks:
        assert chunk.strip() != ""
    for i, chunk in enumerate(chunks):
        print(f"\nCHUNK {i}")
        print(chunk)