import numpy as np


class VectorStore:
    def __init__(self, dim=768):
        self.dim = dim
        self.vectors = []
        self.texts = []

    def add(self, vectors, texts):
        self.vectors.extend(vectors)
        self.texts.extend(texts)

    def search(self, query_vector, top_k=3):
        def cosine(a, b):
            a = np.array(a)
            b = np.array(b)
            return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8)

        scores = []

        for i, vec in enumerate(self.vectors):
            score = cosine(query_vector, vec)
            scores.append((score, self.texts[i]))

        scores.sort(reverse=True, key=lambda x: x[0])

        return [text for _, text in scores[:top_k]]