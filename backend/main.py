"""FastAPI backend for the AI Knowledge Quiz.

Provides:
- POST /evaluate — send an explanation, get a score + cross-topic credit
- GET /health — check if Ollama is available
- Rate limiting via slowapi (IP-based: 200 req/day, 1000 req/hour)
"""

import os
import uuid
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from models import EvaluateRequest, EvaluateResponse, HealthResponse
from sensing_engine import SensingEngine

load_dotenv()

# --- Rate limiter ---
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[],  # No global default; per-route limits
)


# --- Sensing engine (initialized at startup) ---
engine: SensingEngine = None  # type: ignore


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown: initialize the sensing engine."""
    global engine
    ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
    ollama_model = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

    engine = SensingEngine(
        ollama_url=ollama_url,
        model=ollama_model,
        timeout=float(os.getenv("OLLAMA_TIMEOUT", "60")),
    )
    yield
    if engine:
        await engine.close()


# --- App ---
app = FastAPI(
    title="AI Knowledge Quiz API",
    description="LLM-powered quiz evaluator with cross-topic credit detection",
    version="0.1.0",
    lifespan=lifespan,
)

# Attach rate limiter to app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS — allow the frontend to call from any origin during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
async def health():
    """Check if the backend and Ollama are healthy."""
    ollama_ok = await engine.health_check() if engine else False
    return HealthResponse(
        status="ok" if ollama_ok else "degraded",
        ollama_available=ollama_ok,
        model=engine.model if engine else "not initialized",
    )


@app.post("/evaluate", response_model=EvaluateResponse)
@limiter.limit("200/day;1000/hour")
async def evaluate(request: Request, body: EvaluateRequest):
    """Evaluate a user's explanation and detect cross-topic credit.

    Rate limited to 200 requests/day and 1000 requests/hour per IP.
    """
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
                "detail": f"Ollama evaluation failed: {str(e)}. Is Ollama running? Try: ollama serve",
                "ollama_url": engine.ollama_url if engine else "unknown",
            },
        )


@app.get("/")
async def root():
    return {"service": "AI Knowledge Quiz API", "version": "0.1.0"}
