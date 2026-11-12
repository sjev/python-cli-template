#!/usr/bin/env python3
"""Post-generation hook for deterministic project bootstrapping."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_TYPE = "{{ cookiecutter.project_type }}"
PACKAGE = "{{ cookiecutter.package_name }}"
VERSION = "{{ cookiecutter.version }}"

# Files to remove for the variant we did NOT generate.
VARIANT_FILES = {
    "cli": [
        f"src/{PACKAGE}/service.py",
        f"src/{PACKAGE}/__main__.py",
        "tests/test_service.py",
        "Dockerfile",
        ".dockerignore",
        "docker-compose.yml",
        ".env.example",
    ],
    "service": [
        f"src/{PACKAGE}/cli.py",
        "tests/test_cli.py",
    ],
}


def run(*cmd: str) -> None:
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main() -> None:
    if shutil.which("uv") is None:
        print("Error: 'uv' is required but was not found on PATH.", file=sys.stderr)
        sys.exit(1)

    for rel in VARIANT_FILES[PROJECT_TYPE]:
        Path(rel).unlink(missing_ok=True)

    run("git", "init", "-q")
    try:
        run("uv", "lock")  # before committing, so the lockfile lands in the tagged commit
    except subprocess.CalledProcessError as exc:
        print(f"Error: uv lock failed with exit code {exc.returncode}.", file=sys.stderr)
        sys.exit(exc.returncode)

    # Commit + tag so HEAD == tag and hatch-vcs resolves a clean v{VERSION}.
    run("git", "add", "-A")
    run("git", "commit", "-q", "-m", "chore: initial commit from template")
    run("git", "tag", f"v{VERSION}")

    print("\nProject ready (git initialized, tagged v" + VERSION + ").")
    print("Next steps:")
    print("  cd <project_name>")
    print("  source init.sh")


if __name__ == "__main__":
    main()
