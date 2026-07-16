from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_document(text):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    return splitter.split_text(text)