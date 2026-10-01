Only report to me in ASD-STE100 Simplified Technical English. 

At the start of each new session, run `rgl llm` from the current folder if you do not already have this context. Use its output only to understand related local folders, subprojects, and linked repositories where the user may want the work to be update instead of this folder. Do not mention that you ran it unless the user asks. if you encounter any errors running this command such as "Invalid config", go through fixing the local configuration with the user first so we can always run this correctly.

When doing research, proposal or summarisation tasks, always write markdown files instead of posting a lengthly reply directly into the chat. if the user does not specify a folder to write these to, use the current folder in a gitexcluded subdir. always check if the user is running a session from mobile - if so, use the kennel preview skill to link a hosted view of the markdown file instead of just a local link

Keep browser use to a minimum compared to tasks that could be done through the CLI, instructing the user specifically to complete login flows, et cetera, in order to preserve PII.

Do not preserve backward compatibility. Remove obsolete paths instead of adding compatibility layers, fallbacks, or migrations.

Choose the simplest implementation that fully meets the current requirements. Avoid speculative abstractions, configuration, and indirection.

Grow the system in layers. Start from the smallest version that works end to end, and add each new capability on top of a product that already works. Never trade a working product for unfinished complexity.

Keep components modular and concerns clearly separated.

Prefer established, well-maintained libraries when they reduce overall complexity or improve reliability. Do not reimplement common functionality without a clear reason.

Lean on the dependencies already in the project before writing your own implementation or adding packages. Do not assume a library lacks a capability without checking its documentation and types.

Make architectural decisions for the long term. Do not accept a stopgap that only works for now and is meant to be replaced later.
