import json
import os
from typing import Any, Dict, List

import gradio as gr
import requests


DEFAULT_MODEL = os.getenv("CHATBOT_MODEL", "llama3")
DEFAULT_ENDPOINT = os.getenv("CHATBOT_ENDPOINT", "http://localhost:1434/api/generate")
REQUEST_TIMEOUT = float(os.getenv("CHATBOT_TIMEOUT", 15))


def generate_response(message: str, history: List[List[str]]) -> str:
    """Send the prompt to the model server and return the reply string."""
    payload: Dict[str, Any] = {
        "model": DEFAULT_MODEL,
        "prompt": message,
        "stream": False,
    }

    try:
        response = requests.post(
            DEFAULT_ENDPOINT,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
    except requests.Timeout:
        return "Error: model endpoint timed out."
    except requests.RequestException as exc:
        return f"Error contacting model endpoint: {exc}"

    try:
        body = response.json()
    except ValueError:
        return "Error: invalid JSON from model endpoint."

    return str(body.get("response", ""))


custom_css = """
footer {visibility: hidden}
"""

demo = gr.ChatInterface(
    fn=generate_response,
    title="Customer Support Chatbot",
    description="Ask me anything! I am running locally using Ollama.",
    theme=gr.themes.Soft(),
    css=custom_css,
)


if __name__ == "__main__":
    demo.launch()
