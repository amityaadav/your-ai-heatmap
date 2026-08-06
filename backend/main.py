"""FastAPI backend for the AI Knowledge Quiz.

Provides:
- POST /evaluate — send an explanation, get a score + cross-topic credit
- GET /health — check if the LLM backend is available
- Static file serving for quiz.html + assets (SPA)
- Rate limiting via slowapi (IP-based: 200 req/day, 1000 req/hour)

Supports two LLM backends:
- OpenRouter (cloud): set OPENROUTER_API_KEY + OPENROUTER_MODEL
- Ollama (local): set OLLAMA_URL + OLLAMA_MODEL (default)
"""

import os
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from models import EvaluateRequest, EvaluateResponse, HealthResponse
from sensing_engine import SensingEngine

load_dotenv()

# --- Rate limiter ---
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[],
)

# --- Sensing engine ---
engine: SensingEngine = None  # type: ignore

# --- Static file paths ---
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown: initialize the sensing engine."""
    global engine

    # Detect backend from env
    ollama_api_key = os.getenv("OLLAMA_API_KEY", "")
    openrouter_key = os.getenv("OPENROUTER_API_KEY", "")

    if ollama_api_key:
        model = os.getenv("OLLAMA_CLOUD_MODEL", "deepseek-v4-pro:cloud")
        ollama_url = "http://localhost:11434"  # not used
    elif openrouter_key:
        model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
        ollama_url = "http://localhost:11434"  # not used
    else:
        model = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
        ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")

    engine = SensingEngine(
        ollama_url=ollama_url,
        model=model,
        timeout=float(os.getenv("LLM_TIMEOUT", "60")),
    )
    yield
    if engine:
        await engine.close()


# --- App ---
app = FastAPI(
    title="AI Knowledge Quiz API",
    description="LLM-powered quiz evaluator with cross-topic credit detection",
    version="0.2.0",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── API routes ───

@app.get("/health", response_model=HealthResponse)
async def health():
    """Check if the backend and LLM are healthy."""
    ollama_ok = await engine.health_check() if engine else False
    return HealthResponse(
        status="ok" if ollama_ok else "degraded",
        ollama_available=ollama_ok,
        model=engine.model if engine else "not initialized",
    )


@app.post("/evaluate", response_model=EvaluateResponse)
@limiter.limit("200/day;1000/hour")
async def evaluate(request: Request, body: EvaluateRequest):
    """Evaluate a user's explanation and detect cross-topic credit."""
    if engine is None:
        return JSONResponse(
            status_code=503,
            content={"detail": "Sensing engine not initialized"},
        )

    try:
        result = await engine.evaluate(body)
        return result
    except Exception as e:
        return JSONResponse(
            status_code=502,
            content={
                "detail": f"LLM evaluation failed: {str(e)}",
                "backend": engine.backend if engine else "unknown",
            },
        )


# ─── Static file serving (must be after API routes) ───

@app.get("/quiz.html")
async def serve_quiz():
    """Serve the quiz page."""
    path = STATIC_DIR / "quiz.html"
    if path.is_file():
        return FileResponse(path)
    return JSONResponse(status_code=404, content={"detail": "quiz.html not found"})


@app.get("/")
async def serve_index():
    """Serve the original heatmap as the index."""
    path = STATIC_DIR / "index.html"
    if path.is_file():
        return FileResponse(path)
    return {"service": "AI Knowledge Quiz API", "version": "0.2.0"}


# Mount assets directory for JS/CSS
assets_dir = STATIC_DIR / "assets"
if assets_dir.is_dir():
    app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")
