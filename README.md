# iztro-py

[![PyPI version](https://badge.fury.io/py/iztro-py.svg)](https://pypi.org/project/iztro-py/)
[![Python版本](https://img.shields.io/pypi/pyversions/iztro-py)](https://pypi.org/project/iztro-py/)
[![License](https://img.shields.io/pypi/l/iztro-py)](https://github.com/SylarLong/iztro-py/blob/main/LICENSE)

紫微斗数Python库 - 纯Python实现，支持多语言输出。

[English](./README_EN.md) | [한국어](./README_KO.md)

## 项目简介

`iztro-py` 是一个功能强大的紫微斗数（Purple Star Astrology）Python库。与 py-iztro 不同，这是一个**纯Python原生实现**，无需JavaScript解释器依赖。

### 主要特性

- ✨ **纯Python实现** - 无需JavaScript运行时环境
- 🌍 **多语言支持** - 支持简体中文、繁體中文、English、日本語、한국어、Tiếng Việt
- 🔒 **类型安全** - 使用Pydantic模型确保数据完整性
- 🎯 **流畅API** - 支持方法链式调用
- 📦 **易于使用** - pip一键安装

## 安装

```bash
pip install iztro-py
```

## 快速开始

### 基本用法

```python
from iztro_py import astro

# 通过阳历日期创建星盘（默认中文输出）
chart = astro.by_solar('2000-8-16', 6, '男')

# 获取命宫
soul_palace = chart.get_soul_palace()
print(f"命宫: {soul_palace.translate_name()}")
print(f"天干地支: {soul_palace.translate_heavenly_stem()} {soul_palace.translate_earthly_branch()}")

# 查询主星
for star in soul_palace.major_stars:
    print(f"主星: {star.translate_name()} - 亮度: {star.translate_brightness()}")
```

### 多语言支持

```python
from iztro_py import astro

# 简体中文（默认）
chart = astro.by_solar('2000-8-16', 6, '男', language='zh-CN')
print(chart.get_soul_palace().translate_name('zh-CN'))  # 输出: 福德宫

# 繁體中文
chart = astro.by_solar('2000-8-16', 6, '男', language='zh-TW')
print(chart.get_soul_palace().translate_name('zh-TW'))  # 输出: 福德宮

# English
chart = astro.by_solar('2000-8-16', 6, '男', language='en-US')
print(chart.get_soul_palace().translate_name('en-US'))  # 输出: Spirit

# 日本語
chart = astro.by_solar('2000-8-16', 6, '男', language='ja-JP')
print(chart.get_soul_palace().translate_name('ja-JP'))  # 输出: 福徳宮

# 한국어
chart = astro.by_solar('2000-8-16', 6, '남', language='ko-KR')
print(chart.get_soul_palace().translate_name('ko-KR'))  # 输出: 복덕궁

# Tiếng Việt
chart = astro.by_solar('2000-8-16', 6, 'nam', language='vi-VN')
print(chart.get_soul_palace().translate_name('vi-VN'))  # 输出: Phúc Đức Cung
```

### 查询星曜

```python
# 查找特定星曜
ziwei = chart.star('ziweiMaj')
if ziwei:
    print(f"星曜: {ziwei.translate_name()}")
    print(f"亮度: {ziwei.translate_brightness()}")
    print(f"所在宫位: {ziwei.palace().translate_name()}")
```

### 三方四正

```python
# 获取命宫的三方四正
soul_palace = chart.get_soul_palace()
surpalaces = chart.surrounded_palaces(soul_palace.index)

for palace in surpalaces.all_palaces():
    print(f"{palace.translate_name()}: {[s.translate_name() for s in palace.major_stars]}")
```

## 支持的语言

- **zh-CN**: 简体中文（默认）🇨🇳
- **zh-TW**: 繁體中文 🇹🇼
- **en-US**: English 🇺🇸
- **ja-JP**: 日本語 🇯🇵
- **ko-KR**: 한국어 🇰🇷
- **vi-VN**: Tiếng Việt 🇻🇳

涵盖紫微斗数主要流行的东亚和东南亚地区！

## 文档

- [完整使用文档](./docs/README_zh.md)
- [API参考](./docs/API.md)
- [示例代码](./examples/)

## 与 iztro (JS版本) 的对比

|  | iztro-py | py-iztro |
|---|---|---|
| 实现方式 | 纯Python | JavaScript包装器 |
| 依赖 | 仅Python标准库 | 需要JS解释器 |
| 性能 | 高 | 较低（跨语言调用开销） |
| 类型安全 | ✓ Pydantic模型 | ✗ |
| 多语言支持 | ✓ | ✗ |

## 开发

### 安装开发依赖

```bash
pip install -e ".[dev]"
```

### 运行测试

```bash
pytest
pytest --cov=src/iztro_py --cov-report=html
```

### 代码格式化

```bash
black src tests
mypy src
```

## 相关链接

- [iztro (JavaScript版本)](https://github.com/SylarLong/iztro)
- [在线排盘](https://ziwei.pub)
- [紫微斗数介绍](https://zh.wikipedia.org/wiki/%E7%B4%AB%E5%BE%AE%E6%96%97%E6%95%B0)

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

---

如果这个项目对你有帮助，请给它一个 ⭐️
