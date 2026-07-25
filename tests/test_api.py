"""
Test the main API interface
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from iztro_py import astro


def test_by_solar_api():
    """测试by_solar API"""
    print("=" * 60)
    print("测试：by_solar API")
    print("=" * 60)

    # 通过astro模块调用
    chart = astro.by_solar("2000-8-16", 6, "男")

    print(f"性别: {chart.gender}")
    print(f"阳历: {chart.solar_date}")
    print(f"农历: {chart.lunar_date}")
    print(f"四柱: {chart.chinese_date}")
    print(f"生肖: {chart.zodiac}")
    print(f"星座: {chart.sign}")
    print(f"五行局: {chart.five_elements_class}")

    # 验证基本信息
    assert chart.gender == "男"
    assert chart.zodiac == "龙"
    assert chart.sign == "狮子座"

    print("✓ by_solar API测试通过\n")


def test_functional_palace():
    """测试FunctionalPalace功能"""
    print("=" * 60)
    print("测试：FunctionalPalace功能")
    print("=" * 60)

    chart = astro.by_solar("2000-8-16", 6, "男")

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
        assert has_first is True

    # 测试is_empty
    is_empty = soul_palace.is_empty()
    print(f"命宫是否空宫: {is_empty}")

    # 测试has_mutagen
    has_lu = soul_palace.has_mutagen("禄")
    print(f"命宫是否有化禄: {has_lu}")

    print("✓ FunctionalPalace功能测试通过\n")


def test_functional_star():
    """FunctionalStar 的宫位/对宫/三方四正导航与亮度判断。"""
    chart = astro.by_solar("2000-8-16", 6, "男")
    ziwei = chart.star("紫微")

    assert ziwei is not None
    assert ziwei.name == "ziweiMaj"
    assert ziwei.brightness == "旺"
    assert ziwei.mutagen is None
    assert ziwei.is_major() is True
    assert ziwei.is_minor() is False
    assert ziwei.is_bright() is True
    assert ziwei.is_weak() is False
    assert ziwei.with_brightness(["庙", "旺"]) is True
    assert ziwei.with_mutagen("禄") is False

    palace = ziwei.palace()
    assert palace is not None and palace.name == "soulPalace" and palace.index == 0

    opposite = ziwei.opposite_palace()
    assert opposite is not None and opposite.name == "surfacePalace" and opposite.index == 6

    surpalaces = ziwei.surrounded_palaces()
    assert surpalaces is not None
    assert [p.index for p in surpalaces.all_palaces()] == [0, 6, 8, 4]


def test_palace_query():
    """按索引 / 中文名 / 英文名查询宫位，以及三方四正。"""
    chart = astro.by_solar("2000-8-16", 6, "男")

    assert chart.palace(0).name == "soulPalace"
    assert chart.palace("财帛").name == "wealthPalace"
    assert chart.palace("财帛").index == 8
    assert chart.palace("career").name == "careerPalace"
    assert chart.palace("career").index == 4
    # 同一个宫位，三种写法必须取到同一个对象
    assert chart.palace("命宫") is chart.palace(0) is chart.palace("soulPalace")
    assert chart.palace("不存在的宫") is None
    assert chart.palace(99) is None

    surpalaces = chart.surrounded_palaces("财帛")
    assert surpalaces is not None
    # 三方四正 = 本宫 / 对宫(+6) / 财帛位(+8) / 官禄位(+4)
    assert [p.index for p in surpalaces.all_palaces()] == [8, 2, 4, 0]
    assert surpalaces.have(["紫微"]) is True
    assert surpalaces.not_have(["紫微"]) is False


def test_complete_workflow():
    """端到端：建盘 -> 命身宫 -> 遍历十二宫 -> 定位星曜 -> 四化。"""
    chart = astro.by_solar("1990-1-1", 0, "女")

    soul = chart.get_soul_palace()
    assert soul.name == "soulPalace"
    assert soul.index == 11
    assert (soul.heavenly_stem, soul.earthly_branch) == ("dingHeavenly", "chouEarthly")

    # 该盘命宫与身宫同宫
    body = chart.get_body_palace()
    assert body.index == soul.index
    assert body.is_body_palace is True

    palaces = [chart.palace(i) for i in range(12)]
    assert all(p is not None for p in palaces)
    assert [p.index for p in palaces] == list(range(12))
    assert len({p.name for p in palaces}) == 12
    assert sum(len(p.major_stars) for p in palaces) == 14
    assert sum(1 for p in palaces if p.is_body_palace) == 1

    ziwei = chart.star("紫微")
    assert ziwei is not None
    assert ziwei.palace().name == "spiritPalace"
    assert ziwei.palace().index == 1
    assert ziwei.brightness == "旺"

    # 生年四化：每盘恰好四颗星带四化，且禄权科忌各一
    mutagens = [
        (s.name, s.mutagen) for p in palaces for s in p.major_stars + p.minor_stars if s.mutagen
    ]
    assert {m for _, m in mutagens} == {"禄", "权", "科", "忌"}
    assert len(mutagens) == 4
    assert dict(mutagens) == {
        "tanlangMaj": "权",
        "wenquMin": "忌",
        "tianliangMaj": "科",
        "wuquMaj": "禄",
    }
