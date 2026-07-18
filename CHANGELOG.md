# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2026-07-18

Full-field alignment with `iztro@2.5.8` defaults. A 36-case random/edge sweep
now matches the JS reference on every compared field (star placement with
brightness and in-palace order, adjective stars, 12-god cycles, decadal/age
anchors, and all horoscope indices).

### 🔧 Correctness Fixes (behavior changes)

- **Year/month pillars now split at 农历正月初一** (`yearDivide/horoscopeDivide='normal'`),
  matching iztro defaults. Previously the 立春-based exact divide was used, which
  produced entirely wrong charts for births between Lunar New Year and 立春
- **Nominal age (虚岁) is now computed from lunar years** (`target lunar year −
  birth lunar year + 1`). Previously solar years were used, shifting 大限/小限
  palaces by one year for dates between Jan 1 and Lunar New Year
- **Star brightness tables rewritten from iztro `STARS_INFO`**: every major star
  except 紫微 had incorrect rows; brightness is now also applied to
  文昌/文曲/火星/铃星/擎羊/陀罗 (with the unrated positions left empty)
- **Minor stars are placed in iztro's push order** so stars sharing a palace
  keep the same in-palace ordering as the JS reference

### 🐛 API Fixes

- `astrolabe.star('紫微')`, `palace.has(['紫微'])` and related queries now accept
  translated star names from all six locales (previously only internal keys
  matched, and Chinese names silently returned `None`/`False`)
- `astrolabe.palace('命宫')` returned the wrong palace whenever the soul palace
  was not at index 0 (palace-name offsets were misused as list indices); palace
  lookups now resolve by actual palace name and accept all locale translations
- `FunctionalAstrolabe` now preserves the `language` requested via
  `by_solar(..., language=...)`
- Removed the no-op `fix_leap` parameter from `solar_to_lunar()` and unused
  parameters from `get_horoscope()`

### 🧪 Verification

- Alignment script expanded from 6 to 12 blocking cases: both genders, births
  in the 春节-立春 window, leap-month (闰二月) births, late 子时 births, and
  horoscope targets across lunar-year boundaries; brightness and in-palace star
  order are now compared as blocking fields, and horoscope comparison covers
  小限/流月/流日/流时 indices plus nominal age
- Added `tests/test_regressions.py` covering all fixes above
- Bundled iztro JS reference upgraded from 2.5.3 to 2.5.8

## [0.3.4] - 2026-03-07

### 🔧 Alignment Fixes

- Reworked the solar/lunar and exact Ganzhi pipeline to match `iztro@2.5.8`
- Fixed five-elements-class calculation to use the same rule as upstream `iztro`
- Corrected soul/body palace indexing and palace initialization to stay in the 寅宫=0 coordinate system
- Fixed major and minor star placement to align with upstream palace coordinates
- Matched decadal, age, and yearly anchor logic with upstream `iztro`

### ✨ Feature Parity

- Added adjective, flower, and helper star placement to align birth-chart output with `iztro@2.5.8`
- Added `changsheng12`, `boshi12`, `jiangqian12`, and `suiqian12` palace fields
- Extended `to_iztro_dict()` export with decorative 12-god fields
- Added a JS-vs-Python alignment comparison script for regression checks

### 🧪 Verification

- Added regression coverage for the fixed-hour and leap-year alignment matrix
- Verified zero blocking diffs against `iztro@2.5.8` for the reference matrix
- Confirmed the full pytest suite passes locally

### 📦 Packaging

- Declared the `lunar_python` runtime dependency used by the calendar alignment implementation

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
