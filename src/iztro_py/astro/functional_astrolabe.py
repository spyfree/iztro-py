"""
FunctionalAstrolabe class - Complete astrolabe with functional methods

The main class for interacting with a Zi Wei Dou Shu astrolabe.
Provides rich API for querying palaces, stars, and their relationships.
"""

from typing import List, Optional, Union
from iztro_py.data.types import Astrolabe, PalaceName, StarName
from iztro_py.astro.functional_palace import FunctionalPalace
from iztro_py.astro.functional_star import FunctionalStar
from iztro_py.astro.functional_surpalaces import FunctionalSurpalaces
from iztro_py.data.constants import get_surrounded_indices
from iztro_py.i18n import t


class FunctionalAstrolabe(Astrolabe):
    """
    功能增强的星盘类

    继承自Astrolabe，提供丰富的查询和链式调用API
    """

    def __init__(self, astrolabe: Astrolabe):
        """
        初始化FunctionalAstrolabe

        Args:
            astrolabe: 基础Astrolabe对象
        """
        # 转换宫位为FunctionalPalace
        functional_palaces = [FunctionalPalace(p) for p in astrolabe.palaces]

        super().__init__(
            gender=astrolabe.gender,
            solar_date=astrolabe.solar_date,
            lunar_date=astrolabe.lunar_date,
            chinese_date=astrolabe.chinese_date,
            time=astrolabe.time,
            time_range=astrolabe.time_range,
            sign=astrolabe.sign,
            zodiac=astrolabe.zodiac,
            earthly_branch_of_soul_palace=astrolabe.earthly_branch_of_soul_palace,
            earthly_branch_of_body_palace=astrolabe.earthly_branch_of_body_palace,
            soul=astrolabe.soul,
            body=astrolabe.body,
            five_elements_class=astrolabe.five_elements_class,
            palaces=functional_palaces,
            raw_lunar_date=astrolabe.raw_lunar_date,
            raw_chinese_date=astrolabe.raw_chinese_date,
        )

        # 设置宫位的星盘引用
        for palace in self.palaces:
            palace.set_astrolabe(self)

    def palace(self, index_or_name: Union[int, PalaceName]) -> Optional[FunctionalPalace]:
        """
        获取指定的宫位对象

        Args:
            index_or_name: 宫位索引 (0-11) 或宫位名称

        Returns:
            宫位对象，如果不存在则返回None

        Example:
            >>> astrolabe.palace(0)
            >>> astrolabe.palace('soulPalace')
            >>> astrolabe.palace('命宫')
        """
        if isinstance(index_or_name, int):
            # 按索引查询
            if 0 <= index_or_name < len(self.palaces):
                return self.palaces[index_or_name]
            return None
        else:
            # 按名称查询
            # 先尝试英文名
            for palace in self.palaces:
                if palace.name == index_or_name:
                    return palace

            # 再尝试中文名
            from iztro_py.utils.helpers import get_palace_index_by_name

            palace_index = get_palace_index_by_name(index_or_name)
            if palace_index is not None:
                return self.palaces[palace_index]

            return None

    def star(self, star_name: StarName) -> Optional[FunctionalStar]:
        """
        获取指定的星曜对象

        Args:
            star_name: 星曜名称

        Returns:
            星曜对象，如果不存在则返回None

        Example:
            >>> astrolabe.star('ziweiMaj')
            >>> astrolabe.star('紫微')
        """
        for palace in self.palaces:
            star = palace.get_star(star_name)
            if star:
                return star

        return None

    def surrounded_palaces(
        self, index_or_name: Union[int, PalaceName]
    ) -> Optional[FunctionalSurpalaces]:
        """
        获取指定宫位的三方四正

        Args:
            index_or_name: 宫位索引或名称

        Returns:
            三方四正对象，如果宫位不存在则返回None

        Example:
            >>> astrolabe.surrounded_palaces(0)
            >>> astrolabe.surrounded_palaces('命宫')
        """
        target_palace = self.palace(index_or_name)
        if not target_palace:
            return None

        # 获取三方四正的索引
        indices = get_surrounded_indices(target_palace.index)

        opposite_palace = self.palaces[indices["opposite"]]
        wealth_palace = self.palaces[indices["wealth"]]
        career_palace = self.palaces[indices["career"]]

        return FunctionalSurpalaces(
            target=target_palace,
            opposite=opposite_palace,
            wealth=wealth_palace,
            career=career_palace,
        )

    def not_empty_palaces(self) -> List[FunctionalPalace]:
        """
        获取所有非空宫（有主星的宫位）

        Returns:
            非空宫列表
        """
        return [p for p in self.palaces if not p.is_empty()]

    def empty_palaces(self) -> List[FunctionalPalace]:
        """
        获取所有空宫（无主星的宫位）

        Returns:
            空宫列表
        """
        return [p for p in self.palaces if p.is_empty()]

    def get_soul_palace(self) -> Optional[FunctionalPalace]:
        """
        获取命宫

        Returns:
            命宫对象
        """
        for palace in self.palaces:
            if palace.is_original_palace:
                return palace
        return None

    def get_body_palace(self) -> Optional[FunctionalPalace]:
        """
        获取身宫

        Returns:
            身宫对象
        """
        for palace in self.palaces:
            if palace.is_body_palace:
                return palace
        return None

    def horoscope(self, solar_date: str, time_index: int = 0):
        """
        获取指定日期的运势信息（大限、流年、流月、流日、流时）

        Args:
            solar_date: 查询的阳历日期 (YYYY-M-D or YYYY-MM-DD)
            time_index: 时辰索引 (0-12)，默认为0（子时）

        Returns:
            Horoscope对象，包含大限、流年、流月、流日、流时信息

        Example:
            >>> chart = astro.by_solar('2000-8-16', 6, '男')
            >>> horoscope = chart.horoscope('2024-1-1', 6)
            >>> print(f"大限: {horoscope.decadal.name}")
            >>> print(f"流年: {horoscope.yearly.name}")
        """
        from iztro_py.astro.horoscope import get_horoscope
        from iztro_py.data.types import FiveElementsClass

        # 获取出生年份
        birth_year = int(self.solar_date.split("-")[0])

        # 获取命宫索引
        soul_palace = self.get_soul_palace()
        soul_palace_index = soul_palace.index if soul_palace else 0

        # 获取五行局
        five_elements_class_map = {
            "水二局": FiveElementsClass.WATER_2,
            "木三局": FiveElementsClass.WOOD_3,
            "金四局": FiveElementsClass.METAL_4,
            "土五局": FiveElementsClass.EARTH_5,
            "火六局": FiveElementsClass.FIRE_6,
        }
        five_elements = five_elements_class_map.get(
            self.five_elements_class, FiveElementsClass.WATER_2
        )

        # 获取出生年支阴阳
        if self.raw_chinese_date:
            year_branch = self.raw_chinese_date.year_branch
            # 从地支获取阴阳
            from iztro_py.data.earthly_branches import EARTHLY_BRANCHES_CONFIG

            branch_config = EARTHLY_BRANCHES_CONFIG.get(year_branch)
            year_branch_yin_yang = branch_config.yin_yang if branch_config else "阳"
        else:
            year_branch_yin_yang = "阳"

        return get_horoscope(
            solar_date_str=solar_date,
            time_index=time_index,
            palaces=self.palaces,
            soul_palace_index=soul_palace_index,
            five_elements_class=five_elements,
            gender=self.gender,
            year_branch_yin_yang=year_branch_yin_yang,
            birth_year=birth_year,
        )

    def __str__(self) -> str:
        """字符串表示"""
        lines = [
            f"紫微斗数星盘",
            f"出生日期: {self.solar_date} ({self.lunar_date})",
            f"性别: {self.gender}",
            f"生肖: {self.zodiac} | 星座: {self.sign}",
            f"五行局: {self.five_elements_class}",
            f"命主: {self.soul} | 身主: {self.body}",
            "",
            "十二宫:",
        ]

        for palace in self.palaces:
            lines.append(f"  {palace}")

        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"FunctionalAstrolabe(date={self.solar_date}, gender={self.gender})"

    # ---------------------------------------------------------------------
    # Compatibility Export
    # ---------------------------------------------------------------------
    def to_iztro_dict(self) -> dict:
        """
        导出与原生 iztro/py-iztro 结构一致的字典（字段名与中文值对齐）

        返回字段示例：
        - gender, solarDate, lunarDate, chineseDate, time, timeRange, sign, zodiac
        - earthlyBranchOfSoulPalace, earthlyBranchOfBodyPalace, soul, body, fiveElementsClass
        - palaces: [{ name, isBodyPalace, isOriginalPalace, heavenlyStem, earthlyBranch, majorStars, minorStars }]
        """

        def tr_branch(branch_key: str) -> str:
            return t(f"earthlyBranch.{branch_key}") if "Earthly" in branch_key else branch_key

        def tr_stem(stem_key: str) -> str:
            return t(f"heavenlyStem.{stem_key}") if "Heavenly" in stem_key else stem_key

        def star_dict(star: FunctionalStar) -> dict:
            return {
                "name": star.translate_name(),
                "type": star.type,
                "scope": star.scope,
                "brightness": star.brightness,
                "mutagen": star.mutagen,
            }

        palaces = []
        for p in self.palaces:
            palaces.append(
                {
                    "name": p.translate_name(),
                    "isBodyPalace": p.is_body_palace,
                    "isOriginalPalace": p.is_original_palace,
                    "heavenlyStem": tr_stem(p.heavenly_stem),
                    "earthlyBranch": tr_branch(p.earthly_branch),
                    "majorStars": [star_dict(s) for s in p.major_stars],
                    "minorStars": [star_dict(s) for s in p.minor_stars],
                    "adjectiveStars": [star_dict(s) for s in p.adjective_stars],
                }
            )

        from iztro_py.data.types import Star

        return {
            "gender": self.gender,
            "solarDate": self.solar_date,
            "lunarDate": self.lunar_date,
            "chineseDate": self.chinese_date,
            "time": self.time,
            "timeRange": self.time_range,
            "sign": self.sign,
            "zodiac": self.zodiac,
            "earthlyBranchOfSoulPalace": tr_branch(self.earthly_branch_of_soul_palace),
            "earthlyBranchOfBodyPalace": tr_branch(self.earthly_branch_of_body_palace),
            "soul": Star(name=self.soul, type="major", scope="origin").translate_name(),
            "body": Star(name=self.body, type="major", scope="origin").translate_name(),
            "fiveElementsClass": self.five_elements_class,
            "palaces": palaces,
        }
