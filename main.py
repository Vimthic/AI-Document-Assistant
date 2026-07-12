#For AI response
'''
from app.document_service import summarize_document,explain_document

def main():

    summary = summarize_document(
        #"data/company_policy.txt"
        "data/it_policy.txt"
    )
    print(summary)

    explain = explain_document(
        "data/it_policy.txt"
    )
    print(explain)

if __name__ == "__main__":
    main()


#To Test chunking
from app.pipeline import process_text_document
from app.chunking import split_document

document = process_text_document(
    "data/company_policy.txt"
)

chunks = split_document(document)

print(f"Chunks: {len(chunks)}")

for i, chunk in enumerate(chunks):
    print(f"\nChunk {i+1}")
    print(chunk)

#To Test Embeddings
from app.embeddings import generate_embedding

vector = generate_embedding(
    "Employees receive 20 annual leave days."
)

print(len(vector))
print(vector[:10])
#########

from app.embeddings import generate_embedding
from app.rag_preparation import prepare_document

vector = generate_embedding("Employees receive 20 annual leave days.")
print("--- Initial Test Vector Length ---")
print(len(vector))
print(vector[:10])    
print("=" * 40)

file_path = "data/security_policy.txt" 

# This returns a list of dictionaries: [{'text': chunk, 'embedding': embedding}, ...]
document_vectors = prepare_document(file_path)

# Logic for Total Chunks: Check the length of the returned list
total_chunks = len(document_vectors)
print(f"Total chunks: {total_chunks}")
print("-" * 40)

# Loop through each chunk to get individual lengths and slices
for index, chunk_data in enumerate(document_vectors, start=1):
    chunk_text = chunk_data["text"]
    chunk_embedding = chunk_data["embedding"]
    
    # Logic for Length of each chunk: Measure character length of string
    chunk_length = len(chunk_text)
    
    # Logic for First 5 values: Slice the embedding list up to index 5
    first_five_embeddings = chunk_embedding[:5]
    
    # Print the specific metadata out
    print(f"Chunk {index}:")
    print(f"  Length of chunk: {chunk_length} characters")
    print(f"  First 5 embedding values: {first_five_embeddings}")
    print("-" * 40)
'''

from app.retriever import Retriever

retriever = Retriever()

retriever.add_document(
    "Employees receive 20 annual leave days."
)

retriever.add_document(
    "Remote work is allowed 3 days every week."
)

retriever.add_document(
    "Managers approve leave requests."
)

question = "How many vacation days do employees receive?"

results = retriever.search(
    question
)

print(results)