import os
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from app.rag_service import RAGService

# 1. Load API configurations cleanly
load_dotenv(find_dotenv())

# 2. Configure the dashboard window layout
st.set_page_config(
    page_title="AI Document Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Document Assistant")
st.write("Upload company files or ask questions about your documents stored in the system.")

# Ensure a temporary directory exists for newly uploaded files
UPLOAD_DIR = "data"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# 3. FIX: Persist the RAG service and index documents ONLY ONCE
if "rag_service" not in st.session_state:
    try:
        # Create the service skeleton once
        service = RAGService()
        
        # Read and index ONLY text/csv files sitting in your data folder on startup
        existing_files = [f for f in os.listdir(UPLOAD_DIR) if f.endswith(('.txt', '.csv'))]
        for existing_file in existing_files:
            file_path = os.path.join(UPLOAD_DIR, existing_file)
            service.retriever.index_document(file_path)
            
        # Store the fully indexed service in session state permanently
        st.session_state.rag_service = service
        st.session_state.indexed_files = set(existing_files)
    except Exception as e:
        st.error(f"Initialization error: Check your .env file setup. Details: {e}")
        st.stop()

# Helper state tracking for chat logs
if "messages" not in st.session_state:
    st.session_state.messages = []
if "indexed_files" not in st.session_state:
    st.session_state.indexed_files = set()

# Sidebar utility layout (Handles file uploads and configurations)
with st.sidebar:
    st.header("Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload Text or CSV documents", 
        type=["txt", "csv"], 
        accept_multiple_files=True
    )
    
    if uploaded_files:
        new_files_added = False
        
        # Save incoming files to disk safely
        for uploaded_file in uploaded_files:
            if uploaded_file.name not in st.session_state.indexed_files:
                file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                    f.flush()
                    os.fsync(f.fileno())
                
                # Index the new file immediately into our existing running instance
                try:
                    st.session_state.rag_service.retriever.index_document(file_path)
                    st.session_state.indexed_files.add(uploaded_file.name)
                    new_files_added = True
                except Exception as e:
                    st.error(f"Error indexing {uploaded_file.name}: {e}")
        
        if new_files_added:
            st.toast("✅ New documents successfully indexed!", icon="🚀")
            st.success("Database fully updated!")

    st.header("Actions")
    if st.button("Clear Conversation Log"):
        st.session_state.messages = []
        st.sidebar.success("Chat history cleared!")
        st.rerun()

# 4. Display all previous messages (Enables historical scrolling)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. User interactive query input field (No-rerun configuration)
if question := st.chat_input("Ask a question about your documents"):
    
    # Render user query instantly on screen
    with st.chat_message("user"):
        st.markdown(question)
    
    # Save user query to historical message log
    st.session_state.messages.append({"role": "user", "content": question})
    
    # Fetch answer from your backend architecture
    with st.chat_message("assistant"):
        with st.spinner("Searching files..."):
            try:
                # Executes your verified backend query function
                response = st.session_state.rag_service.ask(question)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_msg = f"Error generating response: {e}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
