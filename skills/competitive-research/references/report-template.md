# Report Template

This is the structure for `./competitive-research/runs/YYYY-MM-DD/report.md`. Use it as-is. Consistent structure across weekly runs makes them comparable.

---

```markdown
# Competitive Research Report — [Product Name] — YYYY-MM-DD

## 1. Executive summary

*(≤ 200 words. The 3–5 most important findings. Written for a busy founder. No fluff. No "in this report we will..." — just the conclusions.)*

## 2. What I understood about your product

*(One paragraph summarizing the Phase 0 dossier: name, one-liner, target user, JTBDs, inferred strategic constraints. End with this exact line:)*

> If anything in this section is wrong, set the relevant override in `./competitive-research/overrides.yaml` before next week's run — every recommendation below depends on this.

## 3. Landscape snapshot

*(One paragraph. How has the competitive set shifted since the last run? Who's gaining momentum? Who's quiet? What themes are emerging across competitor changelogs? If this is the first run, say so and describe the current shape of the market.)*

## 4. Feature matrix

*(The full ✅/❌/🟡 table from Phase 4. Rows = features, columns = our product + each competitor.)*

## 5. Top 10 feature recommendations

*(For each, use this exact sub-structure. Number them 1–10, ranked by Strategic Fit after RICE pre-filter.)*

### #N — [Feature name]

**Tag:** `[NEW]` | `[RECURRING — first suggested YYYY-MM-DD]` | `[REVISITED]`

**One-line description:** [what it is in plain language]

**Evidence:**
- Shipped by [competitor], [competitor], [competitor]
- Users say: "[direct quote]" — [source link]
- Users say: "[direct quote]" — [source link]

**Why it matters:**
- **JTBD it advances:** [which one from the dossier]
- **Kano class:** [Must-Have / Performance / Delighter]
- **User pain it solves:** [specific friction this removes]

**Scores:**
- Reach: [number]/qtr — [justification]
- Impact: [3/2/1/0.5/0.25] — [justification]
- Confidence: [%] — [justification]
- Effort: [person-months] — [justification]
- **RICE: [value]**
- **Strategic Fit: [1–10]** — [justification]

**How we could ship it:**
- **MVP wedge:** [smallest version that delivers core value]
- **Full version:** [what mature looks like]
- **Where it lands in our codebase:** [specific files/modules — e.g., "extends `src/importers/csv.ts`, adds new route in `app/import/`"]

**Risks / why we might NOT build it:**
- [steelman the opposing case in 1–3 sentences]

---

*(Repeat for #2 through #10.)*

## 6. Gaps we should intentionally NOT close

*(At least 3 items. Features competitors have that we should deliberately skip. For each: feature name, who has it, why we should skip it. Not-building is a strategic choice, and most analyses ignore it.)*

### Skip: [Feature name]

**Who has it:** [competitors]
**Why skip:** [reasoning — usually one of: doesn't fit our JTBDs, would dilute positioning, requires infra we lack, classified as Kano Indifferent, low Strategic Fit]

---

*(Repeat for at least 2 more.)*

## 7. Non-feature observations

*(Pricing moves, positioning shifts, messaging changes, new market segments competitors are entering. Sometimes the best move is repackaging or retargeting, not a feature. Bullet list is fine here.)*

## 8. Assumptions I made

*(Judgment calls made during auto-discovery. Especially flag inferences about target user and strategic constraints. End each bullet with the override field name the user can set to correct it.)*

- Inferred target user as [X] based on [signal]. To override, set `target_user_override` in `./competitive-research/overrides.yaml`.
- ...

## 9. Sources

*(Full URL list, grouped by competitor. Every claim in sections 3–7 should be traceable to a source here.)*

### [Competitor 1]
- [url] — [what was extracted]
- ...

### [Competitor 2]
- ...
```

---

## Notes on writing the report

**Tighten everything.** Hedge words ("might," "could potentially," "it may be the case that") are filler. Cut them. A PM should be able to act on this report Monday morning.

**Quotes from real users beat your own analysis.** When you have a customer quote that says "I switched from X to Y because Z," that one quote is worth more than three paragraphs of your reasoning. Use direct quotes liberally in section 5 evidence subsections.

**Don't bury the lead.** Section 1 (executive summary) should stand alone. If a founder reads only section 1 and the top 3 recommendations, they should still walk away with the right action items.

**File references in section 5 are the unique value of running this from inside the repo.** Don't skip them. "We could ship this by extending `src/billing/checkout.ts` and adding a new tier definition in `lib/plans.ts`" is what makes this report feel grounded vs. generic.

---

## JSON sidecar schema (`report.json`)

Phase 8 writes a structured `report.json` next to `report.md`. This is what downstream tooling (Linear/Jira/Notion ingestion, dashboards, longitudinal trend analysis) reads. The JSON must mirror the markdown shortlist exactly — same ranking, same scores, same evidence. Never let them diverge.

```json
{
  "run_date": "YYYY-MM-DD",
  "product_name": "string",
  "report_md_path": "competitive-research/runs/YYYY-MM-DD/report.md",
  "competitors": ["string", "..."],
  "shortlist": [
    {
      "rank": 1,
      "name": "string — same as markdown heading",
      "tag": "NEW | RECURRING | REVISITED",
      "first_suggested_date": "YYYY-MM-DD or null if NEW",
      "description": "string — one-line plain language",
      "evidence": {
        "shipped_by": ["competitor name", "..."],
        "user_quotes": [
          {"text": "string", "source_url": "string"}
        ]
      },
      "jtbd_advanced": "string — which JTBD from the dossier",
      "kano_class": "Must-Have | Performance | Delighter",
      "user_pain": "string",
      "scores": {
        "reach_per_qtr": 800,
        "impact": 2,
        "confidence": 0.8,
        "effort_person_months": 1,
        "rice": 1280,
        "strategic_fit": 7
      },
      "implementation": {
        "mvp_wedge": "string",
        "full_version": "string",
        "codebase_landing": ["src/path/to/file.ts", "app/path/"]
      },
      "risks": "string"
    }
  ],
  "skipped_features": [
    {"name": "string", "competitors_with_it": ["string"], "reason": "string"}
  ],
  "non_feature_observations": ["string", "..."],
  "in_flight": [
    {"name": "string", "in_progress_since": "YYYY-MM-DD", "competitors_with_it": ["string"]}
  ],
  "assumptions_to_verify": [
    {"inference": "string", "override_field": "target_user_override | ..."}
  ]
}
```

Notes:
- `confidence` is decimal (0.0–1.0), not percent.
- `tag` enum is exactly the three strings listed — don't invent variants.
- Omit `user_quotes` entries where you don't have a real source URL. Don't fabricate URLs to fill the schema.
- `in_flight` is populated from Phase 7's status filtering (entries with `status: in-progress` in `seen-features.jsonl`).
