---
name: domain-finder
description: Quick-check domain name availability across TLDs and brainstorm registerable name candidates using bundled DNS+WHOIS scripts. Use whenever the user asks to check if a domain is free or taken, find available domain names, test a name across .com/.io/.app/.co/etc, brainstorm brandable domain ideas, see if a startup/project/product name is registerable, hunt for short unclaimed domains, or pick which TLD to grab first. Trigger on phrases like "is X available", "check this domain", "find a domain for", "what TLDs are free for", "domain name ideas", "is the .com taken", even when the user doesn't say the word "skill".
---

# Domain Finder

Quickly test whether domain names are available across TLDs, suggest registerable variants when the obvious name is taken, and rank what to grab first. Backed by two bundled scripts in `scripts/`:

- `domain_name_finder.sh` — the primary checker. For each `<name>.<tld>` it runs `nslookup` (DNS resolve = definitely active/taken), then falls back to `whois` for "no match / not found / available" vs "creation date / registered" signals, and prints a grouped AVAILABLE/TAKEN summary.
- `quick_domain_test.py` — fast DNS-only bulk pre-filter and random short-name generator. Importable: `from quick_domain_test import check_domain_dns, generate_5_char_domains`.

## Why the two-layer check matters

A domain that resolves in DNS is definitely registered and in use. A domain with no DNS record is *probably* available, but parked, expired, or reserved names can also lack DNS — so WHOIS is the tie-breaker. The shell script already layers these: trust "TAKEN" from DNS, trust "AVAILABLE" only when WHOIS confirms "no match / not found / status: available". Anything else is "UNKNOWN" and should be verified manually at a registrar. Treat every result as indicative, not authoritative — always confirm at a registrar before buying.

## Verify setup

```bash
bash scripts/domain_name_finder.sh example com,io
python3 scripts/quick_domain_test.py
which nslookup whois   # both ship with macOS
```

If `whois` is missing, DNS-only mode (the python script's `check_domain_dns`) still works but loses the confirmation layer.

## Workflow

1. **Get the base name(s).** Take them from the user when given. If the user only describes a project/product idea, propose 3–8 candidate base names first (short, brandable, easy to spell, no hyphens if avoidable) and confirm before mass-checking.

2. **Suggest variants when the user wants ideas** (or when the obvious name is likely taken). Useful variant families:
   - The base name as-is.
   - Prefixes/suffixes: `get<name>`, `go<name>`, `<name>app`, `<name>io`, `<name>hq`, `<name>ly`, `try<name>`.
   - Shortened/abbreviated forms (drop vowels, keep consonant skeleton).
   - Compounds with a relevant word (`<name>labs`, `<name>ai`, `<name>data`).
   - Random 5-char strings via `generate_5_char_domains(count=...)` for hunting unclaimed short names — note these are random lowercase, not pronounceable, so treat them as raw material, not final picks.

   Don't generate hundreds; keep the candidate list focused (≤ ~15) so checks stay fast and the shortlist stays readable.

3. **Check across TLDs.** Run the shell script with either the default TLD set or a user-specified list:
   ```bash
   bash scripts/domain_name_finder.sh <name>                # default TLDs
   bash scripts/domain_name_finder.sh <name> com,io,app,co  # custom
   ```
   Default TLDs in the script: `com,net,org,info,biz,co,io,me,tv,cc,us,uk,de,fr,ca,au,jp,in,cn,br`.

   For a large candidate list, pre-filter fast with DNS-only first, then WHOIS-confirm the survivors with the shell script:
   ```python
   from quick_domain_test import check_domain_dns
   survivors = [d for d in candidates if check_domain_dns(f"{d}.com")]
   ```

4. **Rank the available domains** by TLD desirability for a brandable/startup context:
   `com` > `app` ≈ `io` ≈ `ai` > `co` ≈ `dev` ≈ `so` > `me` > `xyz` > `org` > `net` > `info` ≈ `biz` > `tv` ≈ `cc` > country TLDs (`us,uk,de,...`).
   If the user's context is non-commercial (e.g. an open-source project), bump `.org` up. If the user states a TLD preference, honor it above the default ranking.

5. **Output a ranked shortlist.** Lead with available domains best-first, each with the TLD and a one-line note on why it ranks there. End with a single decisive recommendation: which one to grab first, and the runner-up. Append the standard caveat that results are indicative and to verify at a registrar before purchase.

## Output format

```text
AVAILABLE (ranked):
  1. example.com        — best: memorable, default trust
  2. example.io         — strong tech/startup TLD
  3. getexample.com     — prefix variant, decent fallback

TAKEN:
  example.app, example.co, example.ai

RECOMMENDATION: Grab example.com first; example.io as runner-up.
Verify at a registrar (e.g. Porkbun, Namecheap, Cloudflare) before buying — these checks are indicative.
```

## Quality rules

- Don't report a domain as available without either a WHOIS "no match / not found / available" signal or an explicit user request to treat DNS-only as good enough.
- Don't invent TLDs the script didn't actually check.
- If everything the user wanted is taken, say so plainly and offer the best variant/TLD combinations worth trying next rather than pretending a taken name is free.
- Keep candidate generation focused; avoid spraying hundreds of random names.
