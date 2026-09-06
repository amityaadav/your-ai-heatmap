# Architecture: AI Knowledge Quiz System

## High-Level Structure
The project has two tiers: a **FastAPI backend** that evaluates user responses via LLM, and a **client-side SPA** for the quiz interface. A separate **static heatmap** (`index.html`) displays pre-scored results.

```
┌──────────────┐     HTTP/POST     ┌──────────────┐     LLM API      ┌────────────────┐
│  quiz.html   │ ────────────────> │  FastAPI      │ ───────────────> │  Ollama Cloud   │
│  (browser)   │ <──────────────── │  (Cloud Run)  │ <─────────────── │  / OpenRouter   │
└──────────────┘     JSON          └──────────────┘                   │  / local Ollama │
       │                                                              └────────────────┘
       │ localStorage
       ▼
┌──────────────┐
│ Session state │
│ (browser)    │
└──────────────┘
```

## Deployment

Triggered on push to `main`:

- **Google Cloud Run** (`.github/workflows/deploy-cloudrun.yml`) — builds a Docker image in the GitHub Actions runner, pushes to Artifact Registry, and deploys to Cloud Run. This is the full app (backend + static files). Cloud Run scales to zero when idle, staying within the free tier for low traffic.

Authentication from GitHub Actions to GCP uses **Workload Identity Federation** (keyless — no service account JSON key needed).

See `README.md` for one-time GCP setup steps and required GitHub secrets.

## Backend (`backend/`)

### Components
1. **`main.py`** — FastAPI application with:
   - `POST /evaluate` — accepts a user's explanation + remaining topics, returns score + struck topics
   - `GET /health` — checks LLM backend availability
   - Rate limiting via slowapi (200 req/day, 1000 req/hour per IP)
   - CORS enabled for cross-origin requests
   - Static file serving for `index.html`, `quiz.html`, and `assets/`

2. **`sensing_engine.py`** — The core evaluator supporting three backends (auto-detected from environment):
   - **Ollama Cloud**: `OLLAMA_API_KEY` set — calls `https://ollama.com/v1` (OpenAI-compatible)
   - **OpenRouter**: `OPENROUTER_API_KEY` set — calls `https://openrouter.ai/api/v1` (OpenAI-compatible)
   - **Local Ollama**: neither key set — calls `http://localhost:11434/api/chat`
   - Uses a structured system prompt with the L1–L4 scoring rubric
   - Low temperature (0.1) for consistent scoring

3. **`models.py`** — Pydantic schemas:
   - `EvaluateRequest` / `EvaluateResponse`
   - `StruckTopic` (auto-evaluated via cross-topic credit)
   - `HealthResponse`

### Data Flow
`User types explanation` → `quiz.html POST /evaluate` → `SensingEngine.evaluate()` → `LLM API` → `JSON response parsed` → `quiz.html updates state`

### Cross-Topic Credit
The LLM receives the full list of remaining topics alongside the user's explanation. It scores the target topic AND scans for collateral knowledge. If the user's answer about "MCP Protocol" also demonstrates knowledge of "Structured Outputs", that topic gets auto-struck with a score and reason.

## Frontend

### `quiz.html` — Interactive Quiz
- Single-file SPA (no build step, no dependencies)
- Talks to the FastAPI backend at `/evaluate` (relative path, works on any host)
- **Session persistence via localStorage**: auto-saves quiz state on every evaluation so users can resume across sessions
- **Profile export/import**: users can export their progress as a portable JSON file and import profiles from others
- Generates the final heatmap by injecting scores into the original `index.html` template

### `index.html` — Static Heatmap
- Loads Amit's scores from `assets/data/amit-profile.json` on page load (fetched via `fetch()`)
- Design gold standard — quiz.html mirrors its visual style
- **Score toggle**: if the viewer has localStorage quiz data, a toggle switches between Amit's scores and theirs
- **Topic retake**: clicking a cell shows a "Retake this topic" link that opens `quiz.html?retake=TopicName`
- **Learning resources**: the detail rail shows 2 free, credible learning links per topic sourced from the profile's `resources` field

### `assets/data/amit-profile.json` — Canonical Profile
- Amit's pre-scored profile in the same JSON format as quiz export: `{profileName, exportedAt, totalTopics, evaluatedCount, domainNotes, domains}`
- Editable directly on GitHub — update a score, push, and the dashboard reflects it on next page load
- `domainNotes` is a lightweight extension (domain → note string) for the dashboard's per-domain commentary
- Each topic includes a `resources` array of `{title, url}` objects pointing to free, credible learning materials

### `assets/js/data.js` — Shared Data
- Contains the `DOMAINS` array (148 topics across 12 domains) used by `quiz.html`
- Each topic: `[name, level, reasoning, evidence, resources]`

## Container (`Dockerfile`)
- Python 3.12 base image
- Installs backend dependencies, copies backend code and frontend files
- Runs uvicorn on the port Cloud Run provides (`$PORT`, defaults to 8080)

## File Structure
```
your-ai-heatmap/
├── index.html              # Static heatmap (design gold standard)
├── quiz.html               # Interactive quiz SPA with session persistence
├── Dockerfile              # Container for Cloud Run deployment
├── assets/
│   ├── data/
│   │   └── amit-profile.json  # Amit's scores (canonical, editable on GitHub)
│   └── js/
│       └── data.js            # 143 topics shared between index.html and quiz.html
├── backend/
│   ├── main.py             # FastAPI app (serves API + static files)
│   ├── sensing_engine.py   # LLM evaluator (Ollama Cloud / OpenRouter / local)
│   ├── models.py           # Pydantic schemas
│   ├── requirements.txt    # Python deps
│   └── .env.example        # Config template for LLM backend selection
├── .github/
│   └── workflows/
│       └── deploy-cloudrun.yml # Cloud Run deploy (full app)
├── .gitlab-ci.yml          # Legacy GitLab Pages mirror (inactive)
├── ARCHITECTURE.md
├── DESIGN.md
├── README.md
├── REQUIREMENTS.md
└── TEST_PLAN.md
```

## Running Locally
```bash
# Backend
cd backend
cp .env.example .env        # configure LLM backend (see file for options)
pip install -r requirements.txt
uvicorn main:app --reload --port 8080

# Frontend — open quiz.html in browser (or serve with python -m http.server)
```
