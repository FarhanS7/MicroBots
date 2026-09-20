"""Public documentation validator for MicroBots repository."""

import sys
from pathlib import Path

REQUIRED_PUBLIC_DOCS = [
    Path("README.md"),
    Path("CONTRIBUTING.md"),
    Path("services/backend/README.md"),
]


def check_public_docs_exist() -> int:
    """Verify all required public documentation files exist."""
    missing = []
    root = Path(__file__).resolve().parent.parent

    for rel_path in REQUIRED_PUBLIC_DOCS:
        full_path = root / rel_path
        if not full_path.exists():
            missing.append(str(rel_path))

    if missing:
        print(f"[ERROR] Missing required public documentation files: {', '.join(missing)}")
        return 1

    print("[SUCCESS] All required public documentation files exist.")
    return 0


def main() -> None:
    code = check_public_docs_exist()
    sys.exit(code)


if __name__ == "__main__":
    main()
