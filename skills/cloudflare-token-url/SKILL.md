---
name: cloudflare-token-url
description: Generate Cloudflare API token creation URLs with scoped permissionGroupKeys. Use when the user needs a Cloudflare dashboard link for creating a token for Wrangler deploys, Workers, Pages, Access, DNS, custom domains, protected VitePress docs, or Kennel/CDP documentation publishing.
---

# Cloudflare Token URL

## Overview

Use this skill to produce a Cloudflare API token creation URL that pre-fills the permissions required for a deployment workflow. Prefer a generated custom-token URL when Cloudflare's built-in templates are too broad, split across several products, or do not include the exact Worker/Access/DNS/email combination needed.

## Quick Start

Generate the protected-docs token URL first:

```bash
python3 scripts/generate_token_url.py protected-docs --name "Kennel CDP protected docs deploy"
```

Use a custom list when the deployment has a narrower scope:

```bash
python3 scripts/generate_token_url.py custom workers_scripts:edit workers_routes:edit dns:edit --name "Worker custom domain deploy"
```

The script prints the dashboard URL, selected permissions, and resource-scope reminders. It is deterministic and does not call the Cloudflare API.

## Protected Docs Preset

Use the `protected-docs` preset for Cloudflare-hosted static docs hidden behind an email-code or Access-style login flow, especially for VitePress/Kennel/CDP publishing.

The preset includes:

- `workers_scripts:edit` for Wrangler Worker deploys, secrets, and Worker Static Assets.
- `workers_routes:edit` for Worker routes and custom-domain triggers.
- `page:edit` for Pages deploy and Pages domain operations.
- `access:edit` for Access applications and policies.
- `access_acct:edit` for account-level Access organization and identity-provider settings.
- `dns:edit` for replacing conflicting records and setting required hostnames.
- `ssl_and_certificates:edit` for Cloudflare-managed certificate setup on custom domains.
- `email_sending:edit` for Cloudflare Email Service bindings and Worker email-code delivery.

Resource scoping should normally be:

- Account: the target Cloudflare account only.
- Zone: the target zone only, such as `example.com`.

Use broader scopes only when the user explicitly needs cross-account or cross-zone setup.

## Workflow

1. Identify whether the target is a Worker, Pages project, Access app, DNS/custom-domain change, or a combined protected-docs deployment.
2. Run `scripts/generate_token_url.py` with the closest preset or a custom permission list.
3. Give the user the generated URL and the permission/resource checklist.
4. Tell the user to create the token in Cloudflare, store the token in Doppler or the project secret store, and avoid pasting token values into chat.
5. Verify a created token with Cloudflare's `/user/tokens/verify` endpoint or `wrangler whoami` without printing the token.

## Cloudflare Templates

Cloudflare's built-in templates are useful for simple cases like "Edit Cloudflare Workers" or "Edit zone DNS", but the protected-docs workflow spans several products. If no single template includes all required permissions, generate a custom URL with this skill.

Load `references/cloudflare-token-urls.md` when you need the URL format, official docs links, or known deployment gotchas.
