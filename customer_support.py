import json
import os
from typing import Any, Dict, List

import gradio as gr
import requests


DEFAULT_MODEL = os.getenv("CHATBOT_MODEL", "llama3")
DEFAULT_ENDPOINT = os.getenv("CHATBOT_ENDPOINT", "http://localhost:11434/api/chat")
REQUEST_TIMEOUT = float(os.getenv("CHATBOT_TIMEOUT", 15))


SYSTEM_PROMPT = """You are a helpful and professional customer support agent.
Your goal is to assist users with their inquiries efficiently and politely.
If you don't know the answer, admit it and offer to escalate the issue to a human agent.
Always maintain a courteous tone."""


def generate_response(message: str, history: List[List[str]]) -> str:
    """Send the conversation history to the model server and return the reply."""
    
    # Convert Gradio history [[user, bot], ...] to Ollama messages format
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    for user_msg, bot_msg in history:
        if user_msg:
            messages.append({"role": "user", "content": user_msg})
        if bot_msg:
            messages.append({"role": "assistant", "content": bot_msg})
            
    # Add the current message
    messages.append({"role": "user", "content": message})

    payload: Dict[str, Any] = {
        "model": DEFAULT_MODEL,
        "messages": messages,
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

    # In api/chat, the response is in body['message']['content']
    message_obj = body.get("message", {})
    return str(message_obj.get("content", ""))


custom_css = """
footer {visibility: hidden}
"""

demo = gr.ChatInterface(
    fn=generate_response,
    title="Customer Support Chatbot",
    description="Ask me anything! I am running locally using Ollama.",
)


if __name__ == "__main__":
    demo.launch()
