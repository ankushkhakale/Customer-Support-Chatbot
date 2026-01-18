# Customer Support Chatbot

FastAPI + Gradio front-end for a local LLM-powered customer support chatbot. The UI proxies user messages to a running Ollama-style HTTP endpoint and renders responses in a chat interface.

## Features
- Gradio chat interface with a clean theme and hidden footer
- FastAPI app hosting the Gradio UI at `/`
- Pluggable LLM backend (defaults to local Ollama at `http://localhost:1434/api/generate`)

## Project Layout
- [app.py](app.py): FastAPI app that mounts the Gradio demo
- [customer_support.py](customer_support.py): Chat interface and request handler to the model API

## Prerequisites
- Python 3.9+ (tested locally)
- An LLM endpoint compatible with the Ollama `POST /api/generate` API running at `http://localhost:1434`
- Recommended: virtual environment (e.g., `python -m venv .venv`)

## Setup
1) Install dependencies
```bash
pip install fastapi gradio requests uvicorn
```

2) Ensure your model server is running locally and listening on port 1434 (default for Ollama). Adjust the URL in `customer_support.py` if using a different host/port.

## Run
Launch the FastAPI app with Uvicorn:
```bash
uvicorn app:app --reload --port 8000
```

Open http://localhost:8000 to use the chat UI.

### Alternate direct launch
You can also run the Gradio demo directly (bypassing FastAPI) during development:
```bash
python customer_support.py
```

## Configuration
- Model endpoint: update `url` in `customer_support.py` to point to your inference server.
- Model name: change the `model` field in the request payload.
- UI text/theme: tweak `title`, `description`, or `theme` in `customer_support.py`.

## How It Works
1) Gradio collects user input and passes it to `generate_response`.
2) The function POSTs a JSON payload to the configured LLM endpoint.
3) The JSON response is parsed and streamed back to the Gradio chat window.

## Notes
- Streaming is disabled by default (`"stream": False`); enable it if your backend supports streaming responses.
- Errors from the backend are surfaced in the chat window for easier debugging.

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
