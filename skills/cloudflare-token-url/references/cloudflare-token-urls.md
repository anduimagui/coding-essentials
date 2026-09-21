# Cloudflare Token URL Reference

## Official docs

- Account-owned token template URLs: https://developers.cloudflare.com/fundamentals/api/how-to/account-owned-token-template/
- API token permissions reference: https://developers.cloudflare.com/fundamentals/api/reference/permissions/
- Wrangler custom domains: https://developers.cloudflare.com/workers/wrangler/configuration/#custom-domains
- Worker Static Assets: https://developers.cloudflare.com/workers/static-assets/
- Cloudflare Email Service Workers API: https://developers.cloudflare.com/email-service/api/send-emails/workers-api/

## URL formats

User token creation URL:

```text
https://dash.cloudflare.com/profile/api-tokens?permissionGroupKeys=[ENCODED_JSON]&accountId=*&zoneId=all&name=[TOKEN_NAME]
```

Account-owned token creation URL:

```text
https://dash.cloudflare.com/?to=/:account/api-tokens&permissionGroupKeys=[ENCODED_JSON]&name=[TOKEN_NAME]
```

The `permissionGroupKeys` value is URL-encoded JSON:

```json
[{"key":"dns","type":"edit"}]
```

## Current protected-docs permissions

Use this list for a Cloudflare-hosted protected docs deployment that may need Worker Static Assets, Cloudflare Access, Pages cleanup, DNS replacement, Worker custom domains, and email-code delivery:

```text
workers_scripts:edit
workers_routes:edit
page:edit
access:edit
access_acct:edit
dns:edit
ssl_and_certificates:edit
email_sending:edit
```

## Gotchas

- Cloudflare's dashboard templates are split by product. A combined protected-docs deployment usually needs a custom token.
- Pages config does not support the `send_email` binding used by Cloudflare Email Service. Use a Worker with Static Assets for email-code gates.
- Worker Static Assets can serve assets before the Worker unless `assets.run_worker_first` is enabled for protected routes.
- A prior Pages custom-domain record can conflict with a Worker Custom Domain. Keep `dns:edit` available when migrating a hostname from Pages to a Worker.
- `doppler secrets get --raw` can still produce table output in some contexts. Use `--plain --raw` when a command needs only the secret value.
- Do not print token values. Verify tokens through Cloudflare token verification or Wrangler using environment-loaded credentials.
