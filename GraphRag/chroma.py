import chromadb
import ollama

def setup_chromadb(collection_name: str, path: str = "./chroma_data") -> chromadb.Collection:
    """
    Create a ChromaDB client and a collection for storing embeddings and text documents.

    This function creates a ChromaDB client and a collection with the given name.
    The collection is used to store embeddings and text documents.

    Args:
        collection_name (str): The name of the collection to be created in ChromaDB.

    Returns:
        chromadb.Collection: A ChromaDB collection.
    """
    # Create a ChromaDB client
    # client = chromadb.Client()
    # client = chromadb.HttpClient(host='localhost', port=8000)
    client = chromadb.PersistentClient(path=path)
    # Create a collection for storing embeddings and text documents
    collection = client.get_or_create_collection(name=collection_name)
    
    return collection


def knowledge_entities_to_chromadb(
    Knowledge_Entities: list[str], 
    collection: chromadb.Collection, 
    model: str = "mxbai-embed-large"
) -> None:
    """
    Store each document in a vector embedding database in ChromaDB.

    This function takes a list of text documents representing knowledge entities,
    a collection, and the name of a language model as input, generates an embedding
    for each document using the specified language model, and then adds the embedding,
    document ID, and the document itself to the collection in ChromaDB.

    Args:
        Knowledge_Entities (list[str]): List of text documents representing knowledge entities.
        collection (chromadb.Collection): ChromaDB collection where the embeddings will be stored.
        client (chromadb.Client): ChromaDB client.
        model (str): Name of the language model to use for generating embeddings by default model is mxbai-embed-large.
    """
    # store each document in a vector embedding database
    for i, d in enumerate(Knowledge_Entities):
        # generate an embedding for each document
        response = ollama.embeddings(model=model, prompt=d)
        embedding = response["embedding"]
        # add the embedding, document ID, and the document itself to ChromaDB
        collection.add(
            ids=[str(i)],
            embeddings=[embedding],
            documents=[d]
        )