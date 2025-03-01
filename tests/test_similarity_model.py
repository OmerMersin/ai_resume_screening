# tests/test_similarity_model.py

import pytest
from nlp_utils.similarity_model import TextSimilarityModel

def test_compute_similarity():
    model = TextSimilarityModel()
    text1 = "Python is a great programming language."
    text2 = "I love coding in Python!"
    score = model.compute_similarity(text1, text2)
    assert score > 0.5  # Should be fairly similar