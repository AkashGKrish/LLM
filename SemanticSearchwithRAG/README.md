# AI Assignment

The core of the assignment is to take the attached source document and create a multi-modal (text + images) semantic search engine using Langchain or Llamaindex:

- The goal of the engine is to be able to reliably return 2-3 most semantically relevant artefacts to the user query - either small chunks of text alone (something between 500-1000 characters per chunk), or images alone, or chunks of text + images, depending on the relevance to the user query

- The second part of the assignment is completely optional as we do not want you to spend any money on proprietary text generation models, however, you can but do not have to, optionally implement this second part as well, which would be adding the text generation on top of the multi-modal semantic search, making it eventually multi-modal retrieval augmented generation (RAG) system which would, apart from the search itself, be able to generate the final answer to the user query in natural language based on the retrieved context. As mentioned before, this is not mandatory, so it is completely up to you. There is also a possibility to use some open-source/open-weights text generation model for this non-mandatory second component of the assignment

- The only requirements for the technologies you use is Langchain or Llamaindex. You can get creative with everything else and choose freely whatever you find appropriate for the task at hand

- The format of your final solution can be either a shared Google Colab, or a link to the GH repo with the code, or a Streamlit app with very basic UI. However, due to the fact that developing the UI is not at all important for the assignment, shared Google Colab or GH repo would be the go-to choices

- Optional parts
  - dockerize the whole project

## Requirements

To set up the project environment, follow these steps:

### 1. Clone the Repository

First, clone the repository to your local machine:

    $ git clone <repository-url> 

### 2. Python Environment Setup

    $ python -m venv env
    $ source env/bin/activate

### 3. Install Dependencies

    $ pip install -r requirements.txt

## Additional Information

- Delete the datastore folder and image folder before executing the codeblocks for the first time.
- Make sure you have a access token from <https://huggingface.co/settings/tokens>, before you start the AI text generation part.
