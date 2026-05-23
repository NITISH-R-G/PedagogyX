# Maintenance Report 02

## Repository Health Report

**Strengths:**

- Existing python linter dependencies added in Maintenance Report 01 to `benchmarks/requirements-bench.txt`.
- Existing robust structure around docker-compose environments (`infra/compose.dev.yaml`).
- Strict lint checks for markdown documentation leveraging markdownlint-cli and prettier.

**Weaknesses:**

- `dev-verify.sh` assumes `black`, `isort`, and `flake8` are installed on `$PATH`, ignoring the local python virtual environment `benchmarks/.venv/bin/` if it exists.
- The `dev-verify.sh` script currently will swallow missing command issues by redirecting errors for checking the existence of tools to `/dev/null`. Specifically, `flake8` might fail without halting the execution if it isn't part of a properly orchestrated tool chain.
- No systematic way to enforce formatting across markdown files uniformly.

**Risks:**

- CI/CD checks for python could run globally installed versions of black/flake8, conflicting with versions mandated in `requirements-bench.txt`.
- Unformatted markdown files could be merged because formatting is not universally enforced.

**Opportunities:**

- Use the virtual environment specifically configured in `benchmarks/.venv` to run `flake8`, `isort`, and `black` inside `dev-verify.sh`, ensuring consistent formatting.
- Auto-format all markdown files through `npx prettier --write` to maintain clean code and standardize format.

## Competitor Analysis

**Repositories Analyzed:**

- Supabase
- Cal.com
- Next.js AI templates

**Advantages Discovered:**

- Hard constraints on virtual environment paths for executing python scripts in node/monorepo infrastructures.
- Comprehensive enforcement of formatting using pre-commit hooks and explicit script definitions.

**Gaps Identified:**

- PedagogyX relies on whatever lint tool is first in the `$PATH` globally when running `dev-verify.sh`.

**Opportunities to Outperform:**

- We can implement smart resolution to prefer the local virtual environment for linters (`benchmarks/.venv/bin/`) when available, providing more consistent local development experience while gracefully falling back to global for pure CI environments if needed.

## Priority Improvements

1. Update `./scripts/dev-verify.sh` to explicitly prioritize python linters (`black`, `isort`, `flake8`) from `benchmarks/.venv/bin/`.
2. Format all markdown documentation correctly utilizing `prettier --write`.

## Sprint Plan

**Sprint Goal:** Ensure rock-solid tooling resolution for python linters and auto-format all markdown files for consistency.

**Tasks:**

- Create `docs/11-maintenance/MAINTENANCE_REPORT_02.md`.
- Refactor python linting blocks in `scripts/dev-verify.sh` to check for linters in `benchmarks/.venv/bin/` before using system-wide tools.
- Run `npx prettier --write '**/*.md'` to enforce markdown uniformity.
- Validate that the dev verify scripts still run perfectly locally.

**Implementation Roadmap:**

- Adjust `scripts/dev-verify.sh`.
- Execute markdown formatting.
- Validate through `./scripts/dev-verify.sh`.

**Expected Outcomes:**

- No version conflicts when testing python benchmarking scripts.
- Consistent documentation styling throughout the repository.

## Technical Improvements

- **DevOps/Testing:** Hardened `dev-verify.sh` to prioritize local dependencies over global dependencies.
- **Documentation:** All documentation fully linted and automatically formatted with standard styling tools.
- **Maintenance:** Drafted continuous improvement maintenance log 02.

## Metrics Improved

- **Developer Productivity:** By resolving tooling correctly to `.venv`, developers no longer suffer from mismatched linting rules between different machines or system configurations.
- **Code Quality Gains:** Markdown files fully formatted.
