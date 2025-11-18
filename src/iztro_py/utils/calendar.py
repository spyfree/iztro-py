"""
Calendar conversion utilities for iztro-py

Provides functions for converting between solar and lunar calendars,
and calculating heavenly stems and earthly branches (天干地支).
"""

from datetime import datetime, date
from typing import Tuple, Optional
from lunarcalendar import Converter, Solar, Lunar, DateNotExist

from iztro_py.data.types import (
    LunarDate,
    HeavenlyStemAndEarthlyBranchDate,
    HeavenlyStemName,
    EarthlyBranchName,
)
from iztro_py.data.constants import (
    HEAVENLY_STEMS,
    EARTHLY_BRANCHES,
    TIGER_RULE,
    RAT_RULE,
    fix_index,
)


# ============================================================================
# Solar to Lunar Conversion
# ============================================================================


def solar_to_lunar(year: int, month: int, day: int, fix_leap: bool = True) -> LunarDate:
    """
    阳历转农历

    Args:
        year: 阳历年
        month: 阳历月
        day: 阳历日
        fix_leap: 是否修正闰月（如果在闰月前半月则调整为前一个月）

    Returns:
        LunarDate对象

    Raises:
        ValueError: 如果日期无效
    """
    try:
        solar = Solar(year, month, day)
        lunar = Converter.Solar2Lunar(solar)

        is_leap = lunar.isleap

        # 修正闰月：如果在闰月的前半月，调整为前一个月
        if fix_leap and is_leap and lunar.day <= 15:
            # 调整为前一个月的非闰月
            is_leap = False

        return LunarDate(year=lunar.year, month=lunar.month, day=lunar.day, is_leap_month=is_leap)

    except DateNotExist:
        raise ValueError(f"Invalid solar date: {year}-{month}-{day}")
    except Exception as e:
        raise ValueError(f"Error converting solar to lunar: {e}")


def parse_solar_date(date_str: str) -> Tuple[int, int, int]:
    """
    解析阳历日期字符串

    Args:
        date_str: 日期字符串，格式：YYYY-M-D 或 YYYY-MM-DD

    Returns:
        (year, month, day) 元组

    Raises:
        ValueError: 如果日期格式无效
    """
    try:
        parts = date_str.split("-")
        if len(parts) != 3:
            raise ValueError(f"Invalid date format: {date_str}")

        year = int(parts[0])
        month = int(parts[1])
        day = int(parts[2])

        return year, month, day

    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid date string: {date_str}. Expected format: YYYY-M-D")


# ============================================================================
# Lunar to Solar Conversion
# ============================================================================


def lunar_to_solar(
    year: int, month: int, day: int, is_leap_month: bool = False
) -> Tuple[int, int, int]:
    """
    农历转阳历

    Args:
        year: 农历年
        month: 农历月
        day: 农历日
        is_leap_month: 是否闰月

    Returns:
        (year, month, day) 元组

    Raises:
        ValueError: 如果日期无效
    """
    try:
        lunar = Lunar(year, month, day, isleap=is_leap_month)
        solar = Converter.Lunar2Solar(lunar)

        return solar.year, solar.month, solar.day

    except DateNotExist:
        raise ValueError(f"Invalid lunar date: {year}-{month}-{day} (leap={is_leap_month})")
    except Exception as e:
        raise ValueError(f"Error converting lunar to solar: {e}")


def parse_lunar_date(date_str: str) -> Tuple[int, int, int]:
    """
    解析农历日期字符串

    Args:
        date_str: 日期字符串，格式：YYYY-M-D

    Returns:
        (year, month, day) 元组

    Raises:
        ValueError: 如果日期格式无效
    """
    return parse_solar_date(date_str)  # 格式相同


# ============================================================================
# Heavenly Stems and Earthly Branches Calculation
# ============================================================================


def get_year_stem_branch(year: int) -> Tuple[HeavenlyStemName, EarthlyBranchName]:
    """
    根据年份计算年干支

    年干 = (年份 - 4) % 10
    年支 = (年份 - 4) % 12

    Args:
        year: 年份

    Returns:
        (天干, 地支) 元组
    """
    stem_index = (year - 4) % 10
    branch_index = (year - 4) % 12

    return HEAVENLY_STEMS[stem_index], EARTHLY_BRANCHES[branch_index]


def get_month_stem_branch(
    year_stem: HeavenlyStemName, month: int
) -> Tuple[HeavenlyStemName, EarthlyBranchName]:
    """
    根据年干和月份计算月干支（五虎遁）

    五虎遁口诀：
    甲己之年丙作首，乙庚之岁戊为头
    丙辛之岁庚寅上，丁壬壬寅顺水流
    戊癸甲寅为岁首

    Args:
        year_stem: 年干
        month: 月份 (1-12)

    Returns:
        (天干, 地支) 元组
    """
    # 月支固定：寅(正月)开始
    # 索引：寅=2, 卯=3, ..., 丑=1
    branch_index = fix_index(month + 1)  # 正月从寅开始，索引2
    month_branch = EARTHLY_BRANCHES[branch_index]

    # 根据五虎遁获取正月天干
    first_month_stem = TIGER_RULE[year_stem]
    first_month_stem_index = HEAVENLY_STEMS.index(first_month_stem)

    # 计算本月天干
    month_stem_index = fix_index(first_month_stem_index + month - 1, 10)
    month_stem = HEAVENLY_STEMS[month_stem_index]

    return month_stem, month_branch


def get_day_stem_branch(solar_date: date) -> Tuple[HeavenlyStemName, EarthlyBranchName]:
    """
    根据阳历日期计算日干支

    使用公元元年1月1日为甲子日的算法

    Args:
        solar_date: 日期对象

    Returns:
        (天干, 地支) 元组
    """
    # 计算从公元元年1月1日到指定日期的天数
    # 公元元年1月1日是甲子日后的第37天
    base_date = date(1, 1, 1)
    days_diff = (solar_date - base_date).days

    # 甲子日是第37天（索引36）
    # 所以实际偏移是 days_diff - 36
    offset = days_diff - 36

    stem_index = offset % 10
    branch_index = offset % 12

    return HEAVENLY_STEMS[stem_index], EARTHLY_BRANCHES[branch_index]


def get_time_stem_branch(
    day_stem: HeavenlyStemName, time_index: int
) -> Tuple[HeavenlyStemName, EarthlyBranchName]:
    """
    根据日干和时辰索引计算时干支（五鼠遁）

    五鼠遁口诀：
    甲己还加甲，乙庚丙作初
    丙辛从戊起，丁壬庚子居
    戊癸何方发，壬子是真途

    Args:
        day_stem: 日干
        time_index: 时辰索引 (0-12)

    Returns:
        (天干, 地支) 元组
    """
    # 时支：子=0, 丑=1, ..., 亥=11
    # 特殊处理：早子时(0)和晚子时(12)都是子时
    if time_index == 12:
        time_branch_index = 0  # 子时
    elif time_index == 0:
        time_branch_index = 0  # 子时
    else:
        time_branch_index = time_index

    time_branch = EARTHLY_BRANCHES[time_branch_index]

    # 根据五鼠遁获取子时天干
    zi_hour_stem = RAT_RULE[day_stem]
    zi_hour_stem_index = HEAVENLY_STEMS.index(zi_hour_stem)

    # 计算本时辰天干
    time_stem_index = fix_index(zi_hour_stem_index + time_branch_index, 10)
    time_stem = HEAVENLY_STEMS[time_stem_index]

    return time_stem, time_branch


def get_heavenly_stem_and_earthly_branch_date(
    year: int, month: int, day: int, time_index: int, lunar_month: Optional[int] = None
) -> HeavenlyStemAndEarthlyBranchDate:
    """
    获取完整的四柱（年月日时的天干地支）

    Args:
        year: 阳历年
        month: 阳历月
        day: 阳历日
        time_index: 时辰索引 (0-12)
        lunar_month: 农历月（用于月干支计算）

    Returns:
        HeavenlyStemAndEarthlyBranchDate对象
    """
    # 年干支
    year_stem, year_branch = get_year_stem_branch(year)

    # 月干支（使用农历月）
    if lunar_month is None:
        lunar_date = solar_to_lunar(year, month, day)
        lunar_month = lunar_date.month

    month_stem, month_branch = get_month_stem_branch(year_stem, lunar_month)

    # 日干支
    solar_date = date(year, month, day)
    day_stem, day_branch = get_day_stem_branch(solar_date)

    # 时干支
    time_stem, time_branch = get_time_stem_branch(day_stem, time_index)

    return HeavenlyStemAndEarthlyBranchDate(
        year_stem=year_stem,
        year_branch=year_branch,
        month_stem=month_stem,
        month_branch=month_branch,
        day_stem=day_stem,
        day_branch=day_branch,
        time_stem=time_stem,
        time_branch=time_branch,
    )


# ============================================================================
# Zodiac and Sign Calculation
# ============================================================================

# 生肖对应地支
ZODIAC_NAMES = {
    "ziEarthly": "鼠",
    "chouEarthly": "牛",
    "yinEarthly": "虎",
    "maoEarthly": "兔",
    "chenEarthly": "龙",
    "siEarthly": "蛇",
    "wuEarthly": "马",
    "weiEarthly": "羊",
    "shenEarthly": "猴",
    "youEarthly": "鸡",
    "xuEarthly": "狗",
    "haiEarthly": "猪",
}

# 星座日期范围 (月, 日)
SIGN_DATES = [
    ((3, 21), (4, 19), "白羊座"),  # Aries
    ((4, 20), (5, 20), "金牛座"),  # Taurus
    ((5, 21), (6, 21), "双子座"),  # Gemini
    ((6, 22), (7, 22), "巨蟹座"),  # Cancer
    ((7, 23), (8, 22), "狮子座"),  # Leo
    ((8, 23), (9, 22), "处女座"),  # Virgo
    ((9, 23), (10, 23), "天秤座"),  # Libra
    ((10, 24), (11, 22), "天蝎座"),  # Scorpio
    ((11, 23), (12, 21), "射手座"),  # Sagittarius
    ((12, 22), (12, 31), "摩羯座"),  # Capricorn
    ((1, 1), (1, 19), "摩羯座"),  # Capricorn (continued)
    ((1, 20), (2, 18), "水瓶座"),  # Aquarius
    ((2, 19), (3, 20), "双鱼座"),  # Pisces
]


def get_zodiac(year_branch: EarthlyBranchName) -> str:
    """
    根据年支获取生肖

    Args:
        year_branch: 年支

    Returns:
        生肖名称
    """
    return ZODIAC_NAMES.get(year_branch, "未知")


def get_sign(month: int, day: int) -> str:
    """
    根据阳历月日获取星座

    Args:
        month: 月份 (1-12)
        day: 日期 (1-31)

    Returns:
        星座名称
    """
    for start, end, sign_name in SIGN_DATES:
        start_month, start_day = start
        end_month, end_day = end

        if start_month == end_month:
            # 同一个月内
            if month == start_month and start_day <= day <= end_day:
                return sign_name
        else:
            # 跨月
            if (month == start_month and day >= start_day) or (
                month == end_month and day <= end_day
            ):
                return sign_name

    return "未知"


# ============================================================================
# Format Functions
# ============================================================================


def format_lunar_date(lunar_date: LunarDate) -> str:
    """
    格式化农历日期为中文字符串

    Args:
        lunar_date: 农历日期对象

    Returns:
        格式化后的字符串，如 "2000年七月十八" 或 "2000年闰七月十八"
    """
    # 数字转中文
    chinese_numbers = ["〇", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
    months = ["", "正", "二", "三", "四", "五", "六", "七", "八", "九", "十", "冬", "腊"]

    # 月份
    if lunar_date.month <= 12:
        month_str = months[lunar_date.month]
    else:
        month_str = str(lunar_date.month)

    if lunar_date.is_leap_month:
        month_str = f"闰{month_str}"

    # 日期
    if lunar_date.day <= 10:
        day_str = f"初{chinese_numbers[lunar_date.day]}"
    elif lunar_date.day < 20:
        day_str = f"十{chinese_numbers[lunar_date.day - 10]}"
    elif lunar_date.day == 20:
        day_str = "二十"
    elif lunar_date.day < 30:
        day_str = f"廿{chinese_numbers[lunar_date.day - 20]}"
    elif lunar_date.day == 30:
        day_str = "三十"
    else:
        day_str = str(lunar_date.day)

    return f"{lunar_date.year}年{month_str}月{day_str}"


def format_chinese_date(chinese_date: HeavenlyStemAndEarthlyBranchDate) -> str:
    """
    格式化干支日期为中文字符串

    Args:
        chinese_date: 干支日期对象

    Returns:
        格式化后的字符串，如 "庚辰年七月十八 午时"
    """
    # 天干地支中文映射
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

    year_str = f"{stem_names[chinese_date.year_stem]}{branch_names[chinese_date.year_branch]}"
    month_str = f"{stem_names[chinese_date.month_stem]}{branch_names[chinese_date.month_branch]}"
    day_str = f"{stem_names[chinese_date.day_stem]}{branch_names[chinese_date.day_branch]}"
    time_str = f"{stem_names[chinese_date.time_stem]}{branch_names[chinese_date.time_branch]}"

    return f"{year_str}年{month_str}月{day_str}日 {time_str}时"
