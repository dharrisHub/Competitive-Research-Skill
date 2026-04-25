---
name: setup
description: Interactive setup wizard for the competitive-research plugin. Walks the user through optional override questions (target user, known competitors, strategic constraints, monorepo scope, etc.) and writes the answers to ./competitive-research/overrides.yaml. Only invoked explicitly via /competitive-research:setup — never auto-triggered.
disable-model-invocation: true
---

# Competitive Research — Interactive Setup

This skill walks the user through the optional override fields for the competitive-research plugin. Use when the user invokes `/competitive-research:setup` and wants to provide hints that auto-discovery would miss or get wrong.

The output is a single file: `./competitive-research/overrides.yaml` in the user's current project. Fields the user leaves blank stay auto-discovered by the main analysis skill at runtime.

## Workflow

### 1. Check current state

Read `./competitive-research/overrides.yaml` if it exists. If it does, briefly show the current values up front so the user knows what's already set. If it doesn't exist, ensure the parent `./competitive-research/` directory will be created when you write.

### 2. Ask the questions, one at a time

Don't ask everything in one wall of text. Ask each question, wait for the response, then move to the next. For every question:

- Briefly explain what the field controls and why it matters
- If a current value exists in the file, show it and ask if they want to keep, change, or clear it
- Accept "skip" or empty response to leave the field for auto-discovery
- Don't proceed to the next question until they've answered

**Question 1 — Product name**
> What's your product called? *(Leave blank to auto-discover from `package.json`, `README.md`, marketing pages, etc.)*

→ Sets `product_name_override`.

**Question 2 — Product URL**
> What's the public URL of your product? *(Leave blank to auto-discover from `homepage` fields, deploy configs, or web search.)*

→ Sets `product_url_override`.

**Question 3 — Target user**
> Who's your target user? Be as specific as you can — *"solo founders running Shopify stores at $10k–$100k/mo"* beats *"small businesses"*. The more specific, the better the recommendations. *(Leave blank to auto-infer from feature shape and README.)*

→ Sets `target_user_override`.

**Question 4 — Extra known competitors**
> Are there competitors I should make sure to include in the research? List them as `Name — https://url`, one per line. *(Leave blank to rely on web discovery alone.)*

→ Sets `extra_known_competitors` as a YAML list.

**Question 5 — Strategic constraints**
> Any strategic constraints I should know about? Examples: *"We're a 2-person team, no enterprise features"* or *"AI is a Q2 priority — bias new ideas toward LLM features"*. These prevent recommendations that don't fit your reality. *(Leave blank to infer from team size, infra shape, and explicit signals in the repo.)*

→ Sets `strategic_constraints_override` as a multi-line block.

**Question 6 — Monorepo scope**
> Is this a monorepo? If so, which subdirectory should the analysis focus on? (e.g., `packages/web-app`). *(Leave blank if not a monorepo, or if the auto-detected scope is correct.)*

→ Sets `monorepo_scope`.

### 3. Show the diff and confirm

Before writing, show the user the full proposed contents of `overrides.yaml`. Ask for explicit confirmation. If they want to revise an answer, jump back to that question.

### 4. Write the file

Write `./competitive-research/overrides.yaml` with this structure (only including fields the user provided values for; omit or leave empty the rest):

```yaml
# competitive-research overrides — only filled fields are used.
# Anything blank or absent gets auto-discovered.
product_name_override: ""
product_url_override: ""
target_user_override: ""
extra_known_competitors: []
strategic_constraints_override: ""
monorepo_scope: ""
```

YAML rules to follow:
- Quote strings that contain colons, hashes, or other YAML-meaningful chars
- Use a `|` block scalar for `strategic_constraints_override` if it's multi-line
- Use a YAML list (`- "Name — url"`) for `extra_known_competitors`, never a comma-separated string
- Preserve any pre-existing field values the user said to "keep"

### 5. Confirm and hand off

Print:
1. The path written: `./competitive-research/overrides.yaml`
2. A one-line summary of what changed (or "created with N overrides")
3. The next step: *"Run the competitive research skill (or say 'run the competitive research') to use these overrides on the next analysis."*

## Quality bar

- Never write the file before all questions are answered and the user confirms.
- Never invent values the user didn't provide. Blank means blank.
- Don't pre-fill answers from the codebase — that's auto-discovery's job at analysis time, not setup's job.
- Keep questions short. The user is filling out a form, not reading docs.
