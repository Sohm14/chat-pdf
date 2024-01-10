import os
import streamlit as st
from llama_index import VectorStoreIndex, SimpleDirectoryReader, PromptHelper, ServiceContext, StorageContext, \
    get_response_synthesizer
from langchain.llms import OpenAI
from dotenv import load_dotenv
from llama_index.retrievers import VectorIndexRetriever
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.postprocessor import SimilarityPostprocessor

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')

uploaded_files = st.file_uploader(
    label="#### Upload Your Data File",
    type=["pdf", "txt"],
    key="file_uploader",
    accept_multiple_files=True
)


def load_document():
    llm = OpenAI(openai_api_key=openai_api_key, temperature=0, model_name="gpt-3.5-turbo", max_tokens=512)
    for uploaded_file in uploaded_files:
        if not os.path.exists("files"):
            os.makedirs("files")
        file_path = os.path.join("files", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())
    documents = SimpleDirectoryReader('./files').load_data()
    service_context = ServiceContext.from_defaults(llm=llm)
    index = VectorStoreIndex.from_documents(documents, service_context=service_context)
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=10,
    )

    # configure response synthesizer
    response_synthesizer = get_response_synthesizer()

    # assemble query engine
    st.session_state.query_engine = RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
        node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7)],
    )


def get_response(query):
    query_engine = st.session_state.query_engine
    response = query_engine.query(query)
    for uploaded_file in uploaded_files:
        file_path = os.path.join("files", uploaded_file.name)
        os.remove(file_path)

    if response is None:
        st.error(f"Oops! No result found ")
    else:
        st.success(f"\nBot says :\n\n{response.response}\n\n\n")


if uploaded_files and st.button('Load'):
    load_document()

st.title("Chat PDF")

query = st.text_input("What would you like to ask?", "")
query = query + " based on documents uploaded"

if st.button("Submit"):
    if not query.strip():
        st.error(f"Please provide the search query.")
    else:
        try:
            if len(openai_api_key) > 0:
                if st.session_state.query_engine is not None:
                    get_response(query)
                else:
                    st.error("Please load the documents before submitting the query.")
            else:
                st.error("Enter a valid openai key")
        except Exception as e:
            st.error(f"An error occurred: {e}")
