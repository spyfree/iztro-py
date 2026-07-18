# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

iztro-py is a **pure Python implementation** of the iztro library for Zi Wei Dou Shu (紫微斗数, Purple Star Astrology) calculations. Unlike py-iztro which wraps JavaScript code, this is a native Python implementation with no JavaScript interpreter dependencies.

**Key characteristics:**
- Pure Python implementation (no JS interpreter)
- Type-safe with Pydantic models
- Fluent API with method chaining
- Multi-language support (currently zh-CN primary)

## Development Commands

### Installation
```bash
# Install in development mode with dev dependencies
pip install -e ".[dev]"
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src/iztro_py --cov-report=html

# Run specific test file
pytest tests/test_api.py

# Run specific test function
pytest tests/test_api.py::test_by_solar_basic

# Full-field diff against the iztro JS reference (exit 0 = aligned)
python scripts/compare_iztro_alignment.py
```

The alignment script and `tests/test_alignment_core.py` need `iztro@2.5.8` as
a JS reference. It is auto-discovered from `/tmp/iztro-2.5.8/node_modules/iztro`
or the repo's tracked `node_modules/iztro`; override with `IZTRO_JS_PACKAGE`.

Note: plain `python somescript.py` resolves `iztro_py` from site-packages, which
may shadow the working tree with an older release. Use `pip install -e .` or
`PYTHONPATH=src`. pytest is unaffected (`pythonpath = src` in pyproject).

### Code Quality
```bash
# Format code
black src tests

# Type checking
mypy src

# Linting (if ruff is configured)
ruff check src tests
```

## Architecture

### Core Data Flow

1. **Entry Point** (`src/iztro_py/astro/astro.py`)
   - `by_solar()` and `by_lunar()` are the main entry functions
   - Convert dates → Calculate positions → Build astrolabe
   - Returns `FunctionalAstrolabe` object

2. **Star Calculation Pipeline**:
   ```
   Date Input
   → Calendar Conversion (utils/calendar.py)
   → Palace Initialization (astro/palace.py)
   → Major Star Placement (star/major_star.py)
   → Minor Star Placement (star/minor_star.py)
   → Mutagen Application (star/mutagen.py)
   → Brightness Calculation (data/brightness.py)
   → FunctionalAstrolabe
   ```

3. **Functional Classes** (Fluent API layer):
   - `FunctionalAstrolabe`: Main entry point with method chaining
   - `FunctionalPalace`: Palace queries and star checks
   - `FunctionalStar`: Star-specific queries
   - `FunctionalSurpalaces`: Three-sided palace relationships (三方四正)

### Key Modules

- **`data/`**: Core type definitions, constants, and lookup tables
  - `types.py`: Pydantic models and type definitions
  - `constants.py`: Palace names, star names, relationships
  - `heavenly_stems.py` / `earthly_branches.py`: Chinese calendar systems
  - `brightness.py`: Star brightness calculations

- **`astro/`**: Main astrolabe logic
  - `astro.py`: Entry point functions
  - `functional_*.py`: Fluent API implementation
  - `palace.py`: Palace positioning algorithms
  - `horoscope.py`: Horoscope system (大限、流年、流月、流日、流时)

- **`star/`**: Star placement algorithms
  - `major_star.py`: 14 main stars (紫微、天府系统)
  - `minor_star.py`: 14 auxiliary stars (左右昌曲魁钺等)
  - `mutagen.py`: Four transformations system (四化)
  - `location.py`: Star positioning calculations

- **`utils/`**: Utility functions
  - `calendar.py`: Solar/Lunar calendar conversions
  - `helpers.py`: Common helper functions

### Important Algorithms

1. **Palace Positioning**: Soul palace (命宫) and body palace (身宫) are calculated from lunar month and birth time
2. **Major Stars**: Ziwei (紫微) position determined by five elements class and lunar day; other stars follow fixed offsets
3. **Five Elements Class (五行局)**: Determined by soul palace's heavenly stem and earthly branch
4. **Horoscope System**: Multi-level fortune analysis (decadal/yearly/monthly/daily/hourly)
5. **Calendar Conventions** (aligned with iztro@2.5.8 defaults; do not change without re-running `scripts/compare_iztro_alignment.py`):
   - Year/month pillars split at 农历正月初一 (`yearDivide/horoscopeDivide='normal'`), NOT at 立春
   - Day pillar rolls to the next day for 晚子时 (`dayDivide='forward'`)
   - Nominal age (虚岁) = target lunar year − birth lunar year + 1
   - Star brightness tables mirror iztro `STARS_INFO` (indexed from 寅=0), including minor stars 昌曲火铃羊陀

### Type System

The project uses Pydantic extensively for data validation and type safety:
- `Literal` types for fixed vocabularies (PalaceName, StarName, etc.)
- `BaseModel` for structured data (Astrolabe, Palace, Star, etc.)
- All core types defined in `data/types.py`

## Code Conventions

### File Structure
- Source code: `src/iztro_py/`
- Tests mirror source structure: `tests/test_*.py`
- Examples: `examples/`

### Naming
- Functions: snake_case
- Classes: PascalCase
- Type aliases: PascalCase (e.g., `PalaceName`, `StarName`)
- Constants: UPPER_SNAKE_CASE

### API Design Patterns

**Method Chaining**:
```python
# Methods return objects that support further chaining
if chart.star('紫微').surrounded_palaces().have_mutagen('忌'):
    # ...
```

**Functional Wrappers**:
- Base types (Astrolabe, Palace, Star) are Pydantic models
- Functional* classes wrap these with query methods
- Keeps data layer clean while adding API convenience

**Name Normalization**:
- Star/palace lookups (`star()`, `palace()`, `palace.has()` etc.) accept internal
  keys (`'ziweiMaj'`, `'soulPalace'`) or translated names from any of the six
  locales (`'紫微'`, `'命宫'`), via `i18n.normalize_star_name` /
  `normalize_palace_name` (the iztro `kot()` equivalent)
- Internally `Star.name` / `Palace.name` always store keys; the `palaces` list is
  anchored at 寅宫 = index 0, so never use palace-name offsets as list indices

## Testing Strategy

Test files in `tests/` directory:
- `test_api.py`: Core API functionality
- `test_calendar.py`: Calendar conversion
- `test_horoscope.py`: Horoscope system
- `test_integration.py`: End-to-end tests
- `test_palace.py`: Palace positioning
- `test_stars.py`: Star placement
- `test_alignment_core.py`: Runs `scripts/compare_iztro_alignment.py` against the JS reference (12 blocking cases)
- `test_iztro_compatibility.py`: Known-chart expectations and API parity checks
- `test_regressions.py`: Pins iztro-verified values for the 2026-07 alignment fixes (year-pillar divide, nominal age, brightness, name lookups)
- `test_coverage_improvements.py`: Additional branch coverage

All tests use pytest framework.

## Known Limitations

1. **i18n**: Six locales ship (zh-CN, zh-TW, en-US, ja-JP, ko-KR, vi-VN); zh-CN is the most complete and untranslated keys fall back to zh-CN. The language setting is process-global (`i18n.set_language`), so charts created with different languages share translation state.
2. **PyPI**: Published as `iztro-py` (latest 0.4.0). Install released builds with `pip install -U iztro-py`; for development use `pip install -e .` so imports resolve to the working tree.
3. **Documentation site**: Planned but not yet implemented
4. **Horoscope feature gaps vs iztro**: no 流曜 (`stars` is always `None` on horoscope items), no 流年将前/岁前十二神 (`yearlyDecStar`), and no config system (`yearDivide`/`ageDivide` etc. are fixed to iztro defaults). `horoscope()` returns a plain data model, not a chainable FunctionalHoroscope.

## Releasing

1. Bump the version in `pyproject.toml` and `src/iztro_py/__init__.py`; add a `CHANGELOG.md` entry.
2. Commit, push, and wait for CI (`ci.yml`) to pass.
3. `gh release create vX.Y.Z ...` — publishing the GitHub release triggers `.github/workflows/publish.yml`, which builds and uploads to PyPI automatically (secret `PYPI_API_TOKEN`). No manual `twine upload`.

## Development Priorities

When adding features or fixing bugs:
1. Maintain type safety - add proper type hints
2. Update tests for any changes
3. Keep API fluent and chainable
4. Document complex algorithms (especially star positioning)
5. Cross-reference with original iztro library for compatibility
