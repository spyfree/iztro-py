"""
Horoscope calculation module - 运势系统

Implements decadal (大限), yearly (流年), monthly (流月),
daily (流日), and hourly (流时) horoscope calculations.
"""

from typing import List, Optional
from datetime import datetime

from iztro_py.data.types import (
    Horoscope,
    HoroscopeItem,
    PalaceName,
    StarName,
    HeavenlyStemName,
    EarthlyBranchName,
    FiveElementsClass,
    Palace,
)
from iztro_py.utils.calendar import (
    solar_to_lunar,
    get_heavenly_stem_and_earthly_branch_date,
    format_lunar_date,
)
from iztro_py.utils.helpers import (
    get_decadal_palace_index,
    get_decadal_range,
    calculate_nominal_age,
    fix_index,
)
from iztro_py.data.constants import HEAVENLY_STEMS, EARTHLY_BRANCHES, fix_index as const_fix_index


def get_horoscope(
    solar_date_str: str,
    time_index: int,
    palaces: List[Palace],
    soul_palace_index: int,
    five_elements_class: FiveElementsClass,
    gender: str,
    year_branch_yin_yang: str,
    birth_year: int,
) -> Horoscope:
    """
    获取指定日期的运势信息

    Args:
        solar_date_str: 阳历日期 (YYYY-M-D or YYYY-MM-DD)
        time_index: 时辰索引 (0-12)
        palaces: 宫位列表
        soul_palace_index: 命宫索引
        five_elements_class: 五行局
        gender: 性别
        year_branch_yin_yang: 出生年支阴阳
        birth_year: 出生年份

    Returns:
        完整的运势信息
    """
    # 解析日期
    parts = solar_date_str.split("-")
    year = int(parts[0])
    month = int(parts[1])
    day = int(parts[2]) if len(parts) > 2 else 1

    # 转换为农历
    lunar_info = solar_to_lunar(year, month, day)
    lunar_date = format_lunar_date(lunar_info)

    # 获取四柱
    stems_branches = get_heavenly_stem_and_earthly_branch_date(year, month, day, time_index)
    year_stem = stems_branches.year_stem
    year_branch = stems_branches.year_branch
    month_stem = stems_branches.month_stem
    month_branch = stems_branches.month_branch
    day_stem = stems_branches.day_stem
    day_branch = stems_branches.day_branch
    hour_stem = stems_branches.time_stem
    hour_branch = stems_branches.time_branch

    # 计算虚岁
    nominal_age = calculate_nominal_age(birth_year, year)

    # 大限
    decadal = get_decadal_horoscope(
        nominal_age,
        five_elements_class,
        soul_palace_index,
        gender,
        year_branch_yin_yang,
        palaces,
        year_stem,
    )

    # 小限
    age_horoscope = get_age_horoscope(nominal_age, soul_palace_index, gender, palaces, year_stem)

    # 流年
    yearly = get_yearly_horoscope(year_branch, year_stem, palaces, year_stem)

    # 流月
    monthly = get_monthly_horoscope(month_branch, month_stem, palaces, year_stem)

    # 流日
    daily = get_daily_horoscope(day_branch, day_stem, palaces, year_stem)

    # 流时
    hourly = get_hourly_horoscope(hour_branch, hour_stem, palaces, year_stem)

    return Horoscope(
        solar_date=solar_date_str,
        lunar_date=lunar_date,
        decadal=decadal,
        age=age_horoscope,
        yearly=yearly,
        monthly=monthly,
        daily=daily,
        hourly=hourly,
        nominal_age=nominal_age,
    )


def get_decadal_horoscope(
    age: int,
    five_elements_class: FiveElementsClass,
    soul_palace_index: int,
    gender: str,
    year_branch_yin_yang: str,
    palaces: List[Palace],
    year_stem: HeavenlyStemName,
) -> HoroscopeItem:
    """
    获取大限信息

    大限从命宫开始，每个宫位管10年
    男阳女阴顺行，男阴女阳逆行

    Args:
        age: 虚岁
        five_elements_class: 五行局
        soul_palace_index: 命宫索引
        gender: 性别
        year_branch_yin_yang: 年支阴阳
        palaces: 宫位列表
        year_stem: 流年天干（用于计算四化）

    Returns:
        大限运势项
    """
    # 获取大限宫位索引
    palace_index = get_decadal_palace_index(
        age, five_elements_class, soul_palace_index, gender, year_branch_yin_yang
    )

    # 获取大限年龄范围
    age_range = get_decadal_range(
        five_elements_class, palace_index, gender, soul_palace_index, year_branch_yin_yang
    )

    # 获取宫位信息
    palace = palaces[palace_index]

    # 获取大限四化（使用大限宫的天干）
    decadal_mutagen = _get_mutagen_stars(palace.heavenly_stem)

    # 获取大限所在的宫位名称列表（大限宫本身）
    palace_names = [palace.name]

    return HoroscopeItem(
        index=palace_index,
        name=f"{age_range[0]}-{age_range[1]}岁",
        heavenly_stem=palace.heavenly_stem,
        earthly_branch=palace.earthly_branch,
        palace_names=palace_names,
        mutagen=decadal_mutagen,
        stars=None,  # 大限不安流耀
    )


def get_age_horoscope(
    age: int,
    soul_palace_index: int,
    gender: str,
    palaces: List[Palace],
    year_stem: HeavenlyStemName,
) -> HoroscopeItem:
    """
    获取小限信息

    小限从命宫起，男顺女逆，每年走一宫

    Args:
        age: 虚岁
        soul_palace_index: 命宫索引
        gender: 性别
        palaces: 宫位列表
        year_stem: 流年天干

    Returns:
        小限运势项
    """
    # 小限从1岁开始
    # 男命顺行，女命逆行
    if gender == "男":
        palace_index = fix_index(soul_palace_index + age - 1)
    else:
        palace_index = fix_index(soul_palace_index - age + 1)

    palace = palaces[palace_index]

    # 小限四化（使用小限宫的天干）
    age_mutagen = _get_mutagen_stars(palace.heavenly_stem)

    return HoroscopeItem(
        index=palace_index,
        name=f"{age}岁",
        heavenly_stem=palace.heavenly_stem,
        earthly_branch=palace.earthly_branch,
        palace_names=[palace.name],
        mutagen=age_mutagen,
        stars=None,
    )


def get_yearly_horoscope(
    year_branch: EarthlyBranchName,
    year_stem: HeavenlyStemName,
    palaces: List[Palace],
    birth_year_stem: HeavenlyStemName,
) -> HoroscopeItem:
    """
    获取流年信息

    流年从年支地支位置开始安命宫

    Args:
        year_branch: 流年地支
        year_stem: 流年天干
        palaces: 宫位列表
        birth_year_stem: 出生年天干

    Returns:
        流年运势项
    """
    # 流年命宫在年支所在的地支位置
    branch_index = _get_branch_index(year_branch)

    # 找到该地支对应的宫位
    palace_index = -1
    for i, palace in enumerate(palaces):
        if _get_branch_index(palace.earthly_branch) == branch_index:
            palace_index = i
            break

    if palace_index == -1:
        palace_index = 0  # fallback

    palace = palaces[palace_index]

    # 流年四化（使用流年天干）
    yearly_mutagen = _get_mutagen_stars(year_stem)

    # 流年宫位名称（流年命宫在本命哪个宫）
    palace_names = [palace.name]

    return HoroscopeItem(
        index=palace_index,
        name=f"{_get_stem_name(year_stem)}{_get_branch_name(year_branch)}年",
        heavenly_stem=year_stem,
        earthly_branch=year_branch,
        palace_names=palace_names,
        mutagen=yearly_mutagen,
        stars=None,  # 可以扩展添加流年星
    )


def get_monthly_horoscope(
    month_branch: EarthlyBranchName,
    month_stem: HeavenlyStemName,
    palaces: List[Palace],
    year_stem: HeavenlyStemName,
) -> HoroscopeItem:
    """
    获取流月信息

    Args:
        month_branch: 流月地支
        month_stem: 流月天干
        palaces: 宫位列表
        year_stem: 流年天干

    Returns:
        流月运势项
    """
    branch_index = _get_branch_index(month_branch)

    palace_index = -1
    for i, palace in enumerate(palaces):
        if _get_branch_index(palace.earthly_branch) == branch_index:
            palace_index = i
            break

    if palace_index == -1:
        palace_index = 0

    palace = palaces[palace_index]
    monthly_mutagen = _get_mutagen_stars(month_stem)

    return HoroscopeItem(
        index=palace_index,
        name=f"{_get_stem_name(month_stem)}{_get_branch_name(month_branch)}月",
        heavenly_stem=month_stem,
        earthly_branch=month_branch,
        palace_names=[palace.name],
        mutagen=monthly_mutagen,
        stars=None,
    )


def get_daily_horoscope(
    day_branch: EarthlyBranchName,
    day_stem: HeavenlyStemName,
    palaces: List[Palace],
    year_stem: HeavenlyStemName,
) -> HoroscopeItem:
    """
    获取流日信息

    Args:
        day_branch: 流日地支
        day_stem: 流日天干
        palaces: 宫位列表
        year_stem: 流年天干

    Returns:
        流日运势项
    """
    branch_index = _get_branch_index(day_branch)

    palace_index = -1
    for i, palace in enumerate(palaces):
        if _get_branch_index(palace.earthly_branch) == branch_index:
            palace_index = i
            break

    if palace_index == -1:
        palace_index = 0

    palace = palaces[palace_index]
    daily_mutagen = _get_mutagen_stars(day_stem)

    return HoroscopeItem(
        index=palace_index,
        name=f"{_get_stem_name(day_stem)}{_get_branch_name(day_branch)}日",
        heavenly_stem=day_stem,
        earthly_branch=day_branch,
        palace_names=[palace.name],
        mutagen=daily_mutagen,
        stars=None,
    )


def get_hourly_horoscope(
    hour_branch: EarthlyBranchName,
    hour_stem: HeavenlyStemName,
    palaces: List[Palace],
    year_stem: HeavenlyStemName,
) -> HoroscopeItem:
    """
    获取流时信息

    Args:
        hour_branch: 流时地支
        hour_stem: 流时天干
        palaces: 宫位列表
        year_stem: 流年天干

    Returns:
        流时运势项
    """
    branch_index = _get_branch_index(hour_branch)

    palace_index = -1
    for i, palace in enumerate(palaces):
        if _get_branch_index(palace.earthly_branch) == branch_index:
            palace_index = i
            break

    if palace_index == -1:
        palace_index = 0

    palace = palaces[palace_index]
    hourly_mutagen = _get_mutagen_stars(hour_stem)

    return HoroscopeItem(
        index=palace_index,
        name=f"{_get_stem_name(hour_stem)}{_get_branch_name(hour_branch)}时",
        heavenly_stem=hour_stem,
        earthly_branch=hour_branch,
        palace_names=[palace.name],
        mutagen=hourly_mutagen,
        stars=None,
    )


# ============================================================================
# Helper Functions
# ============================================================================


def _get_mutagen_stars(stem: HeavenlyStemName) -> List[StarName]:
    """
    获取指定天干的四化星

    Args:
        stem: 天干

    Returns:
        四化星列表 [禄, 权, 科, 忌]
    """
    from iztro_py.data.heavenly_stems import get_mutagen

    return get_mutagen(stem)


def _get_branch_index(branch: EarthlyBranchName) -> int:
    """获取地支索引"""
    branch_order = [
        "ziEarthly",  # 0 - 子
        "chouEarthly",  # 1 - 丑
        "yinEarthly",  # 2 - 寅
        "maoEarthly",  # 3 - 卯
        "chenEarthly",  # 4 - 辰
        "siEarthly",  # 5 - 巳
        "wuEarthly",  # 6 - 午
        "weiEarthly",  # 7 - 未
        "shenEarthly",  # 8 - 申
        "youEarthly",  # 9 - 酉
        "xuEarthly",  # 10 - 戌
        "haiEarthly",  # 11 - 亥
    ]

    try:
        return branch_order.index(branch)
    except ValueError:
        return 0


def _get_stem_name(stem: HeavenlyStemName) -> str:
    """获取天干中文名"""
    stem_names = {
        "jiaHeavenly": "甲",
        "yiHeavenly": "乙",
        "bingHeavenly": "丙",
        "dingHeavenly": "丁",
        "wuHeavenly": "戊",
        "jiHeavenly": "己",
        "gengHeavenly": "庚",
        "xinHeavenly": "辛",
        "renHeavenly": "壬",
        "guiHeavenly": "癸",
    }
    return stem_names.get(stem, stem)


def _get_branch_name(branch: EarthlyBranchName) -> str:
    """获取地支中文名"""
    branch_names = {
        "ziEarthly": "子",
        "chouEarthly": "丑",
        "yinEarthly": "寅",
        "maoEarthly": "卯",
        "chenEarthly": "辰",
        "siEarthly": "巳",
        "wuEarthly": "午",
        "weiEarthly": "未",
        "shenEarthly": "申",
        "youEarthly": "酉",
        "xuEarthly": "戌",
        "haiEarthly": "亥",
    }
    return branch_names.get(branch, branch)
