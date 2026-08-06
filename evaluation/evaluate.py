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

# Task 1: Extended 10-Question Evaluation Dataset
EVAL_DATASET = [
    {"question": "How many leave days do I get annually?", "expected_document": "company_policy.txt"},
    {"question": "What is the policy for corporate VPN connections?", "expected_document": "it_policy.txt"},
    {"question": "What are the rules for password length and complexity?", "expected_document": "security_policy.txt"},
    {"question": "How do I get a hotel reimbursement for business travel?", "expected_document": "travel_policy.txt"},
    {"question": "What medical insurance benefits are covered?", "expected_document": "benefits_policy.txt"},
    {"question": "Who signs off on quarterly budget allocations?", "expected_document": "finance_policy.txt"},
    {"question": "Is parental leave fully paid or partially paid?", "expected_document": "company_policy.txt"},
    {"question": "How often do I need to complete security awareness training?", "expected_document": "security_policy.txt"},
    {"question": "What is the maximum allowance for corporate flight bookings?", "expected_document": "travel_policy.txt"},
    {"question": "Where do I submit monthly office equipment expense invoices?", "expected_document": "finance_policy.txt"}
]

def run_system_evaluation():
    print("=" * 80)
    print("🚀 Running Extended RAG Evaluation Suite (10 Test Parameters)")
    print("=" * 80)
    
    base_retriever = Retriever()
    if not base_retriever.has_existing_index():
        print("❌ Error: Missing active FAISS vector database. Ingest files via UI first.")
        return
        
    base_retriever.load_existing_index()
    hybrid_retriever = HybridRetriever(base_retriever)
    
    correct_retrievals = 0
    total_questions = len(EVAL_DATASET)
    
    row_layout = "{:<45} | {:<20} | {:<20} | {:<5}"
    print(row_layout.format("Question Sent", "Expected Target", "Top Hit Returned", "Match"))
    print("-" * 80)
    
    for item in EVAL_DATASET:
        question = item["question"]
        expected = item["expected_document"]
        
        # Query the hybrid pipeline using baseline global search configuration
        hits = hybrid_retriever.search(question, category_filter="All", k=1)
        
        if hits:
            top_hit = hits[0]
            retrieved_doc = top_hit["filename"]
        else:
            retrieved_doc = "None Found"
            
        is_match = "Yes" if retrieved_doc.strip().lower() == expected.strip().lower() else "No"
        if is_match == "Yes":
            correct_retrievals += 1
            
        # Truncate long questions for text-terminal display grid safety
        display_q = question if len(question) <= 42 else question[:39] + "..."
        print(row_layout.format(display_q, expected, retrieved_doc, is_match))
        
    # Calculate target metric indicators
    retrieval_accuracy = (correct_retrievals / total_questions) * 100
    
    print("-" * 80)
    print("📊 FINAL RETRIEVAL PERFORMANCE METRICS:")
    print(f"🔹 Total Questions:     {total_questions}")
    print(f"🔹 Correct Retrievals:   {correct_retrievals}")
    print(f"🎯 Retrieval Accuracy:   {retrieval_accuracy:.2f}%")
    print("=" * 80)

if __name__ == "__main__":
    run_system_evaluation()
