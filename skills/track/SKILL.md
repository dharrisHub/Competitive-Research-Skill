---
name: track
description: Mark past competitive-research recommendations as shipped, in-progress, rejected, or wontfix so future analyses filter them out of new shortlists. Walks through unmarked entries from ./competitive-research/history/seen-features.jsonl and updates their status. Only invoked explicitly via /competitive-research:track — never auto-triggered.
disable-model-invocation: true
---

# Competitive Research — Outcome Tracking

Use this when the user wants to record what they did with past recommendations. Status updates feed into the next analysis run's Phase 7 dedupe step:

- `shipped` → never re-suggest
- `wontfix` → never re-suggest
- `in-progress` → don't re-suggest while work is happening
- `rejected` → may re-suggest but tagged `[REVISITED]` with explanation of changed circumstances

Without this skill, the analysis re-suggests features the user already shipped or explicitly killed, because there's no signal back from outcomes.

## Workflow

### 1. Find the history file

Look for `./competitive-research/history/seen-features.jsonl`. If it doesn't exist:

> No past recommendations to track yet. Run the analysis at least once first (say *"run the competitive research"*) to generate history.

Then exit.

### 2. Load and summarize

Read all entries. Each is one JSON object per line, e.g.:

```json
{"date": "2026-04-17", "name": "Bulk CSV import", "description": "...", "scores": {...}, "status": "unmarked"}
```

Entries without a `status` field are treated as `unmarked`. If a JSONL line is malformed, skip it with a warning — don't crash.

Show a status summary up front:

> **History contains N entries**
> - Unmarked (need triage): N
> - Shipped: N
> - In-progress: N
> - Rejected: N
> - Wontfix: N

### 3. Walk through unmarked entries

For each unmarked entry, in chronological order (oldest first), show:

- Feature name and one-line description
- Date first suggested
- RICE and Strategic Fit scores if present in `scores`

Then ask:

> **`shipped` / `in-progress` / `rejected` / `wontfix` / `skip` (decide later)**

Follow-ups based on choice:
- **shipped** — ask date shipped (default: today's date). Capture in `shipped_date`.
- **rejected** or **wontfix** — ask for a brief reason (1–2 sentences). Capture in `rejection_reason`. Required, not optional — the reason is what makes the dedupe smarter next run.
- **in-progress** — no follow-up.
- **skip** — leave as `unmarked`, move on.

Process one entry at a time. Don't ask about all of them in one batch — the user needs to think about each.

### 4. Optionally re-tag existing statuses

After unmarked entries are done, ask:

> Want to update any entries currently marked `in-progress`, `shipped`, `rejected`, or `wontfix`? (e.g., something marked in-progress last month may now be shipped.)

If yes, walk through one at a time using the same flow as step 3.

### 5. Write the updated history

Rewrite `./competitive-research/history/seen-features.jsonl` with updated entries. For each entry the user updated:

- Preserve all original fields (`date`, `name`, `description`, `scores`, etc.) — never modify these.
- Add or update: `status`, `status_updated` (today's ISO date), `rejection_reason` (if rejected/wontfix), `shipped_date` (if shipped).

Also append change records to `./competitive-research/history/outcomes.jsonl` (create if missing):

```json
{"date": "2026-04-24", "feature_name": "Bulk CSV import", "old_status": "unmarked", "new_status": "shipped", "reason": null}
```

The outcomes log is append-only and never rewritten — it's the audit trail for how decisions changed over time.

### 6. Confirm and hand off

Print:

- Number of entries updated
- Breakdown by new status
- Note: *"These will apply at the next analysis run's Phase 7 dedupe step. Shipped and wontfix items won't be re-suggested; rejected items may resurface as `[REVISITED]` if circumstances change."*

## Quality bar

- Never auto-decide a status. Every update is explicit user input or `skip`.
- Always require a reason for `rejected` / `wontfix` — that's the signal that improves next run.
- Preserve original fields. Status is additive, not replacing.
- Don't process more than ~5 unmarked entries in one session without checking in. *"That's 5 done, N to go — keep going or pause?"*
