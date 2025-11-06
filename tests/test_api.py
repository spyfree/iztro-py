"""
Test the main API interface
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from iztro_py import astro
from iztro_py import by_solar, by_lunar


def test_by_solar_api():
    """测试by_solar API"""
    print("=" * 60)
    print("测试：by_solar API")
    print("=" * 60)

    # 通过astro模块调用
    chart = astro.by_solar('2000-8-16', 6, '男')

    print(f"性别: {chart.gender}")
    print(f"阳历: {chart.solar_date}")
    print(f"农历: {chart.lunar_date}")
    print(f"四柱: {chart.chinese_date}")
    print(f"生肖: {chart.zodiac}")
    print(f"星座: {chart.sign}")
    print(f"五行局: {chart.five_elements_class}")

    # 验证基本信息
    assert chart.gender == '男'
    assert chart.zodiac == '龙'
    assert chart.sign == '狮子座'

    print("✓ by_solar API测试通过\n")
    return chart


def test_functional_palace():
    """测试FunctionalPalace功能"""
    print("=" * 60)
    print("测试：FunctionalPalace功能")
    print("=" * 60)

    chart = astro.by_solar('2000-8-16', 6, '男')

    # 获取命宫
    soul_palace = chart.get_soul_palace()
    print(f"命宫: {soul_palace}")

    # 测试has方法
    major_stars = [s.name for s in soul_palace.major_stars]
    print(f"命宫主星: {major_stars}")

    if major_stars:
        # 测试has方法
        has_first = soul_palace.has([major_stars[0]])
        print(f"命宫包含 {major_stars[0]}: {has_first}")
        assert has_first == True

    # 测试is_empty
    is_empty = soul_palace.is_empty()
    print(f"命宫是否空宫: {is_empty}")

    # 测试has_mutagen
    has_lu = soul_palace.has_mutagen('禄')
    print(f"命宫是否有化禄: {has_lu}")

    print("✓ FunctionalPalace功能测试通过\n")


def test_functional_star():
    """测试FunctionalStar功能"""
    print("=" * 60)
    print("测试：FunctionalStar功能")
    print("=" * 60)

    chart = astro.by_solar('2000-8-16', 6, '男')

    # 查找紫微星
    ziwei = chart.star('紫微')

    if ziwei:
        print(f"找到紫微星: {ziwei}")
        print(f"  亮度: {ziwei.brightness}")
        print(f"  四化: {ziwei.mutagen}")

        # 测试所在宫位
        palace = ziwei.palace()
        if palace:
            print(f"  所在宫位: {palace.name}")

        # 测试对宫
        opposite = ziwei.opposite_palace()
        if opposite:
            print(f"  对宫: {opposite.name}")

        # 测试三方四正
        surpalaces = ziwei.surrounded_palaces()
        if surpalaces:
            print(f"  三方四正宫位: {[p.name for p in surpalaces.all_palaces()]}")

        # 测试亮度判断
        is_bright = ziwei.is_bright()
        print(f"  是否庙旺: {is_bright}")
    else:
        print("未找到紫微星（可能在其他宫位）")

    print("✓ FunctionalStar功能测试通过\n")


def test_palace_query():
    """测试宫位查询功能"""
    print("=" * 60)
    print("测试：宫位查询功能")
    print("=" * 60)

    chart = astro.by_solar('2000-8-16', 6, '男')

    # 通过索引查询
    palace0 = chart.palace(0)
    print(f"索引0的宫位: {palace0.name if palace0 else None}")

    # 通过中文名称查询
    wealth_palace = chart.palace('财帛')
    print(f"财帛宫: {wealth_palace}")

    # 通过英文名称查询
    career_palace = chart.palace('career')
    print(f"事业宫: {career_palace}")

    # 获取三方四正
    if wealth_palace:
        surpalaces = chart.surrounded_palaces('财帛')
        if surpalaces:
            print(f"财帛宫三方四正: {[p.name for p in surpalaces.all_palaces()]}")

            # 测试三方四正的查询方法
            has_ziwei = surpalaces.have(['紫微'])
            print(f"财帛宫三方四正是否有紫微: {has_ziwei}")

    print("✓ 宫位查询功能测试通过\n")


def test_by_lunar_api():
    """测试by_lunar API"""
    print("=" * 60)
    print("测试：by_lunar API")
    print("=" * 60)

    # 直接从顶层导入调用
    chart = by_lunar('2000-7-17', 6, '男')

    print(f"性别: {chart.gender}")
    print(f"阳历: {chart.solar_date}")
    print(f"农历: {chart.lunar_date}")

    # 验证
    assert chart.gender == '男'
    assert '2000' in chart.solar_date

    print("✓ by_lunar API测试通过\n")


def test_complete_workflow():
    """测试完整工作流"""
    print("=" * 60)
    print("测试：完整工作流")
    print("=" * 60)

    # 1. 创建星盘
    chart = astro.by_solar('1990-1-1', 0, '女')

    # 2. 获取命宫
    soul = chart.get_soul_palace()
    print(f"命宫: {soul.name} [{soul.heavenly_stem} {soul.earthly_branch}]")

    # 3. 获取身宫
    body = chart.get_body_palace()
    print(f"身宫: {body.name}")

    # 4. 遍历所有宫位
    print("\n所有宫位：")
    for i in range(12):
        p = chart.palace(i)
        if p:
            major = ', '.join(s.name for s in p.major_stars) if p.major_stars else '空'
            mutagen_stars = [f"{s.name}化{s.mutagen}" for s in p.major_stars + p.minor_stars if s.mutagen]
            mutagen_str = ', '.join(mutagen_stars) if mutagen_stars else ''

            markers = []
            if p.is_original_palace:
                markers.append("命")
            if p.is_body_palace:
                markers.append("身")
            marker = f"[{'/'.join(markers)}]" if markers else ""

            print(f"  {i:2d}. {p.name:4s}{marker:6s} {major:20s} {mutagen_str}")

    # 5. 查找特定星曜
    print("\n查找紫微星：")
    ziwei = chart.star('紫微')
    if ziwei:
        palace = ziwei.palace()
        print(f"  紫微星在 {palace.name if palace else '?'} 宫")
        print(f"  亮度: {ziwei.brightness}, 是否庙旺: {ziwei.is_bright()}")

    print("✓ 完整工作流测试通过\n")


if __name__ == '__main__':
    try:
        test_by_solar_api()
        test_functional_palace()
        test_functional_star()
        test_palace_query()
        test_by_lunar_api()
        test_complete_workflow()

        print("=" * 60)
        print("✓✓✓ 所有API测试通过！")
        print("=" * 60)
    except Exception as e:
        print(f"\n✗✗✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
