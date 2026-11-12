FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder
# git lets hatch-vcs resolve the version from the tag in the copied .git.
RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . .
RUN uv build --wheel \
    && uv export --no-dev --frozen --no-emit-project --no-hashes -o requirements.txt

FROM python:3.12-slim AS runtime
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY --from=builder /app/requirements.txt /app/dist/*.whl ./
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir --no-deps *.whl \
    && python -c "import {{ cookiecutter.package_name }}" \
    && rm -f *.whl requirements.txt
USER 1000:1000
ENTRYPOINT ["python", "-m", "{{ cookiecutter.package_name }}"]
