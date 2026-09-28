#!/usr/bin/env python3
"""Search the Raggle Radar credentials catalog for a provider and return the
dashboard URL where an API key / auth token can be generated.

Reads the `collections.credentials` list from https://raggle.co/radar.json --
the exact same data source used by the API Keys Raycast extension -- so results
match what the extension shows. URL placeholders like {WORKSPACE_ID} are
resolved from values supplied via --var KEY=VALUE.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

RADAR_URL = "https://raggle.co/radar.json"
CACHE_TTL_SECONDS = 24 * 60 * 60  # refresh the cached catalog once per day
USER_AGENT = "credentials-finder-skill/1.0"

PLACEHOLDER_RE = re.compile(r"\{([^{}]+)\}")
# Matches JavaScript encodeURIComponent behavior (keeps unreserved chars only).
URL_SAFE = "!~*'()"


def default_cache_path() -> Path:
    base = os.environ.get("XDG_CACHE_HOME") or os.environ.get("CACHE_DIR")
    if base:
        return Path(base) / "credentials-finder" / "radar.json"
    return Path.home() / ".cache" / "credentials-finder" / "radar.json"


def fetch_catalog(cache_path: Path, refresh: bool = False) -> dict:
    cache_path.parent.mkdir(parents=True, exist_ok=True)

    if not refresh and cache_path.exists():
        age = time.time() - cache_path.stat().st_mtime
        if age < CACHE_TTL_SECONDS:
            try:
                return json.loads(cache_path.read_text())
            except json.JSONDecodeError:
                pass  # fall through to a fresh fetch

    req = urllib.request.Request(RADAR_URL, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    cache_path.write_text(json.dumps(data, indent=2, sort_keys=True))
    return data


def get_credentials(catalog: dict) -> list[dict]:
    return (catalog.get("collections") or {}).get("credentials") or []


def normalize(value: str) -> str:
    return value.strip().lower()


def provider_matches(provider: dict, query: str) -> bool:
    query = normalize(query)
    if not query:
        return True
    haystack = " ".join(
        [
            str(provider.get("name", "")),
            str(provider.get("slug", "")),
            str(provider.get("domain", "")),
            str(provider.get("category", "")),
            str(provider.get("url", "")),
        ]
    ).lower()
    return all(term in haystack for term in query.split())


def required_variables(provider: dict) -> list[dict]:
    return provider.get("variables") or []


def resolve_url(provider: dict, values: dict[str, str]) -> tuple[str, list[str]]:
    """Fill {PLACEHOLDER} tokens. Returns (url, list of unfilled variable keys)."""
    url = provider.get("url", "")
    missing = [
        v["key"] for v in required_variables(provider) if not values.get(v["key"])
    ]

    def replace(match: re.Match) -> str:
        key = match.group(1)
        value = values.get(key, "")
        return urllib.parse.quote(value, safe=URL_SAFE) if value else match.group(0)

    if missing:
        return url, missing
    return PLACEHOLDER_RE.sub(replace, url), []


def parse_vars(raw_vars: list[str]) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw in raw_vars:
        if "=" not in raw:
            print(f"error: --var expects KEY=VALUE, got: {raw}", file=sys.stderr)
            sys.exit(2)
        key, value = raw.split("=", 1)
        values[key.strip()] = value
    return values


def print_text(providers: list[dict], values: dict[str, str]) -> None:
    for index, provider in enumerate(providers, start=1):
        name = provider.get("name", "?")
        slug = provider.get("slug", "")
        category = provider.get("category", "")
        domain = provider.get("domain", "")
        url, missing = resolve_url(provider, values)

        print(f"Match {index} of {len(providers)} - {name}" + (f" (slug: {slug})" if slug else ""))
        print(f"  Category: {category}")
        print(f"  Domain:   {domain}")
        print(f"  URL:      {url}")

        variables = required_variables(provider)
        if variables:
            print("  URL variables:")
            for variable in variables:
                key = variable.get("key", "")
                label = variable.get("label", key)
                print(f"    - {key} ({label})")
            if missing:
                print(
                    f"  NOTE: set the missing variable value and re-run with "
                    f"--var {missing[0]}=<value> to get the fully resolved URL."
                )
        print()


def print_list(providers: list[dict]) -> None:
    for provider in providers:
        print(
            f"{provider.get('slug', ''):<32} {provider.get('name', ''):<28} "
            f"{provider.get('category', '')}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Find the dashboard URL where a provider's API key / auth "
        "token can be generated, from the Raggle Radar credentials catalog."
    )
    parser.add_argument(
        "query",
        nargs="?",
        help="provider search terms (name, slug, domain, category); "
        "every whitespace-separated term must match",
    )
    parser.add_argument(
        "--category",
        help="only show providers in this category (e.g. 'AI/ML', 'Payments')",
    )
    parser.add_argument(
        "--var",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="value for a URL placeholder variable, repeatable",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="print compact slug | name | category lines instead of details",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="print matching providers as JSON (for machine use)",
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="re-fetch the catalog from https://raggle.co/radar.json, "
        "ignoring the local cache",
    )
    parser.add_argument("--cache-dir", help="override the catalog cache directory")
    parser.add_argument(
        "--catalog-file",
        help="search a local radar.json file instead of the network source",
    )

    args = parser.parse_args()
    values = parse_vars(args.var)

    try:
        if args.catalog_file:
            catalog = json.loads(Path(args.catalog_file).read_text())
        else:
            cache_path = Path(args.cache_dir) / "radar.json" if args.cache_dir else default_cache_path()
            catalog = fetch_catalog(cache_path, refresh=args.refresh)
    except Exception as exc:  # network or parse failure
        print(f"error: could not load the credentials catalog: {exc}", file=sys.stderr)
        return 1

    providers = get_credentials(catalog)
    matches = [
        p
        for p in providers
        if provider_matches(p, args.query or "")
        and (not args.category or normalize(p.get("category", "")) == normalize(args.category))
    ]

    if args.json:
        payload = []
        for provider in matches:
            url, missing = resolve_url(provider, values)
            payload.append(
                {
                    "slug": provider.get("slug", ""),
                    "name": provider.get("name", ""),
                    "category": provider.get("category", ""),
                    "domain": provider.get("domain", ""),
                    "url": url,
                    "missing_variables": missing,
                }
            )
        print(json.dumps(payload, indent=2))
    elif args.list:
        print_list(matches)
    else:
        if not args.query and not args.category:
            print(f"catalog loaded: {len(providers)} providers across "
                  f"{sorted({p.get('category', '') for p in providers})}")
            print("add a query to search, e.g. find-provider.py \"stripe\"")
            return 0
        if matches:
            print_text(matches, values)
        else:
            print("no providers matched the query", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())