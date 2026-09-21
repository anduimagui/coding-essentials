---
name: package-local-file-link
description: Temporarily replace a published JavaScript package dependency with a local `file:` dependency, test local package changes in the importing project, and restore the original manifest and lockfile state. Use for short local integration tests that must not publish a package version.
---

# Package Local File Link

Test an unpublished local package build in a project, then return the project to its initial dependency state. This is a temporary development test, not release verification.

## Resolve the Two Repositories

Identify:

- The **consumer project** that imports the published package.
- The **package repository** and the exact package directory that owns the dependency name. In a monorepo, do not link the repository root unless it is also the package root.
- The consumer's package manager from its lockfile and `packageManager` field.
- The original dependency section, version specifier, and lockfile state.
- The package build command and the consumer test command that exercises the new function.

Read the applicable repository instructions in both repositories. Inspect both working trees and preserve unrelated changes. If the local package path or dependency name is ambiguous, ask for the missing value instead of linking a likely match.

Confirm that the local package manifest has the same `name` as the consumer dependency. Check its `exports`, `main`, `module`, `types`, and `files` fields to learn whether the consumer needs built output.

## Prepare the Local Package

Install dependencies only when required. Run the package's normal build so the file dependency exposes the same entry points that a published package exposes. If the package has a prepare step that the consumer's install command will run, confirm that it is safe and sufficient.

Do not change the local package version only to make the link work. Do not publish, tag, commit, or push as part of this workflow.

## Record a Restoration Baseline

Before the swap, record the consumer files that the operation can change, normally `package.json` and the active lockfile. Also record whether those files already have user changes. Use a temporary copy or an exact patch outside the repository when a clean Git version cannot restore the initial state.

Never use a broad reset or checkout to restore files. That can remove changes that existed before this task.

## Apply the Temporary File Dependency

Use a `file:` dependency that points to the package directory. Prefer a relative path from the consumer project when it is clear and stable for the test. Keep the dependency in its existing section.

Use the consumer's package manager to update the manifest and lockfile. Common commands are:

```bash
npm install <package-name>@file:<package-path> --save-exact
pnpm add <package-name>@file:<package-path> --save-exact
yarn add <package-name>@file:<package-path> --exact
bun add <package-name>@file:<package-path> --exact
```

Add the package-manager option that preserves the existing dependency section when necessary. Do not switch package managers or create a second lockfile.

Inspect the manifest, lockfile, and installed package after installation. Confirm that:

- The dependency resolves from the intended local directory.
- The installed package name and entry points are correct.
- No unrelated dependency upgrades occurred.
- The runtime does not use an old registry copy from a cache.

If the package manager copies `file:` dependencies instead of reflecting new builds immediately, reinstall or refresh the dependency after each package rebuild.

## Protect the Consumer Repository

If this temporary setup will live inside the consumer project beyond a single short test, add a repository-specific Husky commit guard before doing normal project commits. The purpose is to stop a developer from accidentally committing a local `file:` dependency that only works in their environment and would break or confuse other contributors.

At minimum, require a pre-commit or equivalent `check:commit` step that inspects the consumer `package.json` and fails when the temporary local package link is still present. The failure should clearly tell the developer to replace the local link with the correct published or updated version before committing.

Check for the actual local dependency form used by the project, normally:

- `file:` dependencies
- other local path specifiers that point outside the normal published dependency flow

Do not rely only on memory or manual review. Any commit path that could reach `git commit` in that repository should run this guard first when Husky is part of the project's setup.

## Test the Integration

Run the smallest consumer test that exercises the new function. Then run the relevant type check, build, or broader test command in proportion to the change. A successful install alone is not evidence that the integration works.

When the test fails, determine whether the cause is the package source, missing build output, package exports, dependency resolution, or the consumer. Keep the link only while it is useful for diagnosis.

## Restore the Consumer

Unless the user explicitly asks to keep the link, restore the exact initial manifest and lockfile content, including changes that existed before this task. Then run the package manager's frozen or immutable install mode when available to restore installed dependencies from the original lockfile.

Verify that no affected manifest or lockfile entry contains the temporary `file:` path and that the installed dependency resolves to the original source and version. Remove only temporary artifacts that this workflow created.

Report:

- The package and local package directory used.
- The consumer behavior tested and its result.
- The package build and consumer checks run.
- Whether the original dependency state was fully restored or, at the user's request, the file dependency was left in place.
- Any source changes that remain in either repository.

Do not describe this local test as proof that a packed or published artifact works. Use a release workflow for registry acceptance.
