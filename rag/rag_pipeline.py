from rag.embeddings import get_embedding
from rag.vector_store import VectorStore
from rag.pdf_loader import extract_text_from_pdf
from rag.text_splitter import chunk_text
from utils.gemini_client import model


class RAGPipeline:
    def __init__(self, pdf_path=None):
        self.vector_store = VectorStore(dim=768)

        if pdf_path:
            self.ingest_pdf(pdf_path)

    def ingest_pdf(self, pdf_path):
        text = extract_text_from_pdf(pdf_path)
        self.ingest_text(text)

    def ingest_text(self, text):
        chunks = chunk_text(text)

        vectors = [get_embedding(c) for c in chunks]

        self.vector_store.add(vectors, chunks)

    def query(self, question):
        q_vector = get_embedding(question)

        top_chunks = self.vector_store.search(q_vector, top_k=3)

        context = "\n\n".join(top_chunks)

        prompt = f"""
You are an AI tutor.

Use the context below to answer:

Context:
{context}

Question:
{question}

Give a clear, structured answer.
"""

        response = model.generate_content(prompt)
        return response.text