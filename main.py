import os
import streamlit as st
from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext, get_response_synthesizer
from langchain.llms import OpenAI
from dotenv import load_dotenv
from llama_index.retrievers import VectorIndexRetriever
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.postprocessor import SimilarityPostprocessor

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')

st.title("Chat PDF")

uploaded_files = st.sidebar.file_uploader(
    label="#### Upload Your Data File",
    type=["pdf", "txt"],
    key="file_uploader",
    accept_multiple_files=True
)

# Initialize loading status
loading_status = st.sidebar.empty()

if 'loaded' not in st.session_state:
    st.session_state.loaded = False
    st.session_state.query_engine = None
    st.session_state.history = []  # Keep track of input and output history


def load_document():
    llm = OpenAI(openai_api_key=openai_api_key, temperature=0, model_name="gpt-3.5-turbo", max_tokens=512)
    if not os.path.exists("files"):
        os.makedirs("files")
    for uploaded_file in uploaded_files:
        file_temp = uploaded_file.name.split('.')[0] + "_temp." + uploaded_file.name.split('.')[1]
        file_path = os.path.join("files", file_temp)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())

    existing_files = os.listdir("files")
    files_to_keep = {f"{uploaded_file.name.split('.')[0]}_temp.{uploaded_file.name.split('.')[1]}" for uploaded_file in
                     uploaded_files}
    files_to_remove = set(existing_files) - files_to_keep
    for file_name in files_to_remove:
        file_path = os.path.join("files", file_name)
        os.remove(file_path)

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
    response_status.text("Querying... Please wait.")
    response = query_engine.query(query)
    response_status.empty()
    if response is None:
        st.error(f"Oops! No result found ")
    else:
        st.success(f"\nBot says :\n\n{response.response}\n\n\n")
        # Save input and output to history
        st.session_state.history.append({"input": query, "output": response.response})


if uploaded_files and st.sidebar.button('Load'):
    loading_status.text("Loading documents... Please wait.")
    try:
        load_document()
        loading_status.empty()
        loading_status.success("Documents loaded successfully!")
        st.session_state.loaded = True
    except Exception as e:
        st.error(f"An error occurred: {e}")

if st.session_state.loaded:
    # Display history
    if st.session_state.history:
        st.subheader("Conversation History:")
    for entry in st.session_state.history:
        st.write(f"User: {entry['input']}")
        st.write(f"Bot: {entry['output']}")
        st.write("-" * 30)

    # Take new input
    query = st.text_input("What would you like to ask?", "")
    query = query + " based on documents uploaded"
    response_status = st.empty()
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
                    st.error("Not a valid openai key")
            except Exception as e:
                st.error(f"An error occurred: {e}")
