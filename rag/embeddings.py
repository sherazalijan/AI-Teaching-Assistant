import numpy as np


def get_embedding(text: str):
    """
    TEMPORARY embedding function for Phase 3.
    We use random vectors to simulate embeddings for FAISS.
    """

    # stable fake embedding (important: same input = same output idea is NOT needed yet)
    np.random.seed(abs(hash(text)) % (2**32))

    return np.random.rand(768).astype("float32")