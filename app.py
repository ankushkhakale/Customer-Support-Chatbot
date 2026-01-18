from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import gradio as gr

from customer_support import demo


def create_app() -> FastAPI:
	"""Create and configure the FastAPI app that hosts the Gradio UI."""
	app = FastAPI(
		title="Customer Support Chatbot",
		description="FastAPI host for the Gradio-powered support chatbot UI",
		version="0.1.0",
	)

	app.add_middleware(
		CORSMiddleware,
		allow_origins=["*"],
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)

	app = gr.mount_gradio_app(app, demo, path="/")

	@app.get("/health", tags=["health"])
	async def health() -> dict[str, str]:
		return {"status": "ok"}

	return app


app = create_app()
