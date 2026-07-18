# Repository Guidelines

## Project Structure & Module Organization
- `src/iztro_py/` — library source (public API re-exported in `src/iztro_py/__init__.py`).
  - `astro/` (chart creation: `by_solar`, `by_lunar`), `star/`, `utils/`, `i18n/`, `data/`.
- `tests/` — pytest suite (`test_*.py`).
- `examples/` — runnable scripts (e.g., `examples/basic_usage.py`).
- `dist/` — build artifacts (do not edit).

## Build, Test, and Development Commands
- Setup dev env: `pip install -e ".[dev]"` — required: an older `iztro-py` in site-packages will
  otherwise shadow the working tree for plain `python` runs (pytest is unaffected; it sets
  `pythonpath = src`). Alternative for one-off scripts: `PYTHONPATH=src python ...`.
- Run tests: `pytest -q`
- Coverage: `pytest --cov=src/iztro_py --cov-report=term-missing`
- JS parity diff: `python scripts/compare_iztro_alignment.py` — the reference package
  (`iztro@2.5.8`) is auto-discovered from `/tmp/iztro-2.5.8/node_modules/iztro` or the repo's
  tracked `node_modules/iztro`; override with `IZTRO_JS_PACKAGE=<dir>`.
  Fresh setup if neither exists: `npm install --prefix /tmp/iztro-2.5.8 iztro@2.5.8`
- Lint: `ruff check .` (auto-fix: `ruff --fix .`)
- Format: `python -m black src tests`
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
- `tests/test_alignment_core.py` depends on a local JS reference package. CI installs `iztro@2.5.8` under `/tmp/iztro-2.5.8` and passes `IZTRO_JS_PACKAGE=/tmp/iztro-2.5.8/node_modules/iztro`.
- `tests/test_regressions.py` pins values verified against `iztro@2.5.8` (year-pillar divide, nominal age, brightness, name lookups). If one of these fails after your change, assume your change broke alignment — re-run `scripts/compare_iztro_alignment.py` before touching the expected values.

## Commit & Pull Request Guidelines
- Use Conventional Commits (examples):
  - `feat: add i18n for ja-JP`
  - `fix: correct star name mapping`
  - `docs: update README with coverage command`
- PRs must include: clear motivation, linked issues, tests, and passing local checks (`pytest`, `ruff`, `black --check`, `mypy`).
- For versioned releases: update version in `pyproject.toml` and `src/iztro_py/__init__.py`, and record changes in `CHANGELOG.md`. Publishing to PyPI is automated: creating a GitHub release (`gh release create vX.Y.Z ...`) triggers `.github/workflows/publish.yml`, which builds and uploads via the `PYPI_API_TOKEN` secret. Do not `twine upload` manually.

## Notes
- Do not commit generated files in `dist/` or cache directories.
- Keep public API stable; discuss breaking changes via an issue before opening a PR.
- Keep formatter changes compatible with the Python 3.8 test matrix. `black>=24.10.0` drops Python 3.8 runtime support, so if CI still installs `.[dev]` in the test jobs, stay on a `black` release that supports `py38` or split tool dependencies by job.
- Calendar conventions are pinned to iztro@2.5.8 defaults (year/month pillars split at 农历正月初一, not 立春; 晚子时 day pillar rolls forward; 虚岁 from lunar-year difference; brightness tables mirror iztro `STARS_INFO`). See "Important Algorithms" in `CLAUDE.md`. Any change to `utils/calendar.py`, `astro/horoscope.py`, or `data/brightness.py` must re-run the JS parity diff.
- The repo intentionally tracks `node_modules/` (the iztro JS reference used by parity tooling). Keep it pinned to the version in `package.json`; upgrade it together with `EXPECTED_JS_VERSION` in `scripts/compare_iztro_alignment.py` and `tests/test_alignment_core.py`.
