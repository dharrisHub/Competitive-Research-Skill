---
name: preview
description: Quick preview of what the full competitive-research analysis would use — runs only Phase 0 (product dossier) and Phase 2 (competitor list), prints them, and asks for confirmation before committing to the 10–20 minute deep dive. Only invoked explicitly via /competitive-research:preview — never auto-triggered.
disable-model-invocation: true
---

# Competitive Research — Preview

Use this when the user wants to sanity-check what the full analysis will *base its work on* — the inferred product identity and the competitor list — before running the full Phase 3–8 deep dive. The full run is 10–20 minutes; this preview is 1–2 minutes and prevents wasting time on a wrong product or competitor model.

The dossier and competitor list this skill writes are reused by the main analysis skill — running the full analysis afterwards picks up where preview left off rather than redoing Phase 0 and Phase 2.

## Workflow

### 1. Check for an existing dossier from today

If `./competitive-research/runs/YYYY-MM-DD/product-dossier.md` exists for today's date, read it and `./competitive-research/competitors.yaml` instead of regenerating. Skip to step 4.

If they exist but the user wants a fresh look, ask first — don't silently overwrite.

### 2. Run Phase 0 (product dossier)

Execute the same Phase 0 logic as the main analysis skill. The detailed playbook is at `${CLAUDE_PLUGIN_ROOT}/skills/competitive-research/references/codebase-discovery.md` — read it and follow it to infer:

- Product name, one-liner, URL, target user, pricing model
- Core JTBDs (2–4 in Christensen form)
- Canonical feature list
- Inferred strategic constraints (with evidence sources)
- In-repo competitor mentions

If `./competitive-research/overrides.yaml` exists, respect those overrides instead of inferring those fields.

Write the dossier to `./competitive-research/runs/YYYY-MM-DD/product-dossier.md` using the format from the codebase-discovery reference (section 0.7).

### 3. Run Phase 2 (expand competitor set)

Same as Phase 2 of the main analysis skill (read `${CLAUDE_PLUGIN_ROOT}/skills/competitive-research/SKILL.md` Phase 2 for the full instructions). Aim for 8–15 competitors covering Direct / Adjacent / Indirect / Emerging categories. Save to `./competitive-research/competitors.yaml`.

### 4. Print the preview

Show the user, in this order:

1. **Product summary** — name, one-liner, target user, top 2–3 JTBDs (one line each)
2. **Strategic constraints** — the 3–6 inferred bullets
3. **Competitor list** — full set with one-liners, grouped by category
4. **Confidence flags** — any inferences the dossier marked as low-confidence (target user often is)

Keep the print compact. Don't reproduce the entire dossier — point at the file path for the full version.

### 5. Ask the user to confirm or correct

End with this exact prompt:

> **Does this look right?**
> - **Yes, run the full analysis** — say *"run the competitive research"* and the main skill will pick up the dossier + competitors from here
> - **Some inferences are wrong** — run `/competitive-research:setup` to set overrides, then preview again
> - **Add/remove specific competitors** — tell me which, and I'll update `competitors.yaml` directly

Do not proceed past Phase 2 from this skill. The full analysis is a separate invocation by design.

## Quality bar

- Phase 0 outputs must be grounded in actual file reads, same standard as the main skill.
- Don't fabricate a competitor list — every entry needs a URL.
- Don't run any phase past Phase 2. Stop and ask.
- If the user has an `overrides.yaml`, respect it. Don't re-infer fields they've already set.
