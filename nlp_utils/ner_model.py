# nlp_utils/ner_model.py

import spacy
from config import SPACY_MODEL_PATH

def load_spacy_model():
    """
    Attempt to load a fine-tuned SpaCy model; if not available, fallback to standard model.
    """
    try:
        nlp = spacy.load(SPACY_MODEL_PATH)
        print(f"Loaded SpaCy model from '{SPACY_MODEL_PATH}'.")
    except Exception as e:
        print(f"Could not load custom SpaCy model '{SPACY_MODEL_PATH}', falling back to 'en_core_web_sm'. Error: {e}")
        nlp = spacy.load("en_core_web_sm")
    return nlp

def extract_named_entities(text: str, nlp) -> list:
    """
    Run the loaded SpaCy NER model on text, returning a list of (entity_text, label).
    """
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]