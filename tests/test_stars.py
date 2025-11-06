"""
Test star positioning algorithms
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from iztro_py.star.location import (
    get_ziwei_index,
    get_tianfu_index,
    get_star_indices,
    get_major_star_positions
)
from iztro_py.star.major_star import place_major_stars
from iztro_py.star.minor_star import place_minor_stars
from iztro_py.star.mutagen import apply_mutagen_to_palaces, get_mutagen_stars
from iztro_py.data.brightness import apply_brightness_to_palaces
from iztro_py.data.types import FiveElementsClass
from iztro_py.astro.palace import get_soul_and_body, initialize_palaces
from iztro_py.utils.helpers import get_five_elements_class


def test_ziwei_tianfu_position():
    """测试紫微天府星定位"""
    print("=" * 60)
    print("测试：紫微天府星定位")
    print("=" * 60)

    # 测试案例：金四局、农历17日
    five_class = FiveElementsClass.METAL_4
    lunar_day = 17

    ziwei_index = get_ziwei_index(five_class, lunar_day)
    tianfu_index = get_tianfu_index(ziwei_index)

    print(f"五行局: {five_class}")
    print(f"农历日: {lunar_day}")
    print(f"紫微星宫位索引: {ziwei_index}")
    print(f"天府星宫位索引: {tianfu_index}")

    assert 0 <= ziwei_index <= 11
    assert 0 <= tianfu_index <= 11
    print("✓ 紫微天府星定位测试通过\n")


def test_major_stars_placement():
    """测试14主星安置"""
    print("=" * 60)
    print("测试：14主星安置")
    print("=" * 60)

    # 准备宫位
    soul_and_body = get_soul_and_body(7, 6, 'gengHeavenly')
    palaces = initialize_palaces(soul_and_body)

    # 计算五行局
    five_class = get_five_elements_class(
        soul_and_body.heavenly_stem_of_soul,
        soul_and_body.earthly_branch_of_soul
    )

    # 安置主星
    place_major_stars(palaces, five_class, 17)

    # 统计主星数量
    total_major_stars = sum(len(p['major_stars']) for p in palaces)

    print(f"五行局: {five_class}")
    print(f"农历日: 17")
    print(f"安置的主星总数: {total_major_stars}")

    # 14主星应该都被安置
    assert total_major_stars == 14

    # 打印有主星的宫位
    for palace in palaces:
        if palace['major_stars']:
            star_names = [s.name for s in palace['major_stars']]
            print(f"宫位 {palace['index']} ({palace['name']}): {', '.join(star_names)}")

    print("\n✓ 14主星安置测试通过\n")


def test_minor_stars_placement():
    """测试14辅星安置"""
    print("=" * 60)
    print("测试：14辅星安置")
    print("=" * 60)

    # 准备宫位
    soul_and_body = get_soul_and_body(7, 6, 'gengHeavenly')
    palaces = initialize_palaces(soul_and_body)

    # 安置辅星
    place_minor_stars(
        palaces,
        lunar_month=7,
        time_index=6,
        year_stem='gengHeavenly',
        year_branch='chenEarthly'
    )

    # 统计辅星数量
    total_minor_stars = sum(len(p['minor_stars']) for p in palaces)

    print(f"安置的辅星总数: {total_minor_stars}")

    # 14辅星应该都被安置
    assert total_minor_stars == 14

    # 打印前3个有辅星的宫位
    count = 0
    for palace in palaces:
        if palace['minor_stars'] and count < 3:
            star_names = [s.name for s in palace['minor_stars']]
            print(f"宫位 {palace['index']} ({palace['name']}): {', '.join(star_names)}")
            count += 1

    print("\n✓ 14辅星安置测试通过\n")


def test_mutagen_application():
    """测试四化应用"""
    print("=" * 60)
    print("测试：四化应用")
    print("=" * 60)

    # 准备宫位和星曜
    soul_and_body = get_soul_and_body(7, 6, 'gengHeavenly')
    palaces = initialize_palaces(soul_and_body)
    five_class = get_five_elements_class(
        soul_and_body.heavenly_stem_of_soul,
        soul_and_body.earthly_branch_of_soul
    )

    place_major_stars(palaces, five_class, 17)
    place_minor_stars(palaces, 7, 6, 'gengHeavenly', 'chenEarthly')

    # 应用四化
    year_stem = 'gengHeavenly'
    apply_mutagen_to_palaces(palaces, year_stem)

    # 获取四化星配置
    mutagen_stars = get_mutagen_stars(year_stem)
    print(f"年干: {year_stem}")
    print(f"四化配置: {mutagen_stars}")

    # 统计四化星数量
    mutagen_count = 0
    for palace in palaces:
        for star in palace['major_stars'] + palace['minor_stars']:
            if star.mutagen:
                mutagen_count += 1
                print(f"  {star.name} 化 {star.mutagen}")

    print(f"\n四化星总数: {mutagen_count}")

    # 应该有4颗四化星（禄权科忌）
    assert mutagen_count == 4
    print("✓ 四化应用测试通过\n")


def test_brightness_application():
    """测试亮度应用"""
    print("=" * 60)
    print("测试：亮度应用")
    print("=" * 60)

    # 准备宫位和星曜
    soul_and_body = get_soul_and_body(7, 6, 'gengHeavenly')
    palaces = initialize_palaces(soul_and_body)
    five_class = get_five_elements_class(
        soul_and_body.heavenly_stem_of_soul,
        soul_and_body.earthly_branch_of_soul
    )

    place_major_stars(palaces, five_class, 17)

    # 应用亮度
    apply_brightness_to_palaces(palaces)

    # 统计有亮度的星曜
    brightness_count = 0
    for palace in palaces:
        for star in palace['major_stars']:
            if star.brightness:
                brightness_count += 1
                if brightness_count <= 5:  # 只打印前5颗
                    print(f"  {star.name} 在 {palace['earthly_branch']} 宫: {star.brightness}")

    print(f"\n有亮度标注的星曜数: {brightness_count}")

    # 14主星都应该有亮度
    assert brightness_count == 14
    print("✓ 亮度应用测试通过\n")


if __name__ == '__main__':
    try:
        test_ziwei_tianfu_position()
        test_major_stars_placement()
        test_minor_stars_placement()
        test_mutagen_application()
        test_brightness_application()

        print("=" * 60)
        print("✓✓✓ 所有星曜定位测试通过！")
        print("=" * 60)
    except Exception as e:
        print(f"\n✗✗✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
