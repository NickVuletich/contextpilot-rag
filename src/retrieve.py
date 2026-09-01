import chromadb
from embed import load_embedding_model, embed_texts
from store import CHROMA_PATH, COLLECTION_NAME

def retrieve_chunks(query: str, top_k: int = 3) -> list[dict]:
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_collection(name=COLLECTION_NAME)

    model = load_embedding_model()

    query_embedding = embed_texts([query], model)[0]

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
    )

    retrieved_list = []

    for index in range(len(results["ids"][0])):
        store = {
            "id": results["ids"][0][index],
            "text": results["documents"][0][index],
            "metadata": results["metadatas"][0][index],
            "distance": results["distances"][0][index],
        }
        retrieved_list.append(store)

    return retrieved_list

if __name__ == "__main__":
    query = "Which day did I hit a PR?"
    results = retrieve_chunks(query)

    print(f"Query: {query}")
    print(f"Results found: {len(results)}")

    for result in results:
        print("=" * 80)
        print(f"Source: {result['metadata']['source']}")
        print(f"Distance: {result['distance']}")
        print(result["text"][:300])