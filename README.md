# AI Knowledge Heatmap

An interactive knowledge survey mapping 148 AI/ML topics across 12 domains,
scored on a 4-level scale (untouched → heard of → can explain → built/taught)
with evidence behind every cell and free learning resources for every topic.

Two parts: a **static dashboard** (`index.html`) that loads scores from a
canonical JSON profile, and an **interactive quiz** (`quiz.html`) backed by a
FastAPI + LLM evaluation engine.

## How it deploys

**Google Cloud Run** (`.github/workflows/deploy-cloudrun.yml`) — builds the
`Dockerfile` (FastAPI backend + static files) and deploys it as a container
service on every push to `main`. This is the full app: dashboard, quiz, and
scoring backend. Cloud Run scales to zero when idle, so it stays within the
free tier for low-traffic personal use.

One-time setup for the Cloud Run workflow (requires a Google Cloud account):

1. Create a GCP project and enable the Cloud Run, Cloud Build, and Artifact
   Registry APIs.
2. Create a service account with the Cloud Run Admin, Cloud Build Editor,
   Artifact Registry Writer, and Service Account User roles.
3. Set up Workload Identity Federation so GitHub Actions can authenticate as
   that service account without a downloadable JSON key (many GCP projects
   now block key creation by org policy, and WIF is the recommended
   approach anyway) — see the commands in
   `.github/workflows/deploy-cloudrun.yml`'s auth step for what it expects.
4. In the repo's GitHub Settings → Secrets, add:
   - `GCP_PROJECT_ID` — your GCP project ID
   - `GCP_WORKLOAD_IDENTITY_PROVIDER` — full resource name of the WIF
     provider (`projects/<number>/locations/global/workloadIdentityPools/<pool>/providers/<provider>`)
   - `GCP_SERVICE_ACCOUNT` — the service account's email
   - `OLLAMA_API_KEY` — your Ollama Cloud key (or adapt the workflow/backend
     to use `OPENROUTER_API_KEY` instead, see `backend/.env.example`)

`.gitlab-ci.yml` is a leftover static-only mirror (copies `index.html` to
`public/` for GitLab Pages) and isn't part of the active deploy path.

## Updating the content

- **Scores & reasoning**: Edit `assets/data/amit-profile.json` directly on
  GitHub — update a score, push, and the dashboard reflects it on next page
  load. Format: `{profileName, exportedAt, totalTopics, evaluatedCount,
  domainNotes, domains}` with each topic carrying `{score, reasoning,
  evidence, resources}`.
- **Topic list**: Edit `assets/js/data.js` — the `DOMAINS` array used by the
  quiz. Each topic is `[name, level, reasoning, evidence, resources]`.
- **Learning resources**: Each topic carries a `resources` array of
  `{title, url}` objects. These appear in the dashboard's detail rail as
  "Learn more" links when a cell is selected.
