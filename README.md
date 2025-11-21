# Intelligent Document Q&A System

A production-ready AI-powered application for intelligent document analysis and question answering. Built with advanced RAG (Retrieval Augmented Generation) architecture, this system enables natural language interactions with multiple PDF documents simultaneously.

## 🎯 Key Features

### 1. Multi-Document Intelligence
- **Simultaneous Processing**: Upload and query multiple PDF documents at once
- **Cross-Document Analysis**: Ask questions that span across different documents
- **Smart Source Attribution**: Automatically identifies which document contains relevant information

### 2. Advanced Citation System
- **Page-Level References**: Precise citations with document name and page numbers
- **Source Verification**: Expandable excerpts showing exact text used for answers
- **Academic-Grade Citations**: Format: "Document.pdf (p. 1, 3, 5)"

### 3. Conversational Memory
- **Context-Aware Dialogue**: Remembers last 3 conversation exchanges
- **Natural Follow-ups**: Ask "tell me more", "what about X?", "explain differently"
- **Reference Resolution**: Understands pronouns and references to previous answers

### 4. Document Insights Dashboard
- **Statistical Analysis**: Word count, page count, character analysis
- **AI-Generated Summaries**: 3-4 sentence document overviews
- **Topic Extraction**: Automatic identification of 5-7 key themes
- **Quick Access**: Per-document insights with one click

### 5. Production-Ready Architecture
- **Local Embeddings**: Privacy-first approach using HuggingFace models
- **Vector Search**: Efficient FAISS indexing for fast retrieval
- **Streaming Responses**: Real-time answer generation
- **Session Management**: Persistent chat history within sessions

## 📋 Technical Architecture

```
┌─────────────────┐
│  User Interface │  Streamlit (Clean, Minimalist UI)
└────────┬────────┘
         │
┌────────▼────────┐
│  Chat Handler   │  Conversation Memory + Query Processing
└────────┬────────┘
         │
┌────────▼────────┐
│ Retrieval Layer │  FAISS Vector Store (Multi-Document)
└────────┬────────┘
         │
┌────────▼────────┐
│   Embeddings    │  HuggingFace Sentence Transformers
└────────┬────────┘
         │
┌────────▼────────┐
│   LLM Layer     │  Google Gemini 2.0 Flash
└─────────────────┘
```

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Frontend | Streamlit | Web interface |
| Embeddings | HuggingFace (sentence-transformers/all-MiniLM-l6-v2) | Local document vectorization |
| Vector Store | FAISS | Fast similarity search |
| LLM | Google Gemini 2.0 Flash | Question answering |
| Document Processing | LangChain + PyPDF | PDF parsing & chunking |
| Deployment | Streamlit Cloud | Production hosting |

## 📦 Installation

### Prerequisites
- Python 3.9 or higher
- Google API Key ([Get it here](https://makersuite.google.com/app/apikey))

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/Bramhaaa/Intelligent_Document_Question-Answering.git
cd Intelligent_Document_Question-Answering
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
# Create .env file
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

5. **Run the application**
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 🌐 Deployment

### Streamlit Cloud (Recommended)

1. Push code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect repository: `Bramhaaa/Intelligent_Document_Question-Answering`
4. Add secrets in app settings:
   ```toml
   GOOGLE_API_KEY = "your_api_key_here"
   ```
5. Deploy!

### Docker Deployment

```bash
docker build -t pdf-qa-system .
docker run -p 8501:8501 -e GOOGLE_API_KEY=your_key pdf-qa-system
```

## 💡 Usage Guide

### Basic Workflow

1. **Upload Documents**
   - Click "Choose PDF files" and select one or more documents
   - Wait for processing (embeddings are created locally)

2. **View Insights**
   - Select a document from the dropdown
   - View statistics, generate summaries, extract topics

3. **Ask Questions**
   - Type your question in the chat input
   - Receive answers with page citations
   - Expand citations to see exact excerpts

4. **Follow-up Conversations**
   - Ask follow-up questions naturally
   - System remembers context from last 3 exchanges
   - Use references like "tell me more about that"

### Example Questions

- "What are the main findings in this research?"
- "Compare the methodologies discussed in both documents"
- "What does it say about X on page 5?"
- "Summarize the conclusion section"

## 🔧 Configuration

Customize in `app.py`:

```python
# Text splitting
chunk_size = 1000        # Characters per chunk
chunk_overlap = 200      # Overlap between chunks

# Retrieval
k = 2                    # Documents retrieved per source

# LLM
temperature = 0.3        # Response creativity (0-1)
model = "gemini-2.0-flash"

# Embeddings
model_name = "sentence-transformers/all-MiniLM-l6-v2"
```

## 📊 Performance Metrics

- **Processing Speed**: ~2-3 seconds per page
- **Query Response**: 1-3 seconds (streaming)
- **Memory Usage**: ~500MB for typical documents
- **Supported Document Size**: Up to 100 pages per PDF

## 📧 Contact

**Bramha Bajannavar**
- GitHub: [@Bramhaaa](https://github.com/Bramhaaa)
- Project Link: [https://github.com/Bramhaaa/Intelligent_Document_Question-Answering](https://github.com/Bramhaaa/Intelligent_Document_Question-Answering)
