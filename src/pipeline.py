import sys
from store import build_vector_store
from retrieve import retrieve_chunks
from generate import generate_answer
import os
import json

PRINT = False

def print_usage():
    print("Available Commands:")
    print("python src/pipeline.py build")
    print('python src/pipeline.py ask "your question"')
    print('python src/pipeline.py eval')

def main():
    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1]

    if command == "build":
        summary = build_vector_store()

        print("Building SourceRecall vector store...")
        print()
        print(f"Documents: {summary['document_count']}")
        print(f"Chunks: {summary['chunk_count']}")
        print(f"Embeddings: {summary['embedding_count']}")
        print(f"Collection: {summary['collection_name']}")
        print()
        print("Build Complete.")

    elif command == "eval":
        eval_results = []

        hit_at_1 = 0
        hit_at_3 = 0
        hit_at_5 = 0

        with open("eval/demo_retrieval_questions.json", "r") as file:
            questions = json.load(file)

        for question in questions:
            query = question['question']
            expected_page = question["expected_page"]
            chunks = retrieve_chunks(query, 5)

            retrieved = []

            for rank, chunk in enumerate(chunks, start=1):
                retrieved.append({
                    "rank": rank,
                    "source": chunk["metadata"]["source"],
                    "page": chunk["metadata"]["page"],
                    "distance": chunk["distance"],
                })

            expected = (
                question["expected_source"],
                question["expected_page"],
            )

            retrieved_locations = [
                (item["source"], item["page"])
                for item in retrieved
            ]

            print("\nEXPECTED TUPLE:")
            print(expected)

            print("\nRETRIEVED TUPLES:")
            for location in retrieved_locations:
                print(location)

            hit_1 = expected in retrieved_locations[:1]
            hit_3 = expected in retrieved_locations[:3]
            hit_5 = expected in retrieved_locations[:5]

            hit_at_1 += int(hit_1)
            hit_at_3 += int(hit_3)
            hit_at_5 += int(hit_5)
            
            result = {
                "id": question["id"],
                "question": query,
                "expected_source": question["expected_source"],
                "expected_page": question["expected_page"],
                "hit_at_1": hit_1,
                "hit_at_3": hit_3,
                "hit_at_5": hit_5,
                "retrieved": retrieved,
            }

            eval_results.append(result)

            if PRINT:
                print("\nQuestion:")
                print(query)
                    
                print("\nRetrieved Sources:")
                for chunk in chunks:
                    source = chunk["metadata"]["source"]
                    distance = chunk["distance"]
                    print(f"- {source} | distance={distance:.4f}")
                    
                print(f"\n Question ID: {question['id']}")
                print(f"\nExpected Source: {question['expected_source']}")
                print(f"\nExpected Page: {question['expected_page']}")

        total = len(questions)

        summary = {
            "question_count": total,
            "hit_at_1": hit_at_1 / total,
            "hit_at_3": hit_at_3 / total,
            "hit_at_5": hit_at_5 / total,
        }

        output = {
            "summary": summary,
            "results": eval_results,
        }

        os.makedirs("outputs", exist_ok=True)

        with open("outputs/demo_retrieval_eval.json", "w") as file:
            json.dump(output, file, indent=2)

        print("\nRetrieval Evaluation")
        print(f"Questions: {total}")
        print(f"Hit@1: {summary['hit_at_1']:.0%}")
        print(f"Hit@3: {summary['hit_at_3']:.0%}")
        print(f"Hit@5: {summary['hit_at_5']:.0%}")
                

    elif command == "ask":
        if len(sys.argv) < 3:
            print_usage()
            return
        
        query = " ".join(sys.argv[2:])
    
        chunks = retrieve_chunks(query)
        answer = generate_answer(query, chunks)
    
        print("\nQuestion:")
        print(query)
    
        print("\nAnswer:")
        print(answer)
    
        print("\nRetrieved Sources:")
        for chunk in chunks:
            source = f"{chunk['metadata']['source']}::page-{chunk['metadata']['page']}"
            distance = chunk["distance"]
            print(f"- {source} | distance={distance:.4f}")

    else:
        print("Unknown Command...")
        print_usage()


if __name__ == "__main__":
    main()