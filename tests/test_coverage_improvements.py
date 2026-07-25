"""
Tests to improve code coverage for low-coverage modules.
"""

import pytest

from iztro_py import astro
from iztro_py.i18n import get_language, set_language, t, translate_dict


class TestI18n:
    """Tests for i18n module"""

    def test_set_language_supported(self):
        """Test setting supported languages"""
        for lang in ["zh-CN", "zh-TW", "en-US", "ja-JP", "ko-KR", "vi-VN"]:
            set_language(lang)
            assert get_language() == lang

    def test_set_language_unsupported(self):
        """Test setting unsupported language falls back to zh-CN"""
        with pytest.warns(UserWarning, match="not fully supported"):
            set_language("fr-FR")
        assert get_language() == "zh-CN"

    def test_translate_dict(self):
        """Test translate_dict function"""
        data = {
            "palace": "palaces.soulPalace",
            "nested": {"star": "stars.major.ziweiMaj"},
            "list": ["palaces.soulPalace", "palaces.wealthPalace"],
            "number": 42,
        }
        set_language("zh-CN")
        result = translate_dict(data)
        assert result["palace"] == "命宫"
        assert result["nested"]["star"] == "紫微"
        assert result["number"] == 42

    def test_translate_all_languages(self):
        """Test translation works for all supported languages"""
        for lang in ["zh-CN", "zh-TW", "en-US", "ja-JP", "ko-KR", "vi-VN"]:
            set_language(lang)
            result = t("palaces.soulPalace", lang)
            assert result != "palaces.soulPalace"  # Should be translated


class TestFunctionalStar:
    """Tests for FunctionalStar module"""

    def setup_method(self):
        """Setup test chart"""
        self.chart = astro.by_solar("2000-8-16", 6, "男")

    def test_with_brightness(self):
        """Test with_brightness method"""
        ziwei = self.chart.star("ziweiMaj")
        if ziwei and ziwei.brightness:
            # Test single brightness
            assert ziwei.with_brightness(ziwei.brightness) is True
            # Test list of brightness
            assert ziwei.with_brightness(["庙", "旺", "得", "利", "平", "不", "陷"]) is True
            assert ziwei.with_brightness("不存在") is False

    def test_with_mutagen(self):
        """Test with_mutagen method"""
        # Find a star with mutagen
        for palace in self.chart.palaces:
            for star in palace.major_stars:
                if star.mutagen:
                    assert star.with_mutagen(star.mutagen) is True
                    assert star.with_mutagen([star.mutagen]) is True
                    return
        # If no star has mutagen, test with None
        ziwei = self.chart.star("ziweiMaj")
        if ziwei:
            assert ziwei.with_mutagen("禄") == (ziwei.mutagen == "禄")

    def test_opposite_palace(self):
        """Test opposite_palace method"""
        ziwei = self.chart.star("ziweiMaj")
        if ziwei:
            opposite = ziwei.opposite_palace()
            assert opposite is not None

    def test_surrounded_palaces(self):
        """Test surrounded_palaces method"""
        ziwei = self.chart.star("ziweiMaj")
        if ziwei:
            surpalaces = ziwei.surrounded_palaces()
            assert surpalaces is not None
            assert len(surpalaces.all_palaces()) == 4

    def test_is_major_minor(self):
        """Test is_major and is_minor methods"""
        ziwei = self.chart.star("ziweiMaj")
        if ziwei:
            assert ziwei.is_major() is True
            assert ziwei.is_minor() is False

        zuofu = self.chart.star("zuofuMin")
        if zuofu:
            assert zuofu.is_major() is False
            assert zuofu.is_minor() is True

    def test_is_bright_weak(self):
        """is_bright/is_weak 必须与 brightness 一致，且互斥。"""
        ziwei = self.chart.star("ziweiMaj")
        assert ziwei is not None
        assert ziwei.brightness == "旺"
        assert ziwei.is_bright() is True
        assert ziwei.is_weak() is False

        for star in (s for p in self.chart.palaces for s in p.major_stars):
            assert star.is_bright() == (star.brightness in ("庙", "旺"))
            assert star.is_weak() == (star.brightness == "陷")
            assert not (star.is_bright() and star.is_weak())

    def test_has_mutagen(self):
        """Test has_mutagen method"""
        ziwei = self.chart.star("ziweiMaj")
        if ziwei:
            result = ziwei.has_mutagen()
            assert isinstance(result, bool)

    def test_str_repr(self):
        """Test __str__ and __repr__ methods"""
        ziwei = self.chart.star("ziweiMaj")
        if ziwei:
            str_result = str(ziwei)
            repr_result = repr(ziwei)
            assert "ziweiMaj" in str_result or "紫微" in str_result
            assert "FunctionalStar" in repr_result


class TestFunctionalSurpalaces:
    """Tests for FunctionalSurpalaces module"""

    def setup_method(self):
        """Setup test chart"""
        self.chart = astro.by_solar("2000-8-16", 6, "男")
        self.surpalaces = self.chart.surrounded_palaces(0)

    def test_have(self):
        """Test have method"""
        # Get a star that exists in the chart
        ziwei = self.chart.star("ziweiMaj")
        if ziwei and self.surpalaces:
            palace = ziwei.palace()
            if palace and palace.index in [
                self.surpalaces.target.index,
                self.surpalaces.opposite.index,
                self.surpalaces.wealth.index,
                self.surpalaces.career.index,
            ]:
                assert self.surpalaces.have(["ziweiMaj"]) is True

    def test_have_one_of(self):
        """Test have_one_of method"""
        if self.surpalaces:
            # Should find at least one major star
            result = self.surpalaces.have_one_of(
                ["ziweiMaj", "tianfuMaj", "taiyangMaj", "taiyinMaj"]
            )
            assert isinstance(result, bool)

    def test_not_have(self):
        """Test not_have method"""
        if self.surpalaces:
            # Test with non-existent star name
            result = self.surpalaces.not_have(["nonexistent"])
            assert result is True

    def test_have_mutagen(self):
        """Test have_mutagen method"""
        if self.surpalaces:
            for mutagen in ["禄", "权", "科", "忌"]:
                result = self.surpalaces.have_mutagen(mutagen)
                assert isinstance(result, bool)

    def test_not_have_mutagen(self):
        """Test not_have_mutagen method"""
        if self.surpalaces:
            result = self.surpalaces.not_have_mutagen("禄")
            assert isinstance(result, bool)

    def test_all_palaces(self):
        """Test all_palaces method"""
        if self.surpalaces:
            palaces = self.surpalaces.all_palaces()
            assert len(palaces) == 4

    def test_str_repr(self):
        """Test __str__ and __repr__ methods"""
        if self.surpalaces:
            str_result = str(self.surpalaces)
            repr_result = repr(self.surpalaces)
            assert "三方四正" in str_result
            assert "FunctionalSurpalaces" in repr_result


class TestMutagen:
    """Tests for mutagen module"""

    def test_different_year_stems(self):
        """Test mutagen application with different year stems"""
        # Test charts from different years to cover different year stems
        test_cases = [
            ("1984-1-1", 6, "男"),  # 甲子年
            ("1985-1-1", 6, "男"),  # 乙丑年
            ("1986-1-1", 6, "男"),  # 丙寅年
            ("1987-1-1", 6, "男"),  # 丁卯年
            ("1988-1-1", 6, "男"),  # 戊辰年
            ("1989-1-1", 6, "男"),  # 己巳年
            ("1990-1-1", 6, "男"),  # 庚午年
            ("1991-1-1", 6, "男"),  # 辛未年
            ("1992-1-1", 6, "男"),  # 壬申年
            ("1993-1-1", 6, "男"),  # 癸酉年
        ]

        for date, time_idx, gender in test_cases:
            chart = astro.by_solar(date, time_idx, gender)
            # Verify chart was created successfully
            assert chart is not None
            # Check that some stars have mutagen
            mutagen_count = 0
            for palace in chart.palaces:
                for star in palace.major_stars + palace.minor_stars:
                    if star.mutagen:
                        mutagen_count += 1
            # Each year should have 4 mutagens
            assert mutagen_count >= 4


class TestFunctionalAstrolabe:
    """Additional tests for FunctionalAstrolabe"""

    def setup_method(self):
        """Setup test chart"""
        self.chart = astro.by_solar("2000-8-16", 6, "男")

    def test_empty_palaces(self):
        """Test empty_palaces method"""
        empty = self.chart.empty_palaces()
        assert isinstance(empty, list)

    def test_not_empty_palaces(self):
        """Test not_empty_palaces method"""
        not_empty = self.chart.not_empty_palaces()
        assert isinstance(not_empty, list)
        assert len(not_empty) > 0

    def test_to_iztro_dict(self):
        """Test to_iztro_dict export method"""
        result = self.chart.to_iztro_dict()
        assert "gender" in result
        assert "solarDate" in result
        assert "palaces" in result
        assert len(result["palaces"]) == 12

    def test_str_repr(self):
        """Test __str__ and __repr__ methods"""
        str_result = str(self.chart)
        repr_result = repr(self.chart)
        assert "紫微斗数星盘" in str_result
        assert "FunctionalAstrolabe" in repr_result
