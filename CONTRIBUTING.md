# Contributing to PedagogyX

First off, thank you for considering contributing to PedagogyX! It's people like you that make open source such a great community.

## Project Status

PedagogyX is currently in **Phase 0 + MVP boilerplate**. The cloud API and Meta Ray-Ban Android client path are being built out, and production school data is blocked until we receive legal sign-off (G2). We welcome contributions, particularly in the areas of architecture, documentation, and the boilerplate stack.

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report. Following these guidelines helps maintainers and the community understand your report, reproduce the behavior, and find related issues.

- Check if the bug has already been reported.
- Use the **Bug Report** issue template.
- Include clear steps to reproduce, expected behavior, and your environment.

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion, including completely new features and minor improvements to existing functionality.

- Check if the enhancement has already been requested.
- Use the **Feature Request** issue template.
- Provide a clear and concise description of the problem and your proposed solution.

### Pull Requests

- **Fork** the repository and create your branch from `main`.
- If you've added code that should be tested, **add tests**.
- Ensure your code passes all linters. Run `./scripts/dev-verify.sh --docs-only` for docs and `ruff check` for Python.
- Update documentation (`docs/` or `README.md`) if necessary.
- Issue that pull request! Please use the provided **Pull Request Template**.

## Development Setup

Please refer to [DEVELOPING.md](DEVELOPING.md) for instructions on setting up the local Docker-based MVP boilerplate, as well as linting and benchmarking tools.

## Code Style & Linting

### Markdown

We use `markdownlint-cli` and `prettier` for all markdown documentation.

```bash
# To check
./scripts/dev-verify.sh --docs-only
```

### Python

We use `ruff` (and `black`, `isort`, `flake8` for benchmarks).

```bash
ruff check services tools packages/capture-core/py
```

## Code of Conduct

This project and everyone participating in it is governed by a Code of Conduct (TBD). By participating, you are expected to uphold this code.
