# API Reference

## Core Functions

### `astro.by_solar()`

Create an astrolabe from a solar (Gregorian) date.

```python
from iztro_py import astro

chart = astro.by_solar(
    solar_date='2000-8-16',  # Date string (YYYY-M-D or YYYY-MM-DD)
    time_index=6,            # Time index (0-12)
    gender='男',             # Gender ('男' or '女')
    fix_leap=True,           # Fix leap month (default: True)
    language='zh-CN'         # Output language (default: 'zh-CN')
)
```

**Time Index Reference:**
| Index | Time Range | Chinese Name |
|-------|------------|--------------|
| 0 | 00:00-01:00 | 早子时 |
| 1 | 01:00-03:00 | 丑时 |
| 2 | 03:00-05:00 | 寅时 |
| 3 | 05:00-07:00 | 卯时 |
| 4 | 07:00-09:00 | 辰时 |
| 5 | 09:00-11:00 | 巳时 |
| 6 | 11:00-13:00 | 午时 |
| 7 | 13:00-15:00 | 未时 |
| 8 | 15:00-17:00 | 申时 |
| 9 | 17:00-19:00 | 酉时 |
| 10 | 19:00-21:00 | 戌时 |
| 11 | 21:00-23:00 | 亥时 |
| 12 | 23:00-00:00 | 晚子时 |

### `astro.by_lunar()`

Create an astrolabe from a lunar (Chinese) date.

```python
chart = astro.by_lunar(
    lunar_date='2000-7-17',  # Lunar date string
    time_index=6,
    gender='男',
    is_leap_month=False,     # Is leap month (default: False)
    fix_leap=True,
    language='zh-CN'
)
```

## FunctionalAstrolabe Class

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `gender` | str | Gender |
| `solar_date` | str | Solar date |
| `lunar_date` | str | Lunar date |
| `chinese_date` | str | Chinese date (四柱) |
| `zodiac` | str | Chinese zodiac |
| `sign` | str | Western zodiac sign |
| `five_elements_class` | str | Five elements class |
| `palaces` | List[FunctionalPalace] | 12 palaces |

### Methods

#### `palace(index_or_name)`

Get a palace by index or name.

```python
# By index
palace = chart.palace(0)

# By English name
palace = chart.palace('soulPalace')

# By Chinese name
palace = chart.palace('命宫')
```

#### `star(star_name)`

Find a star by name.

```python
ziwei = chart.star('ziweiMaj')
# or
ziwei = chart.star('紫微')
```

#### `surrounded_palaces(index_or_name)`

Get the three-sided palaces (三方四正).

```python
surpalaces = chart.surrounded_palaces(0)
# Returns: target, opposite, wealth, career palaces
```

#### `get_soul_palace()`

Get the soul palace (命宫).

```python
soul = chart.get_soul_palace()
```

#### `get_body_palace()`

Get the body palace (身宫).

```python
body = chart.get_body_palace()
```

#### `horoscope(solar_date, time_index=0)`

Get horoscope for a specific date.

```python
horoscope = chart.horoscope('2024-1-1', 6)
print(horoscope.decadal)  # 大限
print(horoscope.yearly)   # 流年
```

## FunctionalPalace Class

### Methods

#### `has(stars)`

Check if palace contains all specified stars.

```python
palace.has(['ziweiMaj', 'tianfuMaj'])
```

#### `has_one_of(stars)`

Check if palace contains any of the specified stars.

```python
palace.has_one_of(['ziweiMaj', 'tianfuMaj'])
```

#### `has_mutagen(mutagen)`

Check if palace has a star with the specified mutagen.

```python
palace.has_mutagen('禄')  # 化禄
palace.has_mutagen('忌')  # 化忌
```

#### `is_empty()`

Check if palace has no major stars.

```python
if palace.is_empty():
    print("Empty palace")
```

## FunctionalStar Class

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `name` | str | Star name |
| `type` | str | Star type (major/soft/tough) |
| `brightness` | str | Brightness level |
| `mutagen` | str | Mutagen (四化) |

### Methods

#### `palace()`

Get the palace where this star is located.

```python
palace = star.palace()
```

#### `is_bright()`

Check if star has good brightness (庙/旺).

```python
if star.is_bright():
    print("Star is bright")
```

#### `surrounded_palaces()`

Get the three-sided palaces of this star's location.

```python
surpalaces = star.surrounded_palaces()
```

## Supported Languages

| Code | Language |
|------|----------|
| `zh-CN` | 简体中文 |
| `zh-TW` | 繁體中文 |
| `en-US` | English |
| `ja-JP` | 日本語 |
| `ko-KR` | 한국어 |
| `vi-VN` | Tiếng Việt |
