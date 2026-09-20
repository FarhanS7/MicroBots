# Contributing to MicroBots

Current status: MicroBots baseline recovery and milestone execution phase.

## Codebase Structure & Branding

- **Project Name**: MicroBots (`microbots-monorepo`, `microbots-backend`).
- **Python Import Namespace**: Internal Python domain logic uses the `oap` namespace (`services/backend/oap/...`).
- **Repository Setup**: Multi-package repository with Python backend (`services/backend`) and JavaScript/TypeScript workspace packages (`apps/*`, `packages/*`).

## Git Branching & Commit Conventions

- `main`: Production release branch. Protected against unverified direct commits.
- `dev`: Integration branch for verified features and milestone candidates.
- `feature/<module>/<task-slug>`: Feature and task implementation branches created off `dev`.
- `hotfix/<description>`: Emergency fixes branched from `main`, merged to `main` and reconciled into `dev`.

### Commit Message Format

Use Conventional Commits: `type(scope): description`
- Types: `feat`, `fix`, `test`, `refactor`, `docs`, `chore`.
- Examples:
  - `feat(tasks): persist idempotent task submission`
  - `test(tasks): cover duplicate delivery after restart`
  - `fix(policy): reject consumed approval grants`
  - `chore(recovery): reconcile project baseline and decisions`

## Verification & Workflow

- Every task commit must be accompanied by passing unit/integration test evidence.
- Run tests from `services/backend`: `python -m pytest tests/unit/ -v`.
- Public pull requests target `dev` and include test execution logs and descriptions accessible without requiring local plan documents.

## License

MicroBots is distributed under the MIT License.
