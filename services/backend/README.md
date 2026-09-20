# MicroBots Backend Service

The MicroBots backend provides core FastAPI REST endpoints, database persistence (SQLAlchemy + Alembic), and Temporal worker execution pipelines under the `oap` domain package.

## Package & Tooling Matrix

- **Python Version**: `>=3.12` (Tested on Python 3.12 and Python 3.13.5)
- **Build Backend**: Hatchling (`hatchling.build`)
- **Package Name**: `microbots-backend` (Imports as `oap`)
- **Frameworks**: FastAPI, Pydantic v2, SQLAlchemy 2.0 (AsyncPG), Alembic, Temporal IO SDK

## Installation & Local Development

Install backend in editable mode with development dependencies:

```sh
cd services/backend
pip install -e ".[dev]"
```

## Environment Configuration

Environment settings are configured via environment variables or a local `.env` file based on `.env.example`:

```sh
cp .env.example .env
```

## Running Unit Tests & Verification

Run the full unit test suite:

```sh
python -m pytest tests/unit/ -v
```

Verify editable package imports outside the source tree:

```sh
python -c "import oap; print(oap.__name__)"
```
