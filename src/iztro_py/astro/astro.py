"""
Main API for iztro-py

Provides high-level functions for creating astrolabes.
"""

from typing import List
from iztro_py.data.types import (
    GenderName,
    Language,
    Astrolabe,
    Palace,
)
from iztro_py.astro.functional_astrolabe import FunctionalAstrolabe
from iztro_py.astro.palace import get_soul_and_body, initialize_palaces, populate_decadal_and_ages
from iztro_py.star.major_star import place_major_stars
from iztro_py.star.minor_star import place_minor_stars
from iztro_py.star.adjective_star import place_adjective_stars
from iztro_py.star.decorative_star import apply_decorative_stars
from iztro_py.star.mutagen import apply_mutagen_to_palaces
from iztro_py.data.brightness import apply_brightness_to_palaces
from iztro_py.data.earthly_branches import get_soul_star, get_body_star
from iztro_py.star.location import get_start_indices
from iztro_py.utils.calendar import (
    parse_solar_date,
    solar_to_lunar,
    lunar_to_solar,
    get_heavenly_stem_and_earthly_branch_date,
    get_zodiac,
    get_sign,
    format_lunar_date,
    format_chinese_date,
)
from iztro_py.utils.helpers import (
    get_five_elements_class,
    get_five_elements_class_name,
    get_time_name,
    get_time_range,
    hour_to_time_index,
    fix_lunar_month_index,
)


def by_solar(
    solar_date: str,
    time_index: int,
    gender: GenderName,
    fix_leap: bool = True,
    language: Language = "zh-CN",
) -> FunctionalAstrolabe:
    """
    通过阳历日期获取紫微斗数星盘

    Args:
        solar_date: 阳历日期字符串，格式 'YYYY-M-D' 或 'YYYY-MM-DD'
        time_index: 时辰索引 (0-12)
            0: 早子时 00:00~01:00
            1: 丑时 01:00~03:00
            ...
            12: 晚子时 23:00~00:00
        gender: 性别 ('男' 或 '女')
        fix_leap: 是否修正闰月（默认True）
        language: 输出语言（默认'zh-CN'）

    Returns:
        FunctionalAstrolabe对象

    Example:
        >>> from iztro_py import astro
        >>> chart = astro.by_solar('2000-8-16', 6, '男')
        >>> print(chart.get_soul_palace())
        >>> print(chart.star('紫微'))
    """
    # 设置语言
    from iztro_py.i18n import set_language

    set_language(language)

    # 1. 解析阳历日期
    year, month, day = parse_solar_date(solar_date)

    # 2. 阳历转农历
    lunar_date = solar_to_lunar(year, month, day, fix_leap)

    # 3. 计算四柱
    chinese_date = get_heavenly_stem_and_earthly_branch_date(year, month, day, time_index)

    # 4. 生肖星座
    zodiac = get_zodiac(chinese_date.year_branch)
    sign = get_sign(month, day)

    # 5. 计算命宫身宫
    soul_and_body = get_soul_and_body(solar_date, time_index, fix_leap=fix_leap)

    # 6. 计算五行局
    five_class = get_five_elements_class(
        soul_and_body.heavenly_stem_of_soul, soul_and_body.earthly_branch_of_soul
    )

    # 7. 命主身主
    soul_star = get_soul_star(soul_and_body.earthly_branch_of_soul)
    body_star = get_body_star(chinese_date.year_branch)

    # 8. 初始化十二宫
    palaces = initialize_palaces(soul_and_body, chinese_date.year_stem)

    # 9. 安置主星（与原生 iztro 对齐的紫微/天府起局算法）
    ziwei_idx, tianfu_idx = get_start_indices(
        solar_date,
        time_index,
        fix_leap,
        soul_and_body.heavenly_stem_of_soul,
        soul_and_body.earthly_branch_of_soul,
    )
    place_major_stars(palaces, ziwei_idx, tianfu_idx)

    # 10. 安置辅星
    adjusted_lunar_month = fix_lunar_month_index(solar_date, time_index, fix_leap) + 1
    place_minor_stars(
        palaces,
        adjusted_lunar_month,
        time_index,
        chinese_date.year_stem,
        chinese_date.year_branch,
    )

    # 11. 安置杂曜
    place_adjective_stars(
        palaces,
        solar_date,
        time_index,
        gender,
        fix_leap,
        soul_and_body.soul_index,
        soul_and_body.body_index,
    )

    # 12. 填充长生/博士/将前/岁前 12 神
    apply_decorative_stars(
        palaces,
        five_class,
        gender,
        chinese_date.year_stem,
        chinese_date.year_branch,
    )

    # 13. 应用四化
    apply_mutagen_to_palaces(palaces, chinese_date.year_stem)

    # 14. 应用亮度
    apply_brightness_to_palaces(palaces)

    # 15. 填充大限与小限锚点
    populate_decadal_and_ages(
        palaces,
        soul_and_body.soul_index,
        five_class,
        gender,
        chinese_date.year_stem,
        chinese_date.year_branch,
    )

    # 16. 创建Astrolabe对象
    body_palace_branch = palaces[soul_and_body.body_index]["earthly_branch"]

    # 将字典列表转换为 Palace 对象列表
    palace_objects: List[Palace] = [Palace(**p) for p in palaces]

    astrolabe = Astrolabe(
        gender=gender,
        solar_date=solar_date,
        lunar_date=format_lunar_date(lunar_date),
        chinese_date=format_chinese_date(chinese_date),
        time=get_time_name(time_index),
        time_range=get_time_range(time_index),
        sign=sign,
        zodiac=zodiac,
        earthly_branch_of_soul_palace=soul_and_body.earthly_branch_of_soul,
        earthly_branch_of_body_palace=body_palace_branch,
        soul=soul_star,
        body=body_star,
        five_elements_class=get_five_elements_class_name(five_class),
        palaces=palace_objects,
        language=language,
        raw_lunar_date=lunar_date,
        raw_chinese_date=chinese_date,
    )

    # 17. 转换为FunctionalAstrolabe
    return FunctionalAstrolabe(astrolabe)


def by_solar_hour(
    solar_date: str,
    hour: int,
    gender: GenderName,
    fix_leap: bool = True,
    language: Language = "zh-CN",
) -> FunctionalAstrolabe:
    """
    通过阳历日期和小时数(0-23)获取星盘（便捷包装）

    将小时映射为时辰索引，以与 iztro 一致：
    - 23点为晚子时 (time_index=12)，0点为早子时 (time_index=0)
    - 其他小时按每2小时一个时辰
    """
    ti = hour_to_time_index(hour)
    return by_solar(solar_date, ti, gender, fix_leap, language)


def by_lunar(
    lunar_date: str,
    time_index: int,
    gender: GenderName,
    is_leap_month: bool = False,
    fix_leap: bool = True,
    language: Language = "zh-CN",
) -> FunctionalAstrolabe:
    """
    通过农历日期获取紫微斗数星盘

    Args:
        lunar_date: 农历日期字符串，格式 'YYYY-M-D'
        time_index: 时辰索引 (0-12)
        gender: 性别 ('男' 或 '女')
        is_leap_month: 是否闰月（默认False）
        fix_leap: 是否修正闰月（默认True）
        language: 输出语言（默认'zh-CN'）

    Returns:
        FunctionalAstrolabe对象

    Example:
        >>> from iztro_py import astro
        >>> chart = astro.by_lunar('2000-7-17', 6, '男')
        >>> print(chart)
    """
    # 1. 解析农历日期
    year, month, day = parse_solar_date(lunar_date)  # 格式相同

    # 2. 农历转阳历
    solar_year, solar_month, solar_day = lunar_to_solar(year, month, day, is_leap_month)

    # 3. 构造阳历日期字符串
    solar_date_str = f"{solar_year}-{solar_month}-{solar_day}"

    # 4. 调用by_solar
    return by_solar(solar_date_str, time_index, gender, fix_leap, language)


def by_lunar_hour(
    lunar_date: str,
    hour: int,
    gender: GenderName,
    is_leap_month: bool = False,
    fix_leap: bool = True,
    language: Language = "zh-CN",
) -> FunctionalAstrolabe:
    """
    通过农历日期和小时数(0-23)获取星盘（便捷包装）
    """
    ti = hour_to_time_index(hour)
    return by_lunar(lunar_date, ti, gender, is_leap_month, fix_leap, language)


def get_zodiac_by_solar_date(solar_date: str, language: Language = "zh-CN") -> str:
    """
    根据阳历日期获取生肖

    Args:
        solar_date: 阳历日期字符串
        language: 语言（默认'zh-CN'）

    Returns:
        生肖名称
    """
    year, month, day = parse_solar_date(solar_date)
    chinese_date = get_heavenly_stem_and_earthly_branch_date(year, month, day, 0)
    return get_zodiac(chinese_date.year_branch)


def get_sign_by_solar_date(solar_date: str, language: Language = "zh-CN") -> str:
    """
    根据阳历日期获取星座

    Args:
        solar_date: 阳历日期字符串
        language: 语言（默认'zh-CN'）

    Returns:
        星座名称
    """
    year, month, day = parse_solar_date(solar_date)
    return get_sign(month, day)
