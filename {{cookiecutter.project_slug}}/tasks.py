# type: ignore
from invoke import task

{%- if cookiecutter.project_type == "service" %}

IMAGE = "{{ cookiecutter.project_slug }}"
SERVICE = "{{ cookiecutter.project_slug }}"
VPS = "vps"  # ssh alias; edit to match your ~/.ssh/config
REMOTE_DIR = "~/stack"  # dir on the VPS holding docker-compose.yml
{%- endif %}


@task
def venv(c):
    """Sync dependencies."""
    c.run("uv sync --group dev")


@task
def format(c):
    """Format code."""
    c.run("uv run ruff format src tests")


@task
def lint(c):
    """Run linters."""
    c.run("uv run ruff check src tests")
    c.run("uv run ruff format --check src tests")
    c.run("uv run mypy src")


@task
def test(c):
    """Run tests with coverage."""
    c.run("uv run pytest --cov=src --cov-report=term-missing")


@task
def ci(c):
    """Run lint and tests."""
    lint(c)
    test(c)
    print("All checks passed!")


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

    c.run("git fetch --tags", hide=True)
    major, minor, patch = (int(x) for x in _latest_tag(c).lstrip("v").split("."))
    if part == "major":
        major, minor, patch = major + 1, 0, 0
    elif part == "minor":
        minor, patch = minor + 1, 0
    else:
        patch += 1

    tag = f"v{major}.{minor}.{patch}"
    c.run(f"git tag {tag}")
    c.run(f"git push origin {tag}")
    print(f"Tagged and pushed {tag}.")
{%- if cookiecutter.project_type == "service" %}


def _version(c) -> str:
    return _latest_tag(c).lstrip("v")


@task
def version(c):
    """Print the current version (latest git tag)."""
    print(_version(c))


@task(pre=[ci])
def build_image(c):
    """Build the runtime image tagged as latest."""
    c.run(f"docker build --network=host -t {IMAGE}:latest .")


@task
def deploy(c):
    """Build image, copy to VPS over SSH, then prompt before restarting the compose service."""
    build_image(c)
    print(f"Transferring {IMAGE}:latest to {VPS}...")
    c.run(f"docker save {IMAGE}:latest | ssh {VPS} docker load", pty=True)
    print("Image transferred.")
    answer = input("Restart service on VPS? [y/N] ").strip().lower()
    if answer != "y":
        print("Skipping restart. Image is available on the VPS.")
        return
    c.run(f'ssh {VPS} "cd {REMOTE_DIR} && docker compose down {SERVICE} && docker compose up -d {SERVICE}"')
    print("Service restarted.")
{%- endif %}


@task
def clean(c):
    """Preview files to delete (safe mode)."""
    c.run("git clean -nfdx")
    if input("Delete? [y/N] ").lower() == "y":
        c.run("git clean -fdx")
