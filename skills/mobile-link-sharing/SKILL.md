---
name: mobile-link-sharing
description: Make a local web server available to a phone or another device through a LAN address, Tailscale, or a Cloudflare tunnel. Use when the user asks to open a local site, preview, or development server on another device. This skill is not specific to one server product.
---

# Mobile Link Sharing

Share an existing local HTTP server with another device. Keep the server command and the served content unchanged unless a network bind change is necessary.

## Select the access method

- Use a private LAN address by default when both devices are on the same local network.
- Use Tailscale only when the user asks for it or when both devices already use the same tailnet.
- Use a Cloudflare Quick Tunnel when the user asks for Cloudflare or needs access from outside the local network.
- Use `127.0.0.1` or `localhost` only on the computer that runs the server. These addresses do not give phone access.

Do not use a public tunnel for sensitive content unless the user accepts the exposure. A Cloudflare Quick Tunnel is public and has no access control. Use a named Cloudflare Tunnel with Cloudflare Access when authentication is necessary.

## LAN access

1. Find the exact server port.
2. Make sure that the server listens on `0.0.0.0` or on the computer's private LAN address. A server that listens only on `127.0.0.1` cannot accept a connection from another device.
3. Find the active private LAN address, such as `192.168.x.x` or `10.x.x.x`.
4. Build the link as `http://<lan-address>:<port>/`.
5. Keep both devices on the same local network.

Do not expose a folder or service with a larger scope than the user selected. Check the macOS firewall if the server listens correctly but the other device cannot connect.

## Tailscale access

1. Confirm that Tailscale is active on both devices and that both devices use the same tailnet.
2. Use the current Tailscale IP or MagicDNS host.
3. If Tailscale Serve is available and suitable, use its HTTPS URL. Otherwise, use `http://<tailscale-address>:<port>/` with a server that accepts the Tailscale interface connection.
4. Do not describe Tailscale access as public.

## Cloudflare Quick Tunnel

1. Confirm that `cloudflared` is available with `command -v cloudflared`.
2. Keep the local server running on a known port. A loopback listener is sufficient for this method.
3. Start this command in a persistent terminal session:

   ```bash
   cloudflared tunnel --url http://127.0.0.1:<port> --no-autoupdate
   ```

4. Read the command output and use the exact HTTPS `trycloudflare.com` URL that it prints.
5. Keep both the local server and `cloudflared` running. The public link stops when either process stops.

## Verify the link

Test the final URL before you return it:

```bash
curl -fsSI --connect-timeout 3 --max-time 5 "<url>/"
```

Also test one expected page or API route when the root response is not sufficient. Confirm these facts:

- The response is successful.
- The page or service is the one that the user selected.
- A mobile link does not contain `localhost` or `127.0.0.1`.
- A Cloudflare link uses the exact HTTPS host that `cloudflared` printed.

Do not return an unverified link. If the check fails, inspect the listener address, port, selected network address, and firewall rule. Correct the cause and test again.

## Report and stop

Lead with one clickable link. State which access method is active and any important condition:

- For LAN access, state that both devices must use the same local network.
- For Tailscale, state that both devices must use the same tailnet.
- For a Cloudflare Quick Tunnel, state that the link is public and temporary.

State that the server must continue to run. When the user asks you to stop sharing, stop only the exact process or terminal session that this workflow started. Do not stop unrelated listeners.
