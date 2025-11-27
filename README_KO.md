# iztro-py

[![PyPI version](https://badge.fury.io/py/iztro-py.svg)](https://pypi.org/project/iztro-py/)
[![Python版本](https://img.shields.io/pypi/pyversions/iztro-py)](https://pypi.org/project/iztro-py/)
[![License](https://img.shields.io/pypi/l/iztro-py)](https://github.com/spyfree/iztro-py/blob/main/LICENSE)

자미두수 Python 라이브러리 - 순수 Python 구현, 다국어 출력 지원.

[简体中文](./README.md) | [English](./README_EN.md)

## 프로젝트 소개

`iztro-py`는 강력한 자미두수(紫微斗數, Purple Star Astrology) Python 라이브러리입니다. py-iztro와 달리, 이것은 **순수 Python 네이티브 구현**으로 JavaScript 인터프리터 의존성이 필요 없습니다.

### 주요 특징

- ✨ **순수 Python 구현** - JavaScript 런타임 환경 불필요
- 🌍 **다국어 지원** - 简体中文, 繁體中文, English, 日本語, 한국어, Tiếng Việt 지원
- 🔒 **타입 안전** - Pydantic 모델을 사용한 데이터 무결성 보장
- 🎯 **유창한 API** - 메서드 체이닝 지원
- 📦 **사용 편의성** - pip 한 번으로 설치

## 설치

```bash
pip install iztro-py
```

## 빠른 시작

### 기본 사용법

```python
from iztro_py import astro

# 양력 날짜로 명반 생성 (기본 한국어 출력)
chart = astro.by_solar('2000-8-16', 6, '남', language='ko-KR')

# 명궁 가져오기
soul_palace = chart.get_soul_palace()
print(f"명궁: {soul_palace.translate_name('ko-KR')}")

# 주성 조회
for star in soul_palace.major_stars:
    print(f"주성: {star.translate_name('ko-KR')}")
```

### 다국어 지원

```python
from iztro_py import astro

# 한국어
chart = astro.by_solar('2000-8-16', 6, '남', language='ko-KR')
print(chart.get_soul_palace().translate_name('ko-KR'))  # 출력: 복덕궁
```

## 지원 언어

- **zh-CN**: 简体中文 🇨🇳
- **zh-TW**: 繁體中文 🇹🇼
- **en-US**: English 🇺🇸
- **ja-JP**: 日本語 🇯🇵
- **ko-KR**: 한국어 🇰🇷
- **vi-VN**: Tiếng Việt 🇻🇳

## 문서

- [전체 사용 문서](./docs/README_zh.md)
- [API 참조](./docs/API.md)
- [예제 코드](./examples/)

## 라이선스

MIT License

## 기여

Issue와 Pull Request를 환영합니다!

---

이 프로젝트가 도움이 되셨다면 ⭐️를 눌러주세요!
