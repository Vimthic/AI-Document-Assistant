'''
import os
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from app.rag_service import RAGService
from app.retriever import Retriever, FAISS_PATH, METADATA_PATH

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

# Core path configurations matching your new clean directory layout
UPLOAD_DIR = "storage/uploads"

# Ensure all individual folder segments exist automatically on system boot
os.makedirs("storage/faiss", exist_ok=True)
os.makedirs("storage/metadata", exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Helper state tracking for chat logs and file manifests
if "messages" not in st.session_state:
    st.session_state.messages = []
if "indexed_files" not in st.session_state:
    st.session_state.indexed_files = set()

# 3. Handle persistent FAISS startup indexing routines cleanly
if "rag_service" not in st.session_state:
    try:
        service = RAGService()
        
        # Check if physical index twins already sit inside data assets
        if Retriever.has_existing_index():
            with st.spinner("💾 Loading existing FAISS index structure from disk..."):
                service.retriever.load_existing_index()
            st.toast("⚡ Loaded index from storage!", icon="💾")
            
            # Populate our session state tracking with files that are inside storage/uploads
            st.session_state.indexed_files = set(os.listdir(UPLOAD_DIR))
        else:
            # If no index exists, build a brand new one from scratch
            with st.spinner("🏗️ No index found. Parsing local documents to build a new index..."):
                found_files = service.retriever.build_index(UPLOAD_DIR)
            st.session_state.indexed_files = set(found_files)
            if found_files:
                st.toast("🎉 Created new FAISS index files successfully!", icon="📝")

        # Store the fully indexed service in session state permanently
        st.session_state.rag_service = service
    except Exception as e:
        st.error(f"Initialization error: Check your .env file setup. Details: {e}")
        st.stop()

# Sidebar utility layout
with st.sidebar:
    st.header("Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload Text or CSV documents", 
        type=["txt", "csv"], 
        accept_multiple_files=True
    )
    
    if uploaded_files:
        just_indexed_now = []
        
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
                    just_indexed_now.append(uploaded_file.name)
                except Exception as e:
                    st.error(f"Error indexing {uploaded_file.name}: {e}")
            else:
                just_indexed_now.append(uploaded_file.name)
        
        # Save updated index state back to local storage paths individually
        if just_indexed_now:
            st.session_state.rag_service.retriever.store.save(FAISS_PATH, METADATA_PATH)
            st.success("🎉 **File Uploaded and Index updated successfully!**")
            for f_name in sorted(just_indexed_now):
                st.markdown(f"📄 `{f_name}`")

# 4. Display all previous messages (Enables historical scrolling)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. User interactive query input field
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

# 6. Position Clear Chat option cleanly under the chat box with backward-compatible syntax
if st.session_state.messages:
    col1, col2 = st.columns(2)
    with col2:
        if st.button("🧹 Clear Chat", use_container_width=True):
            st.session_state.messages = []  # Wipes conversation logs cleanly
            st.rerun()  # Forces immediate visual update to clear screen layout

#for streaming response
'''

import os
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from app.rag_service import RAGService
from app.retriever import Retriever, FAISS_PATH, METADATA_PATH

# 1. Load configuration environment variables cleanly
load_dotenv(find_dotenv())

# 2. Configure the premium dashboard window layout
st.set_page_config(
    page_title="AI Document Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Document Assistant")
st.write("Upload company files or ask questions about your documents stored in the system.")

# Check if a file upload success event happened and print a persistent completion banner
if "upload_success" in st.session_state and st.session_state.upload_success:
    st.success("🎉 **File upload and vector indexing completed successfully!**")
    # Reset the flag immediately so the banner disappears cleanly on your next chat interaction
    st.session_state.upload_success = False

# Core path configurations matching your clean directory layout
UPLOAD_DIR = "storage/uploads"

# Ensure all individual folder segments exist automatically on system boot
os.makedirs("storage/faiss", exist_ok=True)
os.makedirs("storage/metadata", exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Helper state tracking for chat logs and file manifests
if "messages" not in st.session_state:
    st.session_state.messages = []
if "indexed_files" not in st.session_state:
    st.session_state.indexed_files = set()

# PERFORMANCE CACHE FIX: Initialize the RAG engine once and preserve it across reruns
@st.cache_resource
def initialize_rag_system(upload_dir_path):
    """
    Builds or loads the heavy retriever pipeline exactly once.
    This prevents the app from rebuilding the index on every chat submission.
    """
    service = RAGService()
    if Retriever.has_existing_index():
        service.retriever.load_existing_index()
    else:
        service.retriever.build_index(upload_dir_path)
    return service

# 3. Handle persistent FAISS startup indexing routines cleanly using caching
try:
    if "rag_service" not in st.session_state:
        # Trigger the cached loader pattern safely
        st.session_state.rag_service = initialize_rag_system(UPLOAD_DIR)
        
        # Sync the session state manifest with existing disk records
        st.session_state.indexed_files = set(os.listdir(UPLOAD_DIR))
except Exception as e:
    st.error(f"Initialization error: Check your .env file setup. Details: {e}")
    st.stop()

# Short-circuit handle to track real-time engine counters cleanly
retriever_engine = st.session_state.rag_service.retriever

# Sidebar Control Center UI Layout
with st.sidebar:
    st.header("📊 System Status")
    
    with st.container(border=True):
        if Retriever.has_existing_index():
            st.markdown("🟢 **Index Loaded**")
        else:
            st.markdown("🟡 **Index Empty / Missing**")
            
        # Display the real-time counters processed by our retriever instance tracks
        doc_count = len(st.session_state.indexed_files)
        st.markdown(f"📄 **Indexed Documents:** {doc_count}")
        st.markdown(f"🧱 **Total Chunks:** {retriever_engine.total_chunks}")
        
    st.divider()

    st.header("Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload Text or CSV documents", 
        type=["txt", "csv"], 
        accept_multiple_files=True,
        key="production_document_uploader"
    )
    
    if uploaded_files:
        just_indexed_now = []
        
        for uploaded_file in uploaded_files:
            if uploaded_file.name not in st.session_state.indexed_files:
                file_path = os.path.join(UPLOAD_DIR, str(uploaded_file.name))
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                    f.flush()
                    os.fsync(f.fileno())
                
                try:
                    st.session_state.rag_service.retriever.index_document(str(file_path))
                    st.session_state.indexed_files.add(uploaded_file.name)
                    just_indexed_now.append(uploaded_file.name)
                except Exception as e:
                    st.error(f"Error indexing {uploaded_file.name}: {e}")
        
        if just_indexed_now:
            st.session_state.rag_service.retriever.store.save(FAISS_PATH, METADATA_PATH)
            
            # FIXED: Store a success flag in memory so it renders the banner after refreshing the page
            st.session_state.upload_success = True
            
            # Force immediate visual layout refresh to update sidebar counters and show banner
            st.rerun()

# 4. Display all previous messages (Enables historical scrolling layout)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. User interactive query input field
if question := st.chat_input("Ask a question about your documents"):
    
    # Render user query instantly on screen
    with st.chat_message("user"):
        st.markdown(question)
    
    # Save user query to historical message log
    st.session_state.messages.append({"role": "user", "content": question})
    
    # Fetch answer from your backend architecture
    with st.chat_message("assistant"):
        try:
            # 1. Fetch the generator stream from your RAG service
            response_stream = st.session_state.rag_service.ask(str(question))
            
            # 2. Consume the stream live on screen using st.write_stream
            full_response = st.write_stream(response_stream)
            
            # 3. Save the final combined text string into historical chat logs
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            error_msg = f"Error generating response: {e}"
            st.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})

# 6. Position Clear Chat option cleanly under the chat box
if st.session_state.messages:
    col1, col2 = st.columns(2)
    with col2:
        if st.button("🧹 Clear Chat", use_container_width=True):
            st.session_state.messages = []  
            st.rerun()
