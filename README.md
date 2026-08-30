# SourceRecall - Local RAG Assistant for Notes, Logs, and Documents

SourceRecall is a local retrieval-augmented generation system for querying messy notes, logs, and documents with source-grounded answers.

The goal of this project is to understand how practical RAG systems work by building the core pipeline piece by piece: document ingestion, text chunking, embeddings, vector storage, semantic retrieval, prompt construction, and local LLM generation.

SourceRecall runs locally using ChromaDB, Sentence Transformers, and Ollama. It does not require paid API credits.

## Why I Built This

I built SourceRecall to learn how RAG systems work beyond simple demos. Instead of sending a question directly to an LLM, SourceRecall first retrieves relevant source context from local documents and then uses that context to generate a grounded answer.

This project is intentionally built without hiding the entire pipeline behind a large framework. I wanted to understand how data moves through each stage, where retrieval works well, and where RAG systems can fail.

The sample data includes fitness logs, business notes, meeting notes, support tickets, and project documentation. The underlying system is domain-agnostic and can be reused for other local text documents.

## Features

* Load `.md` and `.txt` documents from `data/raw/`
* Split documents into overlapping text chunks
* Create local embeddings using Sentence Transformers
* Store chunks, embeddings, and metadata in ChromaDB
* Retrieve relevant chunks for a natural language query
* Generate grounded answers with a local Ollama model
* Print retrieved source documents and similarity distances
* Provide a simple CLI workflow for building and querying the local vector store

## Tech Stack

* Python
* ChromaDB
* Sentence Transformers
* Ollama
* Local LLM generation
* Vector search
* Retrieval-Augmented Generation

## Project Structure

```txt
source-recall/
├── data/
│   └── raw/
├── src/
│   ├── ingest.py
│   ├── chunk.py
│   ├── embed.py
│   ├── store.py
│   ├── retrieve.py
│   ├── generate.py
│   └── pipeline.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## How It Works

SourceRecall follows a basic local RAG pipeline:

```txt
raw documents
→ document ingestion
→ text chunking
→ embedding generation
→ ChromaDB vector storage
→ semantic retrieval
→ prompt construction
→ local LLM answer generation
```

When a user asks a question, SourceRecall embeds the query, searches ChromaDB for the most relevant chunks, builds a prompt using the retrieved source context, and sends that prompt to a local Ollama model.

The model is instructed to answer using only the retrieved context and to avoid inventing details that are not present in the sources.

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Ollama and pull a local model:

```bash
ollama pull llama3.2
```

## Usage

Add `.txt` or `.md` files to:

```txt
data/raw/
```

Build the local vector store:

```bash
python src/pipeline.py build
```

Ask a question:

```bash
python src/pipeline.py ask "Which workout had a PR?"
```

Whenever documents are added, removed, or edited, rebuild the vector store before asking new questions:

```bash
python src/pipeline.py build
```

## Example Queries

Example query:

```bash
python src/pipeline.py ask "What decisions were made in the AI workflow meeting?"
```

Example output:

```txt
Question:
What decisions were made in the AI workflow meeting?

Answer:
The main goal of the team was to reduce time spent digging through scattered documents. The following decisions were made:

- start with local text files before adding PDFs
- keep the first version CLI-based
- prioritize source-grounded answers over fancy UI
- document known limitations clearly

Retrieved Sources:
- data/raw/meeting_notes_sample.txt | distance=1.1045
- data/raw/business_notes_sample.txt | distance=1.6022
- data/raw/support_ticket_sample.txt | distance=1.7245
```

Another example:

```bash
python src/pipeline.py ask "What possible fixes are listed for unrelated sources?"
```

Example output:

```txt
Answer:
The possible fixes listed for unrelated sources are:

1. rename output from Sources to Retrieved Sources
2. allow top_k to be configured from the command line
3. improve chunking strategy
4. add filtering by document category in the future

Retrieved Sources:
- data/raw/support_ticket_sample.txt | distance=1.0174
- data/raw/project_notes_sample.txt | distance=1.5033
- data/raw/meeting_notes_sample.txt | distance=1.6962
```

## Current Limitations

* The vector store must be rebuilt after adding or editing documents.
* Current chunking is character-based, so long documents may split useful context across chunks.
* Retrieval returns the top matching chunks, which may include loosely related sources when the dataset is small or `top_k` is high.
* RAG is useful for source-grounded recall, but reliable totals, averages, maximums, and other calculations require structured extraction.
* The current version is CLI-based and works best with clean `.txt` or `.md` files.
* Retrieved source distances are useful for debugging, but they are not user-friendly confidence scores.

## Future Improvements

* Add configurable `top_k` from the command line
* Add semantic or section-based chunking
* Add structured extraction for dates, macros, tasks, workouts, and other fields
* Add PDF support
* Add a Streamlit interface
* Add document category filtering
* Add duplicate source handling in the output
* Add automated evaluation tests for retrieval quality
* Add support for multiple document collections

## What I Learned

This project helped me understand that RAG is not just “asking an LLM a question.” A useful RAG system needs a full pipeline around the model: data loading, chunking, embeddings, storage, retrieval, prompt construction, and evaluation.

I also learned that RAG has real limitations. It can retrieve relevant context, but it does not automatically perform reliable full-dataset analysis or calculations unless the system is designed for that. This helped me better understand the difference between semantic retrieval and structured data analysis.

## Status

MVP complete.

SourceRecall can build a local vector store from text files, retrieve relevant chunks, and generate source-grounded answers using a local LLM.
