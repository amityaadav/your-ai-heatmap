# AI Knowledge Heatmap

A self-contained, interactive knowledge survey mapping 143 AI/ML topics across
12 domains, scored on a 4-level scale (untouched → heard of → can explain →
built/taught) with evidence behind every cell.

Single-file app — no build step, no dependencies. `index.html` is the whole
site.

## How it deploys

There are two deploy targets, each covering a different part of the app:

- **GitHub Pages** (`.github/workflows/pages.yml`) — publishes `index.html`,
  `quiz.html`, and `assets/` as static files on every push to `main`. This
  serves the heatmap, but the quiz's `/evaluate` endpoint needs the backend
  below — the quiz won't score answers when only Pages is deployed.
- **Google Cloud Run** (`.github/workflows/deploy-cloudrun.yml`) — builds the
  `Dockerfile` (FastAPI backend + static files) and deploys it as a
  container service on every push to `main`. This is the full app, quiz
  backend included. Cloud Run scales to zero when idle, so it stays within
  the free tier for low-traffic personal use.

One-time setup for the Cloud Run workflow (requires a Google Cloud account):

1. Create a GCP project and enable the Cloud Run, Cloud Build, and Artifact
   Registry APIs.
2. Create a service account with the Cloud Run Admin, Cloud Build Editor,
   Artifact Registry Writer, and Service Account User roles, and generate a
   JSON key for it.
3. In the repo's GitHub Settings → Secrets, add:
   - `GCP_PROJECT_ID` — your GCP project ID
   - `GCP_SA_KEY` — the service account's JSON key
   - `OLLAMA_API_KEY` — your Ollama Cloud key (or adapt the workflow/backend
     to use `OPENROUTER_API_KEY` instead, see `backend/.env.example`)

`.gitlab-ci.yml` is a leftover static-only mirror (copies `index.html` to
`public/` for GitLab Pages) and isn't part of the active deploy path.

## Updating the content

All the data lives in the `DOMAINS` array near the top of the `<script>` block
in `index.html` — each topic is `[name, level, reasoning, evidence]`. Edit,
commit, push; the site rebuilds automatically.
