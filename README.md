# Python Project Template

Minimal Cookiecutter template for Python 3.12+ projects using uv, ruff, mypy,
and pytest. Pick a variant when generating:

- **`cli`** — a Typer command-line tool (distributed as a wheel / `uv tool install`).
- **`service`** — a long-running, containerized script (e.g. an email poller):
  poll loop with graceful SIGTERM shutdown, a self-contained Docker image, and a
  registry-free `docker save | ssh` deploy task.

Versioning is git-tag based (`hatch-vcs`): the tag is the single source of
truth and `inv bump <part>` creates the next `vX.Y.Z` tag.

## Usage

```bash
cruft create https://github.com/sjev/python-cli-template.git
```

You'll be prompted for `project_type` (`cli` or `service`). The generated
project is git-initialized, tagged `v0.1.0`, and ready to `source init.sh`.

## Development (this template)

```bash
bash test.sh   # renders + lint/tests both variants
```

## License

MIT
