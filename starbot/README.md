# StarBot

A chatbot that answers questions based on custom data using free LLM models.

## Features

- Uses free LLM models via Ollama
- Answers questions based only on provided data
- Responds with "I don't know" when information is not available
- Supports multiple data sources (text files, PDFs, websites)

## Requirements

- Python 3.8+
- Ollama installed and running locally

## Installation

1. Clone this repository
2. Install the package:

```bash
pip install -e .
```

## Usage

### Ingesting Data

You can ingest data from various sources:

```bash
# Ingest text files
starbot ingest --text path/to/file1.txt path/to/file2.txt

# Ingest PDF files
starbot ingest --pdf path/to/file.pdf

# Ingest websites
starbot ingest --url https://example.com

# Ingest all text files in a directory
starbot ingest --dir path/to/directory

# Combine multiple sources
starbot ingest --text path/to/file.txt --url https://example.com
```

### Starting a Chat Session

After ingesting data, you can start a chat session:

```bash
starbot chat
```

## How It Works

StarBot uses the following components:

1. **Data Ingestion**: Loads data from various sources and splits it into chunks
2. **Embedding**: Converts text chunks into vector embeddings using Ollama
3. **Vector Storage**: Stores embeddings in a Chroma vector database
4. **Retrieval**: Finds relevant information based on user queries
5. **Response Generation**: Generates answers using only the retrieved information

## Models

StarBot uses the following Ollama models by default:

- LLM: `mistral` (for generating responses)
- Embeddings: `nomic-embed-text` (for creating vector embeddings)

Make sure these models are available in your Ollama installation.
