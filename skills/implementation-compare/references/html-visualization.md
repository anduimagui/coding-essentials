# Inline (non-Mermaid) Visualization

Default to Mermaid. Consider an inline visualization only when Mermaid cannot carry the comparison:

- **Interaction helps**: toggling between options, hovering for detail, or filtering by dimension.
- **Spatial/timing fidelity matters**: real physical topology, timing bars, or a side-by-side layout where left-right position encodes meaning.

Do not switch to an inline format just to add color or icons.

## Follow the loaded contract

If the runtime exposes an inline visualization capability (HTML/JS, canvas, a UI component, or another loaded tool), use whatever contract it actually provides. Do not invent a standalone HTML scaffold; read the capability you have and render through it.

If no inline capability is available, or its contract is unknown, use Mermaid.

## Constraints that apply to any inline artifact

- Keep the comparison on one screenful; avoid scroll-heavy artifacts.
- Pairs of components/options placed side by side must preserve the real relationship (caller left, callee right) — do not wrap arbitrarily.
- Carry the same requirements as the Mermaid guide: mark the recommended option literally `RECOMMENDED` (only when it passes every hard constraint and no shown failure path, assumption, or unknown can violate one — self-audit before final output), mark options that fail a hard constraint `INVALID`, mark options with an unresolved hard-constraint gate `UNPROVEN`, both with the failed/affected constraint, show the deciding constraint, and include each option's failure/recovery path.

## When to fall back

If the interactive or spatial need evaporates as you write it, delete the inline artifact and use a Mermaid block. Prefer the simplest artifact that makes the difference visible.
