"""
Horoscope calculation module - 运势系统

Implements decadal (大限), yearly (流年), monthly (流月),
daily (流日), and hourly (流时) horoscope calculations.
"""

from typing import List, Optional

from iztro_py.data.types import (
    Horoscope,
    HoroscopeItem,
    StarName,
    HeavenlyStemName,
    EarthlyBranchName,
    FiveElementsClass,
    Palace,
    LunarDate,
)
from iztro_py.utils.calendar import (
    solar_to_lunar,
    get_heavenly_stem_and_earthly_branch_date,
    format_lunar_date,
)
from iztro_py.utils.helpers import (
    calculate_nominal_age,
    fix_index,
    fix_earthly_branch_index,
)


def get_horoscope(
    solar_date_str: str,
    time_index: int,
    palaces: List[Palace],
    soul_palace_index: int,
    five_elements_class: FiveElementsClass,
    gender: str,
    year_branch_yin_yang: str,
    birth_year: int,
    birth_lunar_date: Optional[LunarDate] = None,
    birth_time_branch: Optional[EarthlyBranchName] = None,
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

    decadal = get_decadal_horoscope(
        nominal_age,
        five_elements_class,
        palaces,
    )
    age_horoscope = get_age_horoscope(nominal_age, palaces)
    yearly = get_yearly_horoscope(year_branch, year_stem)

    if birth_lunar_date is None:
        birth_lunar_date = lunar_info
    if birth_time_branch is None:
        birth_time_branch = hour_branch

    monthly_index = get_monthly_horoscope_index(
        year_branch=year_branch,
        birth_lunar_date=birth_lunar_date,
        birth_time_branch=birth_time_branch,
        target_lunar_date=lunar_info,
    )
    monthly = get_monthly_horoscope(monthly_index, month_branch, month_stem)

    daily_index = fix_index(monthly_index + lunar_info.day - 1)
    daily = get_daily_horoscope(daily_index, day_branch, day_stem)

    hourly_index = fix_index(daily_index + _get_branch_index(hour_branch))
    hourly = get_hourly_horoscope(hourly_index, hour_branch, hour_stem)

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
    palaces: List[Palace],
) -> HoroscopeItem:
    """
    获取大限信息

    大限从命宫开始，每个宫位管10年
    男阳女阴顺行，男阴女阳逆行

    Args:
        age: 虚岁
        five_elements_class: 五行局
        palaces: 宫位列表

    Returns:
        大限运势项
    """
    palace = next(
        (item for item in palaces if item.decadal and item.decadal.range[0] <= age <= item.decadal.range[1]),
        None,
    )

    if palace is None and age <= five_elements_class.value:
        childhood_order = [
            "soulPalace",
            "wealthPalace",
            "healthPalace",
            "spousePalace",
            "spiritPalace",
            "careerPalace",
        ]
        palace = next((item for item in palaces if item.name == childhood_order[age - 1]), palaces[0])
        item_name = "童限"
    elif palace is None:
        palace = palaces[0]
        item_name = "大限"
    else:
        item_name = "大限"

    return HoroscopeItem(
        index=palace.index,
        name=item_name,
        heavenly_stem=palace.heavenly_stem,
        earthly_branch=palace.earthly_branch,
        palace_names=_get_palace_names(palace.index),
        mutagen=_get_mutagen_stars(palace.heavenly_stem),
        stars=None,  # 大限不安流耀
    )


def get_age_horoscope(
    age: int,
    palaces: List[Palace],
) -> HoroscopeItem:
    """
    获取小限信息

    小限从命宫起，男顺女逆，每年走一宫

    Args:
        age: 虚岁
        palaces: 宫位列表

    Returns:
        小限运势项
    """
    palace = next((item for item in palaces if age in item.ages), palaces[0])

    return HoroscopeItem(
        index=palace.index,
        name="小限",
        heavenly_stem=palace.heavenly_stem,
        earthly_branch=palace.earthly_branch,
        palace_names=_get_palace_names(palace.index),
        mutagen=_get_mutagen_stars(palace.heavenly_stem),
        stars=None,
    )


def get_yearly_horoscope(
    year_branch: EarthlyBranchName,
    year_stem: HeavenlyStemName,
) -> HoroscopeItem:
    """
    获取流年信息

    流年从年支地支位置开始安命宫

    Args:
        year_branch: 流年地支
        year_stem: 流年天干
    Returns:
        流年运势项
    """
    palace_index = fix_earthly_branch_index(year_branch)

    return HoroscopeItem(
        index=palace_index,
        name="流年",
        heavenly_stem=year_stem,
        earthly_branch=year_branch,
        palace_names=_get_palace_names(palace_index),
        mutagen=_get_mutagen_stars(year_stem),
        stars=None,  # 可以扩展添加流年星
    )


def get_monthly_horoscope_index(
    year_branch: EarthlyBranchName,
    birth_lunar_date: LunarDate,
    birth_time_branch: EarthlyBranchName,
    target_lunar_date: LunarDate,
) -> int:
    birth_leap_addition = 1 if birth_lunar_date.is_leap_month and birth_lunar_date.day > 15 else 0
    target_leap_addition = 1 if target_lunar_date.is_leap_month and target_lunar_date.day > 15 else 0
    return fix_index(
        fix_earthly_branch_index(year_branch)
        - (birth_lunar_date.month + birth_leap_addition)
        + _get_branch_index(birth_time_branch)
        + (target_lunar_date.month + target_leap_addition)
    )


def get_monthly_horoscope(
    palace_index: int,
    month_branch: EarthlyBranchName,
    month_stem: HeavenlyStemName,
) -> HoroscopeItem:
    """
    获取流月信息

    Args:
        month_branch: 流月地支
        month_stem: 流月天干
    Returns:
        流月运势项
    """
    return HoroscopeItem(
        index=palace_index,
        name="流月",
        heavenly_stem=month_stem,
        earthly_branch=month_branch,
        palace_names=_get_palace_names(palace_index),
        mutagen=_get_mutagen_stars(month_stem),
        stars=None,
    )


def get_daily_horoscope(
    palace_index: int,
    day_branch: EarthlyBranchName,
    day_stem: HeavenlyStemName,
) -> HoroscopeItem:
    """
    获取流日信息

    Args:
        day_branch: 流日地支
        day_stem: 流日天干
    Returns:
        流日运势项
    """
    return HoroscopeItem(
        index=palace_index,
        name="流日",
        heavenly_stem=day_stem,
        earthly_branch=day_branch,
        palace_names=_get_palace_names(palace_index),
        mutagen=_get_mutagen_stars(day_stem),
        stars=None,
    )


def get_hourly_horoscope(
    palace_index: int,
    hour_branch: EarthlyBranchName,
    hour_stem: HeavenlyStemName,
) -> HoroscopeItem:
    """
    获取流时信息

    Args:
        hour_branch: 流时地支
        hour_stem: 流时天干
    Returns:
        流时运势项
    """
    return HoroscopeItem(
        index=palace_index,
        name="流时",
        heavenly_stem=hour_stem,
        earthly_branch=hour_branch,
        palace_names=_get_palace_names(palace_index),
        mutagen=_get_mutagen_stars(hour_stem),
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


def _get_palace_names(from_index: int) -> List[str]:
    from iztro_py.data.constants import PALACES

    return [PALACES[fix_index(i - from_index)] for i in range(12)]


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
