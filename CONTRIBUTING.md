# Contributing to MicroBots

Current status: MicroBots baseline recovery and milestone execution phase.

## Codebase Structure & Branding

- **Project Name**: MicroBots (`microbots-monorepo`, `microbots-backend`).
- **Python Import Namespace**: Internal Python domain logic uses the `oap` namespace (`services/backend/oap/...`).
- **Repository Setup**: Multi-package repository with Python backend (`services/backend`) and JavaScript/TypeScript workspace packages (`apps/*`, `packages/*`).

## Local Plan Isolation Policy

- All detailed PRD execution roadmaps, completion guides, and internal review context are maintained locally and excluded from Git tracking (`.gitignore`).
- Only `README.md` and `CONTRIBUTING.md` are tracked in the public repository for developer onboarding.
- Public pull requests and issue descriptions must provide self-contained context without referencing local plan paths.

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
- Run unit tests from `services/backend`:
  ```sh
  cd services/backend
  python -m pytest tests/unit/ -v
  ```
- Public pull requests target `dev` and include self-contained test execution logs and descriptions.

## License

MicroBots is distributed under the MIT License.
