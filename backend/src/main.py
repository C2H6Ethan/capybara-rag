import os
import json
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from .config import ENV_PATH
from .rag import ask

load_dotenv(ENV_PATH)

app = FastAPI(title="CapybaraRAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
    question: str
    top_k: int = 5


@app.get("/health")
def health():
    return {"status": "ok", "service": "CapybaraRAG"}


@app.post("/ask")
async def ask_question(request: AskRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    async def generate():
        try:
            from .retriever import retrieve
            from .rag import build_prompt

            # Retrieve relevant chunks
            chunks = retrieve(request.question, top_k=request.top_k)

            # Handle out-of-domain queries
            if not chunks:
                message = "I don't have information about that in my capybara knowledge base. Try asking something about capybara biology, diet, habitat, behavior, or care."
                yield f"data: {json.dumps({'type': 'chunk', 'content': message})}\n\n"
                yield f"data: {json.dumps({'type': 'sources', 'sources': []})}\n\n"
                yield f"data: {json.dumps({'type': 'done'})}\n\n"
                return

            # Build prompt with retrieved context
            prompt = build_prompt(request.question, chunks)

            # Stream answer from Claude
            # Each text chunk arrives as Claude generates it
            # We immediately forward it to the frontend
            import anthropic
            client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

            with client.messages.stream(
                model="claude-haiku-4-5-20251001",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            ) as stream:
                for text in stream.text_stream:
                    yield f"data: {json.dumps({'type': 'chunk', 'content': text})}\n\n"

            # After answer is complete, send sources
            sources = [
                {
                    "source_file": c['source_file'],
                    "distance": c['distance'],
                    "text_preview": c['text'][:150]
                }
                for c in chunks
            ]
            yield f"data: {json.dumps({'type': 'sources', 'sources': sources})}\n\n"

            # Signal completion
            yield f"data: {json.dumps({'type': 'done'})}\n\n"

        except Exception as e:
            error_msg = f"Error processing question: {str(e)}"
            yield f"data: {json.dumps({'type': 'error', 'content': error_msg})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            # Prevent nginx/proxies from buffering the stream
            "X-Accel-Buffering": "no",
            # Prevent browser from caching SSE responses
            "Cache-Control": "no-cache",
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )