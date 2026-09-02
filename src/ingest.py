from pathlib import Path
import os
from pypdf import PdfReader
from dotenv import load_dotenv

load_dotenv()

data_folder = os.getenv("DATA_FOLDER", "data/demo")


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
                    "page_number": 1,
                    "contents": text,
                    "char_count": len(text),
                })
            if name.lower().endswith(".pdf"):
                file_path = Path(root) / name
                reader = PdfReader(file_path)

                for page_number, page in enumerate(reader.pages, start=1):
                    text = page.extract_text()
                    
                    if text:
                        documents.append({
                            "source": str(file_path),
                            "page_number": page_number,
                            "contents": text,
                            "char_count": len(text),
                        })
    return documents

if __name__ == "__main__":
    list_docs = load_documents(data_folder)
    print(f"Number of documents is: {len(list_docs)}")

    for doc in list_docs:
        print(f"Source:", doc["source"])
        print(f"Character count:", doc["char_count"])
        print(f"Preview:", doc["contents"][:300])
