from rdflib import Graph
from rdflib.plugins.stores.sparqlstore import SPARQLStore
import rdflib.exceptions
import requests

def upload_to_fuseki(file_path: str, fuseki_url: str, format: str = 'ttl') -> bool:
    """
    Uploads data in a Turtle file to a Fuseki endpoint.

    Args:
        file_path (str): The path to the Turtle file containing the data to be uploaded (file name included).
        fuseki_url (str): The URL of the Fuseki endpoint to which the data will be uploaded.
        format (str, optional): The format of the file to be uploaded. Defaults to 'ttl'.

    Returns:
        bool: True if the data is uploaded successfully, False otherwise.
    """
    try:
        # Create a new graph
        knowledge_graph = Graph()
        
        # Parse the TTL file
        knowledge_graph.parse(file_path, format=format)
        
        # Serialize the graph to N-Triples
        n_triples = knowledge_graph.serialize(format='nt')
        
        # Send the data to Fuseki
        headers = {'Content-Type': 'application/n-triples'}
        response = requests.put(fuseki_url, data=n_triples, headers=headers)
        
        # Check the response status
        if response.status_code == 200:
            print("Data uploaded successfully")
            return True
        else:
            print("Error uploading data:", response.text)
            return False
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

def fetch_ontology(query_endpoint: str, data_file_path: str = None) -> rdflib.Graph:
    """Retrieves data from an ontology stored in a SPARQL endpoint.

    Args:
        query_endpoint (str): The URL of the SPARQL endpoint containing the ontology.
        data_file_path (str, optional): The path to a Turtle file containing the ontology data. If provided, the ontology data will be parsed from this file instead of being fetched from the SPARQL endpoint.

    Returns:
        The extracted ontology data as an RDF Graph.

    Raises:
        ValueError: If both `query_endpoint` and `data_file_path` are not provided.
        rdflib.exceptions.RDFError: If there's an error parsing the ontology data.
        rdflib.exceptions.SPARQLStoreError: If there's an error connecting to or querying the SPARQL endpoint.
    """

    if not query_endpoint and not data_file_path:
        raise ValueError("Either `query_endpoint` or `data_file_path` must be provided.")
    ontology_graph = Graph()

    if data_file_path:
        try:
            ontology_graph.parse(data_file_path, format="turtle")
        except rdflib.exceptions.RDFError as e:
            raise rdflib.exceptions.RDFError(f"Error parsing ontology data from {data_file_path}: {e}")
    else:
        store = SPARQLStore(query_endpoint)
        ontology_graph = Graph(store)

    return ontology_graph