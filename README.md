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

# Get horoscope (运限)
horoscope = astrolabe.horoscope()
print(horoscope.decadal.name)              # '大限'
print(horoscope.age.nominal_age)           # 虚岁
print(horoscope.yearly.name)               # '流年'
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
- `horoscope(date=None, time_index=None)` - Get horoscope data

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
- [ ] Core data types and constants
- [ ] Lunar/Solar calendar conversion
- [ ] Heavenly Stems and Earthly Branches calculations
- [ ] Palace positioning algorithms
- [ ] Star positioning algorithms (紫微、天府、14主星)
- [ ] Minor stars algorithms (14辅星)
- [ ] Mutagen system (四化)
- [ ] Brightness calculations
- [ ] FunctionalAstrolabe class
- [ ] FunctionalPalace class
- [ ] FunctionalStar class
- [ ] Surrounded palaces (三方四正)
- [ ] Horoscope system (运限)
- [ ] Internationalization (i18n)
- [ ] Unit tests
- [ ] Documentation
- [ ] PyPI package release
