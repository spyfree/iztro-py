"""
Test palace positioning algorithms
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from iztro_py.astro.palace import get_soul_and_body, initialize_palaces
from iztro_py.data.types import FiveElementsClass
from iztro_py.data.constants import EARTHLY_BRANCHES
from iztro_py.utils.helpers import get_five_elements_class


def test_soul_and_body_palace():
    """测试命宫身宫定位"""
    print("=" * 60)
    print("测试：命宫身宫定位")
    print("=" * 60)

    # 测试案例：农历7月、午时(6)、庚年
    soul_and_body = get_soul_and_body(
        lunar_month=7,
        time_index=6,
        year_stem='gengHeavenly'
    )

    print(f"命宫索引: {soul_and_body.soul_index}")
    print(f"身宫索引: {soul_and_body.body_index}")
    print(f"命宫天干: {soul_and_body.heavenly_stem_of_soul}")
    print(f"命宫地支: {soul_and_body.earthly_branch_of_soul}")

    # 验证结果
    assert 0 <= soul_and_body.soul_index <= 11
    assert 0 <= soul_and_body.body_index <= 11
    print("✓ 命宫身宫定位测试通过\n")


def test_five_elements_class():
    """测试五行局计算"""
    print("=" * 60)
    print("测试：五行局计算")
    print("=" * 60)

    # 测试案例
    soul_and_body = get_soul_and_body(
        lunar_month=7,
        time_index=6,
        year_stem='gengHeavenly'
    )

    five_class = get_five_elements_class(
        soul_and_body.heavenly_stem_of_soul,
        soul_and_body.earthly_branch_of_soul
    )

    print(f"命宫: {soul_and_body.heavenly_stem_of_soul} {soul_and_body.earthly_branch_of_soul}")
    print(f"五行局: {five_class} ({five_class.value})")

    assert five_class in [
        FiveElementsClass.WATER_2,
        FiveElementsClass.WOOD_3,
        FiveElementsClass.METAL_4,
        FiveElementsClass.EARTH_5,
        FiveElementsClass.FIRE_6
    ]
    print("✓ 五行局计算测试通过\n")


def test_initialize_palaces():
    """测试宫位初始化"""
    print("=" * 60)
    print("测试：宫位初始化")
    print("=" * 60)

    soul_and_body = get_soul_and_body(
        lunar_month=7,
        time_index=6,
        year_stem='gengHeavenly'
    )

    palaces = initialize_palaces(soul_and_body)

    print(f"宫位数量: {len(palaces)}")
    print(f"命宫位置: 索引 {soul_and_body.soul_index}")
    print(f"身宫位置: 索引 {soul_and_body.body_index}")

    # 验证宫位数量
    assert len(palaces) == 12

    # 验证命宫标记（命宫总是第0个宫位）
    assert palaces[0]['is_original_palace'] == True

    # 验证身宫标记（需要根据地支查找）
    body_palace = next(p for p in palaces if p['earthly_branch'] == EARTHLY_BRANCHES[soul_and_body.body_index])
    assert body_palace['is_body_palace'] == True

    # 打印前3个宫位信息
    for i in range(3):
        palace = palaces[i]
        print(f"\n宫位 {i}: {palace['name']}")
        print(f"  天干地支: {palace['heavenly_stem']} {palace['earthly_branch']}")
        print(f"  是否命宫: {palace['is_original_palace']}")
        print(f"  是否身宫: {palace['is_body_palace']}")

    print("\n✓ 宫位初始化测试通过\n")


if __name__ == '__main__':
    try:
        test_soul_and_body_palace()
        test_five_elements_class()
        test_initialize_palaces()

        print("=" * 60)
        print("✓✓✓ 所有宫位定位测试通过！")
        print("=" * 60)
    except Exception as e:
        print(f"\n✗✗✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
