# Chat PDF Streamlit App

This is a Streamlit app that allows users to upload PDF and TXT files, load them into a document index, and query the index using a Chatbot powered by the OpenAI API.

## Table of Contents

- [Installation](#installation)
- [Instructions](#Instructions)
- [Dependencies](#dependencies)
- [Configuration](#configuration)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/velocius-ailabs/rag-poc.git 
2. Navigate to the project directory:
   ``` bash
   cd rag-poc
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
4. Run command to download tokenizer model and use it for one time
   ```bash
   embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
5. Or Clone repository from hugging face
   ```bash
   git clone https://huggingface.co/BAAI/bge-small-en-v1.5

## Instructions
1. Run the Streamlit app:
   ``` bash
   streamlit run main.py
2. Open your web browser and go to the link provided in the terminal
3. Upload PDF and TXT files
4. Enter your OpenAI or Groq API key. 
5. Use the app to query the document index.

## Dependencies
1. Streamlit
2. llama_index
3. langchain
4. OpenAI API
5. Groq API

