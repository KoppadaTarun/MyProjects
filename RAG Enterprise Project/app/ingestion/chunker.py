
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.ingestion.text_cleaner import clean_text


def chunk_document(
    pages: list[dict],
    chunk_size: int = 800,
    chunk_overlap: int = 150
) -> list[dict]:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = []
    chunk_index = 0

    for page in pages:

        text = clean_text(page["text"])

        if not text:
            continue

        text_chunks = splitter.split_text(text)

        for chunk in text_chunks:

            chunks.append({
                "text": chunk,
                "page_number": page["page_number"],
                "chunk_index": chunk_index
            })

            chunk_index += 1

    return chunks
