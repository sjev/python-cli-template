# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

## Installation

```bash
source init.sh
```

## Usage

{%- if cookiecutter.project_type == "cli" %}
```bash
{{ cookiecutter.project_slug }} --help
{{ cookiecutter.project_slug }} hello
```
{%- else %}
```bash
python -m {{ cookiecutter.package_name }}          # run the poller loop
python -m {{ cookiecutter.package_name }} --once   # single cycle (cron/tests)
```

Configuration is read from the environment (`LOG_LEVEL`, `POLL_INTERVAL`); see
`.env.example`. Put the polling/handling logic in `poll_once` / `handle` in
`src/{{ cookiecutter.package_name }}/service.py`.
{%- endif %}

## Development

```bash
uv run invoke lint
uv run invoke test
uv run invoke format
uv run invoke ci     # lint + test
```

## Versioning

The git tag is the single source of truth (via `hatch-vcs`); the version is
derived at build time — never edited in `pyproject.toml`.

```bash
uv run invoke bump patch   # creates tag vX.Y.Z
git push origin vX.Y.Z
```
{%- if cookiecutter.project_type == "service" %}

## Deployment

Ships a self-contained image; no registry required — the image is copied to the
target over SSH.

```bash
uv run invoke build-image   # build {{ cookiecutter.project_slug }}:<version>
uv run invoke deploy        # build + docker save | ssh + restart compose
```

Edit `VPS`, `REMOTE_DIR`, and `SERVICE` constants in `tasks.py` and the
`docker-compose.yml` on the target host to match your setup.
{%- endif %}
