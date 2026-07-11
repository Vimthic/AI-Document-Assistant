from app.pipeline import process_text_document
from app.chunking import split_document
from app.embeddings import generate_embedding

def prepare_document(path):

    text = process_text_document(path)

    chunks = split_document(text)

    vectors = []

    for chunk in chunks:

        embedding = generate_embedding(chunk)

        vectors.append(
            {
                "text": chunk,
                "embedding": embedding,
            }
        )

    return vectors