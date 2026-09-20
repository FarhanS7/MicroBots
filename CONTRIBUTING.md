# Contributing to Open Agent Platform

Current status: planning only. No application startup command works yet; see [the planning guide](docs/README.md). The project intends MIT licensing; actual copyright holder and public GitHub owner remain to be confirmed before publication.

## Understand and choose work

Read ARCHITECTURE.md and the task index. Pick a ready task with completed prerequisites. Discuss architecture/scope changes in a decision record before implementation. Contributors need not install the author's personal skills: the portable task and phase commands contain required workflow behavior.

## Branches and commits

- `main`: production releases, protected; `dev`: integration, protected once remote exists.
- `feature/<module>/<task-slug>`: one task, from dev, reviewed PR back to dev.
- `hotfix/<description>`: from main, reviewed fix promoted to main and separately reconciled into dev.
- One independently verified subtask per commit, tests included. One review fix per fix commit. Stage explicit paths and inspect the diff; never commit secrets, runtime data, browser cookies, keys, or generated dependency folders.
- Format `type(scope): description`; types `feat`, `fix`, `test`, `refactor`, `docs`, `chore`. Body explains why and references task ID.
- Examples: `feat(tasks): persist idempotent task submission`; `test(tasks): cover duplicate delivery after restart`; `fix(policy): reject consumed approval grants`; `docs(tasks): record F14 review evidence`.

Initial Git bootstrap (only when there is no existing repository):

```sh
git init -b main
git commit --allow-empty -m "chore(repo): establish release baseline"
git switch -c dev
git switch -c feature/foundation/git-community-bootstrap
```

This empty baseline is the sole initialization exception to main's no-direct-commit rule. Do not invent user.name/user.email or alter global Git identity. In existing repositories inspect history and remotes instead.

## Verification and review

Use the task's focused checks plus [verification contract](docs/architecture/verification.md). Every public behavior has happy, error and relevant concurrency/security coverage. Independent review uses the [review command](docs/commands/phase-2.5-review.md), followed by an owner walkthrough. A clean test run is not independent review. Record review evidence even when working solo; a GitHub PR author cannot approve their own PR.

Use merge commits to preserve verified subtask history. Required checks and unresolved critical/high findings block merge. Feature implementation and unrelated cleanup belong in different PRs. Keep public descriptions readable without access to this conversation.

## Public project setup plan

F02 creates README, LICENSE, SECURITY.md, CODE_OF_CONDUCT.md, issue templates and PR template once owner details are known. SECURITY must provide a real private reporting route before the repository advertises one. Use GitHub private vulnerability reporting if available/configured; never invent a maintainer email. Preserve upstream licenses for vendored skill collections; they are not automatically first-party project code.

Bug reports include version, deployment mode, sanitized reproduction, expected/actual outcome and relevant trace IDs. Feature proposals link PRD section and explain value, scope and acceptance. Label beginner-friendly tasks only when prerequisites and setup are clear. PRs link task ID, tests, independent review, migration and rollback details.

## Publication boundary

This plan does not initialize Git, create a remote, push files, or publish a release. When the owner authorizes publication, inspect staged content and configure the chosen repository deliberately. Public issue/PR text must exclude credentials, private task content and unpublished vulnerability details.
