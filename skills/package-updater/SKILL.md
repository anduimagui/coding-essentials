---
name: package-updater
description: "Carry a package change through its complete child-to-parent release pipeline: modify and test a child package repository, version and publish an npm or GitHub-hosted package family, upgrade the freshly released versions in the parent importer repository, and verify the integration. Use when a user asks to change a shared package, CLI, framework, plugin, adapter, or library and prove the released artifact works in an importing repository, including npm registry packages, GitHub Packages, or Git tag/release dependencies."
---

# Package Updater

Move one package change through the child package repository, release channel, and parent importer repository. Treat successful parent verification against the remotely released artifact—not a successful publish command—as the finish line.

Use these terms consistently:

- **Child repository:** owns the source package or related package family and publishes the artifacts.
- **Parent repository:** imports those artifacts and proves the released versions work in the real integration.

## Establish the Release Map

Before editing, identify and report:

- Child repository and package directory, including monorepo workspace when applicable.
- Package name, current version, package manager, lockfile, build command, and test command.
- Release channel: npm registry, GitHub Packages registry, or Git tag/release dependency.
- Release automation and trusted publishing status: workflow file, trigger event, package scope, registry environment, OIDC/provenance settings, and whether a commit or tag causes publication without a manual `npm publish`.
- Downstream update automation: whether the child or parent repository already opens, commits, or applies dependency updates after a successful release.
- Parent repository, dependency declaration, package manager, lockfile, and relevant verification commands.
- Required version bump and release tag/channel such as `latest`, `next`, or a Git tag.
- Authentication and account/organization used for each remote operation.
- Affected-package closure: changed package, internal dependencies it needs, and downstream packages whose manifests or artifacts must be republished.

Inspect repository instructions and working-tree state in both repositories. Preserve unrelated user changes. Read release automation, `package.json`, workspace configuration, registry configuration, trusted publishing configuration, and existing changelog/versioning conventions before choosing commands.

If either repository, package, release channel, or versioning intent cannot be discovered safely, ask only for the missing decision. Do not guess a production package or registry.

## Map a Package Family

Do not assume that a framework change maps to one published package. Build a directed graph from workspace manifests and parent imports:

```text
internal dependency → package containing it → downstream package → parent import or command
```

Classify each affected workspace as:

- **Must publish:** its shipped files or dependency manifest changed.
- **Must bump:** it needs to point at a newly published internal dependency even if its own source did not change.
- **Must verify only:** it is downstream but its existing semver range should resolve the new release without republishing.
- **Local only:** it is not intended for remote consumption; do not invent a release for it.

Publish in topological order, dependencies before dependants. After each publication, make downstream package manifests resolve to the released dependency rather than a workspace or file path, then pack and test the downstream artifact.

## Apply the Child Change

1. Reproduce or characterize the requested behavior in the child.
2. Add or update a focused test that exercises the change when practical.
3. Implement the smallest coherent change.
4. Run the child's relevant tests, type checks, lint, and build.
5. Inspect the packed artifact before publishing.

For npm-compatible packages, prefer the repository's package manager and run the equivalent of:

```bash
npm pack --dry-run
```

Confirm that compiled output, types, exports, and required runtime files are included. Do not rely on unbuilt source unless the package intentionally ships source.

For a package family, inspect every affected tarball independently. Workspace tests can pass while a published tarball is missing a file or refers to an unpublished internal package.

## Choose and Record the Version

Follow the repository's release tooling (for example Changesets, release-please, semantic-release, or workspace version commands) rather than manually competing with it.

If the repository uses trusted publishing, record the version change that the trusted workflow will publish. Do not create a second manual release path. Use local npm checks only to validate metadata and package contents before the workflow runs.

When no policy exists, apply semantic versioning:

- Patch for backward-compatible fixes.
- Minor for backward-compatible functionality.
- Major for breaking API or behavior changes.
- Prerelease for validation that should not become the default stable release.

Update package metadata, lockfiles, and changelog/release notes according to repository conventions. Verify the version does not already exist on the target registry or as the intended Git tag.

## Commit, Push, and Release

Remote writes are part of this workflow only when the user's request includes the end-to-end release. Before the first remote write:

1. Confirm the Git remote, branch, authenticated GitHub identity, registry URL, and package owner/scope.
2. Ensure child checks pass and the diff contains only intended files.
3. Commit and push using the repository's branch and review conventions.
4. Wait for required CI or release automation; fix failures before continuing.
5. If trusted publishing is configured, let the trusted workflow publish from the committed or tagged state. Do not run `npm publish` manually unless the workflow is absent, disabled, or explicitly not the release path.
6. Publish through the established automation when available. Otherwise publish directly with the correct registry and access/tag settings.

For npm-compatible packages, still run manual npm checks before the release path:

```bash
npm whoami
npm view <package> version dist-tags --registry <registry>
npm pack --dry-run
```

Use the repository's package manager for build and test commands. Use npm registry commands to inspect package identity, existing versions, dist-tags, registry source, and packed contents. If a fresh commit or tag will trigger trusted publishing and downstream dependency automation, push the required state, wait for those workflows, and verify their outputs instead of duplicating the update by hand.

For a Git tag/release dependency, push the immutable version tag and create the expected GitHub release if repository convention requires it. For GitHub Packages, confirm `.npmrc`/registry mapping and package scope point to `npm.pkg.github.com`; never print tokens.

Never overwrite an existing release, force-push, reuse a published version, weaken package visibility, or use `--force` without explicit authorization.

## Prove the Release Is Available

Do not update the parent immediately after a publish command. Query the actual release source until the exact version is visible, allowing for registry or workflow propagation.

Verify:

- Package name and exact version or Git tag/commit.
- Expected dist-tag when using a registry.
- Registry/tarball source and integrity metadata where available.
- GitHub Actions/release status when automation performs publication.
- Trusted publishing evidence when used: successful workflow run, intended environment, provenance or OIDC-based publish status, and npm registry visibility for the exact version.
- Downstream update automation result when configured: created pull request, committed dependency bump, or no-op result with a clear reason.

If publication fails, diagnose and repair the child release. Do not substitute a local path, workspace link, tarball, unpublished commit, or cache as proof of release.

## Upgrade the Parent

1. Re-check parent instructions and working-tree state.
2. Update the dependency using the parent's existing package manager.
3. Request the exact released version unless the user explicitly wants a range changed.
4. Commit both manifest and lockfile changes when the parent tracks them.
5. Inspect the lockfile to confirm it resolves from the intended registry or Git tag and exact released artifact.
6. Eliminate misleading local state: ensure no `file:`, `link:`, workspace override, package-manager override, or stale local build is masking the remote package.
7. Use a clean install when feasible, then run focused integration tests followed by the parent's normal checks in proportion to risk.

Exercise the behavior that motivated the release; a generic build alone is insufficient when a focused runtime or API assertion is possible.

## Separate Linked Development from Release Acceptance

Use local `file:`, workspace, or repository links only for the fast development loop between child and parent. Treat them as a different test mode from release acceptance.

For release acceptance:

1. Record the parent's local-link declarations so they can be restored if they are an intentional development convention.
2. Replace every affected link in the dependency closure with an exact released version—not a caret range.
3. Regenerate the parent's canonical lockfile with the canonical package manager.
4. Inspect every affected lockfile entry for a registry tarball URL and integrity value. Absence of a `file:` declaration in the root manifest is not enough; transitive or stale link entries may remain.
5. Remove installed modules or use a clean checkout/sandbox, reinstall from the lockfile, and verify the installed package metadata.
6. Run contract-level tests for the changed surface, then the parent's framework-level generation, validation, build, and runtime smoke tests.

If the parent intentionally keeps local links on its development branch, run registry acceptance in a clean temporary worktree or branch. Preserve the exact-version manifest and lockfile diff as evidence even if the final development configuration is restored.

## Finish the Parent Change

If verification passes, commit and push the parent update when included in the requested workflow, following its branch and review conventions. Wait for required parent CI and resolve failures caused by the update.

Report:

- Child commit and released package version/tag.
- Registry or GitHub release used.
- Parent dependency change and resolved lockfile version/source.
- Child and parent checks run, with results.
- Branches, pull requests, or commits created.
- Any remaining CI, rollout, compatibility, or manual verification risk.

Do not describe the pipeline as complete if the package was only changed, only published, or only installed locally. State the precise stopping point and blocker instead.

## Failure Handling

- If child tests fail, stop before release and fix or report the failure.
- If publish succeeds but availability cannot be verified, preserve the released version and investigate; do not republish it.
- If the parent fails, determine whether the defect is in the package, release artifact, dependency resolution, or parent assumptions.
- If a follow-up child fix is required, create a new version and repeat the release loop; never mutate the existing artifact.
- If the release is breaking or unsafe, do not silently roll back or unpublish. Report impact and obtain authorization for consequential remediation.
