import streamlit as st
import os
import tempfile
from dotenv import load_dotenv

# Import LangChain components
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="Chat with PDF",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Minimal CSS
st.markdown("""
    <style>
    .main {
        max-width: 800px;
    }
    h1 {
        font-size: 2rem;
        font-weight: 500;
        margin-bottom: 2rem;
    }
    .stChatMessage {
        padding: 1rem;
    }
    div[data-testid="stFileUploader"] {
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.title("Chat with PDF")

# Initialize documents storage
if 'documents' not in st.session_state:
    st.session_state.documents = {}

# Show file uploader
if len(st.session_state.documents) == 0:
    st.markdown("##### Upload PDF documents to start chatting")
    uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)
else:
    # Show document manager
    with st.expander(f"📚 Loaded Documents ({len(st.session_state.documents)})", expanded=False):
        for doc_name in list(st.session_state.documents.keys()):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.text(doc_name)
            with col2:
                st.text(f"{st.session_state.documents[doc_name]['pages']} pages")
            with col3:
                if st.button("🗑️", key=f"del_{doc_name}"):
                    del st.session_state.documents[doc_name]
                    st.rerun()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ Add More Documents", use_container_width=True):
                st.session_state.show_uploader = True
                st.rerun()
        with col2:
            if st.button("Clear All", use_container_width=True):
                st.session_state.documents = {}
                if 'chat_history' in st.session_state:
                    del st.session_state.chat_history
                st.rerun()
    
    st.divider()
    
    # Show uploader if requested
    if st.session_state.get('show_uploader', False):
        uploaded_files = st.file_uploader("Add more PDF files", type="pdf", accept_multiple_files=True)
        if uploaded_files:
            st.session_state.show_uploader = False
    else:
        uploaded_files = None

# Process uploaded files
if uploaded_files:
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-l6-v2")
    
    for uploaded_file in uploaded_files:
        # Skip if already loaded
        if uploaded_file.name in st.session_state.documents:
            continue
            
        with st.spinner(f"Processing {uploaded_file.name}..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(uploaded_file.getvalue())
                temp_file_path = temp_file.name

            try:
                loader = PyPDFLoader(temp_file_path)
                docs = loader.load()
                
                # Add document name to metadata
                for doc in docs:
                    doc.metadata['source_document'] = uploaded_file.name

                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000, 
                    chunk_overlap=200
                )
                splits = text_splitter.split_documents(docs)

                vector_store = FAISS.from_documents(splits, embeddings)
                
                # Store document info
                st.session_state.documents[uploaded_file.name] = {
                    'vector_store': vector_store,
                    'pages': len(docs),
                    'chunks': len(splits)
                }
                
                st.success(f"✓ {uploaded_file.name} loaded ({len(docs)} pages)")
                
            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {e}")
            
            finally:
                os.remove(temp_file_path)
    
    st.rerun()

# Chat Interface
if len(st.session_state.documents) > 0:
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            # Show source document if available
            if message.get("source_docs"):
                st.caption(f"📄 Sources: {', '.join(set(message['source_docs']))}")
    
    # Initialize the Gemini Chat Model
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.3
    )

    # Chat input
    user_question = st.chat_input("Ask a question about your documents...")
    
    if user_question:
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": user_question})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_question)
        
        # Retrieve from all documents
        all_related_docs = []
        for doc_name, doc_info in st.session_state.documents.items():
            retriever = doc_info['vector_store'].as_retriever(search_kwargs={"k": 2})
            docs = retriever.invoke(user_question)
            all_related_docs.extend(docs)
        
        # Sort by relevance and take top results
        all_related_docs = all_related_docs[:6]
        
        # Combine context with source document names
        context_parts = []
        source_docs = []
        for doc in all_related_docs:
            source_name = doc.metadata.get('source_document', 'Unknown')
            source_docs.append(source_name)
            context_parts.append(f"[From: {source_name}]\n{doc.page_content}")
        
        context_text = "\n\n".join(context_parts)
        
        prompt = f"""Answer the question based on the provided context from multiple documents.

Context:
{context_text}

Question: {user_question}

Provide a clear and concise answer. If information comes from multiple documents, mention which document each piece of information is from."""
        
        # Stream the answer
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            for chunk in llm.stream(prompt):
                full_response += chunk.content
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
            # Show source documents
            unique_sources = list(set(source_docs))
            st.caption(f"📄 Sources: {', '.join(unique_sources)}")
        
        # Add assistant message to history
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": full_response,
            "source_docs": unique_sources
        })