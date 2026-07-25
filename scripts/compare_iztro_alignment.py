#!/usr/bin/env python3
"""
Compare iztro_py against iztro@2.5.8 for core birth-chart alignment.

Core fields are treated as blocking:
- lunar/chinese date
- five elements class
- soul/body palace anchors
- 12-palace major/minor stars (含亮度) and adjective stars
- changsheng12/boshi12/jiangqian12/suiqian12
- decadal ranges and age anchors
- horoscope anchors: decadal/age/yearly/monthly/daily/hourly indices,
  nominal age, and decadal/yearly mutagen

Cases cover both genders, 春节-立春 window births, leap-month births,
late-rat-hour births, and horoscope targets across lunar-year boundaries.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Sequence


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from iztro_py import astro  # noqa: E402


EXPECTED_JS_VERSION = "2.5.8"


def _resolve_js_package_path() -> Path:
    candidate_paths = []
    env_path = os.environ.get("IZTRO_JS_PACKAGE")
    if env_path:
        candidate_paths.append(Path(env_path))
    candidate_paths.extend(
        [
            Path(f"/tmp/iztro-{EXPECTED_JS_VERSION}/node_modules/iztro"),
            REPO_ROOT / "node_modules" / "iztro",
        ]
    )

    problems = []
    for path in candidate_paths:
        package_json = path / "package.json"
        if not package_json.exists():
            problems.append(f"{path} (missing package.json)")
            continue
        try:
            package = json.loads(package_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            problems.append(f"{path} (invalid package.json: {exc})")
            continue

        version = package.get("version")
        if version != EXPECTED_JS_VERSION:
            problems.append(f"{path} (found {version}, expected {EXPECTED_JS_VERSION})")
            continue

        # A matching package.json is not enough: the package must actually be
        # requireable. A partial checkout (e.g. one where the compiled `lib/`
        # was excluded) has valid metadata but no code, and would otherwise
        # only fail much later with an opaque MODULE_NOT_FOUND.
        main_entry = package.get("main", "index.js")
        if not (path / main_entry).exists():
            problems.append(f"{path} (incomplete: missing main entry {main_entry!r})")
            continue

        return path

    searched = "\n".join(f"- {problem}" for problem in problems) or "- <no candidates>"
    raise FileNotFoundError(
        "Unable to locate a usable iztro JS reference package.\n"
        f"Expected version: {EXPECTED_JS_VERSION}\n"
        "Searched:\n"
        f"{searched}\n"
        "Install it with `npm install` (repo root) or "
        f"`npm install --prefix /tmp/iztro-{EXPECTED_JS_VERSION} iztro@{EXPECTED_JS_VERSION}`, "
        "or set IZTRO_JS_PACKAGE to a directory containing iztro's package.json."
    )


JS_PACKAGE_PATH = _resolve_js_package_path()


CASES: List[Dict[str, Any]] = [
    {
        "label": "1990-10-21 00:30 女",
        "solar_date": "1990-10-21",
        "time_index": 0,
        "gender": "女",
        "source_time": "00:30",
    },
    {
        "label": "1990-10-21 15:00 女",
        "solar_date": "1990-10-21",
        "time_index": 8,
        "gender": "女",
        "source_time": "15:00",
    },
    {
        "label": "1990-10-21 15:30 女",
        "solar_date": "1990-10-21",
        "time_index": 8,
        "gender": "女",
        "source_time": "15:30",
    },
    {
        "label": "1990-10-21 16:59 女",
        "solar_date": "1990-10-21",
        "time_index": 8,
        "gender": "女",
        "source_time": "16:59",
    },
    {
        "label": "1990-10-21 23:30 女",
        "solar_date": "1990-10-21",
        "time_index": 12,
        "gender": "女",
        "source_time": "23:30",
    },
    {
        "label": "2000-02-29 15:30 女",
        "solar_date": "2000-02-29",
        "time_index": 8,
        "gender": "女",
        "source_time": "15:30",
    },
    {
        # 男命，大限顺行方向
        "label": "1990-10-21 15:30 男",
        "solar_date": "1990-10-21",
        "time_index": 8,
        "gender": "男",
        "source_time": "15:30",
    },
    {
        # 出生日落在春节（1-23）与立春（2-4）之间：验证年柱以正月初一分界
        "label": "1993-02-03 12:30 男",
        "solar_date": "1993-02-03",
        "time_index": 6,
        "gender": "男",
        "source_time": "12:30",
    },
    {
        # 闰二月上半月出生
        "label": "2023-03-25 08:30 男",
        "solar_date": "2023-03-25",
        "time_index": 4,
        "gender": "男",
        "source_time": "08:30",
    },
    {
        # 闰二月下半月 + 晚子时出生
        "label": "2023-04-10 23:30 女",
        "solar_date": "2023-04-10",
        "time_index": 12,
        "gender": "女",
        "source_time": "23:30",
    },
    {
        # 元旦-春节间出生（农历仍是己卯年），运限目标日跨农历年：验证虚岁按农历年差
        "label": "2000-01-20 12:30 男 → 2024-06-01",
        "solar_date": "2000-01-20",
        "time_index": 6,
        "gender": "男",
        "source_time": "12:30",
        "horoscope_date": "2024-06-01",
        "horoscope_time_index": 6,
    },
    {
        # 运限目标日在元旦-春节之间（农历仍是癸卯年）：验证运限分界与虚岁
        "label": "2000-08-16 12:30 男 → 2024-01-15",
        "solar_date": "2000-08-16",
        "time_index": 6,
        "gender": "男",
        "source_time": "12:30",
        "horoscope_date": "2024-01-15",
        "horoscope_time_index": 6,
    },
]


def _normalize_python(case: Dict[str, Any]) -> Dict[str, Any]:
    chart = astro.by_solar(case["solar_date"], case["time_index"], case["gender"])
    horoscope = chart.horoscope(
        case.get("horoscope_date", case["solar_date"]),
        case.get("horoscope_time_index", case["time_index"]),
    )

    def star_with_brightness(star: Any) -> str:
        return star.translate_name("zh-CN") + (star.brightness or "")

    def palace_dict(palace: Any) -> Dict[str, Any]:
        return {
            "index": palace.index,
            "name": _translate_palace_name(palace.name),
            "heavenly_stem": palace.translate_heavenly_stem("zh-CN"),
            "earthly_branch": palace.translate_earthly_branch("zh-CN"),
            "is_body_palace": palace.is_body_palace,
            "is_original_palace": palace.is_original_palace,
            "major_stars": [star_with_brightness(star) for star in palace.major_stars],
            "minor_stars": [star_with_brightness(star) for star in palace.minor_stars],
            "adjective_stars": [star.translate_name("zh-CN") for star in palace.adjective_stars],
            "changsheng12": palace.changsheng12,
            "boshi12": palace.boshi12,
            "jiangqian12": palace.jiangqian12,
            "suiqian12": palace.suiqian12,
            "decadal": list(palace.decadal.range) if palace.decadal else None,
            "ages": list(palace.ages),
        }

    return {
        "meta": {
            "label": case["label"],
            "solar_date": case["solar_date"],
            "source_time": case["source_time"],
            "time_index": case["time_index"],
            "gender": case["gender"],
            "timezone": "Asia/Shanghai",
            "longitude": 120.0,
        },
        "lunar_date": chart.lunar_date,
        "chinese_date": chart.chinese_date,
        "five_elements_class": chart.five_elements_class,
        "soul_palace": palace_dict(chart.get_soul_palace()),
        "body_palace": palace_dict(chart.get_body_palace()),
        "palaces": [palace_dict(palace) for palace in chart.palaces],
        "horoscope": {
            "nominal_age": horoscope.nominal_age,
            "decadal": {
                "index": horoscope.decadal.index,
                "name": horoscope.decadal.name,
                "palace_names": [_translate_palace_name(name) for name in horoscope.decadal.palace_names],
                "mutagen": [_translate_star_name(name) for name in horoscope.decadal.mutagen],
            },
            "age": {
                "index": horoscope.age.index,
            },
            "yearly": {
                "index": horoscope.yearly.index,
                "name": horoscope.yearly.name,
                "palace_names": [_translate_palace_name(name) for name in horoscope.yearly.palace_names],
                "mutagen": [_translate_star_name(name) for name in horoscope.yearly.mutagen],
            },
            "monthly": {"index": horoscope.monthly.index},
            "daily": {"index": horoscope.daily.index},
            "hourly": {"index": horoscope.hourly.index},
        },
    }


def _normalize_js(case: Dict[str, Any]) -> Dict[str, Any]:
    payload = json.dumps(case, ensure_ascii=False)
    script = f"""
const iztro = require({json.dumps(str(JS_PACKAGE_PATH))});
const payload = JSON.parse(process.argv[1]);
const chart = iztro.astro.bySolar(payload.solar_date, payload.time_index, payload.gender, true, 'zh-CN');
const horoscopeDate = payload.horoscope_date || payload.solar_date;
const horoscopeTimeIndex = payload.horoscope_time_index !== undefined
  ? payload.horoscope_time_index
  : payload.time_index;
const horoscope = chart.horoscope(horoscopeDate, horoscopeTimeIndex);

function starWithBrightness(star) {{
  return star.name + (star.brightness || '');
}}

function palaceDict(palace) {{
  return {{
    index: palace.index,
    name: palace.name,
    heavenly_stem: palace.heavenlyStem,
    earthly_branch: palace.earthlyBranch,
    is_body_palace: palace.isBodyPalace,
    is_original_palace: palace.isOriginalPalace,
    major_stars: palace.majorStars.map(starWithBrightness),
    minor_stars: palace.minorStars.map(starWithBrightness),
    adjective_stars: palace.adjectiveStars.map((star) => star.name),
    changsheng12: palace.changsheng12,
    boshi12: palace.boshi12,
    jiangqian12: palace.jiangqian12,
    suiqian12: palace.suiqian12,
    decadal: palace.decadal ? palace.decadal.range : null,
    ages: palace.ages,
  }};
}}

console.log(JSON.stringify({{
  meta: {{
    label: payload.label,
    solar_date: payload.solar_date,
    source_time: payload.source_time,
    time_index: payload.time_index,
    gender: payload.gender,
    timezone: 'Asia/Shanghai',
    longitude: 120.0,
  }},
  lunar_date: chart.lunarDate,
  chinese_date: chart.chineseDate,
  five_elements_class: chart.fiveElementsClass,
  soul_palace: palaceDict(chart.palace('命宫')),
  body_palace: palaceDict(chart.palace('身宫')),
  palaces: chart.palaces.map(palaceDict),
  horoscope: {{
    nominal_age: horoscope.age.nominalAge,
    decadal: {{
      index: horoscope.decadal.index,
      name: horoscope.decadal.name,
      palace_names: horoscope.decadal.palaceNames,
      mutagen: horoscope.decadal.mutagen,
    }},
    age: {{
      index: horoscope.age.index,
    }},
    yearly: {{
      index: horoscope.yearly.index,
      name: horoscope.yearly.name,
      palace_names: horoscope.yearly.palaceNames,
      mutagen: horoscope.yearly.mutagen,
    }},
    monthly: {{ index: horoscope.monthly.index }},
    daily: {{ index: horoscope.daily.index }},
    hourly: {{ index: horoscope.hourly.index }},
  }},
}}, null, 2));
"""
    result = subprocess.run(
        ["node", "-e", script, payload],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        # Do NOT let CalledProcessError surface here: it stringifies the whole
        # inlined JS program and buries node's actual error (e.g. a broken or
        # partially-installed iztro package).
        raise RuntimeError(
            f"node failed for case {case['label']!r} (exit {result.returncode}) "
            f"using iztro at {JS_PACKAGE_PATH}\n"
            f"--- stderr ---\n{result.stderr.strip() or '<empty>'}"
        )
    return json.loads(result.stdout)


def _translate_palace_name(name: str) -> str:
    mapping = {
        "soulPalace": "命宫",
        "parentsPalace": "父母",
        "spiritPalace": "福德",
        "propertyPalace": "田宅",
        "careerPalace": "官禄",
        "friendsPalace": "仆役",
        "surfacePalace": "迁移",
        "healthPalace": "疾厄",
        "wealthPalace": "财帛",
        "childrenPalace": "子女",
        "spousePalace": "夫妻",
        "siblingsPalace": "兄弟",
    }
    return mapping.get(name, name)


def _translate_star_name(name: str) -> str:
    mapping = {
        "ziweiMaj": "紫微",
        "tianjiMaj": "天机",
        "taiyangMaj": "太阳",
        "wuquMaj": "武曲",
        "tiantongMaj": "天同",
        "lianzhenMaj": "廉贞",
        "tianfuMaj": "天府",
        "taiyinMaj": "太阴",
        "tanlangMaj": "贪狼",
        "jumenMaj": "巨门",
        "tianxiangMaj": "天相",
        "tianliangMaj": "天梁",
        "qishaMaj": "七杀",
        "pojunMaj": "破军",
        "zuofuMin": "左辅",
        "youbiMin": "右弼",
        "wenchangMin": "文昌",
        "wenquMin": "文曲",
        "tiankuiMin": "天魁",
        "tianyueMin": "天钺",
        "huoxingMin": "火星",
        "lingxingMin": "铃星",
        "dikongMin": "地空",
        "dijieMin": "地劫",
        "lucunMin": "禄存",
        "qingyangMin": "擎羊",
        "tuoluoMin": "陀罗",
        "tianmaMin": "天马",
        "huagai": "华盖",
        "xianchi": "咸池",
        "guchen": "孤辰",
        "guasu": "寡宿",
        "tiancai": "天才",
        "tianshou": "天寿",
        "hongluan": "红鸾",
        "tianxi": "天喜",
        "tianxing": "天刑",
        "tianyao": "天姚",
        "jieshen": "解神",
        "yinsha": "阴煞",
        "tianguan": "天官",
        "tianfuAdj": "天福",
        "tianku": "天哭",
        "tianxu": "天虚",
        "longchi": "龙池",
        "fengge": "凤阁",
        "feilian": "蜚廉",
        "posui": "破碎",
        "tianchu": "天厨",
        "santai": "三台",
        "bazuo": "八座",
        "enguang": "恩光",
        "tiangui": "天贵",
        "taifu": "台辅",
        "fenggao": "封诰",
        "tianwu": "天巫",
        "tianyue": "天月",
        "tiande": "天德",
        "yuede": "月德",
        "tiankong": "天空",
        "xunkong": "旬空",
        "jielu": "截路",
        "kongwang": "空亡",
        "longde": "龙德",
        "jiekong": "截空",
        "jieshaAdj": "劫煞",
        "dahaoAdj": "大耗",
        "tianshi": "天使",
        "tianshang": "天伤",
        "nianjie": "年解",
    }
    return mapping.get(name, name)


def _project_core(data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "lunar_date": data["lunar_date"],
        "chinese_date": data["chinese_date"],
        "five_elements_class": data["five_elements_class"],
        "soul_palace": {
            "index": data["soul_palace"]["index"],
            "name": data["soul_palace"]["name"],
            "earthly_branch": data["soul_palace"]["earthly_branch"],
            "major_stars": data["soul_palace"]["major_stars"],
        },
        "body_palace": {
            "index": data["body_palace"]["index"],
            "name": data["body_palace"]["name"],
            "earthly_branch": data["body_palace"]["earthly_branch"],
        },
        "palaces": [
            {
                "index": palace["index"],
                "name": palace["name"],
                "heavenly_stem": palace["heavenly_stem"],
                "earthly_branch": palace["earthly_branch"],
                "is_body_palace": palace["is_body_palace"],
                "is_original_palace": palace["is_original_palace"],
                "major_stars": palace["major_stars"],
                "minor_stars": palace["minor_stars"],
                "adjective_stars": palace["adjective_stars"],
                "changsheng12": palace["changsheng12"],
                "boshi12": palace["boshi12"],
                "jiangqian12": palace["jiangqian12"],
                "suiqian12": palace["suiqian12"],
                "decadal": palace["decadal"],
                "ages": palace["ages"],
            }
            for palace in data["palaces"]
        ],
        "horoscope": data["horoscope"],
    }


def _diff(prefix: str, left: Any, right: Any) -> List[str]:
    if type(left) is not type(right):
        return [f"{prefix}: type {type(left).__name__} != {type(right).__name__}"]
    if isinstance(left, dict):
        diffs: List[str] = []
        for key in sorted(set(left) | set(right)):
            if key not in left:
                diffs.append(f"{prefix}.{key}: missing on left")
            elif key not in right:
                diffs.append(f"{prefix}.{key}: missing on right")
            else:
                diffs.extend(_diff(f"{prefix}.{key}", left[key], right[key]))
        return diffs
    if isinstance(left, list):
        if len(left) != len(right):
            return [f"{prefix}: len {len(left)} != {len(right)}"]
        diffs: List[str] = []
        for index, (l_item, r_item) in enumerate(zip(left, right)):
            diffs.extend(_diff(f"{prefix}[{index}]", l_item, r_item))
        return diffs
    if left != right:
        return [f"{prefix}: {left!r} != {right!r}"]
    return []


def main(selected_labels: Sequence[str] | None = None) -> int:
    selected = set(selected_labels or [])
    cases = [case for case in CASES if not selected or case["label"] in selected]

    summary = []
    blocking_failure = False

    for case in cases:
        python_data = _normalize_python(case)
        js_data = _normalize_js(case)
        blocking_diffs = _diff("core", _project_core(python_data), _project_core(js_data))

        if blocking_diffs:
            blocking_failure = True

        summary.append(
            {
                "case": case["label"],
                "blocking_diffs": blocking_diffs,
                "python": python_data,
                "js": js_data,
            }
        )

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1 if blocking_failure else 0


if __name__ == "__main__":
    labels = sys.argv[1:]
    raise SystemExit(main(labels))
