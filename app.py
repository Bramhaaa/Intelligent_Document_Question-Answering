import os
import sys

# CRITICAL: Set these BEFORE any other imports
os.environ['TOKENIZERS_PARALLELISM'] = 'false'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import streamlit as st
import tempfile
from dotenv import load_dotenv

# Simple imports only - no PyTorch/TensorFlow
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# Validate API Key
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    st.error("⚠️ GOOGLE_API_KEY not found. Please add it to your .env file.")
    st.stop()

# Page Configuration
st.set_page_config(
    page_title="Learn from PDF",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

st.title("💬 Learn from PDF")

# Initialize
if 'documents' not in st.session_state:
    st.session_state.documents = {}
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# File uploader
if not st.session_state.documents:
    uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)
else:
    st.success(f"✅ {len(st.session_state.documents)} document(s) loaded")
    col1, col2 = st.columns([3, 1])
    with col1:
        with st.expander("➕ Upload more PDFs"):
            uploaded_files = st.file_uploader("Add more PDFs", type="pdf", accept_multiple_files=True, key="more_files")
    with col2:
        if st.button("🗑️ Clear All", use_container_width=True, type="primary"):
            st.session_state.clear()
            st.rerun()

# Process PDFs
if uploaded_files:
    for uploaded_file in uploaded_files:
        if uploaded_file.name in st.session_state.documents:
            continue
            
        with st.spinner(f"Processing {uploaded_file.name}..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(uploaded_file.getvalue())
                temp_file_path = temp_file.name

            try:
                loader = PyPDFLoader(temp_file_path)
                docs = loader.load()
                
                # Store full text
                full_text = "\n\n".join([f"[Page {i+1}]\n{doc.page_content}" for i, doc in enumerate(docs)])
                
                st.session_state.documents[uploaded_file.name] = {
                    'text': full_text,
                    'pages': len(docs)
                }
                
                st.success(f"✓ {uploaded_file.name} loaded ({len(docs)} pages)")
                
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                os.remove(temp_file_path)
    
    # Only rerun after processing is complete
    st.rerun()

# Chat Interface
if st.session_state.documents:
    st.divider()
    
    # Show loaded documents
    doc_names = ", ".join(st.session_state.documents.keys())
    st.info(f"📚 Loaded: {doc_names}")
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Process last message if it needs a response
    if (st.session_state.chat_history and 
        st.session_state.chat_history[-1]["role"] == "user"):
        
        user_question = st.session_state.chat_history[-1]["content"]
        
        # Build context from all documents (first 50k chars to avoid token limits)
        all_text = "\n\n---\n\n".join([
            f"Document: {name}\n{doc['text'][:20000]}" 
            for name, doc in st.session_state.documents.items()
        ])
        
        # Build conversation context
        conversation = ""
        if len(st.session_state.chat_history) > 1:
            recent = st.session_state.chat_history[-7:-1]
            conversation = "Previous conversation:\n" + "\n".join([
                f"{m['role']}: {m['content']}" for m in recent
            ]) + "\n\n"
        
        prompt = f"""{conversation}Documents:
{all_text}

Question: {user_question}

Answer the question based on the documents above. Be concise and cite page numbers when possible."""
        
        # Stream response
        with st.chat_message("assistant"):
            try:
                llm = ChatGoogleGenerativeAI(
                    model="gemini-2.5-flash",
                    google_api_key=API_KEY,
                    temperature=0.3,
                    max_retries=2
                )
                
                message_placeholder = st.empty()
                full_response = ""
                
                for chunk in llm.stream(prompt):
                    full_response += chunk.content
                    message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
                
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": full_response
                })
                
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.error(error_msg)
                st.info("Check your API key and quota at https://aistudio.google.com/")
    
    # Chat input (always show at bottom)
    user_question = st.chat_input("Ask a question about your documents...")
    
    if user_question:
        st.session_state.chat_history.append({"role": "user", "content": user_question})
        st.rerun()
        
else:
    st.info("👆 Upload a PDF to get started")
