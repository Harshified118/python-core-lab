"""
01_text_analyzer.py
Category: Basic / String Processing

Description:
Analyzes prose text to compute readability and structural metrics:
- Word, sentence, and paragraph counts
- Average word and sentence length
- Lexical diversity (unique vs. total words)
- Character frequency distribution
- Estimated reading time (based on 200 wpm standard)
- Top-N most frequent words (excluding common stop words)
"""

from collections import Counter
import re
from typing import Dict, Any, List

STOP_WORDS = {
    "a", "an", "the", "and", "or", "in", "on", "at", "to", "for", "of",
    "with", "by", "is", "was", "are", "were", "it", "this", "that", "as"
}


def analyze_text(text: str) -> Dict[str, Any]:
    if not text.strip():
        return {
            "characters": 0,
            "words": 0,
            "sentences": 0,
            "paragraphs": 0,
            "avg_word_length": 0.0,
            "avg_sentence_length": 0.0,
            "lexical_diversity": 0.0,
            "estimated_reading_time_sec": 0.0,
            "top_words": [],
        }

    # Normalize and extract components
    paragraphs = [p for p in text.split("\n") if p.strip()]
    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    words = re.findall(r"\b[a-zA-Z0-9']+\b", text.lower())

    total_chars = len(text)
    total_words = len(words)
    total_sentences = len(sentences)
    total_paragraphs = len(paragraphs)

    avg_word_len = sum(len(w) for w in words) / total_words if total_words else 0.0
    avg_sentence_len = total_words / total_sentences if total_sentences else 0.0

    unique_words = set(words)
    lexical_diversity = len(unique_words) / total_words if total_words else 0.0

    # Reading time in seconds (standard average: 200 words per minute)
    reading_time_sec = (total_words / 200.0) * 60.0

    # Top words excluding common stop words
    filtered_words = [w for w in words if w not in STOP_WORDS]
    top_words = Counter(filtered_words).most_common(5)

    return {
        "characters": total_chars,
        "words": total_words,
        "sentences": total_sentences,
        "paragraphs": total_paragraphs,
        "avg_word_length": round(avg_word_len, 2),
        "avg_sentence_length": round(avg_sentence_len, 2),
        "lexical_diversity": round(lexical_diversity, 4),
        "estimated_reading_time_sec": round(reading_time_sec, 2),
        "top_words": top_words,
    }


def main():
    sample_text = """
    Python is an interpreted, high-level, general-purpose programming language.
    Created by Guido van Rossum and first released in 1991, Python's design philosophy
    emphasizes code readability with its notable use of significant whitespace.

    Its language constructs and object-oriented approach aim to help programmers write clear,
    logical code for small and large-scale projects. Python features a dynamic type system
    and automatic memory management.
    """

    print("=== 01: Text Analyzer Demo ===")
    stats = analyze_text(sample_text)
    for key, value in stats.items():
        print(f"{key.replace('_', ' ').title():<28}: {value}")


if __name__ == "__main__":
    main()
