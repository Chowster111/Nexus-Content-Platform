import pytest
from engine.recommender import get_combined_embedding, recommend_articles

def test_embedding_generation():
    text = "Test article on AI"
    embedding = get_combined_embedding(text)
    assert embedding is not None
    assert embedding.shape[0] > 0

def test_recommend_articles_empty_query():
    results = recommend_articles("", top_k=3)
    assert isinstance(results, list)