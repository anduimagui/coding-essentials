---
name: pull-request-creator
description: Create pull requests for only the changes made in the current work session while following the project's pull request template, maintainer style, branch workflow, and verification expectations. Use when asked to open, draft, or prepare a pull request.
---

# Pull Request Creator

Use this skill to prepare pull requests for only the work from the current work session. Preserve unrelated worktree changes and commits. Base the PR on the repository's real conventions, not a generic summary format.

## Session Scope

The PR branch, commits, diff, title, and body must contain only changes made in the current work session. Exclude unrelated modified or untracked files, staged changes, and commits from other sessions or user work. Do not alter, stage, commit, push, or describe unrelated work.

## Workflow

1. Read repository instructions and identify the active repository root, target branch, remote host, and intended PR destination.
2. Before commits, pushes, hosting CLIs, or APIs, follow the repo's identity and direnv requirements. Verify the active git and hosting account.
3. Inspect the current branch, worktree, staged changes, recent commits, and diff. Identify the exact files and commits from the current work session. Confirm that the PR branch contains no unrelated commits before publishing it.
4. Look for pull request templates in the repository, including `.github/pull_request_template.md`, `.github/PULL_REQUEST_TEMPLATE.md`, `.github/PULL_REQUEST_TEMPLATE/`, `.gitlab/merge_request_templates/`, or project-specific equivalents.
5. If a relevant template exists, use its structure, headings, checkboxes, required links, testing section, screenshots section, risk section, and release-note expectations. Preserve required sections even when the answer is "not applicable."
6. If no relevant template exists, inspect recent pull requests or merge requests created by maintainers, admins, or core contributors. Match their title style, description shape, testing notes, checklist usage, linking style, and draft/ready conventions.
7. Confirm the PR includes accurate change scope, linked issues, user-visible behavior, test results, deployment notes, screenshots when relevant, and known follow-ups.
8. Open the PR only when the user has asked for creation or publishing. Otherwise provide a ready-to-use title and body.

## Style Rules

- Do not claim tests, screenshots, migrations, release notes, or issue links that were not actually checked.
- Keep unrelated local changes out of the PR description and out of staged or pushed changes.
- Use the repository's normal labels, reviewers, draft status, milestone, and project metadata only when evidence supports them.
- Redact secrets, private URLs, and unnecessary personal data from public PR content.
- If maintainers use a terse style, stay terse; if they use detailed sections, provide comparable detail.

## Output

For drafts, provide the exact title, body, and suggested metadata. For created PRs, return the PR URL, target branch, draft status, and verification performed.
