import os
import streamlit as st
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader, LLMPredictor, PromptHelper, ServiceContext
from langchain.llms.openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')

uploaded_files = st.file_uploader(
    label="#### Upload Your Data File",
    type=["pdf"],
    key="file_uploader",
    accept_multiple_files=True
)


def get_response(query, openai_api_key):
    llm_predictor = LLMPredictor(
        llm=OpenAI(openai_api_key=openai_api_key, temperature=0, model_name="text-davinci-003", max_tokens=512))

    # Configure prompt parameters and initialise helper
    max_input_size = 4096
    num_output = 256
    max_chunk_overlap = 20

    prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_path = os.path.join("files", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())

        documents = SimpleDirectoryReader('./files').load_data()
        using openai as the LLM
        service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor,prompt_helper=prompt_helper)
        # using 'llama2-chat-13B' as the default LLM
        # service_context = ServiceContext.from_defaults()
        index = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)
        response = index.query(query)
        for uploaded_file in uploaded_files:
            file_path = os.path.join("files", uploaded_file.name)
            os.remove(file_path)
        if response is None:
            st.error(f"Oops! No result found ")
        else:
            st.success(f"\nBot says :\n\n{response.response}\n\n\n")


st.title("Chat PDF")
query = st.text_input("What would you like to ask?", "")
query = query + " based on documents uploaded"

if st.button("Submit"):
    if not query.strip():
        st.error(f"Please provide the search query.")
    else:
        try:
            if len(openai_api_key) > 0:
                get_response(query, openai_api_key)
            else:
                st.error(f"Enter a valid openai key")
        except Exception as e:
            st.error(f"An error occurred: {e}")
