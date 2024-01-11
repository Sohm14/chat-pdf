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

## Instructions
1. Run the Streamlit app:
   ``` bash
   streamlit run main.py
2. Open your web browser and go to the link provided in the terminal
3. Upload PDF and TXT files, and use the app to query the document index.

## Dependencies
1. Streamlit
2. llama_index
3. langchain
4. OpenAI API

## Configuration
Create a .env file in the project root and add your OpenAI API key obtained from the OpenAI website:
```bash
OPENAI_API_KEY=your-api-key-goes-here
