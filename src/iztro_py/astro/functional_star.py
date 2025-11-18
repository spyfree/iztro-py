"""
FunctionalStar class - Star with functional methods

Provides a rich API for querying star properties and relationships.
"""

from typing import Optional, TYPE_CHECKING, List, Union
from iztro_py.data.types import Star, Brightness, Mutagen

if TYPE_CHECKING:
    from iztro_py.astro.functional_palace import FunctionalPalace
    from iztro_py.astro.functional_surpalaces import FunctionalSurpalaces


class FunctionalStar(Star):
    """
    功能增强的星曜类

    继承自Star，添加了查询方法和关联宫位的能力
    """

    def __init__(self, star: Star):
        """
        初始化FunctionalStar

        Args:
            star: 基础Star对象
        """
        super().__init__(
            name=star.name,
            type=star.type,
            scope=star.scope,
            brightness=star.brightness,
            mutagen=star.mutagen,
        )
        self._palace: Optional["FunctionalPalace"] = None

    def set_palace(self, palace: "FunctionalPalace") -> None:
        """
        设置星曜所在宫位

        Args:
            palace: 宫位对象
        """
        self._palace = palace

    def palace(self) -> Optional["FunctionalPalace"]:
        """
        获取星曜所在宫位

        Returns:
            宫位对象，如果未设置则返回None
        """
        return self._palace

    def with_brightness(self, brightness: Union[Brightness, List[Brightness]]) -> bool:
        """
        判断星曜是否具有指定亮度

        Args:
            brightness: 亮度或亮度列表

        Returns:
            是否匹配

        Example:
            >>> star.with_brightness('庙')
            >>> star.with_brightness(['庙', '旺'])
        """
        if isinstance(brightness, list):
            return self.brightness in brightness
        else:
            return self.brightness == brightness

    def with_mutagen(self, mutagen: Union[Mutagen, List[Mutagen]]) -> bool:
        """
        判断星曜是否具有指定四化

        Args:
            mutagen: 四化类型或四化列表

        Returns:
            是否匹配

        Example:
            >>> star.with_mutagen('禄')
            >>> star.with_mutagen(['禄', '权'])
        """
        if isinstance(mutagen, list):
            return self.mutagen in mutagen
        else:
            return self.mutagen == mutagen

    def opposite_palace(self) -> Optional["FunctionalPalace"]:
        """
        获取星曜的对宫

        Returns:
            对宫对象，如果未设置宫位则返回None
        """
        if not self._palace:
            return None

        from iztro_py.data.constants import get_opposite_index

        opposite_index = get_opposite_index(self._palace.index)

        # 从星盘中获取对宫
        astrolabe = self._palace.astrolabe()
        if astrolabe:
            return astrolabe.palace(opposite_index)

        return None

    def surrounded_palaces(self) -> Optional["FunctionalSurpalaces"]:
        """
        获取星曜的三方四正宫位

        Returns:
            三方四正对象，如果未设置宫位则返回None
        """
        if not self._palace:
            return None

        astrolabe = self._palace.astrolabe()
        if astrolabe:
            return astrolabe.surrounded_palaces(self._palace.index)

        return None

    def is_major(self) -> bool:
        """判断是否为主星"""
        return self.type == "major"

    def is_minor(self) -> bool:
        """判断是否为辅星"""
        return self.type in ["soft", "tough", "lucun", "tianma"]

    def is_bright(self) -> bool:
        """判断是否庙旺（亮度好）"""
        return self.brightness in ["庙", "旺"]

    def is_weak(self) -> bool:
        """判断是否陷弱（亮度差）"""
        return self.brightness == "陷"

    def has_mutagen(self) -> bool:
        """判断是否有四化"""
        return self.mutagen is not None

    def __str__(self) -> str:
        """字符串表示"""
        parts = [self.name]
        if self.brightness:
            parts.append(f"({self.brightness})")
        if self.mutagen:
            parts.append(f"[化{self.mutagen}]")
        return "".join(parts)

    def __repr__(self) -> str:
        return f"FunctionalStar({self.name}, brightness={self.brightness}, mutagen={self.mutagen})"
