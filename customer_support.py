import requests
import json
import gradio as gr

def generate_response(message, history):
    url = "http://localhost:1434/api/generate"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama3",
        "prompt": message,
        "stream": False
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        if response.status_code == 200:
            response_text = response.text
            data = json.loads(response_text)
            actual_response = data.get("response", "")
            return actual_response
        else:
            return f"Error: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"Error: {str(e)}"

custom_css = """
footer {visibility: hidden}
"""

demo = gr.ChatInterface(
    fn=generate_response,
    title="Customer Support Chatbot",
    description="Ask me anything! I am running locally using Ollama.",
    theme=gr.themes.Soft(),
    css=custom_css
)

if __name__ == "__main__":
    demo.launch()
