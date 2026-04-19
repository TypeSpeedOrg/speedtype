# Displays available commands
help:
    @just --list

# Check the project files and fixes them if it is possible
format:
    ruff format .
    ruff check --fix .
