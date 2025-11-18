"""
FunctionalSurpalaces class - Surrounded palaces (三方四正) with functional methods

Represents the four related palaces in Zi Wei Dou Shu astrology.
"""

from typing import List
from iztro_py.data.types import SurroundedPalaces, StarName, Mutagen
from iztro_py.astro.functional_palace import FunctionalPalace


class FunctionalSurpalaces(SurroundedPalaces):
    """
    功能增强的三方四正类

    三方四正包括：
    - target: 本宫
    - opposite: 对宫（相隔6宫）
    - wealth: 财帛位（相隔8宫）
    - career: 官禄位（相隔4宫）
    """

    def __init__(
        self,
        target: FunctionalPalace,
        opposite: FunctionalPalace,
        wealth: FunctionalPalace,
        career: FunctionalPalace,
    ):
        """
        初始化FunctionalSurpalaces

        Args:
            target: 本宫
            opposite: 对宫
            wealth: 财帛位
            career: 官禄位
        """
        super().__init__(target=target, opposite=opposite, wealth=wealth, career=career)

    def have(self, stars: List[StarName]) -> bool:
        """
        判断三方四正是否包含所有指定的星曜

        Args:
            stars: 星曜名称列表

        Returns:
            是否所有星曜都在三方四正中

        Example:
            >>> surpalaces.have(['紫微', '天府'])
        """
        palaces = [self.target, self.opposite, self.wealth, self.career]

        for star in stars:
            found = any(palace.has([star]) for palace in palaces)
            if not found:
                return False

        return True

    def have_one_of(self, stars: List[StarName]) -> bool:
        """
        判断三方四正是否包含任一指定的星曜

        Args:
            stars: 星曜名称列表

        Returns:
            是否包含任一星曜

        Example:
            >>> surpalaces.have_one_of(['紫微', '天府'])
        """
        palaces = [self.target, self.opposite, self.wealth, self.career]

        for star in stars:
            if any(palace.has([star]) for palace in palaces):
                return True

        return False

    def not_have(self, stars: List[StarName]) -> bool:
        """
        判断三方四正是否不包含任何指定的星曜

        Args:
            stars: 星曜名称列表

        Returns:
            是否都不包含

        Example:
            >>> surpalaces.not_have(['火星', '铃星'])
        """
        palaces = [self.target, self.opposite, self.wealth, self.career]

        for star in stars:
            if any(palace.has([star]) for palace in palaces):
                return False

        return True

    def have_mutagen(self, mutagen: Mutagen) -> bool:
        """
        判断三方四正是否包含指定四化的星曜

        Args:
            mutagen: 四化类型 ('禄'/'权'/'科'/'忌')

        Returns:
            是否包含

        Example:
            >>> surpalaces.have_mutagen('禄')
        """
        palaces = [self.target, self.opposite, self.wealth, self.career]
        return any(palace.has_mutagen(mutagen) for palace in palaces)

    def not_have_mutagen(self, mutagen: Mutagen) -> bool:
        """
        判断三方四正是否不包含指定四化的星曜

        Args:
            mutagen: 四化类型

        Returns:
            是否不包含

        Example:
            >>> surpalaces.not_have_mutagen('忌')
        """
        return not self.have_mutagen(mutagen)

    def all_palaces(self) -> List[FunctionalPalace]:
        """
        获取所有宫位列表

        Returns:
            包含四个宫位的列表
        """
        return [self.target, self.opposite, self.wealth, self.career]

    def __str__(self) -> str:
        """字符串表示"""
        return (
            f"三方四正:\n"
            f"  本宫: {self.target.name}\n"
            f"  对宫: {self.opposite.name}\n"
            f"  财帛: {self.wealth.name}\n"
            f"  官禄: {self.career.name}"
        )

    def __repr__(self) -> str:
        return (
            f"FunctionalSurpalaces("
            f"target={self.target.name}, "
            f"opposite={self.opposite.name}, "
            f"wealth={self.wealth.name}, "
            f"career={self.career.name})"
        )
