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

from typing import Dict, Any, Optional

# 当前语言设置
_current_language = "zh-CN"

# 语言资源缓存
_locales: Dict[str, Dict[str, Any]] = {}


def set_language(lang: str) -> None:
    """
    设置当前语言

    Args:
        lang: 语言代码，支持 'zh-CN', 'zh-TW', 'en-US', 'ja-JP', 'ko-KR', 'vi-VN'
              不支持的语言将降级为 'zh-CN'
    """
    global _current_language
    supported = ["zh-CN", "zh-TW", "en-US", "ja-JP", "ko-KR", "vi-VN"]

    # 如果语言不支持，降级到中文，但不报错
    if lang not in supported:
        import warnings

        warnings.warn(
            f"Language '{lang}' is not fully supported yet. Falling back to 'zh-CN'. Supported: {supported}",
            UserWarning,
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
    except ImportError:
        raise ValueError(f"Language resource not found: {lang}")


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

    # 支持嵌套键，如 'palaces.soulPalace'
    keys = key.split(".")
    value = locale
    for k in keys:
        if isinstance(value, dict):
            value = value.get(k, key)
        else:
            return key

    return value if isinstance(value, str) else key


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


# 默认加载中文
_load_locale("zh-CN")


__all__ = ["set_language", "get_language", "t", "translate_dict"]
