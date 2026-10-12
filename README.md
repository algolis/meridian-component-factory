> [!IMPORTANT]
> **This repository has moved.**
> The active version is maintained at:
> **https://eu.git.epam.com/zsolt_hever/meridian-component-factory**
> This copy is no longer updated.

---

# Meridian Angular AI Factory

**AI/RUN Mission 2026 — Build Your AI Factory**


---

## What it is

A two-agent agentic delivery system that turns a GitHub Issue into a reviewed Angular 18 pull request — with no human writing code.

```
GitHub Issue  ──(label: ai-generate)──▶  Factory Agent
                                               │
                                          opens PR
                                               ▼
                                        Review Agent
                                               │
                               ┌───────────────┴───────────────┐
                            APPROVE                     REQUEST_CHANGES
                               │                               │
                          Human merges            Re-labels issue → ai-regenerate
                                                       │
                                                  Factory re-runs
```

---

## AI Factory Primitives

| Primitive | Artefact |
|-----------|----------|
| **Skill** | `agents/factory/SKILL.md` — issue spec → component files |
| **Skill** | `agents/review/SKILL.md` — PR diff → comments + verdict |
| **Agent** | `agents/factory/agent.py` — Factory orchestrator |
| **Agent** | `agents/review/agent.py` — Review orchestrator |
| **Hook** | `.github/workflows/factory.yml` — trigger on issue label |
| **Hook** | `.github/workflows/review.yml` — trigger on PR open/sync |
| **Rule** | `context/meridian-coding-standards.md` — injected into both agents |

---

## Setup

### 1. Create a new GitHub repo

This folder IS the repo root. Push it to a new GitHub repository:

```bash
git init
git add .
git commit -m "feat: Meridian Angular AI Factory"
gh repo create meridian-angular-factory --public --source=. --push
```

### 2. Add secrets

In your GitHub repo → Settings → Secrets → Actions:

| Secret | Value |
|--------|-------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key |

(`GITHUB_TOKEN` is provided automatically by GitHub Actions.)

### 3. Create the Angular app (optional for demo)

```bash
npm install -g @angular/cli
ng new meridian-app --standalone --style=scss
# move src/ into this repo or point the factory at the existing src/
```

If you don't have an Angular app yet, the factory still creates the files — they just won't compile until you add Angular. For the demo, the generated files and the PR review loop are the deliverable.

### 4. Trigger the factory

1. Open a GitHub Issue using the spec in `demo/sample-issue.md`
2. Add the label `ai-generate` to the issue
3. Watch GitHub Actions → Factory workflow fires
4. Within ~60 s: a PR appears with 5 generated Angular files
5. Watch GitHub Actions → Review workflow fires on the new PR
6. Review comments appear on the PR

---

## Demo Scenario

See `demo/sample-issue.md` for the "Click-and-collect slot picker" feature spec — the primary demo for the AI/RUN submission.

---

## Metrics (update as you run)

| Date | Issue | Component | Factory runs | Review verdict | Cycles to APPROVE |
|------|-------|-----------|-------------|----------------|-------------------|
| — | — | — | — | — | — |

---

## Local run (Podman / Docker)

To run an agent locally without GitHub Actions:

```bash
# Build container
podman build -t meridian-factory -f Containerfile .

# Run factory agent
podman run --rm \
  -e GITHUB_TOKEN=<token> \
  -e ANTHROPIC_API_KEY=<key> \
  -e ISSUE_NUMBER=1 \
  -e REPO_NAME=your-org/meridian-angular-factory \
  meridian-factory python agents/factory/agent.py

# Run review agent
podman run --rm \
  -e GITHUB_TOKEN=<token> \
  -e ANTHROPIC_API_KEY=<key> \
  -e PR_NUMBER=1 \
  -e REPO_NAME=your-org/meridian-angular-factory \
  meridian-factory python agents/review/agent.py
```

---

## Project structure

```
.
├── .github/workflows/
│   ├── factory.yml          # trigger: issue labelled ai-generate
│   └── review.yml           # trigger: PR opened/updated (ai-generated label)
├── agents/
│   ├── factory/
│   │   ├── agent.py         # Factory Agent orchestrator
│   │   ├── SKILL.md         # Skill contract spec
│   │   └── requirements.txt
│   └── review/
│       ├── agent.py         # Review Agent orchestrator
│       ├── SKILL.md         # Skill contract spec
│       └── requirements.txt
├── context/
│   └── meridian-coding-standards.md   # Injected into both agents
├── demo/
│   └── sample-issue.md      # Demo trigger: slot picker feature spec
├── Containerfile            # Podman/Docker build (optional local run)
└── README.md
```

---

## AI/RUN Mission 2026 mapping

| Competition criterion | How this project addresses it |
|----------------------|-------------------------------|
| AI-native delivery | Full SDLC step (issue → code → review) automated end-to-end |
| Agentic workflow | Two cooperating agents with a feedback loop |
| Runs in production | GitHub Actions on a real repo; output is real Angular code |
| Measurable impact | Lines of code generated, test coverage from zero, review cycles tracked |
| Self-improving | REQUEST_CHANGES loop triggers regeneration automatically |
| L3 standard | Every artefact is a repo file; decisions are traceable in PR history |
