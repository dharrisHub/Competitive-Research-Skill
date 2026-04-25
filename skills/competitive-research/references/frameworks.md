# Frameworks Reference

This file is the cheat-sheet for the product-management frameworks used in Phases 5 and 6 of the competitive-research skill. Read it before classifying gaps and scoring features. The point is not to recite definitions — it's to apply each lens correctly so the recommendations don't all collapse into "competitor has it, we should too."

## Jobs-to-be-Done (Christensen / Ulwick)

A JTBD is what the user is trying to accomplish — the underlying motivation, not the surface request. The classic statement form:

> *"When [situation], I want to [motivation], so I can [expected outcome]."*

**Why it matters here:** every feature recommendation should advance one of the product's JTBDs. If a feature competitors have doesn't advance any of our JTBDs, copying it just bloats the product. Be skeptical of recommendations that fail this check.

**Common mistake:** writing JTBDs that describe the product instead of the user's life. "When I want to use the dashboard, I want to see metrics, so I can use the dashboard" is not a JTBD; it's a tautology. Real JTBDs are situational and outcome-driven: "When I'm preparing my Monday standup, I want to see what shipped over the weekend, so I can flag anything risky to my manager."

## Kano model

Every feature falls into one of five categories:

- **Must-Have** — Users assume it. Absence kills satisfaction; presence is invisible. (Login that works. Data that doesn't get lost.)
- **Performance** — More is better. Linear satisfaction. (Faster page loads. More integrations. Lower price.)
- **Delighter** — Unexpected. Creates love disproportionate to effort. Often becomes a Performance or Must-Have over time. (Linear's keyboard shortcuts when they launched. Stripe's docs.)
- **Indifferent** — Users don't care. Building these is wasted effort. (Most "competitor has X so we should too" features.)
- **Reverse** — Users actively dislike. (Adding a complex pricing tier. Forcing account creation for trivial actions.)

**Why it matters here:** the dominant failure mode of competitive analysis is recommending Indifferents. If three competitors have a feature and users haven't asked for it once in your reviews/issues, that's an Indifferent — skip it. Conversely, a Delighter that no competitor has yet is the highest-leverage recommendation.

**How to classify from competitor evidence:** look at the voice-of-customer notes from Phase 3. If users *complain* about its absence at competitors, it's at least Performance, possibly Must-Have. If users *praise* it as a surprising win, it's a Delighter. If it's never mentioned in reviews despite being shipped, it's likely Indifferent.

## Differentiation type (Moore / Porter)

Closing a feature gap is one of three things:

- **(a) Parity on table stakes** — Necessary to be in the game. Rarely a moat. Build only if absence is actively losing deals.
- **(b) Leapfrog on a dimension we already lead** — We're known for X; competitors have weaker X; we go further. Highest defensibility.
- **(c) New axis of differentiation** — A dimension competitors aren't competing on. Riskier, but potentially the largest payoff (Moore: "compete by category creation, not feature wars").

**Why it matters here:** (c) is usually the highest-leverage recommendation but the easiest to miss because it requires *not* looking at what competitors have. Force at least 1–2 (c)-type recommendations in every report, even if they come from voice-of-customer complaints rather than feature inventories.

## RICE scoring

A standard prioritization formula. For each feature:

- **Reach** — number of users affected per quarter (or per relevant time window). Use real numbers when possible (active users, downloads, signups). Estimate when not.
- **Impact** — magnitude of the effect on each user. Use the Intercom-style scale: 3 (massive), 2 (high), 1 (medium), 0.5 (low), 0.25 (minimal).
- **Confidence** — how sure are we about the numbers? 100% (have data), 80% (some evidence), 50% (gut feel).
- **Effort** — person-months to ship.

**RICE = (Reach × Impact × Confidence) / Effort**

**Why it matters here:** numerical scoring forces explicit assumptions and makes recommendations comparable. The numbers are not precise — they don't need to be — but the act of writing them down catches recommendations that sounded good but score poorly under the math.

**How to score:** include explicit numbers and a one-line justification per dimension. Don't just write "RICE: 12." Write:

```
- Reach: 800/qtr (about 40% of MAU based on routes most used)
- Impact: 2 (eliminates a manual step done daily by power users)
- Confidence: 80% (3 G2 reviews of competitors mention this exact gap)
- Effort: 1 person-month (existing import infra can be extended)
- RICE = (800 × 2 × 0.8) / 1 = 1280
```

## Strategic Fit (1–10)

A second score, applied *after* RICE, to catch the cases where the numbers say "build it" but strategy says "don't." Score 1–10 based on:

1. **Alignment with inferred strategic constraints** — does it fit the team size, infrastructure, and explicit "we don't do X" signals from Phase 0.5?
2. **Positioning** — does it reinforce or dilute what the product is known for?
3. **Red-ocean vs. blue-ocean** — are competitors all about to ship this anyway (red, lower fit) or is everyone missing it (blue, higher fit)?

**Why it matters here:** RICE alone is silent on strategy. A feature with high RICE that pulls the product upmarket when the team has explicitly said "we serve solo founders" should not ship, regardless of the math. Strategic Fit is the override.

## Buyer vs. user value

In B2B, the person who pays is often not the person who uses. A feature that helps only one of them can still fail.

- **Buyer-only value** — admin controls, audit logs, SSO, role-based permissions. Helps the procurement decision; doesn't change daily UX.
- **User-only value** — keyboard shortcuts, themes, productivity features. Helps the daily user; rarely closes deals.
- **Both** — a feature that lands in both columns is the strongest type.

**Why it matters here:** a recommendation that helps neither the buyer nor the user is a non-starter. Forcing this classification catches features that sound good in the abstract but don't have a clear beneficiary.

## Moat / defensibility

If we ship the feature, how long until a competitor can match it?

- **Weekend** — pure UI, simple integration, no data dependency. Low moat.
- **A quarter** — requires real engineering work, design iteration, or partner integrations. Medium moat.
- **Years** — requires accumulated user data, network effects, exclusive partnerships, or hard-won expertise. High moat.

**Why it matters here:** weekend-moat features are necessary sometimes (parity moves) but should not dominate the recommendation list. A report full of weekend-moat suggestions is treadmill work — competitors copy them as fast as we ship them.

## How to combine the lenses

When classifying a gap in Phase 5, walk through them in order:

1. **JTBD fit** — does this advance any JTBD? If no, drop it (or keep only as a Don't-Build entry with reasoning).
2. **Kano** — what category is it? If Indifferent, drop it.
3. **Differentiation type** — (a), (b), or (c)? Note it.
4. **Buyer/user value** — which? If neither, drop it.
5. **Moat** — weekend, quarter, or years?

Then in Phase 6, score the survivors with RICE, then re-rank by Strategic Fit.

The combined effect: most features competitors have will get filtered out before scoring. That's correct. The point of the framework stack is to surface the small number of features where multiple lenses agree — those are the recommendations worth shipping.
