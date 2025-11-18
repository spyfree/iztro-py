"""
FunctionalPalace class - Palace with functional methods

Provides a rich API for querying palace properties and stars.
"""

from typing import Optional, List, TYPE_CHECKING
from iztro_py.data.types import Palace, StarName, Mutagen
from iztro_py.astro.functional_star import FunctionalStar

if TYPE_CHECKING:
    from iztro_py.astro.functional_astrolabe import FunctionalAstrolabe
    from iztro_py.astro.functional_surpalaces import FunctionalSurpalaces


class FunctionalPalace(Palace):
    """
    功能增强的宫位类

    继承自Palace，添加了星曜查询方法和关联星盘的能力
    """

    def __init__(self, palace: Palace):
        """
        初始化FunctionalPalace

        Args:
            palace: 基础Palace对象
        """
        # 转换星曜为FunctionalStar
        major_stars = [FunctionalStar(s) for s in palace.major_stars]
        minor_stars = [FunctionalStar(s) for s in palace.minor_stars]
        adjective_stars = [FunctionalStar(s) for s in palace.adjective_stars]

        super().__init__(
            index=palace.index,
            name=palace.name,
            is_body_palace=palace.is_body_palace,
            is_original_palace=palace.is_original_palace,
            heavenly_stem=palace.heavenly_stem,
            earthly_branch=palace.earthly_branch,
            major_stars=major_stars,
            minor_stars=minor_stars,
            adjective_stars=adjective_stars,
            changsheng12=palace.changsheng12,
            boshi12=palace.boshi12,
            jiangqian12=palace.jiangqian12,
            suiqian12=palace.suiqian12,
            decadal=palace.decadal,
            ages=palace.ages,
        )

        self._astrolabe: Optional["FunctionalAstrolabe"] = None

        # 设置星曜的宫位引用
        for star in self.major_stars + self.minor_stars + self.adjective_stars:
            star.set_palace(self)

    def set_astrolabe(self, astrolabe: "FunctionalAstrolabe") -> None:
        """
        设置宫位所属的星盘

        Args:
            astrolabe: 星盘对象
        """
        self._astrolabe = astrolabe

    def astrolabe(self) -> Optional["FunctionalAstrolabe"]:
        """
        获取宫位所属的星盘

        Returns:
            星盘对象，如果未设置则返回None
        """
        return self._astrolabe

    def has(self, stars: List[StarName]) -> bool:
        """
        判断宫位是否包含所有指定的星曜

        Args:
            stars: 星曜名称列表

        Returns:
            是否包含所有星曜

        Example:
            >>> palace.has(['紫微', '天府'])
        """
        all_stars = self.major_stars + self.minor_stars + self.adjective_stars
        star_names = [s.name for s in all_stars]

        return all(star in star_names for star in stars)

    def has_one_of(self, stars: List[StarName]) -> bool:
        """
        判断宫位是否包含任一指定的星曜

        Args:
            stars: 星曜名称列表

        Returns:
            是否包含任一星曜

        Example:
            >>> palace.has_one_of(['紫微', '天府'])
        """
        all_stars = self.major_stars + self.minor_stars + self.adjective_stars
        star_names = [s.name for s in all_stars]

        return any(star in star_names for star in stars)

    def not_have(self, stars: List[StarName]) -> bool:
        """
        判断宫位是否不包含任何指定的星曜

        Args:
            stars: 星曜名称列表

        Returns:
            是否都不包含

        Example:
            >>> palace.not_have(['火星', '铃星'])
        """
        all_stars = self.major_stars + self.minor_stars + self.adjective_stars
        star_names = [s.name for s in all_stars]

        return all(star not in star_names for star in stars)

    def has_mutagen(self, mutagen: Mutagen) -> bool:
        """
        判断宫位是否包含指定四化的星曜

        Args:
            mutagen: 四化类型 ('禄'/'权'/'科'/'忌')

        Returns:
            是否包含

        Example:
            >>> palace.has_mutagen('禄')
        """
        all_stars = self.major_stars + self.minor_stars + self.adjective_stars
        return any(s.mutagen == mutagen for s in all_stars)

    def not_have_mutagen(self, mutagen: Mutagen) -> bool:
        """
        判断宫位是否不包含指定四化的星曜

        Args:
            mutagen: 四化类型

        Returns:
            是否不包含

        Example:
            >>> palace.not_have_mutagen('忌')
        """
        return not self.has_mutagen(mutagen)

    def is_empty(self, exclude_stars: Optional[List[StarName]] = None) -> bool:
        """
        判断宫位是否为空宫（无主星）

        Args:
            exclude_stars: 要排除的星曜列表（可选）

        Returns:
            是否为空宫

        Example:
            >>> palace.is_empty()
            >>> palace.is_empty(exclude_stars=['禄存', '天马'])
        """
        major_stars = self.major_stars

        if exclude_stars:
            major_stars = [s for s in major_stars if s.name not in exclude_stars]

        return len(major_stars) == 0

    def get_star(self, star_name: StarName) -> Optional[FunctionalStar]:
        """
        获取指定名称的星曜对象

        Args:
            star_name: 星曜名称

        Returns:
            星曜对象，如果不存在则返回None
        """
        all_stars = self.major_stars + self.minor_stars + self.adjective_stars

        for star in all_stars:
            if star.name == star_name:
                return star

        return None

    def __str__(self) -> str:
        """字符串表示"""
        markers = []
        if self.is_original_palace:
            markers.append("命")
        if self.is_body_palace:
            markers.append("身")

        marker_str = f"[{'/'.join(markers)}]" if markers else ""

        major_str = ", ".join(str(s) for s in self.major_stars) if self.major_stars else "空宫"

        return f"{self.name}{marker_str}: {major_str}"

    def __repr__(self) -> str:
        return f"FunctionalPalace(index={self.index}, name={self.name})"
