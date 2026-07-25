"""
Regression tests for bugs found in the iztro 2.5.8 alignment audit (2026-07).

覆盖以下修复（期望值均与 iztro@2.5.8 默认配置逐项核对过）：
1. 年柱以农历正月初一分界（非立春），yearDivide/horoscopeDivide='normal'
2. 虚岁按农历年差计算
3. 亮度表与 iztro STARS_INFO 对齐（含辅星亮度）
4. 中文星名/宫名查询（palace 列表以寅宫为索引 0，宫名不能当列表下标）
5. FunctionalAstrolabe 保留 language 字段
6. 同宫辅星按 iztro push 顺序排列
7. `utils` 导出的历法函数与生产路径（四柱计算）保持一致
"""

from datetime import date, timedelta

from iztro_py import astro
from iztro_py.data.brightness import get_star_brightness
from iztro_py.utils.calendar import (
    get_day_stem_branch,
    get_heavenly_stem_and_earthly_branch_date,
    get_time_stem_branch,
    get_year_stem_branch,
)


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


class TestExportedCalendarHelpers:
    """`iztro_py.utils` 导出的历法函数必须与生产路径（四柱计算）一致。

    这几个函数库内部并不调用，所以对齐测试覆盖不到它们。此前
    `get_day_stem_branch` 用自制的公元元年偏移量，锚点算错，**每一个日期**
    的日柱都偏了 51 天，却因为无人断言其返回值而长期存活。
    """

    def test_day_stem_branch_matches_production_path(self):
        """跨 150 年抽样比对，任一日期都不得与四柱计算分叉。"""
        start = date(1900, 1, 1)
        checked = 0
        for offset in range(0, 55000, 97):
            day = start + timedelta(days=offset)
            # time_index=6（午时）：远离晚子时进位，日柱即该日历日的日柱
            expected = get_heavenly_stem_and_earthly_branch_date(day.year, day.month, day.day, 6)
            assert get_day_stem_branch(day) == (
                expected.day_stem,
                expected.day_branch,
            ), f"day pillar mismatch on {day.isoformat()}"
            checked += 1
        assert checked > 500

    def test_day_stem_branch_known_values(self):
        # 用 iztro@2.5.8 核对过的固定值
        assert get_day_stem_branch(date(1900, 1, 1)) == ("jiaHeavenly", "xuEarthly")  # 甲戌
        assert get_day_stem_branch(date(2000, 8, 16)) == ("bingHeavenly", "wuEarthly")  # 丙午
        assert get_day_stem_branch(date(1990, 10, 21)) == ("jiHeavenly", "weiEarthly")  # 己未

    def test_day_stem_branch_does_not_roll_for_late_rat_hour(self):
        """本函数只认日历日；晚子时进位是四柱计算的职责，不在这里发生。"""
        day = date(1990, 10, 21)
        assert get_day_stem_branch(day) == ("jiHeavenly", "weiEarthly")  # 己未
        late_rat = get_heavenly_stem_and_earthly_branch_date(1990, 10, 21, 12)
        assert (late_rat.day_stem, late_rat.day_branch) == ("gengHeavenly", "shenEarthly")  # 庚申

    def test_year_stem_branch_takes_lunar_year_not_solar_year(self):
        """入参是农历年。传阳历年在元旦-春节之间会差一年——这是函数契约，不是 bug。"""
        assert get_year_stem_branch(2000) == ("gengHeavenly", "chenEarthly")  # 庚辰

        # 2000-01-20 当天农历仍是己卯年，生产路径给出己卯
        actual = get_heavenly_stem_and_earthly_branch_date(2000, 1, 20, 6)
        assert (actual.year_stem, actual.year_branch) == ("jiHeavenly", "maoEarthly")  # 己卯
        # 传该日所属的农历年才对得上
        assert get_year_stem_branch(1999) == (actual.year_stem, actual.year_branch)

    def test_time_stem_branch_needs_next_day_stem_for_late_rat_hour(self):
        """晚子时须传次日日干；文档已明确，此处把行为钉死。"""
        expected = get_heavenly_stem_and_earthly_branch_date(1990, 10, 21, 12)
        assert (expected.time_stem, expected.time_branch) == ("bingHeavenly", "ziEarthly")  # 丙子

        same_day = get_day_stem_branch(date(1990, 10, 21))[0]  # 己
        next_day = get_day_stem_branch(date(1990, 10, 22))[0]  # 庚
        assert get_time_stem_branch(next_day, 12) == (expected.time_stem, expected.time_branch)
        assert get_time_stem_branch(same_day, 12) != (expected.time_stem, expected.time_branch)

    def test_time_stem_branch_matches_production_for_normal_hours(self):
        for time_index in range(0, 12):
            expected = get_heavenly_stem_and_earthly_branch_date(2000, 8, 16, time_index)
            day_stem = get_day_stem_branch(date(2000, 8, 16))[0]
            assert get_time_stem_branch(day_stem, time_index) == (
                expected.time_stem,
                expected.time_branch,
            ), f"time pillar mismatch at time_index={time_index}"


class TestHoroscopeOutOfRange:
    """虚岁不落在任何大限/小限区间时返回 index=-1，而不是静默落回命宫。

    此前越界会 fallback 到 `palaces[0]`，于是「出生前」「虚岁 0」「超过末个
    大限」三种查询都会安静地给出命宫，调用方无从分辨。期望值取自 iztro@2.5.8。
    """

    def test_date_before_birth(self):
        chart = astro.by_solar("2000-8-16", 6, "男")
        horoscope = chart.horoscope("1990-1-1", 6)
        assert horoscope.nominal_age == -10
        assert horoscope.decadal.index == -1
        assert horoscope.age.index == -1

    def test_nominal_age_zero(self):
        # 2000-1-1 仍是农历己卯年：1999 - 2000 + 1 = 0，第一个大限尚未开始
        chart = astro.by_solar("2000-8-16", 6, "男")
        horoscope = chart.horoscope("2000-1-1", 6)
        assert horoscope.nominal_age == 0
        assert horoscope.decadal.index == -1
        assert horoscope.age.index == -1

    def test_age_beyond_last_decadal(self):
        chart = astro.by_solar("2000-8-16", 6, "男")
        horoscope = chart.horoscope("2130-1-1", 6)
        assert horoscope.nominal_age == 130
        assert horoscope.decadal.index == -1
        assert horoscope.age.index == -1

    def test_in_range_still_resolves(self):
        chart = astro.by_solar("2000-8-16", 6, "男")
        horoscope = chart.horoscope("2024-1-15", 6)
        assert horoscope.decadal.index == 1
        assert horoscope.age.index == 7

    def test_childhood_limit_still_resolves(self):
        # 虚岁 1 落在童限，不应被越界分支吃掉
        chart = astro.by_solar("2000-8-16", 6, "男")
        horoscope = chart.horoscope("2000-8-16", 6)
        assert horoscope.nominal_age == 1
        assert horoscope.decadal.name == "童限"
        assert horoscope.decadal.index == 0
        assert horoscope.age.index == 8

    def test_out_of_range_degenerate_fields_match_iztro(self):
        chart = astro.by_solar("2000-8-16", 6, "男")
        decadal = chart.horoscope("1990-1-1", 6).decadal
        # iztro 对 index=-1 恒返回甲子及甲干四化
        assert decadal.heavenly_stem == "jiaHeavenly"
        assert decadal.earthly_branch == "ziEarthly"
        assert decadal.palace_names[0] == "parentsPalace"
        assert decadal.palace_names[-1] == "soulPalace"


class TestTimeName:
    """早子时与晚子时必须区分：两者日柱不同（晚子时按次日计算）。"""

    def test_early_and_late_rat_hour_are_distinct(self):
        assert astro.by_solar("1990-10-21", 0, "女").time == "早子时"
        assert astro.by_solar("1990-10-21", 12, "女").time == "晚子时"

    def test_other_hours_unchanged(self):
        assert astro.by_solar("1990-10-21", 6, "女").time == "午时"
        assert astro.by_solar("1990-10-21", 8, "女").time == "申时"


class TestPerChartLanguage:
    """翻译默认取所属星盘的语言，不再受进程全局语言影响。

    此前 `translate_name()` 直接读全局 `_current_language`，于是新建一张别的
    语言的星盘会静默改掉已有星盘的输出——而 `chart.language` 字段仍显示原
    语言，让人以为一切正常。
    """

    def test_building_another_chart_does_not_mutate_earlier_one(self):
        en = astro.by_solar("2000-8-16", 6, "男", language="en-US")
        before = en.get_soul_palace().translate_name()
        assert before == "Soul"

        astro.by_solar("2000-8-16", 6, "男", language="zh-CN")
        assert en.get_soul_palace().translate_name() == before
        assert en.star("紫微").translate_name() == "Ziwei"

    def test_global_set_language_does_not_leak_into_existing_charts(self):
        import iztro_py.i18n as i18n

        previous = i18n.get_language()
        try:
            en = astro.by_solar("2000-8-16", 6, "男", language="en-US")
            zh = astro.by_solar("2000-8-16", 6, "男", language="zh-CN")
            i18n.set_language("ko-KR")
            assert en.get_soul_palace().translate_name() == "Soul"
            assert zh.get_soul_palace().translate_name() == "命宫"
        finally:
            i18n.set_language(previous)

    def test_explicit_lang_argument_still_wins(self):
        chart = astro.by_solar("2000-8-16", 6, "男", language="en-US")
        assert chart.get_soul_palace().translate_name("zh-CN") == "命宫"
        assert chart.star("紫微").translate_name("zh-CN") == "紫微"

    def test_set_language_is_scoped_to_the_chart(self):
        a = astro.by_solar("2000-8-16", 6, "男", language="zh-CN")
        b = astro.by_solar("2000-8-16", 6, "男", language="zh-CN")
        a.set_language("en-US")
        assert a.get_soul_palace().translate_name() == "Soul"
        assert b.get_soul_palace().translate_name() == "命宫"

    def test_to_iztro_dict_uses_the_chart_language(self):
        en = astro.by_solar("2000-8-16", 6, "男", language="en-US")
        astro.by_solar("2000-8-16", 6, "男", language="zh-CN")
        exported = en.to_iztro_dict()
        assert exported["palaces"][0]["name"] == "Soul"

    def test_detached_star_falls_back_to_global_language(self):
        from iztro_py.data.types import Star

        star = Star(name="ziweiMaj", type="major", scope="origin")
        assert star.translate_name("en-US") == "Ziwei"
        assert star.translate_name("zh-CN") == "紫微"
