import re
from typing import List


def clean_text(text: str) -> str:
    """
    Basic cleaning for financial news articles.
    """
    if not text:
        return ""

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    # Remove weird control characters
    text = "".join(ch for ch in text if ch.isprintable() or ch.isspace())

    return text.strip()


def split_into_chunks(text: str, max_tokens: int = 1500) -> List[str]:
    """
    Naive chunking by sentence length approximation.
    Here we assume ~4 chars per token as a rough heuristic.
    """
    if not text:
        return []

    approx_chars = max_tokens * 4
    chunks = []
    current = []

    for sentence in re.split(r"(?<=[.!?])\s+", text):
        current.append(sentence)
        if sum(len(s) for s in current) > approx_chars:
            chunks.append(" ".join(current))
            current = []

    if current:
        chunks.append(" ".join(current))

    return chunks
