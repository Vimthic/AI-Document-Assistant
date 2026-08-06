# app/search.py
import re

def keyword_search(chunks, query):
    """
    Scores chunks based on keyword matches.
    Returns a list of dicts with an added 'keyword_score'.
    """
    # Clean and extract query words longer than 2 characters
    query_words = [w.lower() for w in re.findall(r'\b\w{3,}\b', query)]
    if not query_words:
        return []

    scored_chunks = []
    for chunk in chunks:
        text = chunk.get("text", "").lower()
        # Count how many unique query words appear in this text chunk
        match_count = sum(1 for word in query_words if word in text)
        
        if match_count > 0:
            # Normalize score relative to the query length
            keyword_score = round(match_count / len(query_words), 2)
            
            # Create a shallow copy to append the temporary search score safely
            chunk_copy = chunk.copy()
            chunk_copy["keyword_score"] = keyword_score
            scored_chunks.append(chunk_copy)
            
    # Sort descending by performance keyword score
    scored_chunks.sort(key=lambda x: x["keyword_score"], reverse=True)
    return scored_chunks
