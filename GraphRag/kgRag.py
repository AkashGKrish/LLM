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
model="llama3.1:70b"
# model="llama3.2:latest"
llm = OllamaLLM(model=model)

file_path = "ontology_to_text.txt"




def get_sparql_response(knowledge_graph,question):

    # question="list all the concepts present in the knowledge graph"

    prompt_template = """
    Task:Generate Sparql query to query a graph database.
    Instructions:
    Use only the provided prefixes, otologies, subject, predicate, ojects and properties in the knowledge graph.
    Do not use any other relationship types,predicate, object or properties that are not provided.
    Konwledge:
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

    chain = LLMChain(llm=llm, prompt=prompt)


    response = chain.run(question=question, knowledge_graph=knowledge_graph)
    
    return response



def get_nl_response(knowledge_graph,question):

    # question="list all the concepts present in the knowledge graph"

    prompt_template = """
    Instructions:
    Use only the provided prefixes, otologies, subject, predicate, objects and properties in the knowledge graph.
    Do not use any other relationship types,predicate, object or properties that are not provided.
    Konwledge graph and its description is as follows:
    {knowledge_graph}

    Note:
    Do not include any explanations or apologies in your responses.
    Do not give me sparql queries
    Only respond to questions related to knowledge graph 
    The question is:
    {question}
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=["knowledge_graph", "question"])

    chain = LLMChain(llm=llm, prompt=prompt)


    response = chain.run(question=question, knowledge_graph=knowledge_graph)
    
    return response