# MicroBots Backend Service

The MicroBots backend provides core FastAPI REST endpoints, database persistence (SQLAlchemy + Alembic), and Temporal worker execution pipelines under the `oap` domain package.

## Package & Tooling Matrix

- **Python Version**: `>=3.12` (Tested on Python 3.12 and 3.13)
- **Build Backend**: Hatchling (`hatchling.build`)
- **Package Name**: `microbots-backend` (Imports as `oap`)
- **Frameworks**: FastAPI, Pydantic v2, SQLAlchemy 2.0 (AsyncPG), Alembic, Temporal IO SDK

## Installation & Local Development

Install backend in editable mode with development dependencies:

```sh
cd services/backend
pip install -e ".[dev]"
```

## Running Unit Tests

Run the test suite using pytest:

```sh
python -m pytest tests/unit/ -v
```
