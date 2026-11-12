#!/bin/bash

set -euo pipefail

TEMPLATE_DIR="$(cd "$(dirname "$0")" && pwd)"
BUILD_DIR="$TEMPLATE_DIR/build"

echo "Removing old build dir..."
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

run_variant() {
    local type="$1"
    local slug="demo-$type"

    echo
    echo "=== Generating '$type' variant ==="
    cd "$BUILD_DIR"
    cookiecutter "$TEMPLATE_DIR" \
        --no-input \
        project_name="Demo $type" \
        project_slug="$slug" \
        package_name="demo_$type" \
        description="A demo $type project" \
        project_type="$type" \
        author_name="Test Author" \
        author_email="test@example.com" \
        version="0.1.0"

    cd "$BUILD_DIR/$slug"
    echo "Generated at: $(pwd)"

    echo "Running init.sh..."
    # shellcheck disable=SC1091
    source init.sh

    echo "Running lint..."
    uv run invoke lint

    echo "Running tests..."
    uv run invoke test
}

run_variant cli
run_variant service

echo
echo "All checks passed for both variants."
