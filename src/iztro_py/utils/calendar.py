"""
Calendar conversion utilities for iztro-py

Provides functions for converting between solar and lunar calendars,
and calculating heavenly stems and earthly branches (天干地支).
"""

from datetime import date
from typing import Tuple, Optional
from lunar_python import Solar as LunarSolar
from lunar_python import Lunar as LunarDateValue

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


def solar_to_lunar(year: int, month: int, day: int) -> LunarDate:
    """
    阳历转农历

    返回原始农历日期（闰月以 is_leap_month 标记）。
    斗数排盘所需的闰月修正在 `fix_lunar_month_index` 中处理，
    与 iztro 的 solar2lunar / fixLunarMonthIndex 分工一致。

    Args:
        year: 阳历年
        month: 阳历月
        day: 阳历日

    Returns:
        LunarDate对象

    Raises:
        ValueError: 如果日期无效
    """
    try:
        solar = LunarSolar.fromYmd(year, month, day)
        lunar = solar.getLunar()
        lunar_month = lunar.getMonth()
        return LunarDate(
            year=lunar.getYear(),
            month=abs(lunar_month),
            day=lunar.getDay(),
            is_leap_month=lunar_month < 0,
        )
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

    except (ValueError, IndexError):
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
        lunar_month = -month if is_leap_month else month
        lunar = LunarDateValue.fromYmd(year, lunar_month, day)
        solar = lunar.getSolar()
        return solar.getYear(), solar.getMonth(), solar.getDay()
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


def get_year_stem_branch(lunar_year: int) -> Tuple[HeavenlyStemName, EarthlyBranchName]:
    """
    根据**农历**年份计算年干支

    年干 = (农历年 - 4) % 10
    年支 = (农历年 - 4) % 12

    .. warning::
        入参必须是**农历年**，不是阳历年。本库的年柱以正月初一分界
        （对齐 iztro ``yearDivide='normal'``），元旦到春节之间阳历年已经
        进位、农历年还没有，此时传阳历年会整整差一年：

        >>> get_year_stem_branch(2000)          # 农历庚辰年 → 正确
        ('gengHeavenly', 'chenEarthly')
        >>> # 但 2000-01-20 当天农历仍是己卯年，传 2000 会得到错误的庚辰

        要从**阳历日期**得到年柱，请用
        :func:`get_heavenly_stem_and_earthly_branch_date`，它会正确处理分界。

    Args:
        lunar_year: 农历年份

    Returns:
        (天干, 地支) 元组
    """
    stem_index = (lunar_year - 4) % 10
    branch_index = (lunar_year - 4) % 12

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

    返回该**日历日**的日柱（正午取值，不做晚子时进位）。晚子时按次日计算
    的规则由 :func:`get_heavenly_stem_and_earthly_branch_date` 处理
    （对齐 iztro ``dayDivide='forward'``）。

    Args:
        solar_date: 日期对象

    Returns:
        (天干, 地支) 元组

    Note:
        实现委托给 ``lunar_python``，与
        :func:`get_heavenly_stem_and_earthly_branch_date` 走同一套历法数据，
        两者不会再分叉。此前这里用「公元元年1月1日为甲子日后第37天」的自
        制偏移量，锚点是错的，导致**每一个日期**的日柱都偏了 51 天。
    """
    # 固定取正午：避开 23:00 之后的晚子时进位，得到的就是该日历日的日柱。
    solar = LunarSolar.fromYmdHms(solar_date.year, solar_date.month, solar_date.day, 12, 0, 0)
    return _parse_ganzhi(solar.getLunar().getDayInGanZhi())


def get_time_stem_branch(
    day_stem: HeavenlyStemName, time_index: int
) -> Tuple[HeavenlyStemName, EarthlyBranchName]:
    """
    根据日干和时辰索引计算时干支（五鼠遁）

    五鼠遁口诀：
    甲己还加甲，乙庚丙作初
    丙辛从戊起，丁壬庚子居
    戊癸何方发，壬子是真途

    .. warning::
        ``time_index=12``（晚子时，23:00~00:00）时，本库的日柱已经进位到次日
        （对齐 iztro ``dayDivide='forward'``），因此**必须传次日的日干**，
        传当天日干会得到错误的时柱：

        >>> # 1990-10-21 当天日干为己、次日为庚
        >>> get_time_stem_branch('jiHeavenly', 12)      # 传当天 → 甲子（错）
        ('jiaHeavenly', 'ziEarthly')
        >>> get_time_stem_branch('gengHeavenly', 12)    # 传次日 → 丙子（对）
        ('bingHeavenly', 'ziEarthly')

        要从阳历日期直接得到时柱，请用
        :func:`get_heavenly_stem_and_earthly_branch_date`，它已处理好进位。

    Args:
        day_stem: 日干（晚子时须传次日日干，见上方警告）
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

    对齐 iztro 默认配置（yearDivide='normal'、horoscopeDivide='normal'）：
    - 年柱以农历正月初一为分界（非立春）
    - 月柱按农历月序自年干起五虎遁（闰月下半月算下月）
    - 日柱晚子时（23:00 后）按次日计算（dayDivide='forward'）

    Args:
        year: 阳历年
        month: 阳历月
        day: 阳历日
        time_index: 时辰索引 (0-12)
        lunar_month: 农历月（用于月干支计算）

    Returns:
        HeavenlyStemAndEarthlyBranchDate对象
    """
    solar = LunarSolar.fromYmdHms(year, month, day, _time_index_to_hour(time_index), 0, 0)
    lunar = solar.getLunar()

    year_stem, year_branch = _parse_ganzhi(lunar.getYearInGanZhi())
    month_stem, month_branch = _get_normal_month_stem_branch(year_stem, lunar)
    day_stem, day_branch = _parse_ganzhi(lunar.getDayInGanZhiExact())
    time_stem, time_branch = _parse_ganzhi(lunar.getTimeInGanZhi())

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


def _get_normal_month_stem_branch(
    year_stem: HeavenlyStemName, lunar: "LunarDateValue"
) -> Tuple[HeavenlyStemName, EarthlyBranchName]:
    """按农历月序（初一分界）计算月干支，对齐 lunar-lite 的 normal 模式。"""
    raw_month = lunar.getMonth()
    month_num = abs(raw_month)
    # 闰月下半月按下一个月计算
    leap_addition = 1 if raw_month < 0 and lunar.getDay() > 15 else 0

    first_month_stem = TIGER_RULE[year_stem]
    stem_index = fix_index(
        HEAVENLY_STEMS.index(first_month_stem) + month_num - 1 + leap_addition, 10
    )
    branch_index = fix_index(EARTHLY_BRANCHES.index("yinEarthly") + month_num - 1 + leap_addition)
    return HEAVENLY_STEMS[stem_index], EARTHLY_BRANCHES[branch_index]


# ============================================================================
# Zodiac and Sign Calculation
# ============================================================================

# 生肖对应地支（值为 i18n 翻译键）
ZODIAC_NAMES = {
    "ziEarthly": "rat",  # 鼠
    "chouEarthly": "ox",  # 牛
    "yinEarthly": "tiger",  # 虎
    "maoEarthly": "rabbit",  # 兔
    "chenEarthly": "dragon",  # 龙
    "siEarthly": "snake",  # 蛇
    "wuEarthly": "horse",  # 马
    "weiEarthly": "sheep",  # 羊
    "shenEarthly": "monkey",  # 猴
    "youEarthly": "rooster",  # 鸡
    "xuEarthly": "dog",  # 狗
    "haiEarthly": "pig",  # 猪
}

# 星座日期范围 (月, 日)，值为 i18n 翻译键
SIGN_DATES = [
    ((3, 21), (4, 19), "aries"),  # 白羊座
    ((4, 20), (5, 20), "taurus"),  # 金牛座
    ((5, 21), (6, 21), "gemini"),  # 双子座
    ((6, 22), (7, 22), "cancer"),  # 巨蟹座
    ((7, 23), (8, 22), "leo"),  # 狮子座
    ((8, 23), (9, 22), "virgo"),  # 处女座
    ((9, 23), (10, 23), "libra"),  # 天秤座
    ((10, 24), (11, 22), "scorpio"),  # 天蝎座
    ((11, 23), (12, 21), "sagittarius"),  # 射手座
    ((12, 22), (12, 31), "capricorn"),  # 摩羯座
    ((1, 1), (1, 19), "capricorn"),  # 摩羯座（跨年后半段）
    ((1, 20), (2, 18), "aquarius"),  # 水瓶座
    ((2, 19), (3, 20), "pisces"),  # 双鱼座
]


def get_zodiac(year_branch: EarthlyBranchName, lang: Optional[str] = None) -> str:
    """
    根据年支获取生肖

    Args:
        year_branch: 年支
        lang: 目标语言代码，默认使用当前全局语言

    Returns:
        本地化生肖名称，如 "龙" / "dragon"
    """
    from iztro_py.i18n import t

    key = ZODIAC_NAMES.get(year_branch)
    if key is None:
        return "未知"
    return t(f"zodiac.{key}", lang)


def get_sign(month: int, day: int, lang: Optional[str] = None) -> str:
    """
    根据阳历月日获取星座

    Args:
        month: 月份 (1-12)
        day: 日期 (1-31)
        lang: 目标语言代码，默认使用当前全局语言

    Returns:
        本地化星座名称，如 "狮子座" / "leo"
    """
    from iztro_py.i18n import t

    for start, end, sign_key in SIGN_DATES:
        start_month, start_day = start
        end_month, end_day = end

        if start_month == end_month:
            # 同一个月内
            if month == start_month and start_day <= day <= end_day:
                return t(f"sign.{sign_key}", lang)
        else:
            # 跨月
            if (month == start_month and day >= start_day) or (
                month == end_month and day <= end_day
            ):
                return t(f"sign.{sign_key}", lang)

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

    year_str = "".join(chinese_numbers[int(d)] for d in str(lunar_date.year))
    return f"{year_str}年{month_str}月{day_str}"


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

    return f"{year_str} {month_str} {day_str} {time_str}"


def _time_index_to_hour(time_index: int) -> int:
    """Map iztro time index to a concrete hour for `lunar_python`."""
    time_index_to_hour = [0, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23]
    if not (0 <= time_index < len(time_index_to_hour)):
        raise ValueError(f"Invalid time index: {time_index}. Must be 0-12.")
    return time_index_to_hour[time_index]


def _parse_ganzhi(value: str) -> Tuple[HeavenlyStemName, EarthlyBranchName]:
    """Convert a 2-char Chinese ganzhi string like '庚午' into internal enum keys."""
    stem_map = {
        "甲": "jiaHeavenly",
        "乙": "yiHeavenly",
        "丙": "bingHeavenly",
        "丁": "dingHeavenly",
        "戊": "wuHeavenly",
        "己": "jiHeavenly",
        "庚": "gengHeavenly",
        "辛": "xinHeavenly",
        "壬": "renHeavenly",
        "癸": "guiHeavenly",
    }
    branch_map = {
        "子": "ziEarthly",
        "丑": "chouEarthly",
        "寅": "yinEarthly",
        "卯": "maoEarthly",
        "辰": "chenEarthly",
        "巳": "siEarthly",
        "午": "wuEarthly",
        "未": "weiEarthly",
        "申": "shenEarthly",
        "酉": "youEarthly",
        "戌": "xuEarthly",
        "亥": "haiEarthly",
    }
    if len(value) != 2:
        raise ValueError(f"Invalid ganzhi value: {value}")
    return stem_map[value[0]], branch_map[value[1]]
