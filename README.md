# PDF Document Assistant

A professional AI-powered application for chatting with PDF documents. Upload your PDFs and ask questions to get instant, accurate answers.

## Features

- **Local Document Processing**: Documents are processed locally using HuggingFace embeddings
- **AI-Powered Chat**: Powered by Google's Gemini 2.0 Flash model
- **Context-Aware Responses**: Get accurate answers based on your document content
- **Professional Interface**: Clean, modern UI with chat history
- **Source References**: Optional source citations for transparency
- **Secure & Private**: Your documents are processed locally

## Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd paf
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your Google API key:
```
GOOGLE_API_KEY=your_google_api_key_here
```

## Running Locally

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Deployment

### Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Add your `GOOGLE_API_KEY` in the Secrets section:
   ```toml
   GOOGLE_API_KEY = "your_api_key_here"
   ```
5. Deploy!

### Deploy to Other Platforms

This app can be deployed to:
- **Heroku**: Add a `Procfile` with `web: streamlit run app.py --server.port=$PORT`
- **AWS/GCP/Azure**: Use container deployment with Docker
- **Railway**: Direct deployment from GitHub

## Usage

1. Upload a PDF document using the file uploader
2. Wait for the document to be processed
3. Start asking questions in the chat interface
4. Enable "Show source references" in the sidebar to see where answers come from

## Technology Stack

- **Frontend**: Streamlit
- **Embeddings**: HuggingFace Sentence Transformers
- **Vector Store**: FAISS
- **LLM**: Google Gemini 2.0 Flash
- **Document Processing**: LangChain + PyPDF

## Configuration

You can customize the app by modifying:
- `chunk_size` and `chunk_overlap` in text splitting
- `temperature` for LLM responses
- `k` value for number of retrieved contexts
- Embedding model in HuggingFaceEmbeddings
