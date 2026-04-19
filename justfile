# Displays available commands.
help:
    @just --list

# Initialize a project. Installs dependencies and pre-commit hooks.
init:
    #!/usr/bin/env bash

    uv python install 3.14
    uv venv --python 3.14
    source .venv/bin/activate && \
      uv sync && \
      pre-commit install
    echo "Project initialized. Dependencies, pre-commit hooks successfully installed."

# Check the project files and fixes them if it is possible.
format:
    ruff format
    ruff check --fix
