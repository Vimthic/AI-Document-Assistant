# evaluation/evaluate.py
import sys
import os

# Set execution path reference logic to workspace base path root folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from app.retriever import Retriever
    from app.hybrid_retriever import HybridRetriever
except ImportError as e:
    print(f"Directory configuration mismatch error details: {e}")
    sys.exit(1)

# Task 4 Target System Evaluation Dataset Array
EVAL_DATASET = [
    {"question": "How many leave days?", "expected_document": "company_policy.txt"},
    {"question": "VPN policy?", "expected_document": "it_policy.txt"},
    {"question": "Password rules?", "expected_document": "security_policy.txt"},
    {"question": "Hotel reimbursement?", "expected_document": "travel_policy.txt"}
]

def run_system_evaluation():
    print("=" * 75)
    print("🚀 Running Hybrid Architecture RAG Application Evaluation Engine")
    print("=" * 75)
    
    base_retriever = Retriever()
    if not base_retriever.has_existing_index():
        print("❌ Error: Missing active FAISS vector database. Ingest files via UI first.")
        return
        
    base_retriever.load_existing_index()
    hybrid_retriever = HybridRetriever(base_retriever)
    
    match_count = 0
    total = len(EVAL_DATASET)
    
    print(f"Testing {total} complex evaluation parameters against active index...")
    print("-" * 75)
    
    row_layout = "{:<25} | {:<20} | {:<20} | {:<6} | {:<5}"
    print(row_layout.format("Question Sent", "Expected Target", "Top Hit Returned", "Score", "Match"))
    print("-" * 75)
    
    for item in EVAL_DATASET:
        question = item["question"]
        expected = item["expected_document"]
        
        # Test query execution pipeline (defaults category filter to All for comprehensive baseline evaluation)
        hits = hybrid_retriever.search(question, category_filter="All", k=1)
        
        if hits:
            top_hit = hits[0]
            retrieved_doc = top_hit["filename"]
            score = top_hit["score"]
        else:
            retrieved_doc = "None Found"
            score = 0.00
            
        is_match = "Yes" if retrieved_doc.strip().lower() == expected.strip().lower() else "No"
        if is_match == "Yes":
            match_count += 1
            
        print(row_layout.format(
            question[:23],
            expected[:18],
            retrieved_doc[:18],
            str(score),
            is_match
        ))
        
    accuracy_percentage = (match_count / total) * 100
    print("-" * 75)
    print(f"📊 Accuracy Metric Result: {accuracy_percentage:.1f}% ({match_count}/{total} Test Items Passed)")
    print("=" * 75)

if __name__ == "__main__":
    run_system_evaluation()
