#!/usr/bin/env python3
"""Regenerate iztro_py locale modules from the iztro@2.5.8 reference locales.

zh-CN keeps its existing values (authoritative, avoids churn); the other five
languages are sourced from iztro so the 84 previously-missing sections stop
falling back to Simplified Chinese.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, "/home/user/iztro-py/src")
from iztro_py.i18n.locales import zh_CN  # noqa: E402

SCRATCH = Path(__file__).resolve().parent
OUT = Path("/home/user/iztro-py/src/iztro_py/i18n/locales")
L = json.loads((SCRATCH / "iztro_locales.json").read_text())

LANGS = {
    "zh-CN": ("zh_CN", "简体中文"),
    "zh-TW": ("zh_TW", "繁體中文"),
    "en-US": ("en_US", "English"),
    "ja-JP": ("ja_JP", "日本語"),
    "ko-KR": ("ko_KR", "한국어"),
    "vi-VN": ("vi_VN", "Tiếng Việt"),
}

# Our key -> iztro key, where the two spell the same concept differently.
RENAMED = {
    "dahaoAdj": "dahao",
    "enguang": "engguang",
    "tianfuAdj": "tianfu",
    "xishenJiang": "xiishen",
}

# New sections, keyed by our key -> iztro key.
TIME_KEYS = [
    "earlyRatHour",
    "oxHour",
    "tigerHour",
    "rabbitHour",
    "dragonHour",
    "snakeHour",
    "horseHour",
    "goatHour",
    "monkeyHour",
    "roosterHour",
    "dogHour",
    "pigHour",
    "lateRatHour",
]
ZODIAC_KEYS = [
    "rat",
    "ox",
    "tiger",
    "rabbit",
    "dragon",
    "snake",
    "horse",
    "sheep",
    "monkey",
    "rooster",
    "dog",
    "pig",
]
SIGN_KEYS = [
    "aries",
    "taurus",
    "gemini",
    "cancer",
    "leo",
    "virgo",
    "libra",
    "scorpio",
    "sagittarius",
    "capricorn",
    "aquarius",
    "pisces",
]
FEC_KEYS = ["water2nd", "wood3rd", "metal4th", "earth5th", "fire6th"]
GENDER_KEYS = ["male", "female"]

NESTED = ["palaces", "heavenlyStem", "earthlyBranch"]

# brightness was never a gap — all six languages already had real translations,
# whereas iztro renders it as a score notation ('[+3]'). Preserved verbatim.
BRIGHTNESS = {
    "zh-CN": ["庙", "旺", "得", "利", "平", "不", "陷"],
    "zh-TW": ["廟", "旺", "得", "利", "平", "不", "陷"],
    "en-US": [
        "Temple",
        "Prosperous",
        "Favorable",
        "Beneficial",
        "Neutral",
        "Unfavorable",
        "Trapped",
    ],
    "ja-JP": ["廟", "旺", "得", "利", "平", "不", "陷"],
    "ko-KR": ["묘", "왕", "득", "리", "평", "불", "함"],
    "vi-VN": ["Miếu", "Vượng", "Đắc", "Lợi", "Bình", "Bất", "Hãm"],
}
BRIGHTNESS_KEYS = ["miao", "wang", "de", "li", "ping", "bu", "xian"]


def lookup(lang, our_key):
    src = L[lang]
    key = RENAMED.get(our_key, our_key)
    return src.get(key)


def build(lang):
    ours = zh_CN.translations
    out = {}

    for section in NESTED:
        entries = {}
        for k in ours[section]:
            v = ours[section][k] if lang == "zh-CN" else lookup(lang, k)
            entries[k] = v if v is not None else ours[section][k]
        out[section] = entries

    out["brightness"] = dict(zip(BRIGHTNESS_KEYS, BRIGHTNESS[lang]))

    stars = {}
    for sub in ("major", "minor"):
        entries = {}
        for k in ours["stars"][sub]:
            v = ours["stars"][sub][k] if lang == "zh-CN" else lookup(lang, k)
            entries[k] = v if v is not None else ours["stars"][sub][k]
        stars[sub] = entries
    out["stars"] = stars

    for name, keys in (
        ("time", TIME_KEYS),
        ("zodiac", ZODIAC_KEYS),
        ("sign", SIGN_KEYS),
        ("fiveElementsClass", FEC_KEYS),
        ("gender", GENDER_KEYS),
    ):
        out[name] = {k: L[lang][k] for k in keys}

    # Flat adjective / decorative-god keys.
    flat = {}
    for k, v in ours.items():
        if isinstance(v, dict):
            continue
        if lang == "zh-CN":
            flat[k] = v
        else:
            got = lookup(lang, k)
            flat[k] = got if got is not None else v
    out["_flat"] = flat
    return out


def render(lang):
    mod, label = LANGS[lang]
    data = build(lang)
    flat = data.pop("_flat")
    lines = [
        "# -*- coding: utf-8 -*-",
        f'"""{label} language resources ({lang}).',
        "",
        "Generated from the iztro@2.5.8 reference locales; zh-CN values are the",
        "project's own. Regenerate rather than hand-editing when syncing a new",
        "iztro release.",
        '"""',
        "",
        "translations = {",
    ]

    def emit(name, entries, indent="    "):
        lines.append(f'{indent}"{name}": {{')
        for k, v in entries.items():
            lines.append(f'{indent}    "{k}": "{v}",')
        lines.append(f"{indent}}},")

    emit("palaces", data["palaces"])
    lines.append('    "stars": {')
    for sub in ("major", "minor"):
        emit(sub, data["stars"][sub], indent="        ")
    lines.append("    },")
    for name in (
        "heavenlyStem",
        "earthlyBranch",
        "brightness",
        "time",
        "zodiac",
        "sign",
        "fiveElementsClass",
        "gender",
    ):
        emit(name, data[name])

    lines.append("    # 杂曜、长生/博士/将前/岁前十二神")
    for k, v in flat.items():
        lines.append(f'    "{k}": "{v}",')
    lines.append("}")
    lines.append("")
    return "\n".join(lines)


for lang, (mod, _) in LANGS.items():
    path = OUT / f"{mod}.py"
    path.write_text(render(lang), encoding="utf-8")
    print(f"wrote {path.name}")
