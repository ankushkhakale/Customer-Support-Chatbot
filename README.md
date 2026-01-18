# Customer Support Chatbot

FastAPI + Gradio front-end for a local LLM-powered customer support chatbot. The UI proxies user messages to a running Ollama-style HTTP endpoint and renders responses in a chat interface.

## Features
- Gradio chat interface with a clean theme and hidden footer
- FastAPI app hosting the Gradio UI at `/`
- Pluggable LLM backend (defaults to local Ollama at `http://localhost:1434/api/generate`)

# Customer Support Chatbot

FastAPI hosts a Gradio chat UI that forwards customer questions to a local LLM endpoint (Ollama-style API). You get a browser-ready chatbot with minimal wiring.

## Highlights
- Gradio chat interface with a clean Soft theme and hidden footer
- FastAPI container that mounts Gradio at `/` and exposes `/health`
- Pluggable LLM backend (defaults to `http://localhost:1434/api/generate` with model `llama3`)
- Env-based knobs for endpoint, model, and timeout

## Repository Map
- [app.py](app.py): FastAPI factory, CORS setup, Gradio mount, health check
- [customer_support.py](customer_support.py): Chat handler, request/response plumbing, Gradio demo

## Prerequisites
- Python 3.9+ (local testing target)
- An LLM server that supports `POST /api/generate` (Ollama-compatible) reachable at your configured URL
- Suggested: virtual environment (for isolation)

## Setup
1) Install dependencies
```bash
pip install fastapi gradio requests uvicorn
```

2) Start your model server (default expectation: http://localhost:1434). If using a different host/port or model name, set the env vars below.

## Configuration
You can override defaults via environment variables (no code changes needed):
- `CHATBOT_ENDPOINT` (default `http://localhost:1434/api/generate`)
- `CHATBOT_MODEL` (default `llama3`)
- `CHATBOT_TIMEOUT` (seconds, default `15`)

## Run
Launch the FastAPI app with Uvicorn:
```bash
uvicorn app:app --reload --port 8000
```

Then open http://localhost:8000 to use the chat UI.

### Direct Gradio (dev)
Run the UI without FastAPI:
```bash
python customer_support.py
```

## How It Works
1) Gradio calls `generate_response` with the user message.
2) The function POSTs JSON to the configured LLM endpoint (model, prompt, stream flag).
3) The JSON reply is parsed and the `response` field is shown in the chat.

## Operational Notes
- Streaming is off by default (`"stream": false`); enable it if your backend supports it.
- Errors from the model endpoint are returned in the chat to ease debugging.
- Health probe is available at `/health` when running via FastAPI.

## License
MIT License. See [LICENSE](LICENSE).
