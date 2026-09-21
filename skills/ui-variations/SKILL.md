---
name: ui-variations
description: Build at least four different, fully working UI implementations of one feature inside a single self-contained HTML file, with tabs to flip between them and a section that clearly explains the differences, so the user can compare, pick, and customize. Use when the user asks for UI variations, multiple design options, several implementations of a screen, or when creating an onboarding flow, form, dashboard, landing section, or any new user-facing feature that deserves more than one layout.
---

# UI Variations

Create at least 4 meaningfully different implementations of the same user-facing feature, all embedded in **one self-contained HTML file**. The file has tabs labeled 1, 2, 3, 4 to flip between the working implementations, plus a comparison section that explains exactly how they differ. This lets the user try each one, see the trade-offs, and customize the winner in a single file.

The skill ships with a completed reference test at `examples/dog-onboarding/index.html` — 4 working implementations of a dog app onboarding page in one file. Use it as the template for any feature.

## Rules

1. Always create at least 4 implementations. A variation must differ in layout AND interaction model — not just colors, spacing, or copy. Color-only changes do not count.
2. **Single file by default.** Put every variation in one `index.html`, each as its own tab panel (`<section>`). Only create separate files per variation when the user explicitly asks for it.
3. Functional parity: every variation collects the same information, supports the same steps, and ends at the same success state. The user's data must be equivalent across all four.
4. Standalone and dependency-free: vanilla HTML/CSS/JS only. No build step, no CDN, no frameworks. The file must open directly in a browser by double-click (file:// protocol).
5. A variation is not a mockup — it must actually work: real inputs, navigation between steps, validation, and a completion state.
6. Keep one consistent visual tone across the four variations (same colors, app name, copy voice). The differences being judged are structural, not cosmetic. Note the tone in a code comment so the user can change it once.
7. Scope the code: because all variations share one document, use a unique ID or class prefix per variation (`v1*`, `v2*`, `v3*`, `v4*`) and keep each variation's script in its own IIFE so they never collide.

## The four variation axes

Choose four distinct approaches. Each must use a different layout + interaction model; swap in better-fitting ones when the feature demands it:

1. **Multi-step wizard** — one question group per screen, progress bar, Back/Continue, review step.
2. **Single-page form** — everything on one scrollable page, live preview/summary that updates as you type.
3. **Conversational chat** — messenger-style bubbles, one question at a time, quick-reply chips.
4. **Card/tile picker** — preset profile cards the user picks, then a compact pre-filled editable form.
5. **Dashboard split** — persistent sidebar/tabs with a large working area.
6. **Type-to-fill / command palette** — bare interface driven by an input and autocomplete.

Pick the four that best suit the feature and the user's context (mobile-first? power users? playful brand?).

## Deliverables

Create a `<feature-slug>/` folder (ask where to put it, or follow the repo convention) containing:

- `index.html` — one self-contained file with all of this:
  - Header stating the feature and the job every variation does.
  - A tab bar labeled 1, 2, 3, 4 (with short names) that switches between the embedded variation panels.
  - The four fully working variation panels, each with a one-line **variation caption** at the top that says what's different about that approach (e.g. "One question per screen, 4 steps, progress shown").
  - A "What's different" comparison table **below the preview** — one row per difference axis (layout, interaction model, number of screens, typical time to complete, best for, weak spot), one column per variation.
  - A pros/cons card per variation, directly under the table.
  - A short "How to customize" section: where to change copy, fields, colors, and how to run.
- `README.md` — what this is, how to open it, the difference in one sentence per variation, and what to customize.

If the user asks for separate files, use the same structure but split each variation into `variations/1-<name>.html` etc. and link them in `index.html` on tabs; in that mode, add the height-postMessage snippet from the older example layout if a preview iframe is needed.

The comparison table and pros/cons live below the preview; the page never splits into a side-by-side layout. Each tab panel leads with a one-line caption so context is available without leaving the panel.

## Tabs mechanics (single file)

```html
<div class="tabs" role="tablist">
  <button class="tab active" data-var="1">1 · Wizard</button>
  <button class="tab" data-var="2">2 · Single page</button>
  <button class="tab" data-var="3">3 · Chat</button>
  <button class="tab" data-var="4">4 · Card picker</button>
</div>
```

```js
document.querySelectorAll('.tab').forEach(function (btn) {
  btn.addEventListener('click', function () {
    document.querySelectorAll('.tab').forEach(b => b.classList.toggle('active', b === btn));
    document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
    document.getElementById('var' + btn.dataset.var).classList.add('active');
    document.querySelector('.explore').scrollTop = 0;
  });
});
```

## Example test (dog onboarding)

`examples/dog-onboarding/index.html` is the completed test described in this skill — one file, tabs 1–4:

- Variation 1 — multi-step wizard (account → dog → routine → review)
- Variation 2 — single scroll page with a live profile preview
- Variation 3 — conversational chat with quick-reply chips
- Variation 4 — preset profile cards (Puppy / Active adult / Senior / Build your own)

Open it, click tabs 1–4 to see each one run, then customize: change the app name, copy, fields, and colors in one file and watch all four variations update.

## Output summary

When done, report in a few sentences: the feature name, the four approaches and why they differ, the file path, and how to open it. Do not claim the file works unless you opened it yourself (or asked the user to). If you cannot open a browser, say so.