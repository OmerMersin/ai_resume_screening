# tests/test_ner_model.py

import pytest
from nlp_utils.ner_model import load_spacy_model, extract_named_entities

def test_extract_named_entities():
    nlp = load_spacy_model()
    test_text = "John Doe worked at Google in California."
    ents = extract_named_entities(test_text, nlp)
    # We might get PERSON, ORG, GPE depending on the model
    assert len(ents) > 0