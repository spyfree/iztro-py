# Repository Guidelines

## Project Structure & Module Organization
- `src/iztro_py/` — library source (public API re-exported in `src/iztro_py/__init__.py`).
  - `astro/` (chart creation: `by_solar`, `by_lunar`), `star/`, `utils/`, `i18n/`, `data/`.
- `tests/` — pytest suite (`test_*.py`).
- `examples/` — runnable scripts (e.g., `examples/basic_usage.py`).
- `dist/` — build artifacts (do not edit).

## Build, Test, and Development Commands
- Setup dev env: `pip install -e ".[dev]"`
- Run tests: `pytest -q`
- Coverage: `pytest --cov=src/iztro_py --cov-report=term-missing`
- Lint: `ruff check .` (auto-fix: `ruff --fix .`)
- Format: `black src tests`
- Type check: `mypy src`
- Build package: `pip install build twine && python -m build` (then `twine check dist/*`)

## Coding Style & Naming Conventions
- Python 3.8+; 4-space indent; prefer type hints for all public APIs.
- Formatting: Black with line length 100 (see `pyproject.toml`).
- Lint: Ruff (same line length); fix or justify all warnings.
- Names: modules/files `snake_case`, functions `snake_case`, classes `CamelCase`, constants `UPPER_SNAKE_CASE`.
- Imports: absolute under `iztro_py` (e.g., `from iztro_py.astro import by_solar`). Avoid relative imports across packages.

## Testing Guidelines
- Framework: pytest; place tests under `tests/` and name `test_*.py`.
- Add tests with each user-facing change; prioritize calendar conversion, horoscope flows, and i18n edge cases.
- Aim to maintain or improve coverage (~86% baseline). Use the coverage command above.
- Example fixture pattern: create charts via `astro.by_solar('2000-8-16', 6, '男')`.

## Commit & Pull Request Guidelines
- Use Conventional Commits (examples):
  - `feat: add i18n for ja-JP`
  - `fix: correct star name mapping`
  - `docs: update README with coverage command`
- PRs must include: clear motivation, linked issues, tests, and passing local checks (`pytest`, `ruff`, `black --check`, `mypy`).
- For versioned releases: update version in `pyproject.toml` and `src/iztro_py/__init__.py`, and record changes in `CHANGELOG.md`.

## Notes
- Do not commit generated files in `dist/` or cache directories.
- Keep public API stable; discuss breaking changes via an issue before opening a PR.
