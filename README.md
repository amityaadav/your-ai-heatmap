# AI Knowledge Heatmap

A self-contained, interactive knowledge survey mapping 143 AI/ML topics across
12 domains, scored on a 4-level scale (untouched → heard of → can explain →
built/taught) with evidence behind every cell.

Single-file app — no build step, no dependencies. `index.html` is the whole
site.

## Live site

Once GitLab Pages deploys, this will be live at:

```
https://<your-username>.gitlab.io/ai-knowledge-heatmap/
```

(Replace `<your-username>` with your actual GitLab namespace once deployed —
check **Settings → Pages** in the project for the exact URL.)

## How it deploys

`.gitlab-ci.yml` defines a single `pages` job that copies `index.html` into a
`public/` directory and publishes it as a CI artifact — GitLab Pages serves
whatever lands in `public/` automatically on every push to the default branch.
No further configuration needed.

## Updating the content

All the data lives in the `DOMAINS` array near the top of the `<script>` block
in `index.html` — each topic is `[name, level, reasoning, evidence]`. Edit,
commit, push; the site rebuilds automatically.
