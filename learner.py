# learner.py

import os
import json
from nlp_engine import split_sentences, analyze_sentence, classify_sentence_type, detect_intent

DB_PATH = "knowledge.json"

def load_database():
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_database(data):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def store_sentence(sentence: str, intent: str, sentence_type: str, tokens: list):
    db = load_database()

    # Minimal representation of tokens: only word and POS
    clean_tokens = [{"word": t["word"], "pos": t["pos"]} for t in tokens]

    db[sentence] = {
        "intent": intent,
        "type": sentence_type,
        "tokens": clean_tokens
    }

    save_database(db)

def learn_paragraph(paragraph: str):
    sentences = split_sentences(paragraph)
    learned = []

    for sent in sentences:
        intent = detect_intent(sent)
        sent_type = classify_sentence_type(sent)
        tokens = analyze_sentence(sent)

        store_sentence(sent, intent, sent_type, tokens)
        learned.append({
            "sentence": sent,
            "intent": intent,
            "type": sent_type
        })

    return learned
