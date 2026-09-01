import ollama
from retrieve import retrieve_chunks

def build_prompt(query: str, chunks: list[dict]) -> str:
    context_blocks = []

    for chunk in chunks:
        source = chunk["metadata"]["source"]
        text = chunk["text"]

        context_block = f"[Source: {source}]\n{text}"
        context_blocks.append(context_block)

    context_string = "\n\n".join(context_blocks)

    prompt = f"""
You are SourceRecall, a local RAG assistant.

Use only the retrieved context below to answer the user's question.

Rules:
- If the context directly contains the answer, answer clearly and do not say you lack information.
- If the question asks for action items, tasks, completed work, notes, or limitations, list the relevant items exactly from the context.
- Do not invent details that are not in the context.
- Do not assume the retrieved context includes every document.
- If the answer truly is not present in the retrieved context, say: "I do not have enough information in the retrieved sources."

Context:
{context_string}

Question:
{query}

Answer:
""".strip()
    
    return prompt


def generate_answer(query: str, chunks: list[dict], model_name: str = "llama3.2") -> str:
    prompt = build_prompt(query, chunks)

    response = ollama.generate(
        model=model_name,
        prompt=prompt,
        options={
        "temperature": 0.1
    }
    )

    return response["response"]


if __name__ == "__main__":
    query = "Which day did I hit a PR?"
    chunks = retrieve_chunks(query)

    answer = generate_answer(query, chunks)
    print(answer)

