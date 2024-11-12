from kgConnection import fetch_ontology
from ontoToText import get_ontology_data
from chroma import setup_chromadb, knowledge_entities_to_chromadb
import chromadb
import ollama
import logging
from kgRag import get_nl_response, get_sparql_response
import warnings

warnings.filterwarnings('ignore')

def similarity_search(
    collection: chromadb.Collection, 
    prompt: str, 
    model: str = "mxbai-embed-large", 
    num_entities: int = 5 
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


def populate_db(query_endpoint, collection, logger):
    """
    Populate ChromaDB with knowledge entities.

    This function takes a query endpoint, a collection, and a logger as input, 
    fetches the ontology data from the query endpoint, extracts the knowledge entities 
    from the ontology data, and then populates the collection with the knowledge entities.

    Args:
        query_endpoint (str): The URL of the SPARQL endpoint containing the ontology.
        collection (chromadb.Collection): The ChromaDB collection to be populated.
        logger (logging.Logger): A logger for logging the progress of the function.
    """
    # Fetch the ontology data from the query endpoint
    knowledge_graph = fetch_ontology(query_endpoint)
    
    # Extract the knowledge entities from the ontology data
    Knowledge_Entities = get_ontology_data(knowledge_graph)
    
    # Populate the collection with the knowledge entities
    logger.info("Populating ChromaDB with knowledge entities...")
    knowledge_entities_to_chromadb(Knowledge_Entities, collection)
    logger.info("ChromaDB population completed.")

def chat(collection, logger):
    while True:
        logger.info("Starting Chat")    
        try:
            user_prompt = input("Enter your query or enter 'exit' to stop: ")
            if user_prompt.lower() == 'exit':
                logger.info("Exiting Chat")
                break
            
            
            logger.info(f"Performing similarity search for query: {user_prompt}")
            relevant_documents = similarity_search(collection, user_prompt)
            logger.info("Similarity search completed.")
            knowledge_graph_text=''
            # print("\nMost Relevant Documents:")
            
            for i, doc in enumerate(relevant_documents):
                knowledge_graph_text+=f"{i+1}. {doc}"
            
            response = get_sparql_response(knowledge_graph = knowledge_graph_text,question = user_prompt)

            print("Response: ",response)
        except Exception as e:
            logger.error(f"Error occurred during similarity search: {str(e)}")
            print("An error occurred. Please try again.")
        

def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    query_endpoint = 'http://localhost:3030/rdfLlmOwl'

    # Set up ChromaDB
    logger.info("Setting up ChromaDB")
    collection = setup_chromadb("Knowledge_Entities")
    logger.info("ChromaDB setup completed.")        

    menu = """Make yor selection: 0, 1 or 2 
    0) Exit
    1) Populate DB
    2) Start Chat
    """
    
    while True:
        selection=int(input(menu))
        
        if selection==0:
            break
        elif selection == 1:
            populate_db(query_endpoint, collection, logger) 
        elif selection == 2:
            chat(collection, logger)

    logger.info("Program execution completed.")

if __name__ == "__main__":
    main()