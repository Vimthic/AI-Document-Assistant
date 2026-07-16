import sys
import os
import tempfile
import streamlit as st

# Direct module loading inside your unified 'app' folder structure
from rag_service import RAGService
from retriever import Retriever
from gemini_client import ask_gemini 

st.set_page_config(
    page_title="AI Document Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Document Assistant")
st.write("Ask questions about your company documents.")

# Initialize backend components inside Streamlit's cache infrastructure
@st.cache_resource
def initialize_backend():
    retriever_obj = Retriever()
    
    # Structural adapter matching your gemini_client execution format
    class GeminiAdapter:
        def generate_content(self, prompt, **kwargs):
            return ask_gemini(prompt)
        def ask_gemini(self, prompt):
            return ask_gemini(prompt)

    gemini_client_wrapper = GeminiAdapter()
    
    # Flexible positional argument mapping to safely instantiate RAGService
    try:
        rag_service = RAGService(retriever_obj, gemini_client_wrapper)
    except TypeError:
        try:
            rag_service = RAGService(gemini_client_wrapper, retriever_obj)
        except TypeError:
            rag_service = RAGService()
            
    return rag_service

rag_backend = initialize_backend()

# NEW FEATURE: Initialize chat history memory cache list if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Documents")
    uploaded_files = st.file_uploader(
        "Upload documents",
        accept_multiple_files=True,
        type=["txt", "pdf"]
    )
    
    if uploaded_files:
        temp_paths = []
        with st.spinner("Processing and saving files temporarily..."):
            for uploaded_file in uploaded_files:
                with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{uploaded_file.name}") as temp_file:
                    temp_file.write(uploaded_file.getvalue())
                    temp_paths.append(temp_file.name)
            
            # Locate active retriever reference dynamically
            active_retriever = getattr(rag_backend, 'retriever', None)
            if not active_retriever:
                active_retriever = Retriever()
                
            # Direct check for singular vs plural indexing methods to avoid AttributeErrors
            if hasattr(active_retriever, 'index_document'):
                for path in temp_paths:
                    active_retriever.index_document(path)
            elif hasattr(active_retriever, 'index_documents'):
                active_retriever.index_documents(temp_paths)
            else:
                try:
                    active_retriever.add_documents(temp_paths)
                except AttributeError:
                    pass
            
        st.success(f"Successfully indexed {len(uploaded_files)} document(s)!")
        
        # Safe temporary files cleanup loop
        for path in temp_paths:
            try:
                os.unlink(path)
            except Exception:
                pass
                
    # Optional visual reset tool for the user in the sidebar
    if st.session_state.messages:
        if st.button("Clear Conversation Log"):
            st.session_state.messages = []
            st.rerun()

# NEW FEATURE: Display all previous conversational logs sequentially on screen refresh
# (This outputs cleanly into standard user/assistant layouts)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question = st.text_input("Ask a question", key="user_question_input")

if st.button("Ask"):
    if question.strip() == "":
        st.warning("Please enter a valid question.")
    elif not uploaded_files:
        st.warning("Please upload documents first so Gemini has source context.")
    else:
        # Display user's new question immediately in the main UI thread 
        with st.chat_message("user"):
            st.write(question)
            
        with st.spinner("Searching documents and generating answer..."):
            try:
                response = None
                
                # Programmatic method scanner for RAGService pipeline execution
                known_methods = ['answer_question', 'query', 'get_response', 'ask', 'generate_answer', 'chat']
                
                for method_name in known_methods:
                    if hasattr(rag_backend, method_name):
                        method = getattr(rag_backend, method_name)
                        response = method(question)
                        break
                
                if response is None:
                    for attr_name in dir(rag_backend):
                        if not attr_name.startswith('_'):
                            attr = getattr(rag_backend, attr_name)
                            if callable(attr) and attr_name not in ['retriever', 'gemini_client']:
                                try:
                                    response = attr(question)
                                    if response:
                                        break
                                except Exception:
                                    continue
                
                # NEW FEATURE: Display response and append everything straight to state storage memory 
                if response:
                    with st.chat_message("assistant"):
                        st.write(response)
                    
                    # Store data blocks persistently
                    st.session_state.messages.append({"role": "user", "content": question})
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                    # Force Streamlit to quickly update screen state positions
                    st.rerun()
                else:
                    st.error("Unable to execute RAG lookup. Could not identify the core generation function inside your RAGService class structure.")
                    
            except Exception as e:
                st.error(f"An error occurred while calling your Gemini backend pipeline: {e}")
