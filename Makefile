.PHONY: install dev test lint format typecheck check

install:
	cd backend && uv sync

dev:
	cd backend && uv run fastapi dev app/main.py

test:
	cd backend && uv run pytest

lint:
	cd backend && uv run ruff check .

format:
	cd backend && uv run ruff check . --fix
	cd backend && uv run ruff format .

typecheck:
	cd backend && uv run mypy app

check:
	cd backend && uv run ruff check .
	cd backend && uv run ruff format --check .
	cd backend && uv run mypy app
	cd backend && uv run pytest
