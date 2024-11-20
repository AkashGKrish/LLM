# Retrievel Augmented Generation Pipeline using Pre-Trained Open Source Ollama hosted LLMs with Knowledge Graphs

![Alt text](kgRAG.svg)

## Getting started

1. Install requirements.txt file using pip for required libraries.
2. Install latest versionof Apache Fueski from the [Apache Fueski website](https://jena.apache.org/download/).
3. install compatible Java version and set JAVA_HOME environment variable.
4. Setup your Ollama server from [Ollama website](https://ollama.com/).
5. Start ollama server - `ollama serve`

## Usage

1. Install the python dependencies from the requirements.txt file.
    - `pip install -r requirements.txt`
2. Upload the RDF data to Fuseki datastore (Have to do it only once)
3. Pull Embedding and selected llama model 3.1:70b in ollama server.
    - `ollama run llama3.1:70b`
    - `ollama pull mxbai-embed-large`
4. Populate the ChromaDB vector DB with Knowledge embeddings (Have to do it only once)
5. Now use the chat option to query, update and enhance the knowledge graph.
