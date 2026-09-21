---
name: issue-creator
description: Create repository issues that follow the project's issue templates, maintainer style, labels, and evidence expectations. Use when asked to open, draft, or prepare a GitHub, GitLab, or other hosted repository issue.
---

# Issue Creator

Use this skill to create issues that fit the target repository instead of generic bug reports. Inspect the repository and hosting context before writing.

## Workflow

1. Read repository instructions and identify the active repository root, remote host, and target tracker.
2. Before using hosting CLIs or APIs, follow the repo's identity and direnv requirements. Verify the active git and hosting account.
3. Look for issue templates in the repository, including `.github/ISSUE_TEMPLATE/`, `.github/ISSUE_TEMPLATE.md`, `.gitlab/issue_templates/`, `.gitlab/issue_templates/*.md`, or project-specific equivalents.
4. If a relevant template exists, use its structure, headings, required fields, checkboxes, labels, and placeholder intent. Do not discard sections just because they feel repetitive.
5. If no relevant template exists, inspect recent issues created by maintainers, admins, or core contributors. Match their normal title style, section order, detail level, reproduction format, and metadata conventions.
6. Gather only the evidence needed for a useful issue: observed behavior, expected behavior, reproduction steps, logs with secrets removed, screenshots, version/environment details, affected files, and acceptance criteria.
7. Draft the issue first when the user has not explicitly authorized creating it. Create it only after the requested scope and destination are clear.

## Style Rules

- Respect repository-specific labels, issue types, milestones, projects, and assignee conventions when evidence is available.
- Preserve template wording unless it is clearly a placeholder to be replaced.
- Use concrete facts from the repo, logs, browser, or user-provided context. Do not invent versions, maintainers, labels, or severity.
- If previous maintainer issues are sparse or inconsistent, choose the clearest recent example and state the basis briefly.
- Keep private data out of public issues; redact tokens, customer data, private URLs, and unnecessary personal details.

## Output

For drafts, provide the exact title and body plus any suggested labels or metadata. For created issues, return the issue URL, title, labels or metadata applied, and any verification limits.
