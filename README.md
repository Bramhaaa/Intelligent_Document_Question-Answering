  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.29.224:8501

2025-11-21 23:56:26.800 Uncaught app execution
Traceback (most recent call last):
  File "/Users/bramhabajannavar/Desktop/paf/venv/lib/python3.12/site-packages/streamlit/runtime/state/session_state_proxy.py", line 140, in __delattr__
    del self[key]
        ~~~~^^^^^
  File "/Users/bramhabajannavar/Desktop/paf/venv/lib/python3.12/site-packages/streamlit/runtime/state/session_state_proxy.py", line 126, in __delitem__
    del get_session_state()[key]
        ~~~~~~~~~~~~~~~~~~~^^^^^
  File "/Users/bramhabajannavar/Desktop/paf/venv/lib/python3.12/site-packages/streamlit/runtime/state/safe_session_state.py", line 114, in __delitem__
    del self._state[key]
        ~~~~~~~~~~~^^^^^
  File "/Users/bramhabajannavar/Desktop/paf/venv/lib/python3.12/site-packages/streamlit/runtime/state/session_state.py", line 551, in __delitem__
    raise KeyError(_missing_key_error_message(key))
KeyError: 'st.session_state has no key "document_name". Did you forget to initialize it? More info: https://docs.streamlit.io/develop/concepts/architecture/session-state#initialization'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/bramhabajannavar/Desktop/paf/venv/lib/python3.12/site-packages/streamlit/runtime/scriptrunner/exec_code.py", line 129, in exec_func_with_error_handling
    result = func()
             ^^^^^^
  File "/Users/bramhabajannavar/Desktop/paf/venv/lib/python3.12/site-packages/streamlit/runtime/scriptrunner/script_runner.py", line 669, in code_to_exec
    exec(code, module.__dict__)  # noqa: S102
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/bramhabajannavar/Desktop/paf/app.py", line 58, in <module>
    del st.session_state.document_name
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/bramhabajannavar/Desktop/paf/venv/lib/python3.12/site-packages/streamlit/runtime/state/session_state_proxy.py", line 142, in __delattr__
    raise AttributeError(_missing_attr_error_message(key))
AttributeError: st.session_state has no attribute "document_name". Did you forget to initialize it? More info: https://docs.streamlit.io/develop/concepts/architecture/session-state#initialization
2025-11-21 23:57:04.586 `label` got an empty value. This is discouraged for accessibility reasons and may be disallowed in the future by raising an exception. Please provide a non-empty label and hide it with label_visibility if needed.
Stack (most recent call last):
  File "/opt/homebrew/Cellar/python@3.12/3.12.12/Frameworks/Python.framework/Versions/3.12/lib/python3.12/threading.py", line 1032, in _bootstrap
    self._bootstrap_inner()
  File "/opt/homebrew/Cellar/python@3.12/3.12.12/Frameworks/Python.framework/Versions/3.12/lib/python3.12/threading.py", line 1075, in _bootstrap_inner
    self.run()
  File "/opt/homebrew/Cellar/python@3.12/3.12.12/Frameworks/Python.framework/Versions/3.12/lib/python3.12/threading.py", line 1012, in run
    self._target(*self._args, **self._kwargs)
  File "/Users/bramhabajannavar/Desktop/paf/venv/lib/python3.12/site-packages/streamlit/runtime/scriptrunner/script_runner.py", line 378, in _run_script_thread
    self._run_script(request.rerun_data)
  File "/Users/bramhabajannavar/Desktop/paf/venv/lib/python3.12/site-packages/streamlit/runtime/scriptrunner/script_runner.py", line 685, in _run_script
    ) = exec_func_with_error_handling(code_to_exec, ctx)
  File "/Users/bramhabajannavar/Desktop/paf/venv/lib/python3.12/site-packages/streamlit/runtime/scriptrunner/exec_code.py", line 129, in exec_func_with_error_handling
    result = func()
  File "/Users/bramhabajannavar/Desktop/paf/venv/lib/python3.12/site-packages/streamlit/runtime/scriptrunner/script_runner.py", line 669, in code_to_exec
    exec(code, module.__dict__)  # noqa: S102
  File "/Users/bramhabajannavar/Desktop/paf/app.py", line 49, in <module>
    uploaded_file = st.file_uploader("", type="pdf", label_visibility="collapsed")
  File "/Users/bramhabajannavar/Desktop/paf/venv/lib/python3.12/site-packages/streamlit/runtime/metrics_util.py", line 447, in wrapped_func
    result = non_optional_func(*args, **kwargs)
  File "/Users/bramhabajannavar/Desktop/paf/venv/lib/python3.12/site-packages/streamlit/elements/widgets/file_uploader.py", line 441, in file_uploader
    return self._file_uploader(
  File "/Users/bramhabajannavar/Desktop/paf/venv/lib/python3.12/site-packages/streamlit/elements/widgets/file_uploader.py", line 481, in _file_uploader
    maybe_raise_label_warnings(label, label_visibility)
  File "/Users/bramhabajannavar/Desktop/paf/venv/lib/python3.12/site-packages/streamlit/elements/lib/policies.py", line 184, in maybe_raise_label_warnings
    _LOGGER.warning(
2025-11-21 23:57:08.549 `label` got an empty value. This is discouraged for accessibility reasons and may be disallowed in the future by raising an exception. Please provide a non-empty label and hide it with label_visibility if needed.
Stack (most recent call last):
  File "/opt/homebrew/Cellar/python@3.12/3.12.12/Frameworks/Python.framework/Versions/3.12/lib/python3.12/threading.py", line 1032, in _bootstrap
    self._bootstrap_inner()
  File "/opt/homebrew/Cellar/python@3.12/3.12.12/Frameworks/Python.framework/Versions/3.12/lib/python3.12/threading.py", line 1075, in _bootstrap_inner
    self.run()
  File "/opt/homebrew/Cellar/python@3.12/3.12.12/Frameworks/Python.framework/Versions/3.12/lib/python3.12/threading.py", line 1012, in run
    self._target(*self._args, **self._kwargs)
  File "/Users/bramhabajannavar/Desktop/paf/venv/lib/python3.12/site-packages/streamlit/runtime/scriptrunner/script_runner.py", line 378, in _run_script_thread
    self._run_script(request.rerun_data)
  File "/Users/bramhabajannavar/Desktop/paf/venv/lib/python3.12/site-packages/streamlit/runtime/scriptrunner/script_runner.py", line 685, in _run_script
    ) = exec_func_with_error_handling(code_to_exec, ctx)
  File "/Users/bramhabajannavar/Desktop/paf/venv/lib/python3.12/site-packages/streamlit/runtime/scriptrunner/exec_code.py", line 129, in exec_func_with_error_handling
    result = func()
  File "/Users/bramhabajannavar/Desktop/paf/venv/lib/python3.12/site-packages/streamlit/runtime/scriptrunner/script_runner.py", line 669, in code_to_exec
    exec(code, module.__dict__)  # noqa: S102
  File "/Users/bramhabajannavar/Desktop/paf/app.py", line 49, in <module>
    uploaded_file = st.file_uploader("", type="pdf", label_visibility="collapsed")
  File "/Users/bramhabajannavar/Desktop/paf/venv/lib/python3.12/site-packages/streamlit/runtime/metrics_util.py", line 447, in wrapped_func
    result = non_optional_func(*args, **kwargs)
  File "/Users/bramhabajannavar/Desktop/paf/venv/lib/python3.12/site-packages/streamlit/elements/widgets/file_uploader.py", line 441, in file_uploader
    return self._file_uploader(
  File "/Users/bramhabajannavar/Desktop/paf/venv/lib/python3.12/site-packages/streamlit/elements/widgets/file_uploader.py", line 481, in _file_uploader
    maybe_raise_label_warnings(label, label_visibility)
  File "/Users/bramhabajannavar/Desktop/paf/venv/lib/python3.12/site-packages/streamlit/elements/lib/policies.py", line 184, in maybe_raise_label_warnings
    _LOGGER.warning(
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
