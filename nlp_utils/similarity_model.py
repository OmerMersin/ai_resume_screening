# nlp_utils/similarity_model.py

import torch
from transformers import AutoTokenizer, AutoModel, pipeline
from sklearn.metrics.pairwise import cosine_similarity

from config import TRANSFORMER_MODEL_NAME, POOLING_STRATEGY, SUMMARIZATION_MODEL_NAME

class TextSimilarityModel:
    def __init__(self, model_name: str = TRANSFORMER_MODEL_NAME, pooling_strategy: str = POOLING_STRATEGY):
        self.model_name = model_name
        self.pooling_strategy = pooling_strategy

        # Load the model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def encode_text(self, text: str):
        """
        Encode text into a vector using a Transformer model.
        """
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=512
        )
        with torch.no_grad():
            outputs = self.model(**inputs)
        last_hidden_state = outputs.last_hidden_state

        if self.pooling_strategy == "cls":
            # [CLS] token is at index 0
            embeddings = last_hidden_state[:, 0, :]
        else:
            # Mean pooling
            embeddings = last_hidden_state.mean(dim=1)

        return embeddings.numpy()

    def compute_similarity(self, text1: str, text2: str) -> float:
        """
        Use cosine similarity between the embeddings of two texts.
        """
        emb1 = self.encode_text(text1)
        emb2 = self.encode_text(text2)
        return float(cosine_similarity(emb1, emb2)[0][0])

# Optional Summarization
def load_summarizer(model_name=SUMMARIZATION_MODEL_NAME):
    """
    Load a huggingface pipeline for text summarization (e.g., BART or T5).
    """
    summarizer = pipeline("summarization", model=model_name, tokenizer=model_name)
    return summarizer

def summarize_text(summarizer, text: str, max_length=150, min_length=30) -> str:
    """
    Summarize a given text using a huggingface summarization pipeline.
    """
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]["summary_text"]