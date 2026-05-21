"""
Utility helpers for resume ranking.
"""

from __future__ import annotations

from typing import List

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def compute_tfidf_similarity(job_description: str, resume_texts: List[str]) -> List[float]:
    """
    Compute cosine similarity between JD and each resume using TF-IDF.
    Returns a list of similarity scores in range [0, 1].
    """
    if not resume_texts:
        return []

    corpus = [job_description.lower()] + resume_texts
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(corpus)

    jd_vector = tfidf_matrix[0:1]
    resume_vectors = tfidf_matrix[1:]
    similarities = cosine_similarity(jd_vector, resume_vectors).flatten()
    return similarities.tolist()

