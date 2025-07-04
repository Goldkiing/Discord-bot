# nlp_engine.py

import spacy
import json
import re
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Load sentence embedding model
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Load intent examples from external JSON file
with open("intents.json", "r", encoding="utf-8") as f:
    intent_examples = json.load(f)

# Generate intent embeddings by averaging example sentence vectors
intent_embeddings = {
    intent: np.mean([embedder.encode(e) for e in samples], axis=0)
    for intent, samples in intent_examples.items()
}


def split_sentences(text: str):
    """Split a paragraph into individual sentences."""
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents]


def analyze_sentence(sentence: str):
    """Analyze sentence structure using spaCy. Returns POS info."""
    doc = nlp(sentence)
    return [{
        "word": token.text,
        "lemma": token.lemma_,
        "pos": token.pos_,
        "tag": token.tag_,
        "dep": token.dep_,
        "is_stop": token.is_stop
    } for token in doc]


def classify_sentence_type(sentence: str):
    """
    Classify sentence type: question, command, definition, statement.
    Simple heuristic rules based on structure.
    """
    sentence = sentence.strip()
    if sentence.endswith("?"):
        return "question"
    if re.match(r"^(what|who|when|where|why|how)\b", sentence.lower()):
        return "question"
    if re.match(r"^(define|what is|explain)\b", sentence.lower()):
        return "definition"
    if re.match(r"^[a-z]+\s", sentence.lower()) and nlp(sentence)[0].pos_ == "VERB":
        return "command"
    return "statement"


def detect_intent(sentence: str):
    """
    Detect intent by comparing sentence embedding with predefined intent embeddings.
    Returns best matching intent label.
    """
    vec = embedder.encode(sentence)
    similarities = {
        intent: cosine_similarity([vec], [emb])[0][0]
        for intent, emb in intent_embeddings.items()
    }
    best_intent = max(similarities, key=similarities.get)
    return best_intent
