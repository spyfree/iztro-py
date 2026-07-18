"""
Regression tests for bugs found in the iztro 2.5.8 alignment audit (2026-07).

覆盖以下修复（期望值均与 iztro@2.5.8 默认配置逐项核对过）：
1. 年柱以农历正月初一分界（非立春），yearDivide/horoscopeDivide='normal'
2. 虚岁按农历年差计算
3. 亮度表与 iztro STARS_INFO 对齐（含辅星亮度）
4. 中文星名/宫名查询（palace 列表以寅宫为索引 0，宫名不能当列表下标）
5. FunctionalAstrolabe 保留 language 字段
6. 同宫辅星按 iztro push 顺序排列
"""

from iztro_py import astro
from iztro_py.data.brightness import get_star_brightness


class TestYearDivide:
    """出生日在春节与立春之间时，年柱应取春节（初一）分界。"""

    def test_birth_between_lunar_new_year_and_lichun(self):
        # 1993 年春节为 1-23，立春为 2-4；2-3 出生年柱应为癸酉（1993），而非壬申（1992）
        chart = astro.by_solar("1993-2-3", 6, "男")
        assert chart.chinese_date.startswith("癸酉")
        assert chart.five_elements_class == "木三局"

    def test_birth_before_lunar_new_year(self):
        # 2000 年春节为 2-5；1-20 出生年柱应为己卯（农历 1999 年）
        chart = astro.by_solar("2000-1-20", 6, "男")
        assert chart.chinese_date.startswith("己卯")


class TestNominalAge:
    """虚岁 = 目标农历年 - 出生农历年 + 1。"""

    def test_target_before_lunar_new_year(self):
        # 2024-1-15 仍是农历癸卯（2023）年：2023 - 2000 + 1 = 24
        chart = astro.by_solar("2000-8-16", 6, "男")
        horoscope = chart.horoscope("2024-1-15", 6)
        assert horoscope.nominal_age == 24
        # 与 iztro 一致的大限/小限落宫
        assert horoscope.decadal.index == 1
        assert horoscope.age.index == 7

    def test_birth_before_lunar_new_year(self):
        # 出生 2000-1-20 为农历己卯（1999）年：2024 - 1999 + 1 = 26
        chart = astro.by_solar("2000-1-20", 6, "男")
        horoscope = chart.horoscope("2024-6-1", 6)
        assert horoscope.nominal_age == 26


class TestBrightness:
    """亮度表与 iztro STARS_INFO 对齐。"""

    def test_major_star_brightness_values(self):
        # 旧表除紫微外均与 iztro 不一致，抽查修正后的值
        assert get_star_brightness("tianjiMaj", "maoEarthly") == "旺"
        assert get_star_brightness("tianfuMaj", "maoEarthly") == "得"  # 旧表错误地全标庙
        assert get_star_brightness("taiyangMaj", "shenEarthly") == "得"
        assert get_star_brightness("ziweiMaj", "wuEarthly") == "庙"

    def test_minor_star_brightness_applied(self):
        # 辅星（文昌文曲火铃羊陀）也有亮度；擎羊在四马地（寅申巳亥）不标亮度
        assert get_star_brightness("qingyangMin", "yinEarthly") is None
        assert get_star_brightness("qingyangMin", "maoEarthly") == "陷"
        chart = astro.by_solar("2000-8-16", 6, "男")
        huoxing = chart.star("huoxingMin")
        assert huoxing is not None
        assert huoxing.brightness == "陷"


class TestChineseNameLookup:
    """中文星名/宫名查询。"""

    def test_star_by_chinese_name(self):
        chart = astro.by_solar("2000-8-16", 6, "男")
        assert chart.star("紫微") is not None
        assert chart.star("紫微").name == chart.star("ziweiMaj").name
        assert chart.star("左辅") is not None
        assert chart.star("红鸾") is not None
        assert chart.star("不存在的星") is None

    def test_palace_has_with_chinese_names(self):
        chart = astro.by_solar("2000-8-16", 6, "男")
        ziwei_palace = chart.get_soul_palace()
        # 命宫主星为紫微（该盘已与 iztro 核对）
        assert ziwei_palace.has(["紫微"])
        assert ziwei_palace.has_one_of(["紫微", "天府"])

    def test_palace_by_chinese_name_with_rotated_soul_index(self):
        # 该盘命宫在索引 8：宫名序号不能直接当 palaces 列表下标
        chart = astro.by_solar("1995-6-15", 8, "男")
        soul = chart.get_soul_palace()
        assert soul.index == 8

        palace = chart.palace("命宫")
        assert palace is not None
        assert palace.name == "soulPalace"
        assert palace.index == soul.index

        wealth = chart.palace("财帛")
        assert wealth is not None
        assert wealth.name == "wealthPalace"

        friends = chart.palace("仆役宫")
        assert friends is not None
        assert friends.name == "friendsPalace"


class TestLanguageRetention:
    def test_language_field_preserved(self):
        chart = astro.by_solar("2000-8-16", 2, "女", language="en-US")
        assert chart.language == "en-US"
        chart_default = astro.by_solar("2000-8-16", 2, "女")
        assert chart_default.language == "zh-CN"


class TestMinorStarOrder:
    """同宫辅星按 iztro push 顺序排列（禄存在火星之前等）。"""

    def test_minor_star_order_matches_iztro(self):
        chart = astro.by_solar("2000-8-16", 6, "男")
        palace = chart.palace(6)
        names = [star.name for star in palace.minor_stars]
        assert names == ["lucunMin", "huoxingMin"]
