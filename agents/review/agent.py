#!/usr/bin/env python3
"""Review Agent: Angular PR diff → inline comments + verdict."""

import json
import os
import re
from pathlib import Path

import anthropic
from github import Github, GithubException


def load_context() -> str:
    ctx = Path(__file__).parent.parent.parent / "context" / "meridian-coding-standards.md"
    return ctx.read_text(encoding="utf-8")


def review_diff(files: list[dict], standards: str) -> dict:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    files_text = "\n\n".join(
        f"### {f['filename']}\n```\n{f['patch']}\n```"
        for f in files
        if f.get("patch")
    )

    prompt = f"""You are a senior Angular 18 engineer reviewing a PR for the Meridian Retail project.

## Meridian Coding Standards
{standards}

## PR Diff
{files_text}

## Task
Review this Angular code. Return ONLY a valid JSON object with:
- "verdict": "APPROVE" or "REQUEST_CHANGES"
- "summary": one sentence (e.g. "Component looks solid; two minor gaps in test coverage.")
- "comments": array, each item:
  - "path": exact file path from the diff
  - "line": line number (integer, use the + side line from the diff)
  - "body": markdown comment text with actionable fix suggestion
  - "severity": "blocker" | "warning" | "suggestion"

Focus areas (blockers only block approval):
1. Public methods or @Input() with zero test coverage → blocker
2. Hardcoded strings/values that should be @Input() → blocker
3. Missing aria-* on interactive elements → warning
4. Raw hex colors instead of design tokens → warning
5. OnPush not set → warning
6. Minor naming / style suggestions → suggestion

If no comments needed, return an empty array.
Return ONLY the JSON object, no markdown."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()
    raw = re.sub(r"^```(?:json)?\n?", "", raw)
    raw = re.sub(r"\n?```$", "", raw)
    return json.loads(raw)


def post_review(repo, pr, review: dict) -> None:
    # Post summary
    badge = ":white_check_mark:" if review["verdict"] == "APPROVE" else ":x:"
    pr.create_issue_comment(
        f"""## AI Factory — Review Agent {badge}

**Verdict:** `{review['verdict']}`

{review['summary']}

---
*Meridian Angular AI Factory · Review Agent*"""
    )

    # Post inline comments
    commit = list(pr.get_commits())[-1]
    for c in review.get("comments", []):
        label = f"**[{c['severity'].upper()}]**"
        try:
            pr.create_review_comment(
                body=f"{label} {c['body']}",
                commit=commit,
                path=c["path"],
                line=int(c["line"]),
            )
        except GithubException:
            # Line number mismatch — fall back to issue comment
            pr.create_issue_comment(
                f"{label} `{c['path']}` (line {c['line']}): {c['body']}"
            )


def maybe_trigger_regen(repo, pr, verdict: str) -> None:
    """If changes requested, re-label the source issue to trigger re-generation."""
    if verdict != "REQUEST_CHANGES":
        return
    match = re.search(r"Closes #(\d+)", pr.body or "")
    if not match:
        return
    issue_number = int(match.group(1))
    issue = repo.get_issue(issue_number)
    try:
        issue.remove_from_labels("ai-generate")
    except GithubException:
        pass
    try:
        issue.remove_from_labels("ai-regenerate")
    except GithubException:
        pass
    issue.add_to_labels("ai-regenerate")
    issue.create_comment(
        ":repeat: Review agent requested changes — re-queuing for regeneration."
    )


def main() -> None:
    token = os.environ["GITHUB_TOKEN"]
    pr_number = int(os.environ["PR_NUMBER"])
    repo_name = os.environ["REPO_NAME"]

    gh = Github(token)
    repo = gh.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    files = [{"filename": f.filename, "patch": f.patch} for f in pr.get_files()]
    standards = load_context()
    review = review_diff(files, standards)

    post_review(repo, pr, review)
    maybe_trigger_regen(repo, pr, review["verdict"])

    print(f"Review posted: {review['verdict']}")


if __name__ == "__main__":
    main()
