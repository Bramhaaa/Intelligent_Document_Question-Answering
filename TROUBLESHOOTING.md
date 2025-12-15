# Troubleshooting Guide

## Fixed Issues ✅

### 1. Google GenAI ClientError
**Problem:** `google.genai.errors.ClientError` when streaming responses

**Solution:**
- Changed model from `gemini-2.0-flash` (experimental) to `gemini-1.5-flash` (stable)
- Added API key validation at startup
- Added proper error handling with retry logic
- Added timeout configuration for better reliability

### 2. Keras 3 Compatibility Error
**Problem:** `ValueError: Your currently installed version of Keras is Keras 3`

**Solution:**
- Installed `tf-keras` package for backwards compatibility
- Updated requirements.txt with necessary dependencies

### 3. Torch/Streamlit Warning
**Problem:** RuntimeError with torch._classes when running Streamlit

**Solution:**
- Added warning suppressions in app.py
- Set environment variables to minimize noise

## Environment Setup

### Required Environment Variables (.env file)
```bash
GOOGLE_API_KEY=your_actual_api_key_here
```

### Get Your API Key
Visit: https://aistudio.google.com/app/apikey

## Running the App

```bash
cd /Users/bramhabajannavar/Desktop/pdf_qs-ans
streamlit run app.py
```

The app will be available at: http://localhost:8501

## Common Issues

### Issue: API Key Not Found
**Error:** "⚠️ GOOGLE_API_KEY not found"
**Fix:** Create a `.env` file with your Google API key

### Issue: API Quota Exceeded
**Error:** ClientError with quota message
**Fix:** Check your quota at https://aistudio.google.com/

### Issue: Module Not Found
**Error:** ImportError for any package
**Fix:** Run `pip install -r requirements.txt`

### Issue: PDF Processing Fails
**Error:** Error processing PDF files
**Fix:** Ensure PDFs are not password-protected or corrupted

## Performance Tips

1. **Install Watchdog** for better file watching:
   ```bash
   xcode-select --install
   pip install watchdog
   ```

2. **Use smaller PDFs** for faster processing (under 50 pages recommended)

3. **Clear conversation** regularly to free up memory

## Dependencies

All required packages are in `requirements.txt`:
- streamlit
- langchain-google-genai
- sentence-transformers
- faiss-cpu
- pypdf
- tf-keras (for Keras 3 compatibility)
- transformers

## Support

If you encounter other issues:
1. Check the Streamlit logs in the terminal
2. Verify your API key is valid
3. Ensure all dependencies are installed
4. Try clearing the Streamlit cache: `streamlit cache clear`
