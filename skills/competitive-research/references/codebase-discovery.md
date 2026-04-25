# Codebase Discovery (Phase 0 detailed guide)

This is the playbook for Phase 0 of the competitive-research skill: how to derive product identity, JTBDs, features, and constraints from the code itself, with no input from the user.

The output of Phase 0 is `./competitive-research/runs/YYYY-MM-DD/product-dossier.md`. Every later phase reads from this file, so quality here determines quality everywhere.

## 0.1 Establish scope

If `overrides.yaml` has `monorepo_scope` set, restrict all reads to that subdirectory.

Otherwise, detect a monorepo by checking for any of:

- `packages/`, `apps/`, `services/` directories
- `pnpm-workspace.yaml`, `lerna.json`, `turbo.json`, `nx.json`
- `workspaces` field in root `package.json`
- A `[workspace]` section in root `Cargo.toml`

If it's a monorepo and scope isn't obvious, pick the most user-facing package (typically the one with the marketing site, the public web app, or the one whose README reads like product copy rather than internal docs). Flag this choice in the report's "Assumptions I made" section so the user can correct it via `monorepo_scope`.

## 0.2 Identity signals

Pull the basics from whichever of these exist, in priority order:

**Product name & description:**
- `README.md` (root and any marketing-oriented ones in subdirs)
- `package.json` `name` and `description`
- `pyproject.toml` `[project]` table
- `Cargo.toml`, `go.mod`, `Gemfile`, `composer.json`, `*.csproj`
- `public/index.html` `<title>` and `<meta name="description">` tags
- Marketing site directories: `docs/`, `website/`, `www/`, `marketing/`, `landing/`, `site/`

**Public URL:**
- `package.json` `homepage` field
- `CNAME` files (GitHub Pages convention)
- Deployed URLs in `vercel.json`, `netlify.toml`, `wrangler.toml`, `fly.toml`
- CI configs that mention deployment domains
- If none in repo, web-search the product name to find it

**Target user:**
- README intro paragraphs and any "who is this for" / "for X who Y" sections
- Marketing site hero copy
- If genuinely unclear, infer from feature shape — a CLI implies developers, a drag-and-drop builder implies non-technical users — and explicitly flag the inference

**Pricing model:**
- A `/pricing` route or `pricing.{tsx,jsx,vue,html,md,astro}` file
- Stripe product/price IDs in code or env files (`STRIPE_PRICE_PRO`, etc.)
- Billing-related modules: `billing/`, `subscription/`, `payments/`
- A `PLANS`, `TIERS`, or `SUBSCRIPTION_TIERS` constant
- Pricing info in the README
- If none of the above exists, note "no pricing surface in repo — likely pre-revenue, open-source, or enterprise/contract"

## 0.3 Derive jobs-to-be-done

Don't guess. Derive JTBDs from concrete signals:

1. **README promises** — what the first 3 paragraphs of the README *promise* the user. The verbs and outcomes there are the most explicit JTBD statements the team has written.

2. **Top-level routes/pages** — the workflows the product makes first-class. Look in:
   - `app/` (Next.js app router, Remix, Nuxt 3)
   - `pages/` (Next.js pages router, Vue)
   - `src/routes/` (SvelteKit, SolidStart)
   - `src/views/` or `src/screens/` (Vue, React Native)
   - `views/` and `controllers/` (Rails, Django, Laravel)

3. **CLI commands** — for CLI tools, scan:
   - `bin/` directory
   - `cmd/` directory (Go convention)
   - `package.json` `bin` field and `scripts`
   - Cobra (Go), Click/Typer (Python), Clap (Rust), Commander (Node) command definitions

4. **API endpoints** — endpoints named after user outcomes reveal JTBDs better than CRUD-named ones. `/publish`, `/invoice`, `/deploy`, `/notify` are JTBD-shaped; `/users/:id`, `/items` are not. Check:
   - `routes/`, `api/`, `routers/`
   - OpenAPI/Swagger specs (`openapi.yaml`, `swagger.json`)
   - Rails `config/routes.rb`
   - Django `urls.py` files
   - FastAPI router files
   - tRPC router definitions

5. **Documentation section headers** — `docs/` table-of-contents headers often correspond to JTBDs ("Sending email," "Tracking conversions," "Building a workflow").

Write 2–4 JTBD statements in Christensen's classic form:

> *"When [situation], I want to [motivation], so I can [expected outcome]."*

## 0.4 Build the canonical feature list

This is the baseline every competitor is compared against. READMEs lag code, so don't rely on the README alone. Combine these sources:

- README feature bullets
- Marketing/docs pages — especially `/features`, `/how-it-works`, comparison pages
- Top-level routes and page components
- Exported API endpoints
- CLI subcommands and their flags
- Feature flag definitions — search the codebase for: `featureFlags`, `flags.`, `LaunchDarkly`, `Unleash`, `split.io`, `posthog.isFeatureEnabled`, `growthbook`, `flagsmith`
- `CHANGELOG.md` — every entry from the last 12 months
- Recent git log:
  ```bash
  git log --since="12 months ago" --pretty=format:"%s" | head -200
  ```
- Recent merged PR titles (if `gh` is available):
  ```bash
  gh pr list --state merged --limit 100 --json title,mergedAt
  ```

Dedupe. Write one bullet per distinct user-visible capability, at the granularity of "bulk CSV import with column mapping" — not "import" and not "added a new function to `importer.go`". Internal refactors, dependency bumps, and CI changes are not features. Drop them.

## 0.5 Derive strategic constraints

If `overrides.yaml` has `strategic_constraints_override`, use that and skip this step. Otherwise, infer from these signals:

**Strategy documents:**
- `CONTRIBUTING.md`, `ROADMAP.md`, `VISION.md`, `ARCHITECTURE.md`
- ADRs in `docs/adr/`, `docs/decisions/`, `architecture/decisions/`

**Team size & cadence:**
- Contributor count: `git shortlog -sn | wc -l`
- LoC count: `tokei` or `cloc` if available; otherwise `find . -type f \( -name "*.py" -o -name "*.ts" -o ... \) | xargs wc -l`
- Active commit days in last 90 days:
  ```bash
  git log --since="90 days ago" --pretty=format:"%ad" --date=short | sort -u | wc -l
  ```

A 2-person team with 20 active commit days/quarter cannot ship the same recommendations as a 50-person team with 80 active commit days. Factor this in.

**Infrastructure shape:**
- Serverless: `vercel.json`, `netlify.toml`, `wrangler.toml`, `serverless.yml`, `sam-template.yaml`
- Container/k8s: `Dockerfile`, `k8s/`, `helm/`, `kustomization.yaml`
- IaC: `terraform/`, `pulumi/`, `cdk/`
- Self-hosted/on-prem: install scripts, OS-specific build artifacts

Recommending "add real-time collaboration" to a product with no websocket infrastructure is a red flag. Note infra constraints explicitly.

**Explicit strategic signals (gold when they exist):**
- Issue labels (if `gh` available): `gh label list` — labels like `upmarket`, `enterprise`, `wont-do`, `out-of-scope` reveal explicit strategic lanes
- Recent commit messages mentioning "pivot," "sunset," "deprecating," "focus on," "killing":
  ```bash
  git log --since="6 months ago" --grep="pivot\|sunset\|deprecat\|focus on\|killing" --pretty=format:"%s"
  ```

**Synthesize** a 3–6 bullet list of inferred strategic constraints. Tag each bullet with its evidence source so the user can sanity-check, e.g.:

- "Small team — 2 active contributors, 18 active commit days last quarter (`git shortlog`, `git log`)"
- "No realtime infra — no websocket libraries, no PartyKit/Liveblocks dependencies, no `socket.io` (`package.json` audit)"
- "Consumer-focused — pricing tiers top out at $99/mo, no SSO/SAML code, no enterprise plan in `pricing.tsx`"

## 0.6 Identify in-repo competitors

Before going to the web, harvest competitors named in:

- README sections: "alternatives to," "why not X," "compared to," comparison tables
- Marketing site comparison pages — common paths: `compare/`, `vs/`, `alternatives/`, `versus/`
- Docs that mention migrating *from* another tool
- GitHub issues asking "how does this compare to X" (if `gh` available)
- Dependency lists — if the product depends on a competitor's SDK, that's coopetition, worth noting separately from pure competition

Combine this list with `extra_known_competitors` from `overrides.yaml` if set.

## 0.7 Write the dossier

Save everything to `./competitive-research/runs/YYYY-MM-DD/product-dossier.md` using this structure:

```markdown
# Product Dossier — YYYY-MM-DD

## Identity
- **Name:** [name]
- **One-liner:** [description]
- **URL:** [url]
- **Target user:** [target] *(source: [where this came from])*
- **Pricing:** [model] *(source: [file path])*

## Jobs-to-be-Done
1. When [situation], I want to [motivation], so I can [outcome]. *(evidence: [routes/files/docs])*
2. ...

## Canonical Feature List
- [feature 1]
- [feature 2]
- ...

## Inferred Strategic Constraints
- [constraint] *(evidence: [command/file])*
- ...

## In-repo Competitor Mentions
- [competitor name] — mentioned in [file]
- ...

## Auto-discovery confidence
Note any sections where signals were weak or contradictory. These are candidates for the user to override.
```

This dossier is the single source of truth for Phases 2 through 8. Don't re-derive identity later — read it from here.
