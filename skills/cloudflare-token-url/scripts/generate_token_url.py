#!/usr/bin/env python3
import argparse
import json
from urllib.parse import urlencode


PRESETS = {
    "protected-docs": [
        "workers_scripts:edit",
        "workers_routes:edit",
        "page:edit",
        "access:edit",
        "access_acct:edit",
        "dns:edit",
        "ssl_and_certificates:edit",
        "email_sending:edit",
    ],
    "worker-custom-domain": [
        "workers_scripts:edit",
        "workers_routes:edit",
        "dns:edit",
        "ssl_and_certificates:edit",
    ],
    "pages-deploy": [
        "page:edit",
        "dns:edit",
    ],
}


def permission(value):
    if ":" not in value:
        raise argparse.ArgumentTypeError(f"expected key:type, got {value!r}")

    key, kind = value.split(":", 1)
    if not key or not kind:
        raise argparse.ArgumentTypeError(f"expected key:type, got {value!r}")

    return {"key": key, "type": kind}


def build(args, permissions):
    body = json.dumps(permissions, separators=(",", ":"))

    if args.account_token:
        params = urlencode({"permissionGroupKeys": body, "name": args.name})
        return f"https://dash.cloudflare.com/?to=/:account/api-tokens&{params}"

    params = urlencode(
        {
            "permissionGroupKeys": body,
            "accountId": args.account_id,
            "zoneId": args.zone_id,
            "name": args.name,
        }
    )
    return f"https://dash.cloudflare.com/profile/api-tokens?{params}"


def main():
    parser = argparse.ArgumentParser(
        description="Generate a Cloudflare API token creation URL."
    )
    parser.add_argument(
        "preset",
        choices=[*PRESETS.keys(), "custom"],
        help="Permission preset, or 'custom' with key:type values.",
    )
    parser.add_argument(
        "permissions",
        nargs="*",
        type=permission,
        help="Custom permission values such as workers_scripts:edit.",
    )
    parser.add_argument(
        "--name",
        default="Protected docs deploy",
        help="Token name to pre-fill in Cloudflare.",
    )
    parser.add_argument(
        "--account-id",
        default="*",
        help="User-token account scope. Use a concrete account ID when known.",
    )
    parser.add_argument(
        "--zone-id",
        default="all",
        help="User-token zone scope. Use a concrete zone ID when known.",
    )
    parser.add_argument(
        "--account-token",
        action="store_true",
        help="Generate an account-owned token URL instead of a user-token URL.",
    )
    args = parser.parse_args()

    if args.preset == "custom":
        if not args.permissions:
            parser.error("custom requires at least one key:type permission")
        permissions = args.permissions
    else:
        if args.permissions:
            parser.error("preset permissions cannot be mixed with custom values")
        permissions = [permission(value) for value in PRESETS[args.preset]]

    url = build(args, permissions)

    print(url)
    print()
    print("Permissions:")
    for item in permissions:
        print(f"- {item['key']}:{item['type']}")

    print()
    if args.account_token:
        print("Scope in Cloudflare: select the target account only.")
    else:
        print(f"Requested account scope: {args.account_id}")
        print(f"Requested zone scope: {args.zone_id}")
        print("Narrow these in Cloudflare to the target account and zone when possible.")

    print("Store the created token in Doppler or another secret store; do not print it.")


if __name__ == "__main__":
    main()
