# Architecture: AI Knowledge Quiz System

## High-Level Structure
The project has two tiers: a **FastAPI backend** that talks to Ollama for LLM-powered evaluation, and a **client-side SPA** for the quiz interface.

```
┌──────────────┐     HTTP/POST     ┌──────────────┐     Ollama API     ┌──────────┐
│  quiz.html   │ ────────────────> │  FastAPI      │ ────────────────> │  Ollama  │
│  (browser)   │ <──────────────── │  (Python)     │ <──────────────── │  (local) │
└──────────────┘     JSON          └──────────────┘     /api/chat      └──────────┘
```

## Backend (`backend/`)

### Components
1. **`main.py`** — FastAPI application with:
   - `POST /evaluate` — accepts a user's explanation + remaining topics, returns score + struck topics
   - `GET /health` — checks Ollama availability
   - Rate limiting via slowapi (200 req/day, 1000 req/hour per IP)
   - CORS enabled for local development

2. **`sensing_engine.py`** — The core evaluator:
   - Sends the user's explanation + remaining topics to Ollama
   - Uses a structured system prompt with the L1-L4 scoring rubric
   - Parses JSON response for target score + cross-topic credit
   - Low temperature (0.1) for consistent scoring

3. **`models.py`** — Pydantic schemas:
   - `EvaluateRequest` / `EvaluateResponse`
   - `StruckTopic` (auto-evaluated via cross-topic credit)
   - `HealthResponse`

### Data Flow
`User types explanation` → `quiz.html POST /evaluate` → `SensingEngine.evaluate()` → `Ollama /api/chat` → `JSON response parsed` → `quiz.html updates state`

### Cross-Topic Credit
The LLM receives the full list of remaining topics alongside the user's explanation. It scores the target topic AND scans for collateral knowledge. If the user's answer about "MCP Protocol" also demonstrates knowledge of "Structured Outputs", that topic gets auto-struck with a score and reason.

## Frontend (`quiz.html`)
- Single-file SPA (no build step)
- Talks to the FastAPI backend at `http://localhost:8000`
- Maintains quiz state in LocalStorage for save/resume
- Generates the final heatmap by injecting scores into the original `index.html` template

## File Structure
```
your-ai-heatmap/
├── index.html              # Original mockup (READ ONLY — design gold standard)
├── quiz.html               # The quiz interface (to be built)
├── assets/
│   └── js/
│       └── data.js          # 143 topics extracted from index.html
├── backend/
│   ├── main.py              # FastAPI app
│   ├── sensing_engine.py    # LLM evaluator
│   ├── models.py            # Pydantic schemas
│   ├── requirements.txt     # Python deps
│   └── .env.example         # Config template
├── REQUIREMENTS.md
├── ARCHITECTURE.md
├── DESIGN.md
└── TEST_PLAN.md
```

## Running
```bash
# Backend
cd backend
cp .env.example .env
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Frontend — open quiz.html in browser (or serve with python -m http.server)
```
