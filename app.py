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

# Show file uploader only if no document loaded
if 'vector_store' not in st.session_state:
    st.markdown("##### Upload a PDF document to start chatting")
    uploaded_file = st.file_uploader("Choose a PDF", type="pdf")
else:
    # Show document name and clear option
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**Document:** {st.session_state.get('document_name', 'Unknown')}")
    with col2:
        if st.button("Clear", use_container_width=True):
            for key in ['vector_store', 'document_name', 'chat_history']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    st.divider()
    uploaded_file = None

# Process uploaded file
if uploaded_file is not None:
    with st.spinner("Processing..."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_file_path = temp_file.name

        try:
            loader = PyPDFLoader(temp_file_path)
            docs = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, 
                chunk_overlap=200
            )
            splits = text_splitter.split_documents(docs)

            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-l6-v2")
            vector_store = FAISS.from_documents(splits, embeddings)
            
            st.session_state.vector_store = vector_store
            st.session_state.document_name = uploaded_file.name
            st.success(f"Document loaded ({len(docs)} pages)")
            st.rerun()
            
        except Exception as e:
            st.error(f"Error: {e}")
        
        finally:
            os.remove(temp_file_path)

# Chat Interface
if 'vector_store' in st.session_state:
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Initialize the Gemini Chat Model
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.3
    )

    # Chat input
    user_question = st.chat_input("Ask a question about your document...")
    
    if user_question:
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": user_question})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_question)
        
        # Retrieval: Find relevant chunks
        retriever = st.session_state.vector_store.as_retriever(search_kwargs={"k": 4})
        related_docs = retriever.invoke(user_question)
        
        # Combine context + question for Gemini
        context_text = "\n\n".join([doc.page_content for doc in related_docs])
        
        prompt = f"""Answer the question based on the provided context.

Context:
{context_text}

Question: {user_question}

Provide a clear and concise answer based only on the context above."""
        
        # Stream the answer
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            for chunk in llm.stream(prompt):
                full_response += chunk.content
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
        
        # Add assistant message to history
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": full_response
        })