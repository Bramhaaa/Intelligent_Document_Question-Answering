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
    initial_sidebar_state="auto"
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
    .memory-indicator {
        background-color: #f0f9ff;
        border-left: 3px solid #3b82f6;
        padding: 0.5rem;
        margin-bottom: 1rem;
        font-size: 0.85rem;
        color: #1e40af;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar for conversation controls
if len(st.session_state.get('documents', {})) > 0:
    with st.sidebar:
        st.markdown("### Conversation")
        
        chat_count = len(st.session_state.get('chat_history', [])) // 2
        st.metric("Messages", chat_count)
        
        if st.button("🔄 Clear Conversation", use_container_width=True):
            if 'chat_history' in st.session_state:
                st.session_state.chat_history = []
            st.rerun()
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        **Conversation Memory**: The AI remembers your last 3 exchanges for natural follow-up questions.
        
        Try:
        - "Tell me more about that"
        - "What did you say about X?"
        - "Can you explain it differently?"
        """)

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
    # Document selector for insights
    st.markdown("##### 📚 Your Documents")
    doc_names = list(st.session_state.documents.keys())
    selected_doc = st.selectbox(
        "Select a document to view insights",
        doc_names,
        key="doc_selector",
        label_visibility="collapsed"
    )
    
    # Quick actions
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("➕ Add More", use_container_width=True):
            st.session_state.show_uploader = True
            st.rerun()
    with col2:
        if st.button("🗑️ Remove", use_container_width=True):
            if selected_doc:
                del st.session_state.documents[selected_doc]
                st.rerun()
    with col3:
        if st.button("Clear All", use_container_width=True):
            st.session_state.documents = {}
            if 'chat_history' in st.session_state:
                del st.session_state.chat_history
            st.rerun()
    
    
    # Document Insights - Always visible for selected document
    if selected_doc and selected_doc in st.session_state.documents:
        doc_info = st.session_state.documents[selected_doc]
        
        with st.expander(f"📊 Insights: {selected_doc}", expanded=True):
            # Statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Pages", doc_info['pages'])
            with col2:
                st.metric("Words", f"{doc_info['word_count']:,}")
            with col3:
                st.metric("Characters", f"{doc_info['char_count']:,}")
            with col4:
                avg_words = doc_info['word_count'] // doc_info['pages'] if doc_info['pages'] > 0 else 0
                st.metric("Avg Words/Page", avg_words)
            
            st.markdown("---")
            
            # AI Insights
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📝 Generate Summary", use_container_width=True, key="gen_summary"):
                    with st.spinner("Generating summary..."):
                        llm = ChatGoogleGenerativeAI(
                            model="gemini-2.0-flash",
                            google_api_key=os.getenv("GOOGLE_API_KEY"),
                            temperature=0.3
                        )
                        
                        summary_prompt = f"""Provide a concise summary of this document in 3-4 sentences. Focus on the main topics and key points.

Document excerpt:
{doc_info['full_text']}

Summary:"""
                        
                        summary = llm.invoke(summary_prompt)
                        st.session_state.documents[selected_doc]['summary'] = summary.content
                        st.rerun()
            
            with col2:
                if st.button("🔑 Extract Topics", use_container_width=True, key="gen_topics"):
                    with st.spinner("Extracting topics..."):
                        llm = ChatGoogleGenerativeAI(
                            model="gemini-2.0-flash",
                            google_api_key=os.getenv("GOOGLE_API_KEY"),
                            temperature=0.3
                        )
                        
                        topics_prompt = f"""Extract 5-7 key topics or themes from this document. List them as bullet points.

Document excerpt:
{doc_info['full_text']}

Key Topics:"""
                        
                        topics = llm.invoke(topics_prompt)
                        st.session_state.documents[selected_doc]['topics'] = topics.content
                        st.rerun()
            
            # Display insights if available
            if 'summary' in doc_info:
                st.markdown("**Summary:**")
                st.info(doc_info['summary'])
            
            if 'topics' in doc_info:
                st.markdown("**Key Topics:**")
                st.markdown(doc_info['topics'])
    
    st.divider()
    
    # Show uploader if requested
    if st.session_state.get('show_uploader', False):
        uploaded_files = st.file_uploader("Add more PDF files", type="pdf", accept_multiple_files=True, key="additional_files")
        if not uploaded_files:
            uploaded_files = None
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
                
                # Preserve page numbers and add document name to metadata
                for i, doc in enumerate(docs):
                    doc.metadata['source_document'] = uploaded_file.name
                    # PyPDFLoader already includes 'page' in metadata, ensure it's there
                    if 'page' not in doc.metadata:
                        doc.metadata['page'] = i

                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000, 
                    chunk_overlap=200
                )
                splits = text_splitter.split_documents(docs)

                vector_store = FAISS.from_documents(splits, embeddings)
                
                # Calculate document statistics
                full_text = " ".join([doc.page_content for doc in docs])
                word_count = len(full_text.split())
                char_count = len(full_text)
                
                # Store document info with stats
                st.session_state.documents[uploaded_file.name] = {
                    'vector_store': vector_store,
                    'pages': len(docs),
                    'chunks': len(splits),
                    'word_count': word_count,
                    'char_count': char_count,
                    'full_text': full_text[:5000]  # Store first 5000 chars for summary
                }
                
                st.success(f"✓ {uploaded_file.name} loaded ({len(docs)} pages)")
                
            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {e}")
            
            finally:
                os.remove(temp_file_path)
    
    # Reset uploader flag and rerun
    if 'show_uploader' in st.session_state:
        del st.session_state.show_uploader
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
            # Show citations if available
            if message.get("citations"):
                citations = message["citations"]
                # Show summary of sources
                summary = {}
                for cite in citations:
                    doc_name = cite['document']
                    if doc_name not in summary:
                        summary[doc_name] = []
                    summary[doc_name].append(cite['page'])
                
                citation_text = ", ".join([f"{doc} (p. {', '.join(map(str, sorted(set(pages))))})" 
                                          for doc, pages in summary.items()])
                st.caption(f"📄 {citation_text}")
                
                # Expandable section with full excerpts
                with st.expander("View citations"):
                    for i, cite in enumerate(citations, 1):
                        st.markdown(f"**[{i}] {cite['document']} - Page {cite['page']}**")
                        st.text(cite['excerpt'][:300] + "..." if len(cite['excerpt']) > 300 else cite['excerpt'])
                        st.divider()
    
    # Initialize the Gemini Chat Model
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.3
    )

    # Show memory indicator if conversation exists
    if len(st.session_state.chat_history) > 0:
        exchanges = len(st.session_state.chat_history) // 2
        st.markdown(f'<div class="memory-indicator">💭 Conversation memory active ({exchanges} exchange{"s" if exchanges != 1 else ""})</div>', 
                   unsafe_allow_html=True)
    
    # Chat input
    user_question = st.chat_input("Ask a question about your documents...")
    
    if user_question:
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": user_question})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_question)
        
        # Build conversation context (last 3 exchanges)
        conversation_context = ""
        recent_history = st.session_state.chat_history[-7:-1]  # Last 3 Q&A pairs (6 messages)
        if recent_history:
            conversation_context = "Previous conversation:\n"
            for msg in recent_history:
                role = "User" if msg["role"] == "user" else "Assistant"
                conversation_context += f"{role}: {msg['content']}\n"
            conversation_context += "\n"
        
        # Retrieve from all documents (use conversation-aware query if needed)
        all_related_docs = []
        for doc_name, doc_info in st.session_state.documents.items():
            retriever = doc_info['vector_store'].as_retriever(search_kwargs={"k": 2})
            docs = retriever.invoke(user_question)
            all_related_docs.extend(docs)
        
        # Sort by relevance and take top results
        all_related_docs = all_related_docs[:6]
        
        # Build citations
        citations = []
        context_parts = []
        for i, doc in enumerate(all_related_docs, 1):
            source_name = doc.metadata.get('source_document', 'Unknown')
            page_num = doc.metadata.get('page', 0) + 1  # Convert to 1-indexed
            
            # Store citation info
            citations.append({
                'document': source_name,
                'page': page_num,
                'excerpt': doc.page_content
            })
            
            # Build context with citation markers
            context_parts.append(f"[Citation {i} - {source_name}, Page {page_num}]\n{doc.page_content}")
        
        context_text = "\n\n".join(context_parts)
        
        prompt = f"""Answer the question based on the provided context from multiple documents and the conversation history.

{conversation_context}Document Context:
{context_text}

Current Question: {user_question}

Instructions:
- Provide a clear and concise answer
- Use the conversation history to understand follow-up questions and references (like "it", "that", "explain more")
- The context includes citation markers showing which document and page each piece of information comes from
- If the question refers to previous answers, acknowledge that and build upon it"""
        
        # Stream the answer
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            for chunk in llm.stream(prompt):
                full_response += chunk.content
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
            # Show citation summary
            summary = {}
            for cite in citations:
                doc_name = cite['document']
                if doc_name not in summary:
                    summary[doc_name] = []
                summary[doc_name].append(cite['page'])
            
            citation_text = ", ".join([f"{doc} (p. {', '.join(map(str, sorted(set(pages))))})" 
                                      for doc, pages in summary.items()])
            st.caption(f"📄 {citation_text}")
            
            # Expandable citations
            with st.expander("View citations"):
                for i, cite in enumerate(citations, 1):
                    st.markdown(f"**[{i}] {cite['document']} - Page {cite['page']}**")
                    st.text(cite['excerpt'][:300] + "..." if len(cite['excerpt']) > 300 else cite['excerpt'])
                    st.divider()
        
        # Add assistant message to history
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": full_response,
            "citations": citations
        })