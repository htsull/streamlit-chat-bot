# Streamlit Chat Bot

A lightweight Streamlit application that wraps a LangChain-powered chat interface. Users can converse with an OpenAI model in the browser, while conversation history is preserved with Streamlit session state. Responses are streamed token-by-token for a responsive feel.

## Features
- **Streaming chat responses** using `langchain-openai` and `StrOutputParser` for incremental output.
- **Persistent conversation history** stored in `st.session_state` so earlier turns stay visible during a session.
- **Chat-style UI** built with `st.chat_message` and `st.chat_input` components.
- **Environment-driven configuration** that loads secrets (like `OPENAI_API_KEY`) from a local `.env` file via `python-dotenv`.

## Project structure
```
.
├── main.py                # CLI entry that prints a greeting (not used by Streamlit)
├── src/
│   └── main.py            # Streamlit app with chat logic
├── pyproject.toml         # Project metadata and dependencies
└── uv.lock                # Resolved dependency lockfile for uv/pip
```

## Requirements
- Python 3.9+
- An OpenAI API key with access to chat models
- The dependencies listed in `pyproject.toml` (Streamlit, LangChain, python-dotenv, etc.)

## Setup
1. **Install dependencies** (use your preferred installer):
   ```bash
   # Using pip
   pip install -e .

   # Or using uv
   uv pip install -e .
   ```

2. **Create a `.env` file** in the project root with your API key:
   ```bash
   echo "OPENAI_API_KEY=sk-..." > .env
   ```

3. **Verify environment variables** are loaded (the app calls `load_dotenv()` at startup). Your key must be available as `OPENAI_API_KEY` before the first chat request.

## Running the app
Start the Streamlit UI pointed at the application module:
```bash
streamlit run src/main.py
```
The app sets a page title, icon, and wide layout. Once running, open the provided local URL in your browser to begin chatting.

## How it works
- On launch, `src/main.py` loads environment variables and initializes `st.session_state["chat_history"]` to hold a list of LangChain `HumanMessage` and `AIMessage` objects. 【F:src/main.py†L11-L69】
- The helper `get_chat_response` builds a simple prompt template that includes prior turns and the latest user input, then streams the model response via `ChatOpenAI` configured with your API key. 【F:src/main.py†L27-L44】
- Previous messages are rendered with `st.chat_message`, preserving user/assistant roles. User input is collected with `st.chat_input`, appended to history, and the streamed assistant response is written to the page and stored. 【F:src/main.py†L47-L69】

## Tips for use
- Keep your `.env` file out of version control to avoid leaking keys.
- Because responses stream, network interruptions may leave partial output; resubmit if needed.
- To reset the conversation, clear the `chat_history` in the sidebar (if using Streamlit's session state inspector) or restart the app.

## Development notes
- `main.py` at the repository root is only a placeholder CLI that prints a greeting; the Streamlit experience lives in `src/main.py`.
- No automated tests are included. When contributing features, consider adding unit or integration tests around prompt construction and session behavior.
- Follow Streamlit's guidance for secrets management in production deployments (e.g., environment variables or Streamlit Community Cloud secrets).
