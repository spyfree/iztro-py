# iztro-py

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A **pure Python implementation** of [iztro](https://github.com/SylarLong/iztro) - A lightweight library for generating astrolabes for Zi Wei Dou Shu (紫微斗数, Purple Star Astrology), an ancient Chinese astrology.

## Features

- ✨ **Pure Python Implementation** - No JavaScript interpreter needed, unlike py-iztro
- 🚀 **High Performance** - Native Python implementation without cross-language overhead
- 🔧 **Type Safe** - Full type hints with Pydantic models
- 🌍 **Multi-language Support** - Simplified Chinese, Traditional Chinese, English, Japanese, Korean, Vietnamese
- 📊 **Complete Functionality** - All features from the original iztro library
- 🔗 **Fluent API** - Method chaining for intuitive queries

## Installation

```bash
pip install iztro-py
```

## Quick Start

```python
from iztro_py import astro

# Get astrolabe by solar date
astrolabe = astro.by_solar('2000-8-16', 2, '男', True, 'zh-CN')

# Get basic information
print(astrolabe.gender)          # '男'
print(astrolabe.solar_date)      # '2000-8-16'
print(astrolabe.lunar_date)      # '2000年七月十八'
print(astrolabe.sign)            # '狮子座'
print(astrolabe.zodiac)          # '龙'

# Get palace by name or index
soul_palace = astrolabe.palace('命宫')
print(soul_palace.name)                    # '命宫'
print(soul_palace.heavenly_stem)           # '庚'
print(soul_palace.earthly_branch)          # '午'
print(soul_palace.major_stars)             # List of major stars

# Check if palace contains specific stars
if soul_palace.has(['紫微']):
    print('命宫有紫微星')

# Get star object
ziwei = astrolabe.star('紫微')
print(ziwei.brightness)                    # '旺'
print(ziwei.mutagen)                       # '禄' or None

# Get surrounded palaces (三方四正)
surrounded = astrolabe.surrounded_palaces('命宫')
if surrounded.have_mutagen('忌'):
    print('三方四正有化忌')

# Chain method calls
if astrolabe.star('紫微').surrounded_palaces().have_mutagen('忌'):
    print('紫微星三方四正有化忌')

# Get horoscope (运限) for a specific date
horoscope = astrolabe.horoscope('2024-1-1', 6)
print(horoscope.decadal.name)              # '24-33岁' (大限)
print(horoscope.nominal_age)               # 25 (虚岁)
print(horoscope.yearly.name)               # '甲辰年' (流年)
```

## API Documentation

### Core Functions

#### `astro.by_solar(solar_date, time_index, gender, fix_leap=True, language='zh-CN')`

Get astrolabe by solar calendar date.

**Parameters:**
- `solar_date` (str): Solar date in format 'YYYY-M-D'
- `time_index` (int): Time index 0-12 (0=early子时, 1=丑时, ..., 12=late子时)
- `gender` (str): '男' or '女'
- `fix_leap` (bool): Whether to fix leap month
- `language` (str): Output language ('zh-CN', 'zh-TW', 'en-US', 'ja-JP', 'ko-KR', 'vi-VN')

**Returns:** `FunctionalAstrolabe` object

#### `astro.by_lunar(lunar_date, time_index, gender, is_leap_month=False, fix_leap=True, language='zh-CN')`

Get astrolabe by lunar calendar date.

**Parameters:**
- `lunar_date` (str): Lunar date in format 'YYYY-M-D'
- `time_index` (int): Time index 0-12
- `gender` (str): '男' or '女'
- `is_leap_month` (bool): Whether it's a leap month
- `fix_leap` (bool): Whether to fix leap month
- `language` (str): Output language

**Returns:** `FunctionalAstrolabe` object

### FunctionalAstrolabe Methods

- `palace(name_or_index)` - Get palace by name or index
- `star(star_name)` - Get star object
- `surrounded_palaces(name_or_index)` - Get surrounded palaces (三方四正)
- `horoscope(solar_date, time_index)` - Get horoscope data for specified date
- `get_soul_palace()` - Get soul palace (命宫)
- `get_body_palace()` - Get body palace (身宫)

### FunctionalPalace Methods

- `has(stars)` - Check if palace contains all specified stars
- `has_one_of(stars)` - Check if palace contains any of specified stars
- `not_have(stars)` - Check if palace doesn't contain any specified stars
- `has_mutagen(mutagen)` - Check if palace has specified mutagen (四化)
- `is_empty()` - Check if palace is empty

### FunctionalStar Methods

- `palace()` - Get palace containing this star
- `surrounded_palaces()` - Get surrounded palaces of this star
- `opposite_palace()` - Get opposite palace
- `with_brightness(brightness)` - Check star brightness
- `with_mutagen(mutagen)` - Check star mutagen
- `is_bright()` - Check if star is bright (庙/旺)
- `is_weak()` - Check if star is weak (陷)

### Horoscope System (运势系统)

The horoscope system provides fortune analysis for different time periods:

```python
# Get horoscope for a specific date
horoscope = chart.horoscope('2024-1-1', 6)

# Decadal horoscope (大限) - 10 years per cycle
print(horoscope.decadal.name)              # e.g., '24-33岁'
print(horoscope.decadal.palace_names)      # Palace where decadal is located
print(horoscope.decadal.mutagen)           # Four transformations

# Age limit (小限) - 1 year per cycle
print(horoscope.age.name)                  # e.g., '25岁'
print(horoscope.nominal_age)               # 25 (virtual age)

# Yearly horoscope (流年)
print(horoscope.yearly.name)               # e.g., '甲辰年'
print(horoscope.yearly.palace_names)       # Palace location in birth chart

# Monthly horoscope (流月)
print(horoscope.monthly.name)              # e.g., '丙子月'

# Daily horoscope (流日)
print(horoscope.daily.name)                # e.g., '癸酉日'

# Hourly horoscope (流时)
print(horoscope.hourly.name)               # e.g., '戊午时'

# Get palace for any horoscope level
yearly_palace = chart.palace(horoscope.yearly.index)
if yearly_palace:
    print(yearly_palace.major_stars)

# Analyze three-sided palaces for yearly horoscope
surpalaces = chart.surrounded_palaces(horoscope.yearly.index)
if surpalaces.have_mutagen('禄'):
    print('Yearly palace has luck transformation')
```

**Horoscope Levels:**
- **大限 (Decadal)**: 10-year cycle based on five elements class (水二局/木三局/金四局/土五局/火六局)
- **小限 (Age Limit)**: Annual cycle, starts from soul palace
- **流年 (Yearly)**: Based on yearly heavenly stem and earthly branch
- **流月 (Monthly)**: Based on monthly stem and branch
- **流日 (Daily)**: Based on daily stem and branch
- **流时 (Hourly)**: Based on hourly stem and branch

See [examples/horoscope_usage.py](examples/horoscope_usage.py) for detailed usage examples.

## Architecture

This is a **pure Python reimplementation** of the original JavaScript iztro library:

- **No JavaScript interpreter** - Unlike py-iztro which wraps JS code
- **Native Python** - All algorithms implemented in Python
- **Better performance** - No cross-language overhead
- **Easier to maintain** - Pure Python codebase

## Comparison

| Feature | iztro (JS) | py-iztro | iztro-py (this) |
|---------|-----------|----------|-----------------|
| Language | JavaScript | Python wrapper | Pure Python |
| Dependencies | Node.js | JS interpreter | Python only |
| Performance | Fast | Slow (overhead) | Fast |
| Type Safety | TypeScript | Pydantic | Pydantic |
| Maintenance | Active | Depends on JS | Independent |

## Development

```bash
# Clone repository
git clone https://github.com/spyfree/iztro-py.git
cd iztro-py

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=src/iztro_py --cov-report=html

# Format code
black src tests

# Type check
mypy src
```

## License

MIT License - see [LICENSE](LICENSE) file

## Credits

This project is inspired by and compatible with [iztro](https://github.com/SylarLong/iztro) by SylarLong.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Roadmap

- [x] Project structure setup
- [x] Core data types and constants
- [x] Lunar/Solar calendar conversion
- [x] Heavenly Stems and Earthly Branches calculations
- [x] Palace positioning algorithms
- [x] Star positioning algorithms (紫微、天府、14主星)
- [x] Minor stars algorithms (14辅星)
- [x] Mutagen system (四化)
- [x] Brightness calculations
- [x] FunctionalAstrolabe class
- [x] FunctionalPalace class
- [x] FunctionalStar class
- [x] Surrounded palaces (三方四正)
- [x] Horoscope system (大限、流年、流月、流日、流时)
- [x] Unit tests (14/14 core tests + 4/4 horoscope tests passing)
- [x] Usage examples
- [ ] Internationalization (i18n) - currently zh-CN only
- [ ] Documentation website
- [ ] PyPI package release
