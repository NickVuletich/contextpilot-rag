from ingest import load_documents
from chunk import chunk_documents
from embed import load_embedding_model, embed_texts
from chromadb.api.models.Collection import Collection
from chromadb.api import ClientAPI
import chromadb

CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "sourcerecall_docs"

def build_vector_store() -> dict[str, int | str]:
    documents = load_documents("data/raw")
    chunks = chunk_documents(documents)
    texts = [chunk["text"] for chunk in chunks]
    model = load_embedding_model()
    embeddings = embed_texts(texts, model)

    ids = [chunk["id"] for chunk in chunks]
    metadatas = []
    
    for chunk in chunks:
        metadatas.append({
            "source": chunk["source"],
            "chunk_index": chunk["chunk_index"],
        })

    client = get_chroma_client()
    collection = reset_collection(client)

    assert len(ids) == len(texts) == len(embeddings) == len(metadatas)

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    summary_dict = {
        "document_count": len(documents),
        "chunk_count": len(chunks),
        "embedding_count": len(embeddings),
        "collection_name": COLLECTION_NAME,
    }
    return summary_dict

def get_chroma_client(path: str = CHROMA_PATH) -> ClientAPI:
    client = chromadb.PersistentClient(path=path)
    return client

def reset_collection(client: ClientAPI, collection_name: str = COLLECTION_NAME) -> Collection:
    try:
        client.delete_collection(name=collection_name)
    except Exception:
        pass
    collection = client.create_collection(name=collection_name)
    return collection


if __name__ == "__main__":
    result = build_vector_store()
    print(f"Results:")
    print(f"Document Count: {result['document_count']}")
    print(f"Chunk Count: {result['chunk_count']}")
    print(f"Embedding Count: {result['embedding_count']}")
    print(f"Collection: {result['collection_name']}")