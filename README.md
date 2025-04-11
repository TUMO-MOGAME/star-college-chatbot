# Star College Durban Chatbot

A web-based chatbot that answers questions about Star College Durban using information from their website.

## Features

- Clean, responsive user interface with Star College branding
- Answers questions about Star College Durban
- Responds with "I don't have enough information" when uncertain
- Based on free LLM models via Ollama and LangChain

## Demo

You can try the static demo by visiting: [https://tumo-mogame.github.io/star-college-chatbot/](https://tumo-mogame.github.io/star-college-chatbot/)

## About Star College Durban

Star College Durban is an Independent, English Medium School established by Horizon Educational Trust. It follows the curriculum from the Department of Education and aims to be academically strong, producing excellent results in the National Matric exams as well as National and International Mathematics, Science and Computer Olympiads.

## Project Structure

- `docs/index.html` - Static demo HTML file (GitHub Pages)
- `static/index.html` - Interactive frontend for the Flask server
- `star_college_server.py` - Flask server for the interactive chatbot
- `starbot/` - Python package with the chatbot logic

## Deployment Options

### Static Demo (GitHub Pages)

The static demo is already deployed at [https://tumo-mogame.github.io/star-college-chatbot/](https://tumo-mogame.github.io/star-college-chatbot/). This version uses pre-defined answers and doesn't require a backend server.

### Interactive Version (Render.com)

To deploy the interactive version that can answer any question about Star College:

1. Sign up for a free account at [Render.com](https://render.com/)
2. Create a new Web Service
3. Connect your GitHub repository
4. Use the following settings:
   - **Name**: star-college-chatbot
   - **Runtime**: Python 3.9
   - **Build Command**: `pip install -r requirements-server.txt`
   - **Start Command**: `gunicorn star_college_server:app`
   - **Environment Variables**:
     - `LLM_PROVIDER`: Set to `openai`, `deepseek`, or `ollama` (default is `mock`)
     - `OPENAI_API_KEY`: Your OpenAI API key (if using OpenAI)
     - `DEEPSEEK_API_KEY`: Your DeepSeek API key (if using DeepSeek)
5. Click "Create Web Service"

### Interactive Version (Railway.app)

Alternatively, you can deploy on Railway.app:

1. Sign up for a free account at [Railway.app](https://railway.app/)
2. Create a new project from GitHub
3. Connect your GitHub repository
4. Add the following environment variables:
   - `PORT`: 8000
5. Deploy the project

### Local Development

To run the interactive version locally:

1. Install Ollama from [ollama.ai](https://ollama.ai/)
2. Pull the required model: `ollama pull llama2`
3. Install the requirements: `pip install -r requirements-server.txt`
4. Run the server: `python star_college_server.py`
5. Open your browser to `http://localhost:8000`

## Technical Details

The static demo uses:
- HTML, CSS, and JavaScript for the frontend
- Pre-defined answers for demonstration purposes
- Responsive design that works on mobile and desktop

The interactive version uses:
- Flask backend with Python
- Multiple LLM provider options:
  - OpenAI API for cloud-based inference
  - DeepSeek API for high-quality open models
  - Ollama for local LLM inference
  - Mock mode for fallback with pre-defined answers
- Web scraping of Star College Durban website for data
- Simple but effective keyword-based search for relevant context
