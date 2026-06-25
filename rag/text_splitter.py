def chunk_text(text, chunk_size=120, overlap=30):
    """
    Better chunking for RAG systems.
    Forces multiple chunks even for small PDFs.
    """

    words = text.split()

    if len(words) == 0:
        return []

    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = words[start:end]

        chunks.append(" ".join(chunk))

        start = end - overlap

        # safety break to avoid infinite loops
        if start >= len(words):
            break

    return chunks