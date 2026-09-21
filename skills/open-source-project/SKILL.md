---
name: open-source-project
description: Convert an existing script or code directory into a standard open source project with repository metadata, license, README, gitignore, package configuration, contribution guide, changelog, initial commit, remote repository, and optional package publishing. Use when the user asks to open-source a script, scaffold a publishable Python project, prepare a public GitHub repository, add standard OSS files, or turn a local code folder into a reusable package.
---

# Open Source Project

Use this skill to convert an existing script or code directory into a standard open source project. Prefer concrete project-specific files over generic templates: inspect the code first, infer real entry points and dependencies, then create metadata that accurately describes what exists.

## Prerequisites

Before changing files, identify:

- Existing code file(s) and current directory layout.
- Target project directory and repository root.
- Project name, package/import name, and command name if applicable.
- License type. Default to MIT only if the user has not specified another license and the project context makes a permissive license appropriate.
- Intended author/account and hosting target.

If the user asks for commit, push, repository creation, release, publishing, or any remote-hosting action, follow the repository direnv and identity-verification instructions before running the first relevant command.

## Required Outputs

For a typical Python open source project, create or update:

- `LICENSE`
- `README.md`
- `.gitignore`
- `pyproject.toml`
- `CONTRIBUTING.md`
- `CHANGELOG.md`
- `src/<package>/` package layout when packaging is needed
- `tests/` with at least a smoke test when practical

Only initialize git, commit, create a remote repository, push, tag, release, or publish when the user explicitly asks for that step or when it is clearly part of the requested end-to-end workflow.

## Workflow

1. Inspect the codebase:

   ```bash
   pwd
   rg --files
   git status --short
   ```

   Read the main script/module, any existing README/config, and dependency hints such as imports, requirements files, lockfiles, shebangs, or CLI parsers.

2. Choose the structure:

   - Use `src/<package>/` for a reusable Python package.
   - Keep a single top-level script only for intentionally simple script repos.
   - Add `tests/` for behavior that can be exercised without credentials or external state.
   - Avoid moving user code unless packaging requires it or the user asked for cleanup.

3. Initialize git only if needed:

   ```bash
   git init
   ```

4. Create a license.

   For MIT:

   ```text
   MIT License

   Copyright (c) YEAR AUTHOR

   Permission is hereby granted, free of charge, to any person obtaining a copy
   of this software and associated documentation files (the "Software"), to deal
   in the Software without restriction, including without limitation the rights
   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
   copies of the Software, and to permit persons to whom the Software is
   furnished to do so, subject to the following conditions:

   The above copyright notice and this permission notice shall be included in all
   copies or substantial portions of the Software.

   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
   SOFTWARE.
   ```

   Common alternatives:

   | License | Use Case |
   |---|---|
   | MIT | Permissive, simple default |
   | Apache-2.0 | Permissive with patent grant |
   | BSD-3-Clause | Permissive, similar to MIT |
   | GPL-3.0 | Copyleft; derivatives must remain GPL |

5. Write a real `README.md`.

   Include:

   - Project name and concise description.
   - Features grounded in the actual code.
   - Installation instructions.
   - Usage examples for Python API and/or CLI.
   - Development setup and test commands.
   - License section.
   - Badges only when the linked services exist or are expected to exist immediately.

   Template:

   ````markdown
   # Project Name

   Brief description of what this project does and who it is for.

   ## Features

   - Feature 1
   - Feature 2
   - Feature 3

   ## Installation

   ```bash
   pip install project-name
   ```

   ## Usage

   ```python
   from package import function

   function()
   ```

   Or CLI:

   ```bash
   project-cli --help
   ```

   ## Development

   ```bash
   git clone https://github.com/user/project
   cd project
   python -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   pytest
   ```

   ## License

   MIT - see [LICENSE](LICENSE).
   ````

6. Create `.gitignore`.

   Start with:

   ```gitignore
   # Python
   __pycache__/
   *.py[cod]
   *$py.class
   *.so
   .Python
   build/
   dist/
   *.egg-info/
   .pytest_cache/
   .mypy_cache/
   .ruff_cache/

   # Virtual environments
   venv/
   env/
   .venv/

   # IDE
   .vscode/
   .idea/
   *.swp
   *.swo

   # OS
   .DS_Store
   Thumbs.db

   # Environment
   .env
   .env.local
   ```

   Extend it for project-specific generated files, caches, logs, local databases, credentials, and build outputs. Do not ignore source files or lockfiles blindly.

7. Create `pyproject.toml` for Python projects.

   Use Hatchling unless the existing project clearly uses another build backend:

   ```toml
   [build-system]
   requires = ["hatchling"]
   build-backend = "hatchling.build"

   [project]
   name = "project-name"
   version = "0.1.0"
   description = "Brief description"
   readme = "README.md"
   requires-python = ">=3.10"
   license = {text = "MIT"}
   authors = [{name = "Author Name", email = "author@example.com"}]
   classifiers = [
       "Development Status :: 3 - Alpha",
       "Intended Audience :: Developers",
       "License :: OSI Approved :: MIT License",
       "Programming Language :: Python :: 3.10",
       "Programming Language :: Python :: 3.11",
   ]
   dependencies = []

   [project.optional-dependencies]
   dev = [
       "pytest>=7.0",
       "ruff>=0.1.0",
       "mypy>=1.0",
   ]

   [project.scripts]
   cli-name = "package.module:main"

   [project.urls]
   Homepage = "https://github.com/user/project"
   Repository = "https://github.com/user/project"
   Issues = "https://github.com/user/project/issues"

   [tool.ruff]
   target-version = "py310"
   line-length = 100

   [tool.mypy]
   python_version = "3.10"
   strict = true
   ```

   Remove unused script entries, dependencies, or metadata rather than leaving placeholders.

8. Create `CONTRIBUTING.md`.

   Include setup, test, lint, contribution, and issue-reporting instructions:

   ````markdown
   # Contributing

   Contributions are welcome.

   ## Development Setup

   ```bash
   git clone https://github.com/user/project
   cd project
   python -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   ```

   ## Making Changes

   1. Fork the repository.
   2. Create a feature branch.
   3. Make changes.
   4. Run tests with `pytest`.
   5. Run linting with `ruff check .`.
   6. Commit with a clear message.
   7. Push the branch.
   8. Open a pull request.

   ## Code Style

   - Follow PEP 8.
   - Use type hints where practical.
   - Add docstrings for public APIs.
   - Write tests for new behavior.

   ## Reporting Issues

   Include a clear description, reproduction steps, expected behavior, actual behavior, and environment details.
   ````

9. Create `CHANGELOG.md`.

   Use Keep a Changelog style:

   ````markdown
   # Changelog

   All notable changes to this project will be documented in this file.

   The format is based on [Keep a Changelog](https://keepachangelog.com/),
   and this project follows [Semantic Versioning](https://semver.org/) where practical.

   ## [Unreleased]

   ## [0.1.0] - YYYY-MM-DD

   ### Added

   - Initial release.
   - Core functionality.

   [unreleased]: https://github.com/user/project/compare/v0.1.0...HEAD
   [0.1.0]: https://github.com/user/project/releases/tag/v0.1.0
   ````

10. Verify the local project:

    ```bash
    python -m pip install -e ".[dev]"
    pytest
    ruff check .
    python -m build
    ```

    Run only commands that fit the project and available dependencies. If a command cannot run because tooling is missing or credentials are unavailable, report that explicitly.

11. Commit only when requested.

    Before history-changing or remote actions, load applicable direnv and verify identity. Then inspect scope:

    ```bash
    git status --short
    git diff
    git log -5 --oneline
    ```

    Stage explicit paths only:

    ```bash
    git add -- LICENSE README.md .gitignore pyproject.toml CONTRIBUTING.md CHANGELOG.md src tests
    git commit -m "Initial open source project setup"
    ```

12. Create the GitHub repository only when requested and only after identity checks:

    ```bash
    gh repo create user/project --public --source=. --remote=origin
    git branch -M main
    git push -u origin main
    ```

13. Publish to PyPI only when requested:

    ```bash
    python -m pip install build twine
    python -m build
    twine upload --repository testpypi dist/*
    twine upload dist/*
    ```

    Verify installation afterward:

    ```bash
    pip install project-name
    ```

## Quick Checklist

- [ ] Inspect real code and current repo state.
- [ ] Confirm project name, package name, author, and license.
- [ ] Initialize git if needed.
- [ ] Create `LICENSE`.
- [ ] Create project-specific `README.md`.
- [ ] Create `.gitignore`.
- [ ] Create `pyproject.toml` for Python projects.
- [ ] Create `CONTRIBUTING.md`.
- [ ] Create `CHANGELOG.md`.
- [ ] Add or preserve package layout.
- [ ] Add basic tests where practical.
- [ ] Run relevant tests, lint, and build checks.
- [ ] Commit only requested/relevant paths if asked.
- [ ] Create remote repository if asked.
- [ ] Push to remote if asked.
- [ ] Add badges only for existing or imminent services.

## Best Practices

Do:

- Choose an appropriate license.
- Write a README with actual examples from the project.
- Include installation and development instructions.
- Keep the changelog current.
- Use semantic versioning where practical.
- Add type hints and tests for Python packages.
- Protect secrets and local environment files.

Do not:

- Leave placeholder metadata in public files.
- Include sensitive data, tokens, credentials, private URLs, or local databases.
- Stage unrelated files or generated clutter.
- Commit, push, create repositories, publish packages, or call hosting APIs before direnv/account verification when applicable.
- Add badges that point to nonexistent packages, workflows, or repositories.

## Common File Structure

```text
project/
├── LICENSE
├── README.md
├── .gitignore
├── pyproject.toml
├── CONTRIBUTING.md
├── CHANGELOG.md
├── src/
│   └── package/
│       ├── __init__.py
│       └── module.py
└── tests/
    └── test_module.py
```

## Common Commands

| Task | Command |
|---|---|
| Initialize git | `git init` |
| Create repo | `gh repo create user/project --public --source=. --remote=origin` |
| Initial commit | `git add -- <paths> && git commit -m "Initial open source project setup"` |
| Push | `git push -u origin main` |
| Build | `python -m build` |
| Upload PyPI | `twine upload dist/*` |
| Install editable | `python -m pip install -e ".[dev]"` |
