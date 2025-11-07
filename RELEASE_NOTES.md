# Release Notes for v0.1.0

## 🎉 iztro-py v0.1.0 - Initial Release

We're excited to announce the first public release of **iztro-py**, a pure Python implementation of the excellent [iztro](https://github.com/SylarLong/iztro) library by [SylarLong](https://github.com/SylarLong)!

### 📦 Installation

```bash
pip install iztro-py
```

**PyPI Package:** https://pypi.org/project/iztro-py/0.1.0/

### ✨ What's New

#### Complete Feature Set
- ✅ **Pure Python Implementation** - No JavaScript interpreter needed
- ✅ **Full API Compatibility** - 100% compatible with original iztro library
- ✅ **Type Safety** - Complete type hints with Pydantic models
- ✅ **48 Tests Passing** - Comprehensive test coverage (86%)
- ✅ **Production Ready** - Stable API, well-documented

#### Core Features
- 🌟 **12 Palace System** (十二宫)
- ⭐ **14 Major Stars** (14主星)
- 🌙 **14 Minor Stars** (14辅星)
- 💫 **Four Transformations** (四化: 禄权科忌)
- 📅 **Horoscope System** (大限、小限、流年、流月、流日、流时)
- 🔄 **Three-sided Palaces** (三方四正)
- 🔗 **Fluent API** with method chaining

### 🚀 Quick Start

```python
from iztro_py import astro

# Create astrolabe
chart = astro.by_solar('2000-8-16', 6, '男')

# Query palaces and stars
soul_palace = chart.get_soul_palace()
ziwei_star = chart.star('ziweiMaj')

# Get horoscope
horoscope = chart.horoscope('2024-1-1', 6)
print(horoscope.decadal.name)  # '24-33岁'
```

### 📊 Test Results

- ✅ **48/48 tests passed** (100% pass rate)
- ✅ **86% code coverage**
- ✅ **26 compatibility tests** with original iztro
- ✅ **All edge cases handled** (leap months, different time zones, etc.)

### 🙏 Special Thanks

A huge thank you to [SylarLong](https://github.com/SylarLong) for creating the original [iztro](https://github.com/SylarLong/iztro) library. His excellent work made Zi Wei Dou Shu accessible through modern programming, and this Python implementation aims to bring the same quality to the Python ecosystem.

### 📚 Documentation

- **README:** https://github.com/spyfree/iztro-py#readme
- **PyPI:** https://pypi.org/project/iztro-py/
- **Examples:** See `examples/` directory
- **API Docs:** See README.md

### 🔗 Links

- **GitHub Repository:** https://github.com/spyfree/iztro-py
- **PyPI Package:** https://pypi.org/project/iztro-py/
- **Original iztro (JS):** https://github.com/SylarLong/iztro
- **Issue Tracker:** https://github.com/spyfree/iztro-py/issues

### 📈 What's Next?

#### Version 0.2.0 (Planned)
- Complete internationalization (i18n) support
- Additional language outputs
- Performance optimizations

#### Version 0.3.0 (Planned)
- Documentation website
- Interactive examples
- Visualization tools

### 🐛 Bug Reports & Feature Requests

Please report any issues or suggest features on our [GitHub Issues](https://github.com/spyfree/iztro-py/issues) page.

### 📄 License

MIT License - Free to use, modify, and distribute.

---

**Enjoy using iztro-py! 🎊**

If you find this project useful, please consider:
- ⭐ Starring the repository
- 📢 Sharing with the community
- 🐛 Reporting bugs or suggesting features
- 💝 Supporting the original [iztro](https://github.com/SylarLong/iztro) project
