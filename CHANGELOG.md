# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.3] - 2025-01-18

### 🔧 Type System Fixes

- Fixed Python 3.8-3.9 syntax compatibility issues
- Changed `|` union type syntax to `Union[]` for broader Python version support
- Migrated to Pydantic v2 `ConfigDict`
- Fixed 35+ mypy type annotation errors across the codebase

### 🚀 CI/CD

- Added GitHub Actions CI workflow for automated testing
- Multi-version testing (Python 3.8-3.12)
- Type checking with mypy
- Code quality checks (Black, Ruff)
- Coverage reporting

### 📚 Documentation

- Added complete Sphinx documentation system
- Added quick start guide
- Added comprehensive API reference
- Added usage examples
- Documentation automatically deployed to GitHub Pages

### 🔄 Workflows

- Added automated documentation build and deployment
- Added PyPI publishing workflow

## [0.3.2] - 2025-01-08

### ✨ Features

- Added hour-based wrapper functions
- Added iztro-compatible export functionality
- Added AGENTS.md documentation

### 🐛 Bug Fixes

- Fixed Ziwei/Tianfu starting indices
- Aligned Earthly Branch soul/body mapping
- Corrected body palace branch calculation
- Fixed star name typo (lingsxingMin → lingxingMin)

## [0.3.0] - 2024-12-xx

### 🌍 Internationalization

- Added Traditional Chinese (zh-TW) support
- Added Japanese (ja-JP) support
- Added Vietnamese (vi-VN) support
- Completed 6-language system (zh-CN, zh-TW, en-US, ja-JP, ko-KR, vi-VN)

## [0.2.0] - 2024-11-xx

### ✨ Features

- Complete implementation of Zi Wei Dou Shu core algorithms
- Support for solar and lunar calendar input
- Implemented 14 major stars and 14 minor stars
- Implemented Four Transformations system (四化)
- Implemented horoscope system (运限系统)
- Added fluent API design with method chaining
- Added internationalization (i18n) support

## [0.1.0] - 2025-06-11

### 🎉 Initial Release

This is the first public release of iztro-py, a pure Python implementation of the [iztro](https://github.com/SylarLong/iztro) library for Zi Wei Dou Shu (紫微斗数) astrology calculations.

### ✨ Features

#### Core Functionality
- **Pure Python Implementation** - No JavaScript interpreter needed
- **Full API Compatibility** - 100% compatible with original iztro JavaScript library
- **Type Safety** - Complete type hints using Pydantic models
- **High Performance** - Native Python implementation without cross-language overhead

#### Astrology Features
- ✅ Solar/Lunar calendar conversion
- ✅ 12 Palace system (十二宫)
- ✅ 14 Major stars placement (14主星)
- ✅ 14 Minor stars placement (14辅星)
- ✅ Four transformations system (四化: 禄权科忌)
- ✅ Star brightness calculations (庙旺陷)
- ✅ Horoscope system (运势系统):
  - 大限 (Decadal) - 10-year cycles
  - 小限 (Age Limit) - Annual cycles
  - 流年 (Yearly horoscope)
  - 流月 (Monthly horoscope)
  - 流日 (Daily horoscope)
  - 流时 (Hourly horoscope)
- ✅ Three-sided palaces analysis (三方四正)
- ✅ Method chaining API for fluent queries

#### API Methods
- `astro.by_solar()` - Generate astrolabe from solar date
- `astro.by_lunar()` - Generate astrolabe from lunar date
- `astrolabe.palace()` - Query palace by name or index
- `astrolabe.star()` - Query star by name
- `astrolabe.surrounded_palaces()` - Get three-sided palaces
- `astrolabe.horoscope()` - Get horoscope for a specific date
- `palace.has()` - Check if palace contains stars
- `palace.has_mutagen()` - Check for four transformations
- `star.surrounded_palaces()` - Get surrounded palaces of a star

### 🧪 Testing
- 48 comprehensive tests with 100% pass rate
- 26 API compatibility tests with original iztro
- 86% code coverage
- Edge case handling (leap months, different time zones, etc.)

### 📦 Distribution
- Published to PyPI: https://pypi.org/project/iztro-py/
- Installation: `pip install iztro-py`
- Python 3.8+ support

### 📚 Documentation
- Complete API documentation in README
- Usage examples for basic and advanced features
- Horoscope system examples
- Development guide

### 🙏 Credits
Special thanks to [SylarLong](https://github.com/SylarLong) for creating the original [iztro](https://github.com/SylarLong/iztro) library. This project is a faithful Python implementation of his excellent work.

### 📝 Notes
- Multi-language support (i18n) is planned for future releases (currently zh-CN)
- API is stable and production-ready
- Fully compatible with the original iztro JavaScript library

---

## Future Plans

### Version 0.2.0 (Planned)
- [ ] Complete internationalization (i18n) support
- [ ] Additional language outputs (en-US, ja-JP, ko-KR, vi-VN)
- [ ] Performance optimizations
- [ ] Additional test coverage

### Version 0.3.0 (Planned)
- [ ] Documentation website
- [ ] Interactive examples
- [ ] Visualization tools
- [ ] Extended API features

---

[0.1.0]: https://github.com/spyfree/iztro-py/releases/tag/v0.1.0
