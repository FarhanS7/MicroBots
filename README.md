# MicroBots

MicroBots is an open-source platform for persistent AI workers that execute models, shell tools, web browsers, and file workflows under user-controlled permission policies.

> **Project Baseline & Status (Audit Revision: `fcff5bf`)**
> MicroBots is currently undergoing foundational recovery and milestone implementation. 
> Core backend schemas and unit tests (153/153 passing) are established; full application composition, worker execution, and client integration are being actively implemented across Milestones M0–M8.

## System Architecture & Technical Choices

- **Core Backend**: FastAPI (Python 3.12+ / 3.13) with `oap` internal domain package namespace.
- **Workflow & Persistence**: PostgreSQL (Alembic migrations) with Temporal workflow orchestration.
- **Client Interfaces**: Web dashboard and Desktop shell (React/TypeScript monorepo).
- **Supported Platforms**: Windows 10/11, macOS 12+, Linux (Ubuntu 22.04+).
- **Resource & Retention Defaults**: 30-day artifact retention, 14-day execution log retention, 7-day outbox event retention. Default per-run evaluation budget cap set to $5.00 / 100k tokens.

## Capabilities Overview

- **Persistent AI Workers**: Run long-running tasks asynchronously across web, desktop, and background workers.
- **Provider Neutral**: Connect local models (Ollama, llama.cpp, vLLM) or API providers (OpenAI, Anthropic, Google, xAI).
- **Sandboxed Execution**: Isolated Docker execution environments for terminal tools and automated browser journeys.
- **Human Authority**: Strict human-in-the-loop permission and approval controls.

## Development & Onboarding

- [Contribution Guidelines](CONTRIBUTING.md)

*Note: Public onboarding and contribution workflows operate independently without requiring local execution plans.*

## License

MIT License.
