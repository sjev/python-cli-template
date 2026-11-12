# Versioning

## How it works

Version is derived from **git tags** — no version string is stored in source files.

- `pyproject.toml` sets `dynamic = ["version"]` and uses `hatch-vcs` to read the nearest `vX.Y.Z` git tag.
- `local_scheme = "no-local-version"` strips the `+d<hash>` local suffix so versions stay clean everywhere.
- At runtime, `__version__` is populated via `importlib.metadata`, falling back to `"0.0.0"` if uninstalled.

---

## Setup

### pyproject.toml

```toml
[project]
dynamic = ["version"]

[build-system]
requires = ["hatchling", "hatch-vcs"]
build-backend = "hatchling.build"

[tool.hatch.version]
source = "vcs"

[tool.hatch.version.raw-options]
local_scheme = "no-local-version"
```

### src/<package>/__init__.py

```python
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("your-package-name")
except PackageNotFoundError:
    __version__ = "0.0.0"
```

### tasks.py (invoke)

```python
def _latest_tag(c) -> str:
    result = c.run("git describe --tags --abbrev=0", hide=True, warn=True)
    return result.stdout.strip() if result.ok else "v0.0.0"


@task(help={"part": "patch, minor, or major"})
def bump(c, part):
    """Tag a new semver release (git tag is the source of truth)."""
    if part not in ("patch", "minor", "major"):
        raise SystemExit("Usage: inv bump <patch|minor|major>")

    if c.run("git status --porcelain", hide=True).stdout.strip():
        raise SystemExit("Working tree is dirty. Commit or stash changes first.")

    major, minor, patch = (int(x) for x in _latest_tag(c).lstrip("v").split("."))
    if part == "major":
        major, minor, patch = major + 1, 0, 0
    elif part == "minor":
        minor, patch = minor + 1, 0
    else:
        patch += 1

    tag = f"v{major}.{minor}.{patch}"
    c.run(f"git tag {tag}")
    print(f"Tagged {tag}. Push it with: git push origin {tag}")
```

---

## Tagging a release

```sh
inv bump patch   # 1.2.3 → 1.2.4
inv bump minor   # 1.2.3 → 1.3.0
inv bump major   # 1.2.3 → 2.0.0
git push origin v1.2.4   # push explicitly after bump
```

The `bump` task requires a clean working tree, reads the latest tag, creates the next one locally, and prints the push command. You push explicitly.

---

## Migrating an existing repo

1. Remove any hardcoded `version = "x.y.z"` from `pyproject.toml`.
2. Apply the `pyproject.toml`, `__init__.py`, and `tasks.py` snippets above.
3. Create an initial tag if none exists: `git tag v0.1.0`.
4. Reinstall the package (`uv sync`) so `importlib.metadata` picks up the new version source.
