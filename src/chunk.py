from ingest import load_documents

def chunk_text(text: str, chunk_size: int = 700, overlap: int = 100) -> list[str]:
    if chunk_size <= overlap:
        raise ValueError("chunck_size must be greater than overlap")

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunk = chunk.strip()

        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def chunk_documents(documents: list[dict]) -> list[dict]:
    all_chunks = []

    for doc in documents:
        chunks = chunk_text(doc["contents"])

        for index, chunk in enumerate(chunks):
            chunk_dict = ({
                "id": f"{doc['source']}::page-{doc['page_number']}::chunk-{index}",
                "source": f"{doc['source']}",
                "page": doc['page_number'],
                "chunk_index": index, 
                "text": chunk,
            })
            all_chunks.append(chunk_dict)

    return all_chunks

if __name__ == "__main__":
    documents = load_documents("data/raw")
    chunks = chunk_documents(documents)

    print(f"Loaded documents: {len(documents)}")
    print(f"Created chunks: {len(chunks)}")

    for chunk in chunks:
        print(chunk["id"])
        print(chunk["text"][:200])