import streamlit as st
from kgConnection import fetch_ontology, upload_to_fuseki
from ontoToText import get_ontology_data
from chroma import setup_chromadb, knowledge_entities_to_chromadb
import ollama
import logging
from kgRag import get_nl_response
from dotenv import load_dotenv
import os
import chromadb

# Load environment variables
load_dotenv()

query_endpoint = os.getenv("QUERY_ENDPOINT")
chroma_path = os.getenv("CHROMA_PATH")
rdf_file_path = os.getenv("RDF_FILE_PATH")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize ChromaDB
collection = setup_chromadb("Knowledge_Entities", chroma_path)


def upload_file_to_fuseki(file_path, endpoint):
    """Uploads an RDF file to Apache Fuseki."""
    upload_to_fuseki(file_path, endpoint)
    return "File uploaded successfully!"


def populate_db(query_endpoint, collection, logger):
    """Populates ChromaDB with knowledge entities."""
    knowledge_graph = fetch_ontology(query_endpoint)
    Knowledge_Entities = get_ontology_data(knowledge_graph)
    knowledge_entities_to_chromadb(Knowledge_Entities, collection)
    logger.info("ChromaDB population completed.")
    return "ChromaDB populated successfully!"


def similarity_search(
    collection: chromadb.Collection, 
    prompt: str, 
    model: str = "mxbai-embed-large", 
    num_entities: int = 10 
) -> str:
    """
    Performs a similarity search using the provided prompt and model.

    This function takes a prompt and a collection of documents as input, generates an
    embedding for the prompt using the specified language model, and then retrieves the
    most relevant document from the collection based on the similarity between the prompt
    and the documents in the collection.

    Args:
        collection (chromadb.Collection): ChromaDB collection where the embeddings will be stored.
        prompt (str): The user's prompt (e.g. "What is the subclass of unit?").
        model (str): Name of the language model to use for generating embeddings by default model is mxbai-embed-large.
        num_entities (int): The number of relevant documents to retrieve from the collection.

    Returns:
        str: The most relevant document from the collection based on the similarity between the prompt and the documents in the collection.
    """

    # Generate an embedding for the prompt
    response = ollama.embeddings(
        prompt=prompt,
        model=model
    )

    # Retrieve the most relevant document from the collection
    results = collection.query(
        query_embeddings=[response["embedding"]],
        n_results= num_entities
    )
    # Return the most relevant document
    return results['documents'][0]


def chat(collection, logger, model):
    """Handles a chat query."""
    st.subheader("Chat Interface")
    user_prompt = st.text_input("Enter your query:")
    if st.button("Submit Query"):
        if user_prompt:
            try:
                logger.info(f"Performing similarity search for query: {user_prompt}")
                relevant_documents = similarity_search(collection, user_prompt)
                logger.info("Similarity search completed.")
                knowledge_graph_text = "\n".join(relevant_documents)

                response = get_nl_response(
                    knowledge_graph=knowledge_graph_text,
                    question=user_prompt,
                    model=model
                )
                st.write(f"Response: {response}")
            except Exception as e:
                logger.error(f"Error occurred during similarity search: {str(e)}")
                st.error("An error occurred. Please try again.")


# Streamlit UI
st.title("Knowledge Graph Assistant")
st.sidebar.title("Options")

# Sidebar
st.sidebar.subheader("Upload and Populate")
uploaded_file = st.sidebar.file_uploader("Upload a .ttl file", type=["ttl"])
if uploaded_file:
    save_path = f"./data/{uploaded_file.name}"
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.sidebar.success(f"File {uploaded_file.name} saved successfully.")

if st.sidebar.button("Upload to Fuseki"):
    if uploaded_file:
        st.sidebar.text(upload_file_to_fuseki(save_path, query_endpoint))
    else:
        st.sidebar.error("Please upload a file first.")

if st.sidebar.button("Populate ChromaDB"):
    st.sidebar.text(populate_db(query_endpoint, collection, logger))

# Model selection
st.sidebar.subheader("Model Selection")
model_options = ["llama3.1:latest", "llama3.1:70b", "llama3.2:latest"]
selected_model = st.sidebar.selectbox("Select a model", model_options)

# Chat window
chat(collection, logger, selected_model)

# Exit button
if st.sidebar.button("Close App"):
    st.write("Closing the app.")
    st.stop()
