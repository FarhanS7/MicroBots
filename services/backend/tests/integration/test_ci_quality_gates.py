"""Integration test verifying CI quality gate scripts and verification rules."""

import subprocess
import sys
from pathlib import Path


def test_docs_check_script_executes_successfully() -> None:
    # Path: services/backend/tests/integration/test_ci_quality_gates.py -> 5 parents up to repo root
    root = Path(__file__).resolve().parents[4]
    script_path = root / "scripts" / "check_docs.py"
    result = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True, cwd=str(root))
    assert result.returncode == 0
    assert "[SUCCESS]" in result.stdout
