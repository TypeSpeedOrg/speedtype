# Displays available commands
help:
    @just --list

# Check the project files and fixes them if it is possible
format:
    black .
    ruff format .
    ruff check --fix .
