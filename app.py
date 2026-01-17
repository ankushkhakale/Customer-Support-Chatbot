from fastapi import FastAPI
import gradio as gr
from customer_support import demo

app = FastAPI()

app = gr.mount_gradio_app(app, demo, path="/")
