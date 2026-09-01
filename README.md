# SourceRecall - Local RAG Assistant for Notes, Logs, and Documents

SourceRecall is a local retrieval-augmented generation system for querying notes, logs, technical documents, and research PDFs with source-grounded answers.

The goal of this project is to understand how practical RAG systems work by building the core pipeline piece by piece: document ingestion, text chunking, embeddings, vector storage, semantic retrieval, prompt construction, local LLM generation, and retrieval evaluation.

SourceRecall runs locally using ChromaDB, Sentence Transformers, and Ollama. It does not require paid API credits.

## Why I Built This

I built SourceRecall to learn how RAG systems work beyond simple demos. Instead of sending a question directly to an LLM, SourceRecall first retrieves relevant source context from local documents and then uses that context to generate a grounded answer.

This project is intentionally built without hiding the entire pipeline behind a large RAG framework. I wanted to understand how data moves through each stage, where retrieval works well, and where RAG systems can fail.

The sample data includes fitness logs, business notes, meeting notes, support tickets, project documentation, and technical research PDFs. The underlying system is domain-agnostic and can be reused with other local document collections.

## Features

* Load `.pdf`, `.md`, and `.txt` documents from `data/raw/`
* Extract text from PDFs while preserving page-level provenance
* Split document contents into overlapping text chunks
* Create local embeddings using Sentence Transformers
* Store chunks, embeddings, and metadata in ChromaDB
* Preserve source, page, and chunk metadata through the retrieval pipeline
* Retrieve semantically relevant chunks for natural-language queries
* Generate grounded answers using a local Ollama model
* Display retrieved sources and similarity distances
* Evaluate retrieval quality using a manually labeled benchmark
* Provide a CLI workflow for building, querying, and evaluating the system

## Tech Stack

* Python
* ChromaDB
* Sentence Transformers
* Ollama
* pypdf
* Vector search
* Retrieval-Augmented Generation

## Project Structure

```txt
source-recall/
├── data/
│   └── raw/
├── eval/
│   └── retrieval_questions.json
├── outputs/
│   └── retrieval_eval.json
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

SourceRecall follows a local RAG pipeline:

```txt
raw documents
→ document ingestion
→ page-aware PDF extraction
→ text chunking
→ embedding generation
→ ChromaDB vector storage
→ semantic retrieval
→ prompt construction
→ local LLM answer generation
```

During ingestion, text and Markdown files are loaded directly while PDFs are extracted page by page. Page information is preserved as metadata so retrieved PDF content can be traced back to its original page.

Documents are divided into overlapping chunks and embedded using a Sentence Transformer model. The resulting chunks, embeddings, and metadata are stored in ChromaDB.

When a user asks a question, SourceRecall embeds the query using the same embedding model and searches ChromaDB for the most semantically similar chunks.

The retrieved context is then placed into a prompt and sent to a local Ollama model. The model is instructed to answer using only the retrieved information and to avoid inventing unsupported details.

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

Add `.pdf`, `.txt`, or `.md` files to:

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

Run the retrieval evaluation:

```bash
python src/pipeline.py eval
```

Whenever documents are added, removed, or edited, rebuild the vector store before querying it again:

```bash
python src/pipeline.py build
```

## Example Query

```bash
python src/pipeline.py ask "How much protein per kilogram of body weight is discussed for training?"
```

Example output:

```txt
Question:
How much protein per kilogram of body weight is discussed for training?

Answer:
...

Retrieved Sources:
- data/raw/research_paper.pdf::page-11 | distance=0.5555
- data/raw/research_paper.pdf::page-10 | distance=0.6281
- data/raw/research_paper.pdf::page-10 | distance=0.6536
```

PDF results retain page-level provenance so retrieved information can be traced back to its source location.

## Retrieval Evaluation

Rather than relying only on manual testing, SourceRecall includes a retrieval benchmark designed to measure whether relevant information is actually being retrieved.

The initial benchmark contains 25 manually written questions based on a technical research paper. Each question was labeled with the page containing the expected information.

For every query, SourceRecall retrieves the five highest-ranking chunks. Retrieval performance is measured using page-level Hit@k:

* **Hit@1** — the expected page appears as the highest-ranked result
* **Hit@3** — the expected page appears within the top three results
* **Hit@5** — the expected page appears within the top five results

### Baseline Results

| Metric | Result |
| --- | ---: |
| Hit@1 | 48% |
| Hit@3 | 80% |
| Hit@5 | 92% |

These results represent the baseline retrieval performance using:

* Character-based chunking
* 700-character chunks
* 100-character overlap
* `all-MiniLM-L6-v2` embeddings
* ChromaDB vector retrieval

This benchmark evaluates page-level retrieval within a single technical PDF and is intended to establish a reproducible baseline rather than claim general retrieval performance across arbitrary document collections.

### Observed Failure Mode

One observed failure mode was that bibliography and reference pages could rank highly for some queries because they contain dense concentrations of terminology related to the query.

This is useful because it provides a measurable failure case for future experiments involving chunking strategies, embedding models, metadata filtering, or other retrieval improvements.

## Current Limitations

* The vector store must currently be rebuilt after documents are added, removed, or edited.
* Chunking is character-based, which can split useful semantic context across chunk boundaries.
* PDF chunks are currently bounded by extracted page contents, so information spanning page boundaries may be separated.
* Retrieval always returns the closest matching chunks even when none are strongly relevant.
* Bibliography and reference sections can sometimes rank highly because of their dense topic-related terminology.
* Similarity distances are useful for debugging but are not user-friendly confidence scores.
* Scanned or image-only PDFs are not currently supported because SourceRecall does not perform OCR.
* RAG retrieval is not a replacement for structured analysis when tasks require reliable calculations across an entire dataset.

## Future Improvements

* Add a Streamlit web interface
* Add a public interactive demo
* Add configurable `top_k`
* Add semantic or section-aware chunking experiments
* Expand evaluation to multiple documents and document types
* Add support for multiple document collections
* Improve handling of bibliography and reference sections
* Add document category filtering
* Add duplicate-source handling in retrieval output
* Explore PostgreSQL and pgvector as an alternative vector storage backend
* Add structured extraction for use cases that require reliable aggregation or calculations

## What I Learned

This project helped me understand that RAG is not simply "asking an LLM a question." A useful RAG system requires an entire pipeline around the model: ingestion, preprocessing, chunking, embeddings, vector storage, retrieval, prompt construction, generation, metadata tracking, and evaluation.

Adding PDF support also showed me why source provenance matters. Retrieving the correct document is useful, but retaining page-level metadata makes retrieved information much easier to inspect and verify.

Building a retrieval benchmark reinforced another important lesson: a RAG system can produce plausible answers while still having weak retrieval. Evaluating the retriever separately makes it possible to identify failures and measure whether future changes actually improve the system.

I also learned that retrieval has limitations. Semantic similarity does not automatically mean relevance, and dense sections such as bibliographies can sometimes appear highly similar to a query even when they are not the best source for answering it.

## Status

**MVP complete — currently being expanded into an evaluated, interactive RAG application.**

SourceRecall currently supports `.txt`, `.md`, and `.pdf` ingestion, page-aware PDF provenance, local embeddings, ChromaDB vector retrieval, source-grounded local LLM generation, and page-level retrieval evaluation.

Current baseline retrieval performance on the initial 25-question technical-PDF benchmark:

* Hit@1: **48%**
* Hit@3: **80%**
* Hit@5: **92%**

The next milestone is an interactive Streamlit interface and public demo.