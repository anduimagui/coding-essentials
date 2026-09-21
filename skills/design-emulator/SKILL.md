---
name: design-emulator
description: Match an application's UI to a supplied screenshot, mockup, or code-identified design reference through iterative visual comparison, implementation, and verification. Use when the user asks to emulate, approximate, recreate, or make a screen look like a reference design.
---

# Design Emulator

Use this skill when a user provides a screenshot, image, mockup, live page, or specific design in the codebase and asks the agent to make the current application closely match it.

The goal is not blind copying. Adapt the reference to the current product's real content, components, routes, and constraints while preserving the reference's visible design qualities: layout, hierarchy, spacing, density, typography, color relationships, media treatment, controls, and responsive behavior.

## Workflow

1. Identify the target surface in the current app: route, component, state, viewport, and existing design system.
2. Inspect the reference carefully. Extract concrete design traits: grid, section order, scale, alignment, whitespace, type sizes, weight, radius, shadows, color roles, image treatment, icons, controls, and interaction states.
3. Separate transferable traits from context-specific content. Keep the current app's domain, copy, data model, accessibility, and user flow unless the user explicitly asks to change them.
4. Capture the current UI in the same viewport as the reference when possible. Use browser automation or app screenshots instead of judging from code alone.
5. Implement the smallest complete pass that moves the UI toward the reference. Prefer existing components, tokens, icons, and libraries already in the project.
6. Recapture and compare. Repeat focused passes until the important visual differences are resolved or the remaining gaps are blocked by missing assets, product constraints, or unclear user intent.
7. Verify mobile and desktop behavior when the reference implies responsive design or when the changed surface is user-facing across devices.

## Similarity Tools

Use image metrics as diagnostics, not as the final definition of success.

- Use Playwright screenshots to capture stable current-state images at fixed viewport sizes and device scale.
- Use `pixelmatch`, `looks-same`, `resemblejs`, or `odiff` when exact or near-exact visual regression comparison is useful.
- Use SSIM or MS-SSIM for structural similarity across layout, luminance, and contrast when exact pixels differ.
- Use LPIPS when perceptual closeness matters more than pixel equality.
- Use CLIP or SigLIP image embeddings for coarse semantic or style similarity, but do not rely on them for spacing, typography, or alignment.
- Use OpenCV for practical preprocessing: crop the relevant region, align screenshots, mask dynamic content, compare color histograms, detect edges, or measure bounding boxes.

Prefer a simple local comparison script only when it will speed iteration. Do not add new dependencies solely for scoring unless the score changes the implementation decisions.

## Matching Criteria

Judge closeness by visible product quality:

- Primary content and actions occupy similar positions and visual priority.
- Section rhythm, grid, and alignment resemble the reference at the target viewport.
- Type scale, line length, weight, and contrast feel close.
- Color roles match the reference without forcing an incompatible brand palette.
- Images, icons, cards, controls, dividers, radius, and shadows follow the same visual language.
- Text fits, controls remain usable, and accessible labels and focus states still work.

When the reference is a landing page, preserve the reference's composition and first-viewport impact while replacing content with the current product's domain-specific message. When the reference is an app screen, prioritize task flow, density, and controls over decorative similarity.

## Boundaries

- Do not copy proprietary logos, images, exact brand identity, or distinctive content from the reference unless the user owns it or explicitly supplied it for reuse.
- Do not replace a working app architecture with a parallel static mockup.
- Do not add compatibility layers or obsolete paths while making design changes.
- Do not chase perfect pixel equality when fonts, assets, data, or viewport conditions differ. Explain the remaining gap instead.
- Do not expand into a full redesign unless the user asks for broad design emulation.

## Output

After implementation, report the reference used, the main design traits matched, files changed, and verification performed. Include screenshot or metric artifacts when they help the user judge the result.
