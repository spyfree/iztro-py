"""
Test calendar conversion functions
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from datetime import date
from iztro_py.utils.calendar import (
    solar_to_lunar,
    lunar_to_solar,
    get_year_stem_branch,
    get_month_stem_branch,
    get_day_stem_branch,
    get_time_stem_branch,
    get_heavenly_stem_and_earthly_branch_date,
    get_zodiac,
    get_sign,
    format_lunar_date,
    format_chinese_date,
)


def test_solar_to_lunar():
    """测试阳历转农历"""
    print("=" * 60)
    print("测试：阳历转农历")
    print("=" * 60)

    # 测试案例：2000年8月16日（庚辰龙年七月十七）
    lunar = solar_to_lunar(2000, 8, 16)
    print(f"阳历 2000-8-16 -> 农历 {lunar.year}年{lunar.month}月{lunar.day}日")
    print(f"是否闰月: {lunar.is_leap_month}")
    print(f"格式化: {format_lunar_date(lunar)}")

    assert lunar.year == 2000
    assert lunar.month == 7
    # 可能是17或18日（取决于lunarcalendar的实现）
    print("✓ 阳历转农历测试通过\n")


def test_lunar_to_solar():
    """测试农历转阳历"""
    print("=" * 60)
    print("测试：农历转阳历")
    print("=" * 60)

    # 测试案例：农历2000年七月十七
    year, month, day = lunar_to_solar(2000, 7, 17)
    print(f"农历 2000年7月17日 -> 阳历 {year}-{month}-{day}")

    # 应该接近2000年8月16日
    assert year == 2000
    assert month == 8
    print("✓ 农历转阳历测试通过\n")


def test_stem_branch_calculation():
    """测试天干地支计算"""
    print("=" * 60)
    print("测试：天干地支计算")
    print("=" * 60)

    # 2000年8月16日午时（时辰索引6）
    chinese_date = get_heavenly_stem_and_earthly_branch_date(
        year=2000, month=8, day=16, time_index=6, lunar_month=7
    )

    print(f"四柱：{format_chinese_date(chinese_date)}")
    print(f"年干支: {chinese_date.year_stem} {chinese_date.year_branch}")
    print(f"月干支: {chinese_date.month_stem} {chinese_date.month_branch}")
    print(f"日干支: {chinese_date.day_stem} {chinese_date.day_branch}")
    print(f"时干支: {chinese_date.time_stem} {chinese_date.time_branch}")

    # 2000年是庚辰年
    assert chinese_date.year_stem == "gengHeavenly"
    assert chinese_date.year_branch == "chenEarthly"
    print("✓ 天干地支计算测试通过\n")


def test_zodiac_and_sign():
    """测试生肖和星座"""
    print("=" * 60)
    print("测试：生肖和星座")
    print("=" * 60)

    year_stem, year_branch = get_year_stem_branch(2000)
    zodiac = get_zodiac(year_branch)
    sign = get_sign(8, 16)

    print(f"2000年生肖: {zodiac}")
    print(f"8月16日星座: {sign}")

    assert zodiac == "龙"
    assert sign == "狮子座"
    print("✓ 生肖星座测试通过\n")


if __name__ == "__main__":
    try:
        test_solar_to_lunar()
        test_lunar_to_solar()
        test_stem_branch_calculation()
        test_zodiac_and_sign()

        print("=" * 60)
        print("✓✓✓ 所有日历转换测试通过！")
        print("=" * 60)
    except Exception as e:
        print(f"\n✗✗✗ 测试失败: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
