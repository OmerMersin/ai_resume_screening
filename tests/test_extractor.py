# tests/test_extractor.py

import io
import pytest
from nlp_utils.extractor import extract_text

def test_extract_text_txt():
    fake_text_file = io.BytesIO(b"Hello, this is a test resume.")
    fake_text_file.name = "test_resume.txt"
    content = extract_text(fake_text_file)
    assert "Hello" in content