# Competitive Research Skill for Claude Code

A weekly competitive analysis workflow that auto-discovers your product from
its codebase, researches competitors on the web, and produces a ranked,
evidence-backed list of features you're missing — scored with PM frameworks
(Jobs-to-be-Done, Kano, RICE) and deduped against prior weeks.

Zero-config: drop the skill in, run it from your repo, get a report. No
filling out forms.

---

## What you get

Every run produces a `report.md` with:

1. **Executive summary** — the 3–5 most important findings
2. **Product dossier** — what the skill inferred about your product (so you can correct it if wrong)
3. **Landscape snapshot** — how the competitive set has shifted since last run
4. **Feature matrix** — a ✅/❌/🟡 table across you and 8–15 competitors
5. **Top 10 feature recommendations** — each with RICE scoring, evidence quotes from real users, and specific files/modules in *your* codebase where the work would land
6. **"Don't build" list** — features competitors have that you should deliberately skip
7. **Non-feature observations** — pricing, positioning, and messaging shifts
8. **Sources** — every claim traceable to a URL

State persists across runs in `./competitive-research/`, so each week dedupes against the last and surfaces what's genuinely new.

---

## Prerequisites

- **Claude Code** installed and working — see [the official installation guide](https://docs.claude.com/en/docs/claude-code/overview) if you don't have it yet
- **Python 3.7+** for the dedupe script (almost certainly already installed)
- **`gh` CLI** (optional but recommended) for richer git/issue/PR signals — [install instructions](https://cli.github.com/)
- **`tokei` or `cloc`** (optional) for repo size metrics

---

## Installation

Pick one of the three options below. **Option A** (personal install) is right for almost everyone.

### Option A — Personal install (all projects)

This makes the skill available in every repo on your machine.

```bash
# from the directory where you downloaded the skill
unzip competitive-research.zip -d ~/.claude/skills/
```

Verify the layout — the path must be exactly this, with `SKILL.md` directly inside the skill folder:

```bash
ls ~/.claude/skills/competitive-research/
# should show: SKILL.md  references/  scripts/  README.md
```

If you see a double-nested folder (e.g., `~/.claude/skills/competitive-research/competitive-research/SKILL.md`), the skill won't be discovered. Move things up one level:

```bash
mv ~/.claude/skills/competitive-research/competitive-research/* ~/.claude/skills/competitive-research/
rmdir ~/.claude/skills/competitive-research/competitive-research
```

### Option B — Project-scoped install (one repo, shared with team)

If you want the skill committed to a specific repo so your whole team uses it:

```bash
# from the repo root
mkdir -p .claude/skills
unzip /path/to/competitive-research.zip -d .claude/skills/
git add .claude/skills/competitive-research
git commit -m "Add competitive-research skill"
```

### Option C — Monorepo, per-package install

If you have a monorepo and want the skill available only when working inside a specific package:

```bash
# from the repo root
mkdir -p packages/your-product/.claude/skills
unzip /path/to/competitive-research.zip -d packages/your-product/.claude/skills/
```

Claude Code automatically discovers skills from nested `.claude/skills/` directories when you're working with files in those subdirectories.

### After installing

If Claude Code was already running, the skill is picked up automatically — no restart needed. The exception: if you just created the top-level `~/.claude/skills/` directory for the first time, restart Claude Code so it can start watching the directory.

Verify the skill loaded:

```bash
# Inside Claude Code
/competitive-research
```

You should see the skill name listed. If not, see [Troubleshooting](#troubleshooting) below.

---

## Usage

### First run

1. `cd` into your product's repo (or a monorepo subdirectory if scope C).
2. Open Claude Code.
3. Say something like:

   > Run the competitive research

   Or any of these — the skill is set to trigger broadly:
   - "What features are competitors shipping that we're not?"
   - "Do a gap analysis on my product"
   - "What should I build next quarter?"
   - "Run the weekly competitive review"

The first run takes the longest (typically 10–20 minutes of work) because it's discovering everything from scratch — your product identity, your features, your competitors. Subsequent runs are faster because state persists.

### Weekly cadence

The skill is designed to run weekly. Each run:

- Re-discovers your codebase (catches new features you've shipped)
- Re-checks competitor changelogs and websites
- Tags recommendations as `[NEW]`, `[RECURRING]`, or `[REVISITED]` based on prior runs
- Saves a fresh report under `./competitive-research/runs/YYYY-MM-DD/`

You can run it manually each Monday morning, or automate it. A simple cron job:

```bash
# Run every Monday at 9am, write output to a log file
0 9 * * 1 cd /path/to/your/repo && claude -p "run the competitive research" > ~/competitive-research-$(date +%Y%m%d).log 2>&1
```

(Adjust the `claude -p` invocation to match your Claude Code version and shell. The point is: it's a regular CLI command, schedule it however you like.)

### What gets created in your repo

After the first run, you'll find:

```
your-repo/
└── competitive-research/                    # all skill output, gitignored by default
    ├── runs/
    │   └── 2026-04-24/
    │       ├── product-dossier.md           # what the skill thinks your product is
    │       ├── raw-notes/                   # one file per competitor, full notes
    │       ├── evidence.md                  # quotes, screenshots, pricing snapshots
    │       └── report.md                    # ← the deliverable
    ├── history/
    │   └── seen-features.jsonl              # dedupe log, append-only
    ├── competitors.yaml                     # persistent competitor list
    └── overrides.yaml                       # optional, only if you want to override discovery
```

You probably want to add `competitive-research/` to your `.gitignore` unless you specifically want this committed.

---

## Optional: overriding auto-discovery

If a run got something wrong about your product (e.g., it inferred the wrong target user), create `./competitive-research/overrides.yaml`:

```yaml
# Anything blank gets auto-discovered. Only fill in what's wrong.
product_name_override: ""
product_url_override: ""
target_user_override: "solo founders running Shopify stores doing $10k–$100k/mo"
extra_known_competitors:
  - "Klaviyo — https://klaviyo.com"
  - "Postscript — https://postscript.io"
strategic_constraints_override: |
  - We're a 2-person team, no enterprise features
  - AI features are a Q2 priority
monorepo_scope: ""
```

The skill checks for this file every run. The end of each report flags inferences that the user might want to override, so you only fill in fields that the skill got wrong.

---

## Customization

The skill is just files. Edit them:

- **`SKILL.md`** — change the workflow itself (e.g., add a phase, change the report format)
- **`references/frameworks.md`** — adjust which PM frameworks get applied or how they're scored
- **`references/codebase-discovery.md`** — add signals specific to your stack (e.g., "also check our `feature-flags.json`")
- **`references/report-template.md`** — change the report structure
- **`scripts/dedupe_features.py`** — tune the similarity thresholds for the dedupe pass

If you customize, keep `SKILL.md` under ~500 lines — Claude Code uses progressive disclosure, where SKILL.md is always loaded but reference files only get read when the workflow points to them. Pushing detail into references keeps the skill efficient.

---

## Troubleshooting

**Skill doesn't appear in `/skill-name` autocomplete:**
- Check the path: `ls ~/.claude/skills/competitive-research/SKILL.md` should exist.
- Check for double-nesting (the most common error): if `SKILL.md` is at `~/.claude/skills/competitive-research/competitive-research/SKILL.md`, move things up one level.
- If you just created the top-level `~/.claude/skills/` directory, restart Claude Code so it can start watching it.

**Skill triggers but immediately produces a generic answer:**
- This usually means Claude Code answered without consulting the skill body. Try a more specific phrase like "use the competitive-research skill to..." or invoke it with `/competitive-research`.
- Skills tend to undertrigger on simple-sounding requests. Phrasing the ask as multi-step ("do a full competitive analysis and gap report") helps.

**Phase 0 produces a wrong product description:**
- Open the latest `runs/YYYY-MM-DD/product-dossier.md` to see exactly what was inferred and from which sources.
- Set the relevant override in `./competitive-research/overrides.yaml` and rerun.

**Web research is shallow / few competitors found:**
- This usually means the product category was hard to identify from the codebase alone. Set `extra_known_competitors` in `overrides.yaml` to seed the search with 2–3 competitors you know about.

**Recommendations feel obvious / repetitive across weeks:**
- Check `history/seen-features.jsonl` — make sure entries from prior runs are actually being saved. The dedupe step relies on this file.
- The skill enforces "at least 2 non-obvious recommendations per report" as a quality check. If you're consistently getting obvious ones, the issue is usually that the inferred strategic constraints are too vague — add specific constraints via override.

**Dedupe script errors:**
- Run it manually to see the actual error: `python ~/.claude/skills/competitive-research/scripts/dedupe_features.py --new shortlist.json --history ./competitive-research/history/seen-features.jsonl`
- Common cause: malformed JSONL line in the history file. Open it and remove the bad line.

---

## How it works (under the hood)

The skill is structured around Claude Code's progressive disclosure pattern:

- **`SKILL.md`** is loaded into context whenever the skill is triggered. It's a workflow skeleton with pointers.
- **`references/*.md`** are loaded only when the workflow needs them — frameworks for scoring, the report template for writing, the codebase-discovery guide for Phase 0.
- **`scripts/dedupe_features.py`** runs as a subprocess for the deterministic similarity-matching step. It surfaces likely matches; Claude makes the final semantic call.

This keeps the always-on context small (the SKILL.md is ~170 lines) while making the deeper detail available when needed.

---

## Uninstalling

```bash
rm -rf ~/.claude/skills/competitive-research/
```

Or for a project-scoped install:

```bash
rm -rf .claude/skills/competitive-research/
git rm -r .claude/skills/competitive-research && git commit -m "Remove competitive-research skill"
```

The skill's output (`./competitive-research/` in your repos) is separate and won't be deleted by uninstalling the skill itself — remove that manually if you want.

---

## License & feedback

Use it however you want. If a phase consistently produces bad output, the most useful thing is to capture a real example (the prompt + the output you got + what you wanted) and edit the relevant `references/*.md` file directly. Skills are designed to be edited.
