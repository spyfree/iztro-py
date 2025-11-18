"""
Compatibility tests with original iztro library

Tests to ensure iztro-py API is compatible with the original JavaScript iztro library.
Uses known test cases and expected outputs from the original library.
"""

import pytest
from iztro_py import astro


class TestAPICompatibility:
    """Test API compatibility with original iztro"""

    def test_by_solar_signature(self):
        """Test by_solar function signature matches original"""
        # Original: astro.bySolar('2000-8-16', 2, '女', true, 'zh-CN')
        result = astro.by_solar("2000-8-16", 2, "女", True, "zh-CN")

        assert result is not None
        assert hasattr(result, "gender")
        assert hasattr(result, "solar_date")
        assert hasattr(result, "lunar_date")
        assert hasattr(result, "palaces")
        assert hasattr(result, "palace")
        assert hasattr(result, "star")

    def test_by_lunar_signature(self):
        """Test by_lunar function signature matches original"""
        # Original: astro.byLunar('2000-7-17', 2, '女', false, true, 'zh-CN')
        result = astro.by_lunar("2000-7-17", 2, "女", False, True, "zh-CN")

        assert result is not None
        assert result.gender == "女"

    def test_astrolabe_basic_properties(self):
        """Test astrolabe object has all required properties"""
        chart = astro.by_solar("2000-8-16", 6, "男")

        # Basic properties
        assert chart.gender == "男"
        assert chart.solar_date == "2000-8-16"
        assert "龙" == chart.zodiac  # 龙年
        assert "狮子座" == chart.sign

        # Chinese date properties
        assert chart.chinese_date is not None
        assert chart.lunar_date is not None
        assert chart.five_elements_class is not None

        # Palaces
        assert len(chart.palaces) == 12

    def test_palace_method(self):
        """Test palace() method works like original"""
        chart = astro.by_solar("2000-8-16", 6, "男")

        # By index (0-11)
        palace_0 = chart.palace(0)
        assert palace_0 is not None
        assert palace_0.index == 0

        # By English name
        career = chart.palace("careerPalace")
        assert career is not None

        # By Chinese name (if supported)
        wealth = chart.palace("财帛")
        assert wealth is not None

    def test_star_method(self):
        """Test star() method returns star with correct properties"""
        chart = astro.by_solar("2000-8-16", 6, "男")

        # Find a star
        ziwei = chart.star("ziweiMaj")
        assert ziwei is not None

        # Star properties
        assert hasattr(ziwei, "name")
        assert hasattr(ziwei, "brightness")
        assert hasattr(ziwei, "mutagen")
        assert hasattr(ziwei, "type")

        # Star methods
        assert hasattr(ziwei, "palace")
        assert hasattr(ziwei, "is_bright")

    def test_surrounded_palaces_method(self):
        """Test surroundedPalaces() / surrounded_palaces() method"""
        chart = astro.by_solar("2000-8-16", 6, "男")

        # Get surrounded palaces
        surpalaces = chart.surrounded_palaces(0)
        assert surpalaces is not None

        # Check it has required palaces
        assert hasattr(surpalaces, "target")
        assert hasattr(surpalaces, "opposite")
        assert hasattr(surpalaces, "wealth")
        assert hasattr(surpalaces, "career")

        # Check methods
        assert hasattr(surpalaces, "have")
        assert hasattr(surpalaces, "have_mutagen")

    def test_palace_has_method(self):
        """Test palace.has() method for checking stars"""
        chart = astro.by_solar("2000-8-16", 6, "男")
        soul = chart.get_soul_palace()

        # has() method accepts list of star names
        result = soul.has(["tianjiMaj"])
        assert isinstance(result, bool)

    def test_palace_has_mutagen_method(self):
        """Test palace.has_mutagen() for checking four transformations"""
        chart = astro.by_solar("2000-8-16", 6, "男")

        # Check various palaces for mutagen
        for palace in chart.palaces:
            result = palace.has_mutagen("禄")
            assert isinstance(result, bool)

            result = palace.has_mutagen("权")
            assert isinstance(result, bool)

            result = palace.has_mutagen("科")
            assert isinstance(result, bool)

            result = palace.has_mutagen("忌")
            assert isinstance(result, bool)

    def test_palace_is_empty_method(self):
        """Test palace.is_empty() method"""
        chart = astro.by_solar("2000-8-16", 6, "男")

        # Should have both empty and non-empty palaces
        has_empty = False
        has_non_empty = False

        for palace in chart.palaces:
            if palace.is_empty():
                has_empty = True
            else:
                has_non_empty = True

        assert has_empty, "Should have at least one empty palace"
        assert has_non_empty, "Should have at least one non-empty palace"

    def test_star_palace_method(self):
        """Test star.palace() returns the palace containing the star"""
        chart = astro.by_solar("2000-8-16", 6, "男")

        ziwei = chart.star("ziweiMaj")
        if ziwei:
            palace = ziwei.palace()
            assert palace is not None
            # Verify star is in that palace
            assert ziwei.name in [s.name for s in palace.major_stars]

    def test_star_surrounded_palaces_method(self):
        """Test star.surrounded_palaces() method"""
        chart = astro.by_solar("2000-8-16", 6, "男")

        ziwei = chart.star("ziweiMaj")
        if ziwei:
            surpalaces = ziwei.surrounded_palaces()
            assert surpalaces is not None

    def test_star_brightness_check(self):
        """Test star brightness checking methods"""
        chart = astro.by_solar("2000-8-16", 6, "男")

        ziwei = chart.star("ziweiMaj")
        if ziwei:
            # is_bright() method
            result = ziwei.is_bright()
            assert isinstance(result, bool)

            # brightness property
            assert ziwei.brightness in ["庙", "旺", "得", "利", "平", "不", "陷", None]

    def test_horoscope_method(self):
        """Test horoscope() method returns correct structure"""
        chart = astro.by_solar("2000-8-16", 6, "男")

        # Get horoscope for a specific date
        horoscope = chart.horoscope("2024-1-1", 6)

        assert horoscope is not None

        # Check all horoscope levels exist
        assert hasattr(horoscope, "decadal")  # 大限
        assert hasattr(horoscope, "age")  # 小限
        assert hasattr(horoscope, "yearly")  # 流年
        assert hasattr(horoscope, "monthly")  # 流月
        assert hasattr(horoscope, "daily")  # 流日
        assert hasattr(horoscope, "hourly")  # 流时

        # Check nominal age
        assert hasattr(horoscope, "nominal_age")
        assert horoscope.nominal_age > 0

    def test_horoscope_item_structure(self):
        """Test horoscope items have correct structure"""
        chart = astro.by_solar("2000-8-16", 6, "男")
        horoscope = chart.horoscope("2024-1-1", 6)

        # Each horoscope level should have these properties
        for item in [horoscope.decadal, horoscope.yearly, horoscope.monthly]:
            assert hasattr(item, "name")
            assert hasattr(item, "heavenly_stem")
            assert hasattr(item, "earthly_branch")
            assert hasattr(item, "palace_names")
            assert hasattr(item, "index")


class TestKnownTestCases:
    """Test with known test cases from original iztro documentation"""

    def test_example_1_male_chart(self):
        """Test case: 2000-8-16 午时 男"""
        chart = astro.by_solar("2000-8-16", 6, "男")

        # Basic info
        assert chart.gender == "男"
        assert chart.zodiac == "龙"
        assert chart.sign == "狮子座"
        assert "金四局" in chart.five_elements_class

        # Soul palace should be at spiritPalace (福德宫) for this birth data
        soul = chart.get_soul_palace()
        assert soul is not None

        # This specific chart should have certain major stars
        ziwei = chart.star("ziweiMaj")
        assert ziwei is not None
        assert ziwei.brightness in ["庙", "旺", "得", "利", "平"]

    def test_example_2_female_chart(self):
        """Test case: 2000-8-16 午时 女"""
        chart = astro.by_solar("2000-8-16", 6, "女")

        # Basic info
        assert chart.gender == "女"
        assert chart.zodiac == "龙"

        # Female charts have different decadal progression
        horoscope = chart.horoscope("2024-1-1", 6)
        assert horoscope is not None
        assert horoscope.nominal_age == 25

    def test_lunar_solar_consistency(self):
        """Test that lunar and solar dates produce same chart"""
        # 2000-8-16 is lunar 2000-7-17
        chart_solar = astro.by_solar("2000-8-16", 6, "男")
        chart_lunar = astro.by_lunar("2000-7-17", 6, "男", False)

        # Should produce same astrolabe
        assert chart_solar.gender == chart_lunar.gender
        assert chart_solar.zodiac == chart_lunar.zodiac
        assert chart_solar.five_elements_class == chart_lunar.five_elements_class

        # Palaces should be same
        for i in range(12):
            p1 = chart_solar.palace(i)
            p2 = chart_lunar.palace(i)
            assert len(p1.major_stars) == len(p2.major_stars)

    def test_chain_method_pattern(self):
        """Test method chaining like: star('紫微').surrounded_palaces().have_mutagen('忌')"""
        chart = astro.by_solar("2000-8-16", 6, "男")

        # This pattern should work
        ziwei = chart.star("ziweiMaj")
        if ziwei:
            surpalaces = ziwei.surrounded_palaces()
            if surpalaces:
                result = surpalaces.have_mutagen("忌")
                assert isinstance(result, bool)

    def test_all_14_major_stars_present(self):
        """Test that all 14 major stars are placed in the chart"""
        chart = astro.by_solar("2000-8-16", 6, "男")

        major_stars = [
            "ziweiMaj",
            "tianjiMaj",
            "taiyangMaj",
            "wuquMaj",
            "tiantongMaj",
            "lianzhenMaj",
            "tianfuMaj",
            "taiyinMaj",
            "tanlangMaj",
            "jumenMaj",
            "tianxiangMaj",
            "tianliangMaj",
            "qishaMaj",
            "pojunMaj",
        ]

        found_count = 0
        for star_name in major_stars:
            star = chart.star(star_name)
            if star:
                found_count += 1

        assert found_count == 14, f"Should have all 14 major stars, found {found_count}"

    def test_four_transformations_present(self):
        """Test that four transformations (四化) are applied"""
        chart = astro.by_solar("2000-8-16", 6, "男")

        # Count stars with mutagen
        mutagen_count = {"禄": 0, "权": 0, "科": 0, "忌": 0}

        for palace in chart.palaces:
            for star in palace.major_stars + palace.minor_stars:
                if star.mutagen:
                    mutagen_count[star.mutagen] += 1

        # Should have one of each transformation (for origin scope)
        assert mutagen_count["禄"] >= 1, "Should have at least one 化禄"
        assert mutagen_count["权"] >= 1, "Should have at least one 化权"
        assert mutagen_count["科"] >= 1, "Should have at least one 化科"
        assert mutagen_count["忌"] >= 1, "Should have at least one 化忌"

    def test_get_soul_and_body_palace(self):
        """Test get_soul_palace() and get_body_palace() methods"""
        chart = astro.by_solar("2000-8-16", 6, "男")

        soul = chart.get_soul_palace()
        body = chart.get_body_palace()

        assert soul is not None
        assert body is not None
        assert soul.is_original_palace is True
        assert body.is_body_palace is True


class TestEdgeCases:
    """Test edge cases and special scenarios"""

    def test_leap_month_handling(self):
        """Test leap month handling"""
        # Use a year with leap month
        chart = astro.by_solar("2023-5-1", 6, "男", True)
        assert chart is not None

    def test_early_and_late_zi_hour(self):
        """Test early 子时 (0) and late 子时 (12)"""
        chart1 = astro.by_solar("2000-8-16", 0, "男")  # Early 子时
        chart2 = astro.by_solar("2000-8-16", 12, "男")  # Late 子时

        assert chart1 is not None
        assert chart2 is not None
        # They might have different configurations

    def test_different_time_indices(self):
        """Test all time indices 0-12"""
        for time_index in range(13):
            chart = astro.by_solar("2000-8-16", time_index, "男")
            assert chart is not None
            assert len(chart.palaces) == 12

    def test_multiple_languages(self):
        """Test language parameter acceptance"""
        languages = ["zh-CN", "zh-TW", "en-US", "ja-JP", "ko-KR", "vi-VN"]

        for lang in languages:
            chart = astro.by_solar("2000-8-16", 6, "男", True, lang)
            assert chart is not None

    def test_horoscope_different_years(self):
        """Test horoscope calculation for different years"""
        chart = astro.by_solar("2000-8-16", 6, "男")

        years = ["2020-1-1", "2024-1-1", "2030-1-1"]
        for year_date in years:
            horoscope = chart.horoscope(year_date, 6)
            assert horoscope is not None
            assert horoscope.nominal_age > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
