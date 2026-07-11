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
'''
'''
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
'''

#To Test Embeddings
from app.embeddings import generate_embedding

vector = generate_embedding(
    "Employees receive 20 annual leave days."
)

print(len(vector))
print(vector[:10])