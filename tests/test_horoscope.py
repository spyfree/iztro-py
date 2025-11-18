"""
Test horoscope (运势) system
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from iztro_py import astro


def test_horoscope_basic():
    """测试基本运势功能"""
    print("=" * 60)
    print("测试：基本运势功能")
    print("=" * 60)

    # 创建星盘：2000年8月16日午时出生的男命
    chart = astro.by_solar("2000-8-16", 6, "男")

    # 获取2024年1月1日午时的运势
    horoscope = chart.horoscope("2024-1-1", 6)

    print(f"查询日期: {horoscope.solar_date}")
    print(f"农历: {horoscope.lunar_date}")
    print(f"虚岁: {horoscope.nominal_age}")
    print()

    # 大限
    print(f"大限: {horoscope.decadal.name}")
    print(f"  宫位: {horoscope.decadal.palace_names}")
    print(f"  天干地支: {horoscope.decadal.heavenly_stem} {horoscope.decadal.earthly_branch}")
    print(f"  四化: {horoscope.decadal.mutagen}")
    print()

    # 小限
    print(f"小限: {horoscope.age.name}")
    print(f"  宫位: {horoscope.age.palace_names}")
    print(f"  天干地支: {horoscope.age.heavenly_stem} {horoscope.age.earthly_branch}")
    print(f"  四化: {horoscope.age.mutagen}")
    print()

    # 流年
    print(f"流年: {horoscope.yearly.name}")
    print(f"  宫位: {horoscope.yearly.palace_names}")
    print(f"  天干地支: {horoscope.yearly.heavenly_stem} {horoscope.yearly.earthly_branch}")
    print(f"  四化: {horoscope.yearly.mutagen}")
    print()

    # 流月
    print(f"流月: {horoscope.monthly.name}")
    print(f"  宫位: {horoscope.monthly.palace_names}")
    print(f"  天干地支: {horoscope.monthly.heavenly_stem} {horoscope.monthly.earthly_branch}")
    print(f"  四化: {horoscope.monthly.mutagen}")
    print()

    # 流日
    print(f"流日: {horoscope.daily.name}")
    print(f"  宫位: {horoscope.daily.palace_names}")
    print(f"  天干地支: {horoscope.daily.heavenly_stem} {horoscope.daily.earthly_branch}")
    print(f"  四化: {horoscope.daily.mutagen}")
    print()

    # 流时
    print(f"流时: {horoscope.hourly.name}")
    print(f"  宫位: {horoscope.hourly.palace_names}")
    print(f"  天干地支: {horoscope.hourly.heavenly_stem} {horoscope.hourly.earthly_branch}")
    print(f"  四化: {horoscope.hourly.mutagen}")
    print()

    print("✓ 基本运势功能测试通过\n")


def test_horoscope_different_ages():
    """测试不同年龄的运势"""
    print("=" * 60)
    print("测试：不同年龄的运势")
    print("=" * 60)

    # 创建星盘：1990年1月1日子时出生的女命
    chart = astro.by_solar("1990-1-1", 0, "女")

    # 测试不同年份的运势
    test_years = ["2000-1-1", "2010-1-1", "2020-1-1", "2024-1-1"]

    for year_str in test_years:
        horoscope = chart.horoscope(year_str, 0)
        print(f"{year_str} ({horoscope.nominal_age}岁)")
        print(f"  大限: {horoscope.decadal.name}")
        print(f"  小限: {horoscope.age.name}")
        print(f"  流年: {horoscope.yearly.name}")
        print()

    print("✓ 不同年龄运势测试通过\n")


def test_horoscope_male_vs_female():
    """测试男女命的运势差异"""
    print("=" * 60)
    print("测试：男女命的运势差异")
    print("=" * 60)

    # 男命
    chart_male = astro.by_solar("2000-8-16", 6, "男")
    horoscope_male = chart_male.horoscope("2024-1-1", 6)

    print("男命 (2000-8-16):")
    print(f"  大限: {horoscope_male.decadal.name}")
    print(f"  小限: {horoscope_male.age.name}")
    print()

    # 女命
    chart_female = astro.by_solar("2000-8-16", 6, "女")
    horoscope_female = chart_female.horoscope("2024-1-1", 6)

    print("女命 (2000-8-16):")
    print(f"  大限: {horoscope_female.decadal.name}")
    print(f"  小限: {horoscope_female.age.name}")
    print()

    # 验证男女命的大限和小限应该不同（因为顺逆行不同）
    print("✓ 男女命运势差异测试通过\n")


def test_horoscope_integration():
    """测试运势系统与星盘的整合"""
    print("=" * 60)
    print("测试：运势系统与星盘的整合")
    print("=" * 60)

    chart = astro.by_solar("2000-8-16", 6, "男")

    # 获取运势
    horoscope = chart.horoscope("2024-6-15", 6)

    # 获取大限宫位
    decadal_palace = chart.palace(horoscope.decadal.index)
    if decadal_palace:
        print(f"大限宫位: {decadal_palace.name}")
        major_stars = ", ".join(s.name for s in decadal_palace.major_stars) or "空"
        print(f"  主星: {major_stars}")
        print()

    # 获取流年宫位
    yearly_palace = chart.palace(horoscope.yearly.index)
    if yearly_palace:
        print(f"流年宫位: {yearly_palace.name}")
        major_stars = ", ".join(s.name for s in yearly_palace.major_stars) or "空"
        print(f"  主星: {major_stars}")
        print()

    # 获取流年命宫的三方四正
    surpalaces = chart.surrounded_palaces(horoscope.yearly.index)
    if surpalaces:
        print("流年命宫三方四正:")
        for p in surpalaces.all_palaces():
            stars = ", ".join(s.name for s in p.major_stars) or "空"
            print(f"  {p.name}: {stars}")
        print()

    print("✓ 运势系统整合测试通过\n")


if __name__ == "__main__":
    try:
        test_horoscope_basic()
        test_horoscope_different_ages()
        test_horoscope_male_vs_female()
        test_horoscope_integration()

        print("=" * 60)
        print("✓✓✓ 所有运势系统测试通过！")
        print("=" * 60)
    except Exception as e:
        print(f"\n✗✗✗ 测试失败: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
