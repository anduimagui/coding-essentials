---
name: device-parity
description: Verify and fix frontend screens so they preserve visual intent, content hierarchy, and interaction quality across mobile, tablet, and desktop viewports. Use when asked to check responsive design, device parity, mobile/desktop consistency, viewport-specific UI bugs, screenshots that show layout breakage, or frontend QA across multiple screen sizes.
---

# Device Parity

## Overview

Use this skill to make a frontend screen feel like the same product across devices, not merely avoid CSS overflow. Treat parity as preserving hierarchy, affordances, spacing, content visibility, and task completion at each relevant viewport.

## Workflow

1. Inspect the target screen, route, component, and existing styling before changing code. Identify the intended hierarchy and primary action on the largest stable viewport first.
2. Choose a small viewport set that matches the product surface. Default to phone, tablet, and desktop; add narrow or wide extremes only when the issue suggests it.
3. Capture or inspect each viewport on the real running app. Prefer browser automation, screenshots, DOM snapshots, computed layout measurements, and console logs over static code guesses.
4. Compare the same UI elements across viewports:
   - Primary content remains visible and ordered correctly.
   - Headings, buttons, toolbars, controls, media, and cards keep stable proportions.
   - Text does not wrap awkwardly, clip, overlap, or overflow.
   - Tap targets and controls remain usable on touch-sized screens.
   - Decorative elements do not crowd or obscure functional content.
5. Patch the smallest responsive rule that fixes the breakage while preserving the existing design system. Prefer `clamp()`, container widths, grid/flex constraints, aspect ratios, wrapping rules, and breakpoint-local adjustments over duplicated markup.
6. Re-check every viewport affected by the change. Include at least one viewport that previously worked, so the fix does not regress desktop while repairing mobile or vice versa.

## Implementation Rules

- Keep device-specific changes narrow and explain why the breakpoint or fluid value exists.
- Avoid viewport-width font scaling without bounds. Use `clamp()` with readable minimum and maximum values.
- Avoid fixing one device by hiding important content unless the product explicitly has a smaller-screen information hierarchy.
- Do not introduce decorative layout changes while repairing parity unless they are required to preserve the intended composition.
- Prefer semantic and accessible controls at every size; do not make touch targets smaller to force visual fit.
- When the user provides a screenshot, use it as a bug report and verify against the live UI before deciding the patch.

## Verification

Report the viewport sizes tested and the concrete pass condition, such as no horizontal overflow, no overlap, stable primary action visibility, or matching visual hierarchy. Run the package's targeted build, typecheck, or browser test when the repository provides one.
