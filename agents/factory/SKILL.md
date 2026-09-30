---
name: generate-angular-component
description: Reads a GitHub issue spec and generates a complete Angular 18 standalone component (TS + HTML + SCSS + unit tests + barrel export), then opens a PR on the repository.
---

**Role:** Angular 18 code generator for the Meridian Retail AI Factory.

**Goal:** Turn a plain-language feature specification into production-ready Angular component files that pass Meridian linting and have meaningful unit test coverage.

**Inputs:**
| Field | Source | Notes |
|-------|--------|-------|
| `issue.title` | GitHub Issue title | Used as component feature name |
| `issue.body` | GitHub Issue body | Full feature spec (markdown) |
| `ANTHROPIC_API_KEY` | GitHub secret | Claude API access |
| `GITHUB_TOKEN` | GitHub secret | PR creation + issue comment |
| `context/meridian-coding-standards.md` | Repo file | Injected as system context |

**Outputs:**
| Artefact | Path |
|----------|------|
| Component TypeScript | `src/app/components/<kebab>/<kebab>.component.ts` |
| HTML template | `src/app/components/<kebab>/<kebab>.component.html` |
| SCSS styles | `src/app/components/<kebab>/<kebab>.component.scss` |
| Unit tests | `src/app/components/<kebab>/<kebab>.component.spec.ts` |
| Barrel export | `src/app/components/<kebab>/index.ts` |
| Pull Request | Opened on `main`, labelled `ai-generated` |

**Tools:** Claude API (`claude-sonnet-4-6`), PyGithub, GitHub Actions

<!-- chain:rules -->
- ALWAYS use `standalone: true` and `ChangeDetectionStrategy.OnPush`
- NEVER hardcode display strings — expose as `@Input()` with defaults
- SCSS MUST use design tokens (`$color-*`, `$spacing-*`) — raw hex values are rejected
- Unit tests MUST cover every `@Input()` and every public method (at least 3 test cases)
- Branch name: `ai/component-<kebab>-i<issue-number>`
- If the branch already exists, update the existing files (idempotent re-run)
- Escalate to human: ambiguous feature spec (missing component purpose or data shape)
<!-- /chain:rules -->

**Eval rubric:**

| Criterion | Pass |
|-----------|------|
| Files generated | All 5 files present |
| Standalone + OnPush | Both decorators set |
| No hardcoded values | 0 raw strings or hex colors |
| Test count | ≥ 3 test cases in spec.ts |
| PR opened | PR exists and links back to issue |
| Idempotent re-run | Second trigger updates, not duplicates |

**Example trigger:**

GitHub Issue titled "Product tile with add-to-bag button" labelled `ai-generate` →
Factory opens PR with `ProductTileComponent` in `src/app/components/product-tile/`.

**Run log (sample):**
```
[factory] Issue #12: "Click-and-collect slot picker"
[factory] Calling Claude API... done (1 843 tokens)
[factory] Writing 5 files to branch ai/component-slot-picker-i12
[factory] PR #34 opened: https://github.com/algolis/meridian-angular-factory/pull/34
[factory] Commented on issue #12
```
