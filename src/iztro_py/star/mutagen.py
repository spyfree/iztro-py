"""
Mutagen (四化) calculation for iztro-py

Functions for calculating and applying mutagen transformations to stars.
"""

from typing import Any, Dict, List, Optional, Tuple
from iztro_py.data.types import HeavenlyStemName, StarName, Mutagen
from iztro_py.data.heavenly_stems import get_mutagen, get_mutagen_type


def apply_mutagen_to_palaces(palaces: List[Dict[str, Any]], year_stem: HeavenlyStemName) -> None:
    """
    为所有宫位中的星曜添加四化属性

    根据生年天干，为相应的星曜标注四化（禄、权、科、忌）

    Args:
        palaces: 宫位列表
        year_stem: 年干

    Note:
        直接修改palaces列表，不返回值
    """
    # 获取该年干对应的四化星
    mutagen_stars = get_mutagen(year_stem)  # [禄星, 权星, 科星, 忌星]

    # 遍历所有宫位
    for palace in palaces:
        # 检查主星
        for star in palace["major_stars"]:
            mutagen_type = get_mutagen_type(year_stem, star.name)
            if mutagen_type:
                star.mutagen = mutagen_type

        # 检查辅星
        for star in palace["minor_stars"]:
            mutagen_type = get_mutagen_type(year_stem, star.name)
            if mutagen_type:
                star.mutagen = mutagen_type


def get_mutagen_stars(year_stem: HeavenlyStemName) -> Dict[Mutagen, StarName]:
    """
    获取指定年干的四化星配置

    Args:
        year_stem: 年干

    Returns:
        四化类型到星曜名称的映射字典
    """
    mutagen_stars = get_mutagen(year_stem)
    mutagen_types: List[Mutagen] = ["禄", "权", "科", "忌"]

    return {mutagen_types[i]: mutagen_stars[i] for i in range(4)}


def has_mutagen(star_name: StarName, year_stem: HeavenlyStemName) -> Optional[Mutagen]:
    """
    判断指定星曜在指定年干下是否有四化

    Args:
        star_name: 星曜名称
        year_stem: 年干

    Returns:
        四化类型，如果没有则返回None
    """
    return get_mutagen_type(year_stem, star_name)


def get_palace_mutagens(palace: Dict[str, Any]) -> List[Tuple[StarName, Mutagen]]:
    """
    获取宫位中所有带四化的星曜

    Args:
        palace: 宫位字典

    Returns:
        [(星曜名称, 四化类型), ...] 列表
    """
    mutagen_stars = []

    # 检查主星
    for star in palace.get("major_stars", []):
        if star.mutagen:
            mutagen_stars.append((star.name, star.mutagen))

    # 检查辅星
    for star in palace.get("minor_stars", []):
        if star.mutagen:
            mutagen_stars.append((star.name, star.mutagen))

    return mutagen_stars


def has_mutagen_in_palace(palace: dict, mutagen_type: Mutagen) -> bool:
    """
    判断宫位是否包含指定类型的四化

    Args:
        palace: 宫位字典
        mutagen_type: 四化类型

    Returns:
        是否包含
    """
    mutagen_stars = get_palace_mutagens(palace)
    return any(m == mutagen_type for _, m in mutagen_stars)
