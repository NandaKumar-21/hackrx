from typing import List, Tuple

def find_most_relevant_chunk(query: str, chunks: List[str]) -> Tuple[List[str], List[float]]:
    # Naive similarity using common words
    query_words = set(query.lower().split())
    scores = []

    for chunk in chunks:
        chunk_words = set(chunk.lower().split())
        overlap = query_words.intersection(chunk_words)
        scores.append(len(overlap))

    top_index = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:1]
    best_chunks = [chunks[i] for i in top_index]
    best_scores = [scores[i] for i in top_index]

    return best_chunks, best_scores
