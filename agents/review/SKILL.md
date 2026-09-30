---
name: review-angular-pr
description: Fetches an Angular PR diff, analyzes it against Meridian coding standards, posts inline review comments, and either approves or requests changes. If changes are requested, re-labels the source issue to trigger a Factory re-run.
---

**Role:** Senior Angular code reviewer for the Meridian Retail AI Factory.

**Goal:** Catch blockers (untested public API, hardcoded values) and warnings (missing accessibility, raw colors) before human review. Keep the feedback loop tight — request changes that trigger automatic regeneration, not manual rework.

**Inputs:**
| Field | Source | Notes |
|-------|--------|-------|
| PR diff | GitHub API | All changed files with patches |
| `ANTHROPIC_API_KEY` | GitHub secret | Claude API access |
| `GITHUB_TOKEN` | GitHub secret | Comment + label write |
| `context/meridian-coding-standards.md` | Repo file | Injected as system context |

**Outputs:**
| Artefact | Where |
|----------|-------|
| Verdict comment | PR summary comment (`APPROVE` / `REQUEST_CHANGES`) |
| Inline comments | PR review thread, one per finding |
| Re-label (if changes requested) | Source issue re-labelled `ai-regenerate` |

**Tools:** Claude API (`claude-sonnet-4-6`), PyGithub, GitHub Actions

<!-- chain:rules -->
- ALWAYS fire on PRs labelled `ai-generated` only — never on human PRs
- Blockers (severity = "blocker") → verdict must be REQUEST_CHANGES
- Warnings and suggestions alone → verdict may be APPROVE with caveats
- If verdict is REQUEST_CHANGES: remove `ai-generate` / `ai-regenerate`, then add `ai-regenerate` to source issue
- Inline comment line numbers must reference the `+` side of the diff; fall back to issue comment if line is unavailable
- Escalate to human: security-sensitive code (auth, token handling, PII), or ≥ 3 consecutive REQUEST_CHANGES cycles on the same issue
<!-- /chain:rules -->

**Eval rubric:**

| Criterion | Pass |
|-----------|------|
| Fires only on `ai-generated` PRs | No false triggers |
| Verdict matches findings | REQUEST_CHANGES iff ≥1 blocker |
| Inline comments placed | ≥1 comment per blocker finding |
| Re-label on REQUEST_CHANGES | Issue gets `ai-regenerate` within 60 s |
| Graceful line-number fallback | No uncaught GithubException |

**Example review comment (blocker):**

> **[BLOCKER]** `src/app/components/slot-picker/slot-picker.component.ts` (line 34):
> `availableSlots` is a public method with no test case in `slot-picker.component.spec.ts`.
> Add at least one test: empty array, one slot, multiple slots.

**Run log (sample):**
```
[review] PR #34: 5 files, 312 lines changed
[review] Calling Claude API... done (987 tokens)
[review] Verdict: REQUEST_CHANGES (2 blockers, 1 warning)
[review] Posted summary comment + 3 inline comments
[review] Re-labelled issue #12 → ai-regenerate
```
