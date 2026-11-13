from src.matching import similarity


def test_tfidf_similarity_handles_identical_and_unrelated_text():
    same, method = similarity.semantic_similarity(
        "Python data analysis", "Python data analysis", use_embeddings=False
    )
    unrelated, _ = similarity.semantic_similarity(
        "Python data analysis", "gardening and cooking", use_embeddings=False
    )

    assert method == "tfidf"
    assert same == 1.0
    assert unrelated < same


def test_empty_input_is_safe():
    assert similarity.semantic_similarity("", "Python", use_embeddings=False) == (
        0.0,
        "tfidf",
    )


def test_embedding_failure_uses_logged_tfidf_fallback(monkeypatch, caplog):
    def fail(_):
        raise OSError("model unavailable")

    monkeypatch.setattr(similarity, "_load_embedding_model", fail)
    value, method = similarity.semantic_similarity("Python", "Python", use_embeddings=True)

    assert value == 1.0
    assert method == "tfidf"
    assert "TF-IDF fallback" in caplog.text
