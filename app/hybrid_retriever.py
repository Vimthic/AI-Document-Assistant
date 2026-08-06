# app/hybrid_retriever.py
from app.search import keyword_search

class HybridRetriever:
    def __init__(self, vector_retriever):
        self.vector = vector_retriever

    def search(self, question, category_filter="All", k=3, min_threshold=0.45):
        """
        Executes Hybrid Search, filters by category, calculates rankings, 
        and enforces a minimum score threshold to eliminate false-positive sources.
        """
        # 1. Fetch Vector Candidates globally
        vector_results = self.vector.search(question, category_filter="All")
        
        # 2. Extract every single indexed document text chunk to feed Keyword search
        all_chunks = self.vector.store.documents if (self.vector.store and self.vector.store.documents) else []
        keyword_results = keyword_search(all_chunks, question)
        
        combined_pool = {}

        # Process all structural vector results
        for item in vector_results:
            text_key = item["text"]
            combined_pool[text_key] = {
                "text": item["text"],
                "filename": item["filename"],
                "category": item["category"],
                "chunk_number": item["chunk_number"],
                "vector_score": item["score"],
                "keyword_score": 0.0
            }

        # Process and combine all keyword results
        for item in keyword_results:
            text_key = item["text"]
            if text_key in combined_pool:
                combined_pool[text_key]["keyword_score"] = item["keyword_score"]
            else:
                combined_pool[text_key] = {
                    "text": item["text"],
                    "filename": item["filename"],
                    "category": item.get("category", "HR"),
                    "chunk_number": item.get("chunk_number", 1),
                    "vector_score": 0.40, 
                    "keyword_score": item["keyword_score"]
                }

        # 3. Apply Category Filtering, Thresholding, and Score Ranking
        filtered_ranked_results = []
        for doc in combined_pool.values():
            
            # Category Filter Layer
            if category_filter != "All" and doc["category"] != category_filter:
                continue
                
            # Rank Architecture Scoring: 60% Semantic Weight + 40% Keyword Match Weight
            final_hybrid_score = round((doc["vector_score"] * 0.6) + (doc["keyword_score"] * 0.4), 2)
            
            # Enforce Minimum Quality Floor Threshold Check
            if final_hybrid_score < min_threshold:
                continue
            
            filtered_ranked_results.append({
                "text": doc["text"],
                "score": final_hybrid_score,
                "filename": doc["filename"],
                "category": doc["category"],
                "chunk_number": doc["chunk_number"]
            })

        # Sort descending by final structural score
        filtered_ranked_results.sort(key=lambda x: x["score"], reverse=True)
        
        return filtered_ranked_results[:k]
