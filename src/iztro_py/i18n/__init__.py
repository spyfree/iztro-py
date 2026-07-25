"""
国际化 (i18n) 模块

提供多语言支持，默认语言为简体中文 (zh-CN)
支持的语言：
- zh-CN: 简体中文
- zh-TW: 繁體中文
- en-US: English
- ja-JP: 日本語
- ko-KR: 한국어
- vi-VN: Tiếng Việt
"""

from typing import Any, Dict, Optional

# 当前语言设置
_current_language = "zh-CN"

# 支持的语言
SUPPORTED_LANGUAGES = ["zh-CN", "zh-TW", "en-US", "ja-JP", "ko-KR", "vi-VN"]

# 语言资源缓存
_locales: Dict[str, Dict[str, Any]] = {}

# 星曜/宫位名称反查索引（任意语言译名 -> 内部 key），懒加载
_star_name_index: Optional[Dict[str, str]] = None
_palace_name_index: Optional[Dict[str, str]] = None

# 会作为 Star.name 出现的杂曜 key（顶层翻译键）
_ADJECTIVE_STAR_KEYS = [
    "hongluan",
    "tianxi",
    "tianyao",
    "xianchi",
    "jieshen",
    "santai",
    "bazuo",
    "enguang",
    "tiangui",
    "longchi",
    "fengge",
    "tiancai",
    "tianshou",
    "taifu",
    "fenggao",
    "tianwu",
    "huagai",
    "tianguan",
    "tianfuAdj",
    "tianchu",
    "tianyue",
    "tiande",
    "yuede",
    "tiankong",
    "xunkong",
    "jielu",
    "kongwang",
    "guchen",
    "guasu",
    "feilian",
    "posui",
    "tianxing",
    "yinsha",
    "tianku",
    "tianxu",
    "tianshi",
    "tianshang",
    "nianjie",
    "jieshaAdj",
    "dahaoAdj",
]


def _lookup(locale: Dict[str, Any], key: str) -> Optional[str]:
    """Return a nested translation value if present."""
    value: Any = locale
    for part in key.split("."):
        if not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    return value if isinstance(value, str) else None


def set_language(lang: str) -> None:
    """
    设置当前语言

    Args:
        lang: 语言代码，支持 'zh-CN', 'zh-TW', 'en-US', 'ja-JP', 'ko-KR', 'vi-VN'
              不支持的语言将降级为 'zh-CN'
    """
    global _current_language

    # 如果语言不支持，降级到中文，但不报错
    if lang not in SUPPORTED_LANGUAGES:
        import warnings

        warnings.warn(
            f"Language '{lang}' is not fully supported yet. Falling back to 'zh-CN'. "
            f"Supported: {SUPPORTED_LANGUAGES}",
            UserWarning,
            stacklevel=2,
        )
        lang = "zh-CN"

    _current_language = lang
    _load_locale(lang)


def get_language() -> str:
    """
    获取当前语言

    Returns:
        当前语言代码
    """
    return _current_language


def _load_locale(lang: str) -> None:
    """
    加载语言资源文件

    Args:
        lang: 语言代码
    """
    if lang in _locales:
        return

    try:
        if lang == "zh-CN":
            from .locales import zh_CN

            _locales[lang] = zh_CN.translations
        elif lang == "zh-TW":
            from .locales import zh_TW

            _locales[lang] = zh_TW.translations
        elif lang == "en-US":
            from .locales import en_US

            _locales[lang] = en_US.translations
        elif lang == "ja-JP":
            from .locales import ja_JP

            _locales[lang] = ja_JP.translations
        elif lang == "ko-KR":
            from .locales import ko_KR

            _locales[lang] = ko_KR.translations
        elif lang == "vi-VN":
            from .locales import vi_VN

            _locales[lang] = vi_VN.translations
    except ImportError as exc:
        raise ValueError(f"Language resource not found: {lang}") from exc


def t(key: str, lang: Optional[str] = None) -> str:
    """
    翻译函数

    Args:
        key: 翻译键名（英文键）
        lang: 可选，指定语言。如不指定则使用当前语言

    Returns:
        翻译后的文本
    """
    target_lang = lang or _current_language

    # 确保语言资源已加载
    if target_lang not in _locales:
        _load_locale(target_lang)

    locale = _locales.get(target_lang, {})
    value = _lookup(locale, key)
    if value is not None:
        return value

    zh_cn = _locales.get("zh-CN", {})
    fallback = _lookup(zh_cn, key)
    return fallback if fallback is not None else key


def translate_dict(data: Dict[str, Any], lang: Optional[str] = None) -> Dict[str, Any]:
    """
    翻译字典中的值

    Args:
        data: 要翻译的字典
        lang: 可选，指定语言

    Returns:
        翻译后的字典
    """
    result: Dict[str, Any] = {}
    for key, value in data.items():
        if isinstance(value, str):
            result[key] = t(value, lang)
        elif isinstance(value, dict):
            result[key] = translate_dict(value, lang)
        elif isinstance(value, list):
            result[key] = [t(v, lang) if isinstance(v, str) else v for v in value]
        else:
            result[key] = value
    return result


def normalize_star_name(name: str) -> Optional[str]:
    """
    将星曜名称归一化为内部 key（类似 iztro 的 kot）。

    接受内部 key（如 'ziweiMaj'）或任意受支持语言的译名（如 '紫微'）。
    无法识别时返回 None。
    """
    global _star_name_index
    if _star_name_index is None:
        index: Dict[str, str] = {}
        for lang in SUPPORTED_LANGUAGES:
            _load_locale(lang)
            locale = _locales.get(lang, {})
            stars = locale.get("stars", {}) if isinstance(locale.get("stars"), dict) else {}
            for section in ("major", "minor"):
                entries = stars.get(section, {})
                if isinstance(entries, dict):
                    for key, value in entries.items():
                        index.setdefault(key, key)
                        if isinstance(value, str):
                            index.setdefault(value, key)
            for key in _ADJECTIVE_STAR_KEYS:
                index.setdefault(key, key)
                value = locale.get(key)
                if isinstance(value, str):
                    index.setdefault(value, key)
        _star_name_index = index
    return _star_name_index.get(name)


def normalize_palace_name(name: str) -> Optional[str]:
    """
    将宫位名称归一化为内部 key。

    接受内部 key（如 'soulPalace'）或任意受支持语言的译名（如 '命宫'）。
    无法识别时返回 None。
    """
    global _palace_name_index
    if _palace_name_index is None:
        index: Dict[str, str] = {}
        for lang in SUPPORTED_LANGUAGES:
            _load_locale(lang)
            palaces = _locales.get(lang, {}).get("palaces", {})
            if isinstance(palaces, dict):
                for key, value in palaces.items():
                    index.setdefault(key, key)
                    if isinstance(value, str):
                        index.setdefault(value, key)
        # 常见中文别名
        index.setdefault("仆役宫", "friendsPalace")
        index.setdefault("奴仆宫", "friendsPalace")
        index.setdefault("事业宫", "careerPalace")
        _palace_name_index = index
    return _palace_name_index.get(name)


# 默认加载中文
_load_locale("zh-CN")


__all__ = [
    "set_language",
    "get_language",
    "t",
    "translate_dict",
    "normalize_star_name",
    "normalize_palace_name",
    "SUPPORTED_LANGUAGES",
]
