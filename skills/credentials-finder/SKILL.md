---
name: credentials-finder
description: Search the Raggle Radar credentials catalog (the same JSON used by the API Keys Raycast extension) for a specific provider and return the exact dashboard URL where an API key, auth token, or credential can be generated, resolving any URL variables. Use when the user asks where to create, get, or generate an API key, auth token, API token, or application credential for a provider such as OpenAI, Anthropic, Stripe, xAI, Together, ElevenLabs, etc.
---

# Credentials Finder (Provider → Auth-Key Dashboard URL)

Use this skill when the user needs the URL that opens a provider's credential
page to generate or manage an API key / auth token / OAuth secret. It searches
the same hosted catalog used by the "API Keys" Raycast extension, so the
answers match what that extension shows.

Typical asks:
- "Where do I get an OpenAI/Anthropic/Stripe API key?"
- "Find the credentials URL to generate an auth token for X."
- "Which dashboard do I open to create an API key for Together / xAI / ElevenLabs?"

## How to search

Run the bundled helper from this skill's `scripts/` directory:

```bash
python3 "/Users/andrew/Documents/GitHub/anduimagui-essentials/skills/credentials-finder/scripts/find-provider.py" "<provider query>"
```

- The query is matched against name, slug, domain, category, and URL; every
  whitespace-separated term must appear (e.g. `raycast ai` or `stripe`).
- Filter by category with `--category "Payments"` / `AI/ML` / `Cloud`, etc.
- Force a fresh copy of the catalog with `--refresh` (it is cached locally for
  up to 24 hours).
- `--list` prints a compact `slug | name | category` table; `--json` prints
  machine-readable results with missing variables.

## Handling URL variables

A few providers (Polar, Fourthwall, OpenCode, etc.) have `{PLACEHOLDER}` tokens
in their URL, e.g. `https://polar.sh/dashboard/{POLAR_ORG_SLUG}/settings`.
Resolve them from values the user supplies or from values already known in
context:

```bash
python3 .../find-provider.py "polar" --var POLAR_ORG_SLUG=my-org
```

- If a value is not known, do **not** guess (organization slugs, shop URLs, and
  workspace IDs are account-specific). Report the missing variable label(s) and
  ask the user, or fill them from existing project context (e.g. a workspace
  slug already in the repo).
- Values are URL-encoded like the Raycast extension does, so normal slugs pass
  through unchanged.

## Rules

- **Catalog-only.** Only ever return URLs that appear in the catalog data.
  Never invent, construct, or pattern-match a provider URL from memory.
- **Report gaps.** If a provider is not in the catalog, say so and offer the
  closest matches found (or suggest opening the provider's site to look for a
  "Developers"/"Keys" section).
- **Open, don't generate.** The returned URL is the page where the user
  generates/manages the key in their own logged-in browser session. The skill
  only finds the URL.
- **No secrets.** Never echo API keys, tokens, or variable values that look
  secret back into the conversation beyond what is needed to resolve the URL.

## Data source

`https://raggle.co/radar.json` → `collections.credentials` (hosted Raggle Radar
catalog, ~300+ providers in categories such as AI/ML, Payments, Cloud, DevOps,
Email, Analytics, Database, Storage, Fintech, Auth, Commerce). Field shape per
provider: `slug`, `name`, `url`, `category`, `domain`, optional `variables`
(`key`, `label`, `placeholder`).