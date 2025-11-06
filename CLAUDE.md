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
```

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

## Testing Strategy

Test files in `tests/` directory:
- `test_api.py`: Core API functionality
- `test_calendar.py`: Calendar conversion
- `test_horoscope.py`: Horoscope system
- `test_integration.py`: End-to-end tests
- `test_palace.py`: Palace positioning
- `test_stars.py`: Star placement

All tests use pytest framework.

## Known Limitations

1. **i18n**: Currently only zh-CN is fully implemented (language parameter accepted but not used)
2. **Not yet on PyPI**: Package is ready but not published yet
3. **Documentation site**: Planned but not yet implemented

## Development Priorities

When adding features or fixing bugs:
1. Maintain type safety - add proper type hints
2. Update tests for any changes
3. Keep API fluent and chainable
4. Document complex algorithms (especially star positioning)
5. Cross-reference with original iztro library for compatibility
