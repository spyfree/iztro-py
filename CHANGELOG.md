# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - 2026-07-25

Follow-up audit to the 0.4.0 alignment work. The core birth-chart and horoscope
algorithms were re-verified by differential fuzzing against `iztro@2.5.8` — 500
random charts and 500 random horoscope queries (1930–2035, all 13 时辰, both
genders, horoscope targets spanning pre-birth to far-future) match on every
compared field. The defects fixed here were all in the surrounding surface:
exported helpers nothing called internally, i18n, out-of-range handling, and
the test/CI infrastructure meant to catch exactly this.

### 💥 Breaking Changes

- **en-US star and palace names now use iztro's semantic English.**
  `ziweiMaj` renders as `"emperor"` (was `"Ziwei"`), `lucunMin` as `"money"`,
  `soulPalace` as `"soul"` (was `"Soul"`). en-US output is now identical to
  iztro's. `brightness` is the deliberate exception — it keeps this project's
  words (`"Temple"`, `"Prosperous"`) rather than iztro's `[+3]` score notation,
  since it was already fully translated in all six languages
- **`astrolabe.time`, `.zodiac`, `.sign` and `.five_elements_class` are now
  localized** instead of always Simplified Chinese. Charts built with the
  default `language='zh-CN'` are unaffected except for `time` (below)
- **`astrolabe.time` now distinguishes 早子时 from 晚子时.** Both `time_index=0`
  and `time_index=12` previously returned `"子时"`, erasing a distinction that
  matters — the late rat hour rolls the day pillar to the next day
- **`horoscope.decadal.index` / `.age.index` return `-1`** when the nominal age
  falls outside every decadal/age range, matching iztro. They previously
  returned `0` — 命宫 — so an out-of-range query was indistinguishable from a
  real result. Reachable from a date before birth, from a date in the birth
  lunar year before 春节 (nominal age 0), and from any age past ~125.
  `HoroscopeItem.index` accepts `-1` now; it was constrained to `ge=0`, so the
  sentinel was not even representable
- Removed unreferenced internals: `calculate_palace_ages`,
  `get_body_palace_index`, `get_palace_earthly_branch`,
  `FIVE_ELEMENTS_CLASS_LOOKUP`, `ZIWEI_START_POSITIONS`, `BRIGHTNESS_ORDER`,
  `BRIGHTNESS_MAPPING`

### 🐛 Correctness Fixes

- **`get_day_stem_branch()` returned the wrong day pillar for every date.**
  The "公元元年1月1日是甲子日后的第37天" anchor is wrong, putting results 51 days
  off in the 60-ganzhi cycle; a 567-date sweep over 1900–2050 mismatched the
  production four-pillar path 567 times. It now delegates to `lunar_python`.
  Chart building never used it, which is why the alignment suite never caught it
- **Building a chart in another language silently rewrote earlier charts.**
  `translate_name()` read a process-global language, so a second
  `by_solar(..., language=...)` changed what an existing chart rendered — while
  `chart.language` still reported the original. Translations now resolve per
  chart. `Astrolabe.set_language()` is scoped to its own chart and no longer
  moves the global default
- **`horoscope()` silently mis-computed the five elements class for non-Chinese
  charts.** It recovered the class by reverse-parsing the localized display
  string, defaulting to 水二局 on a miss. The enum is now carried on the model as
  `raw_five_elements_class`
- **Deep copies of a chart pointed at a stale astrolabe.** `copy.deepcopy`,
  `model_copy(deep=True)` and `pickle` all produced charts whose palaces
  referenced a third object, so `star.surrounded_palaces()` and
  `opposite_palace()` queried the wrong chart
- `get_year_stem_branch()` and `get_time_stem_branch()` are correct but have
  non-obvious contracts (lunar year; next-day stem for the late rat hour). Both
  are now documented with worked examples, and pinned by tests

### 🌍 i18n

- **All six locales are now complete.** zh-TW, en-US, ja-JP, ko-KR and vi-VN
  each carried only 5 of zh-CN's 89 sections, so all 42 adjective stars and all
  48 長生/博士/將前/歲前十二神 fell back to Simplified Chinese in every non-zh-CN
  language — including Traditional Chinese. Locales are now generated from the
  iztro reference locales via `scripts/generate_locales.py`
- Added `time`, `zodiac`, `sign`, `fiveElementsClass` and `gender` sections
- `get_zodiac_by_solar_date()` and `get_sign_by_solar_date()` honour their
  `language` argument, which they previously accepted and ignored

### 🏗️ Infrastructure

- **The alignment suite was failing, not running, on a fresh clone.** The
  `.gitignore` pattern `lib/`, meant for Python build artifacts, also matched
  `node_modules/iztro/lib/` and excluded the reference package's compiled JS.
  Patterns are anchored to the repo root now, `node_modules/` is ignored
  outright (untracking 730 vendored JS files), and `npm install` reproduces the
  reference. A missing reference skips locally and fails CI via
  `IZTRO_REQUIRE_JS_REFERENCE=1`
- The alignment script no longer raises `CalledProcessError` out of its node
  subprocess, which stringified the entire inlined JS program and buried node's
  actual error
- **mypy and ruff actually gate CI now.** mypy ran as `|| true` *and*
  `continue-on-error`; ruff was `continue-on-error` with no rule selection, so
  an unpinned ruff changed what CI checked from run to run. Rules are selected
  explicitly, ruff is version-pinned, and the tree is clean under both
- Removed 13 of 15 files in `scripts/`; six crashed on APIs that no longer
  exist and three required an undeclared `py_iztro` dependency

### ✅ Tests

- `tests/test_horoscope.py` had four tests and **zero assertions** — they only
  printed, then unconditionally printed "测试通过". Replaced with 24
  parametrized tests covering nominal age, all six scope indices, ganzhi,
  mutagen, palace rotation and decadal direction
- Gave real assertions to the other four assertion-free tests; removed the
  `__main__` blind-except script runners from five files
- 85 → 136 tests; assertion-free tests 8 → 0

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
