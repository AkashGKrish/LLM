from langchain_ollama import OllamaLLM
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import warnings


def get_prompt_templates(filepath):
    with open(filepath, 'r') as file:
        prompts = file.readlines()
        prompts = [s.strip() for s in prompts]
    return prompts

warnings.filterwarnings('ignore')

# model="llama3.1:latest"
# model="llama3.1:70b"
# model="llama3.2:latest"
# llm = OllamaLLM(model=model)

file_path = "ontology_to_text.txt"


def get_sparql_response(knowledge_graph,question,model):

    # question="list all the concepts present in the knowledge graph"

    prompt_template = """
    Task:Generate Sparql query to query a rdf knowledge graph database like fuseki.
    Instructions:
    Use only the provided prefixes, otologies, subject, predicate, ojects and properties in the knowledge graph.
    Do not use any other relationship types,predicate, object or properties that are not provided.
    Semantically related Knowledge graphs are as follows:
    {knowledge_graph}

    Note:
    Do not include any explanations or apologies in your responses.
    Do not respond to any questions that might ask anything else than for you to construct a Query.
    Do not include any text except the generated Query statement.
    If the question is not about query, respond with "False"
    Always include the relevant prefixes
    write complete address of objects predicates and subjects
    The question is:
    {question}
"""

    prompt = PromptTemplate(template=prompt_template, input_variables=["knowledge_graph", "question"])

    llm = OllamaLLM(model=model)
    chain = LLMChain(llm=llm, prompt=prompt)


    response = chain.run(question=question, knowledge_graph=knowledge_graph)
    
    return response



def get_nl_response(knowledge_graph,question,model):

    # question="list all the concepts present in the knowledge graph"

    prompt_template = """
    
    System Prompt:
    You are a highly capable assistant designed to interact with semantic RDF data to provide precise and factual answers. You will receive user queries along with semantically similar RDF data describing relationships, domains, ranges, and properties in natural language.

    Your task is to:

    Parse the RDF data to extract meaningful insights related to the user query.
    Base your response strictly on the RDF data provided.
    If the data does not contain enough information to answer the query, inform the user that the information is not available in the data.
    Avoid assumptions or inferences not explicitly supported by the RDF data.
    
    Example:
    User Query: "What is the range of distance?"
    
    RDF Data Provided:

    Subject: http://purl.org/toco/hasDistance
    Objects and Predicates:
    - Predicate: http://www.w3.org/2000/01/rdf-schema#comment, Object: the Euclidean distance between the LiFi user equipment and access point.
    - Predicate: http://www.w3.org/2000/01/rdf-schema#range, Object: http://www.w3.org/2001/XMLSchema#float
    Your Response: "The range of distance is defined as a float, which typically represents a numerical value. Specifically, it describes the Euclidean distance between the LiFi user equipment and access point."

    User Query: "What is the antenna height?" RDF Data Provided:

    Subject: http://purl.org/toco/hasAntennaHeight
    Objects and Predicates:
    - Predicate: http://www.w3.org/2000/01/rdf-schema#comment, Object: the height of the antenna of a wireless interface
    - Predicate: http://www.w3.org/2000/01/rdf-schema#range, Object: http://www.w3.org/2001/XMLSchema#float
    Your Response: "The antenna height is described as a numerical value (float) representing the height of the antenna of a wireless interface."
    Instructions:
    Use only the provided prefixes, otologies, subject, predicate, objects and properties in the knowledge graph.
    Do not use any other relationship types,predicate, object or properties that are not provided.
    Semantically related Rdf data /Konwledge graph and its description is as follows:
    {knowledge_graph}

    Note:
    Do not include any explanations or apologies in your responses.
    Do not give me sparql queries
    Only respond to questions related to knowledge graph 
    The question is:
    {question}
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=["knowledge_graph", "question"])

    llm = OllamaLLM(model=model)
    chain = LLMChain(llm=llm, prompt=prompt)


    response = chain.run(question=question, knowledge_graph=knowledge_graph)
    
    return response