# UI Variations

A skill that produces multiple working UI implementations of one feature inside a single HTML comparison file, so a user can compare approaches, pick one, and customize it.

## Language

**Variation**:
One fully working implementation of the feature's UI, built with a distinct layout and interaction model. Mockups do not count.
_Avoid_: Option, mockup, version, design

**Variation axis**:
The pairing of layout and interaction model that makes a variation structurally different from the others (wizard, single-page form, chat, card picker, dashboard split, type-to-fill).
_Avoid_: Theme, style, color scheme

**Single-file comparison page**:
The `index.html` deliverable that embeds all variations as tab panels and explains their differences.
_Avoid_: Mockup gallery, design board

**Tab panel**:
A variation embedded in the comparison page, shown one at a time by the 1–4 tab bar.
_Avoid_: Frame, iframe, subpage

**Functional parity**:
The rule that every variation collects the same information through the same steps and ends at the same success state.
_Avoid_: Equal look

**Variation caption**:
The one-line "what's different about this one" note at the top of each tab panel, so the comparison is understandable without leaving the preview.
_Avoid_: Subtitle, description panel