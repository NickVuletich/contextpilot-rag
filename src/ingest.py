from pathlib import Path
import os
def load_documents(data_dir: str) -> list[dict]:
    data_dir = Path(data_dir)

    if not data_dir.exists():
        raise FileNotFoundError(f"File {data_dir} not found.")
    
    documents = []

    for root, _, files in os.walk(data_dir):
        for name in files:
            if name.lower().endswith((".txt", ".md")):
                file_path = Path(root) / name
                text = file_path.read_text(encoding="utf-8")
                documents.append({
                    "source": str(file_path),
                    "text": text,
                    "char_count": len(text),
                })
    return documents

if __name__ == "__main__":
    list_docs = load_documents("data/raw")
    print(f"Number of documents is: {len(list_docs)}")

    for doc in list_docs:
        print(f"Source:", doc["source"])
        print(f"Character count:", doc["char_count"])
        print(f"Preview:", doc["text"][:300])
