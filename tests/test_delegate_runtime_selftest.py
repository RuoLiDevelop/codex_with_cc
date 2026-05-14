#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]


def test_delegate_runtime_selftest_script_passes() -> None:
    if os.name == "nt":
        command = [
            "pwsh",
            "-NoProfile",
            "-File",
            str(REPO / "skills" / "codex-with-cc" / "windows_scripts" / "test_delegate_runtime.ps1"),
        ]
    else:
        command = [str(REPO / "skills" / "codex-with-cc" / "macos_scripts" / "test_delegate_runtime.sh")]

    result = subprocess.run(command, cwd=REPO, text=True, capture_output=True)

    assert result.returncode == 0, result.stdout + result.stderr
