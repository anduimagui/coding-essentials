---
name: custom-dev-port
description: Assign, update, and verify a stable uncommon localhost port for a browser development server. Use when a user wants a local app to avoid common default ports or to have a project-specific local URL.
---

# Custom Dev Port

Give the browser development server one stable, uncommon localhost port. Keep the change limited to the browser server unless the user also asks to change API, bridge, database, or test service ports.

## Find the active configuration

1. Inspect the package scripts and development server configuration.
2. Search the project for the current port, `localhost`, `127.0.0.1`, and environment variables that can override the port.
3. Identify which port serves the browser UI. Do not assume that the first port found is the correct one.

## Select the port

- Prefer a memorable project-specific port from `20000` through `49151`.
- Do not use common framework defaults such as `3000`, `4200`, `5000`, `5173`, `8000`, or `8080`.
- Search nearby repositories or workspace configuration when they can run at the same time. Do not select a port already assigned to another local project.
- Check listeners on both IPv4 and IPv6 before selection, for example with `lsof -nP -iTCP:<port> -sTCP:LISTEN`.
- If the port has a listener, inspect the owning process. A running instance of the current project can be valid and can reload after the configuration change. An unrelated process is a conflict.
- Use one fixed port. Do not add a random-port fallback when the user wants a stable URL.

## Configure the server

- Bind to `localhost` unless access from another device is an explicit requirement.
- Enable the framework's strict-port option so that it does not silently move to a different port.
- Keep one source of truth when the framework supports it. Update required scripts, environment examples, tests, and documentation that contain the old browser port.
- Remove obsolete browser-port paths. Do not keep compatibility aliases or fallback ports.

## Verify

1. Start the normal development command, or use an already running instance of the same project after it reloads.
2. Confirm that the expected process listens on the selected port.
3. Request the exact URL, such as `http://localhost:<port>/`, and require a successful response.
4. Confirm that the app page is the expected app, not another service on that port.
5. Run the project's relevant type checks, tests, or build checks.
6. If browser control is available and the user asks to open or test the app, open the exact URL and test one safe end-to-end interaction. Use a local demo mode when this avoids an unnecessary external request.

Report the verified clickable URL and the checks that passed. If startup fails, report the actual conflict or error. Do not claim that the app runs from configuration inspection alone.
